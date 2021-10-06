import matplotlib.pyplot as plt
import numpy as np

from ocular.core.eyepiece import Eyepiece, degrees_to_arcseconds, arcseconds_to_degrees, BarrelSize
from ocular.core.optical_system import OpticalSystem


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    xaxis_as_focal_length(ax, telescope)
    yaxis_as_field_of_view(ax, telescope)
    max_fov_line(ax, telescope)
    scatter_field_of_view(ax, telescope, eyepieces)


def xaxis_as_focal_length(ax, telescope):
    ax.set_xlim([0, 40])
    ax.set_xlabel(r'$f_L$ (mm)')

    # sec_ax_functions = (curry(focal_length_to_exit_pupil)(telescope), exit_pupil_to_focal_length(telescope))
    sec_ax_functions = (telescope.exit_pupil_for_eyepiece_focal_length, telescope.eyepiece_focal_length_for_exit_pupil)
    sec_ax = ax.secondary_xaxis('top', functions=sec_ax_functions)
    sec_ax.set_xlabel('$D_{ep}$ (mm)')


def yaxis_as_field_of_view(ax, telescope):
    ax.set_ylim([0, 120])
    ax.set_ylabel(r'$\theta_{ep}$ (degrees)')


def scatter_field_of_view(ax, telescope, eyepieces):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [s.eyepiece.focal_length for s in optical_systems]
    y = [s.eyepiece.apparent_field_of_view for s in optical_systems]
    ax.scatter(x, y)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_field_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


def min_focal_length_line(ax, telescope):
    # TODO: Make this work!
    pass


def max_fov_line(ax, telescope):
    fls = np.arange(1, 40, 0.1)

    # TODO: Cleanup this messy code style! (make helper function?)
    # TODO: Setup a color pallete for the barrel sizes (blue-green and orange)
    # TODO: Set the ones using thickness to dashed.

    afovs = [OpticalSystem(
        telescope,
        Eyepiece.generic(fl,
                         barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH)).eyepiece.apparent_field_of_view
             for fl in fls]
    ax.plot(fls, afovs)

    afovs = [OpticalSystem(telescope, Eyepiece.generic(fl,
                                                       barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
                                                       wall_thickness=0.0)).eyepiece.apparent_field_of_view
             for fl in fls]
    ax.plot(fls, afovs)

    afovs = [OpticalSystem(telescope, Eyepiece.generic(fl, barrel_size=BarrelSize.TWO_INCH)).eyepiece.apparent_field_of_view
             for fl in fls]
    ax.plot(fls, afovs)

    afovs = [OpticalSystem(telescope, Eyepiece.generic(fl, barrel_size=BarrelSize.TWO_INCH, wall_thickness=0.0)).eyepiece.apparent_field_of_view
             for fl in fls]
    ax.plot(fls, afovs)




