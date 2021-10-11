import math

import numpy as np

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.optical_system import OpticalSystem, time_in_angle_of_view_to_true_angle_of_view, \
    true_angle_of_view_to_time_in_angle_of_view
from ocular.viz.colors import barrel_color
import ocular.viz.focal_length_axis as fla


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("True Angle of View")
    fla.focal_length_xaxis(ax, telescope)
    taov_yaxis(ax, telescope)
    taov_max_lines(ax, telescope)
    scatter_taov(ax, telescope, eyepieces)
    ax.legend()


def taov_yaxis(ax, telescope):
    max_taov = taov_max(telescope)
    max_taov = math.ceil(max_taov / 0.5) * 0.5

    ax.set_ylim(0.0, max_taov)
    ax.set_ylabel(r'$\Delta\theta_{taov}$ ($\degree$)')

    sec_ax_functions = (true_angle_of_view_to_time_in_angle_of_view, time_in_angle_of_view_to_true_angle_of_view)
    sec_ax = ax.secondary_yaxis('right', functions=sec_ax_functions)
    sec_ax.set_ylabel(r'$\Delta$t (s)')

    max_time = true_angle_of_view_to_time_in_angle_of_view(max_taov)
    sec_ax.set_yticks(np.arange(0, max_time, 60.0))


def scatter_taov(ax, telescope, eyepieces):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [s.eyepiece.focal_length for s in optical_systems]
    y = [s.true_angle_of_view for s in optical_systems]
    s = [s.eyepiece.barrel_size.diameter for s in optical_systems]
    c = [barrel_color(s.eyepiece.barrel_size).value for s in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_angle_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


def taov_max_lines(ax, telescope):
    # These turn out to be lines, but we keep the long-form to be able to adjust to better computations.
    def taov(focal_length, barrel_size, wall_thickness):
        eyepiece = Eyepiece.generic(focal_length,
                                    barrel_size=barrel_size,
                                    wall_thickness=wall_thickness)
        return OpticalSystem(telescope, eyepiece).true_angle_of_view

    options = [
        (BarrelSize.TWO_INCH, 0.0, None),
        (BarrelSize.TWO_INCH, 2.0, 'dashed'),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 0.0, None),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 2.0, 'dashed')
    ]

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.VIZ_FOCAL_LENGTH_MAX, fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        afovs = [taov(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        label_qualifier = 'safe' if (opt[1] > 0.0) else 'max'
        label = opt[0].label if (opt[1] == 0.0) else None
        ax.plot(fls, afovs, color=barrel_color(opt[0]).value, linestyle=opt[2], label=label)


def taov_max(telescope):
    return telescope.max_true_angle_of_view(barrel_size=BarrelSize.TWO_INCH, wall_thickness=0.0)
