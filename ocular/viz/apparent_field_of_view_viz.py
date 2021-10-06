import matplotlib.pyplot as plt
import numpy as np

from ocular.core.eyepiece import Eyepiece, degrees_to_arcseconds, arcseconds_to_degrees, BarrelSize
from ocular.core.optical_system import OpticalSystem
from ocular.viz.colors import Gruvbox as Color, barrel_color


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    xaxis_as_focal_length(ax, telescope)
    yaxis_as_field_of_view(ax, telescope)
    focal_length_lines(ax, telescope)
    max_fov_lines(ax, telescope)
    scatter_field_of_view(ax, telescope, eyepieces)


def yaxis_as_field_of_view(ax, telescope):
    ax.set_ylim([40, 120])
    ax.set_ylabel(r'$\theta_{ep}$ (degrees)')


def scatter_field_of_view(ax, telescope, eyepieces):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [s.eyepiece.focal_length for s in optical_systems]
    y = [s.eyepiece.apparent_field_of_view for s in optical_systems]
    s = [s.eyepiece.barrel_size.diameter for s in optical_systems]
    c = [barrel_color(s.eyepiece.barrel_size).value for s in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_field_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


def max_fov_lines(ax, telescope):

    def afov(focal_length, barrel_size, wall_thickness):
        return Eyepiece.generic(focal_length,
                                barrel_size=barrel_size,
                                wall_thickness=wall_thickness).apparent_field_of_view

    options = [
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 0.0, None),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 2.0, 'dashed'),
        (BarrelSize.TWO_INCH, 0.0, None),
        (BarrelSize.TWO_INCH, 2.0, 'dashed')
    ]

    fls = np.arange(1, 40, 0.1)

    for opt in options:
        afovs = [afov(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        ax.plot(fls, afovs, color=barrel_color(opt[0]).value, linestyle=opt[2])

#
# These are reusable across plots, as long as fL is on the x-axis.
#


def xaxis_as_focal_length(ax, telescope):
    ax.set_xlim([0, 40])
    ax.set_xlabel(r'$f_L$ (mm)')

    sec_ax_functions = (telescope.exit_pupil_for_eyepiece_focal_length, telescope.eyepiece_focal_length_for_exit_pupil)
    sec_ax = ax.secondary_xaxis('top', functions=sec_ax_functions)
    sec_ax.set_xlabel('$D_{ep}$ (mm)')


def focal_length_lines(ax, telescope):
    min_focal_length_line(ax, telescope)
    max_focal_length_span(ax, telescope)
    atmosphere_limit_focal_length_line(ax, telescope)


def min_focal_length_line(ax, telescope):
    min_mag = telescope.min_magnification(6.0)
    max_focal = telescope.eyepiece_focal_length_for_magnification(min_mag)
    ax.axvline(max_focal, color=Color.PURPLE.value)


def max_focal_length_span(ax, telescope):
    max_mag = telescope.max_magnification()
    min_focal = telescope.eyepiece_focal_length_for_magnification(max_mag)
    ax.axvspan(min_focal/2.0, min_focal, color=Color.PURPLE.alpha(0.2))


def atmosphere_limit_focal_length_line(ax, telescope):
    atm_focal = telescope.eyepiece_focal_length_for_magnification(300.0)
    ax.axvline(atm_focal, color=Color.PURPLE.value)





