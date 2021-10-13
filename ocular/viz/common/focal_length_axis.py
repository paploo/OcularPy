import math

from ocular.viz.common.colors import Gruvbox as Color


VIZ_FOCAL_LENGTH_DELTA = 0.1


def focal_length_xaxis(ax, telescope):
    focal_length_xaxis_setup(ax, telescope)
    max_focal_length_line(ax, telescope)
    min_focal_length_span(ax, telescope)
    atmosphere_limit_focal_length_line(ax, telescope)


def focal_length_xaxis_setup(ax, telescope):
    max = max_focal_length(telescope)
    ax.set_xlim([0, max])
    ax.set_xlabel(r'$f_L$ (mm)')

    sec_ax_functions = (telescope.exit_pupil_for_eyepiece_focal_length, telescope.eyepiece_focal_length_for_exit_pupil)
    sec_ax = ax.secondary_xaxis('top', functions=sec_ax_functions)
    sec_ax.set_xlabel(r'$D_{ep}$ (mm)')


def max_focal_length_line(ax, telescope):
    min_mag = telescope.min_magnification(6.0)
    max_focal = telescope.eyepiece_focal_length_for_magnification(min_mag)
    ax.axvline(max_focal, color=Color.PURPLE.value, label=r'Max Usable $f_L$')


def min_focal_length_span(ax, telescope):
    max_mag = telescope.max_magnification()
    min_focal = telescope.eyepiece_focal_length_for_magnification(max_mag)
    ax.axvspan(min_focal/2.0, min_focal, color=Color.PURPLE.alpha(0.2), label=r'Min Usable $f_L$')


def atmosphere_limit_focal_length_line(ax, telescope):
    atm_focal = telescope.eyepiece_focal_length_for_magnification(300.0)
    ax.axvline(atm_focal, color=Color.PURPLE.value, label=r'Atm Limit $f_L$')

def max_focal_length(telescope, max_exit_pupil=8.0):
    max_fl = telescope.eyepiece_focal_length_for_exit_pupil(max_exit_pupil)
    return math.ceil(max_fl / 10.0) * 10.0
