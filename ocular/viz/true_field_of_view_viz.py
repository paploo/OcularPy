import math

import numpy as np

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.optical_system import OpticalSystem, time_in_field_of_view_to_true_field_of_view, \
    true_field_of_view_to_time_in_field_of_view
from ocular.viz.common.colors import barrel_color
import ocular.viz.common.focal_length_axis as fla


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("True Field of View")
    fla.focal_length_xaxis(ax, telescope)
    tfov_yaxis(ax, telescope)
    tfov_max_lines(ax, telescope)
    scatter_tfov(ax, telescope, eyepieces)
    ax.legend()


def tfov_yaxis(ax, telescope):
    max_tfov = tfov_max(telescope)
    max_tfov = math.ceil(max_tfov / 0.5) * 0.5

    ax.set_ylim(0.0, max_tfov)
    ax.set_ylabel(r'$\Delta\theta_{tfov}$ ($\degree$)')

    sec_ax_functions = (true_field_of_view_to_time_in_field_of_view, time_in_field_of_view_to_true_field_of_view)
    sec_ax = ax.secondary_yaxis('right', functions=sec_ax_functions)
    sec_ax.set_ylabel(r'$\Delta$t (s)')

    max_time = true_field_of_view_to_time_in_field_of_view(max_tfov)
    sec_ax.set_yticks(np.arange(0, max_time, 60.0))


def scatter_tfov(ax, telescope, eyepieces):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [s.eyepiece.focal_length for s in optical_systems]
    y = [s.true_field_of_view for s in optical_systems]
    s = [s.eyepiece.barrel_size.diameter for s in optical_systems]
    c = [barrel_color(s.eyepiece.barrel_size).value for s in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_field_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


def tfov_max_lines(ax, telescope):
    # These turn out to be lines, but we keep the long-form to be able to adjust to better computations.
    def tfov(focal_length, barrel_size, wall_thickness):
        eyepiece = Eyepiece.generic(focal_length,
                                    barrel_size=barrel_size,
                                    wall_thickness=wall_thickness)
        return OpticalSystem(telescope, eyepiece).true_field_of_view

    options = [
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 0.0, None),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 2.0, 'dashed'),
        (BarrelSize.TWO_INCH, 0.0, None),
        (BarrelSize.TWO_INCH, 2.0, 'dashed')
    ]

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.VIZ_FOCAL_LENGTH_MAX, fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        afovs = [tfov(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        label = opt[0].label if (opt[1] == 0.0) else None
        ax.plot(fls, afovs, color=barrel_color(opt[0]).value, linestyle=opt[2], label=label)


def tfov_max(telescope):
    return telescope.max_true_field_of_view(barrel_size=BarrelSize.TWO_INCH, wall_thickness=0.0)
