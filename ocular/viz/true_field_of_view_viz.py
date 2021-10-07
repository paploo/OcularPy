import math

import numpy as np

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.optical_system import OpticalSystem, time_in_field_of_view_to_true_field_of_view, \
    true_field_of_view_to_time_in_field_of_view
from ocular.viz.colors import barrel_color
import ocular.viz.focal_length_axis as fla


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    fla.focal_length_xaxis(ax, telescope)
    tfov_yaxis(ax, telescope)
    tfov_max_lines(ax, telescope)
    scatter_tfov(ax, telescope, eyepieces)


def tfov_yaxis(ax, telescope):
    max_tfov = tfov_max(telescope)
    max_tfov = math.ceil(max_tfov / 0.5) * 0.5

    ax.set_ylim(0.0, max_tfov)
    ax.set_ylabel(r'$\Delta\theta_{true}$ ($\degree$)')

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
    # TODO: These turn out to be lines? Validate this and then make a short form version.
    # TODO: Use the short-form version to set the max.
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
        ax.plot(fls, afovs, color=barrel_color(opt[0]).value, linestyle=opt[2])

def tfov_max(telescope):
    # This is focal_length invariant unless we limit the max fov (since the ideal can exceed 180 degrees)!.
    longest_fl = telescope.eyepiece_focal_length_for_magnification(telescope.min_magnification())
    eyepiece = Eyepiece.generic(longest_fl, barrel_size=BarrelSize.TWO_INCH, wall_thickness=0.0)
    return OpticalSystem(telescope, eyepiece).true_field_of_view
