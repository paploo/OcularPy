import math

import numpy as np

from ocular.core.eyepiece import BarrelSize, Eyepiece, TYPICAL_WALL_THICKNESS
import ocular.viz.common.focal_length_axis as fla
from ocular.core.optical_system import OpticalSystem
from ocular.util.tools import snap
from ocular.viz.common.colors import Gruvbox as Color, barrel_color


def system_scatter(ax, telescope, eyepieces, y_from_optical_system, label_points=False, label_func=None):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [os.eyepiece.focal_length for os in optical_systems]
    y = [y_from_optical_system(os) for os in optical_systems]
    s = [os.eyepiece.barrel_size.diameter for os in optical_systems]
    c = [barrel_color(os.eyepiece.barrel_size).value for os in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        if label_func is None:
            label = "{} {:.0f}$\degree$".format(os.eyepiece.manufacturer.code, os.eyepiece.apparent_field_of_view)
        else:
            label = label_func(os)

        if label_points or True:
            ax.annotate(label,
                        (os.eyepiece.focal_length, y_from_optical_system(os)),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=8)


def system_field_stop_lines(ax, telescope, y_from_optical_system):
    def optical_system_func(focal_length, barrel_size, wall_thickness):
        eyepiece = Eyepiece.generic(focal_length,
                                    barrel_size=barrel_size,
                                    wall_thickness=wall_thickness)
        system = OpticalSystem(telescope, eyepiece)
        return y_from_optical_system(system)

    return field_stop_lines(ax, telescope, optical_system_func)


def field_stop_lines(ax, telescope, y_calc_func):
    options = [
        (BarrelSize.TWO_INCH, 0.0, None),
        (BarrelSize.TWO_INCH, TYPICAL_WALL_THICKNESS, 'dashed'),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 0.0, None),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, TYPICAL_WALL_THICKNESS, 'dashed')
    ]

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.max_focal_length(telescope), fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        y_values = [y_calc_func(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        label = opt[0].label if (opt[1] == 0.0) else None
        ax.plot(fls, y_values, color=barrel_color(opt[0]).value, linestyle=opt[2], label=label)


def system_afov_lines(ax, telescope, y_from_optical_system):
    def optical_system_func(focal_length, apparent_field_of_view):
        eyepiece = Eyepiece.generic(focal_length, apparent_field_of_view, telescope.barrel_size)
        os = OpticalSystem(telescope, eyepiece)
        return y_from_optical_system(os)

    return afov_lines(ax, telescope, optical_system_func)


def afov_lines(ax, telescope, y_calc_func):
    options = [
        (50, 'solid', Color.LIGHT_GREEN.alpha(0.3)),
        (60, 'solid', Color.LIGHT_GREEN.alpha(0.3)),
        (70, 'solid', Color.LIGHT_GREEN.alpha(0.3)),
        (80, 'solid', Color.LIGHT_GREEN.alpha(0.3)),
        (100, 'solid', Color.LIGHT_GREEN.alpha(0.3))
    ]

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.max_focal_length(telescope), fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        y_values = [y_calc_func(fl, opt[0]) for fl in fls]
        label = str(opt[0]) + r'$\degree$ AFoV'
        ax.plot(fls, y_values, color=opt[2], linestyle=opt[1], label=label)


def true_yaxis(ax, telescope, max_value, label, max_time_function, secax_functions, max_granularity=0.5):
    snapped_max = snap(max_value, max_granularity)
    ax.set_ylim(0.0, snapped_max)
    ax.set_ylabel(label)

    secax = ax.secondary_yaxis('right', functions=secax_functions)
    secax.set_ylabel(r'$\Delta$t (s)')
    max_time = max_time_function(snapped_max)
    secax.set_yticks(np.arange(0, max_time, 60.0))
