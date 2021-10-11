import math

import numpy as np

from ocular.core.eyepiece import BarrelSize, Eyepiece, TYPICAL_WALL_THICKNESS
import ocular.viz.common.focal_length_axis as fla
from ocular.core.optical_system import OpticalSystem
from ocular.viz.common.colors import barrel_color


def system_scatter(ax, telescope, eyepieces, y_from_optical_system):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [os.eyepiece.focal_length for os in optical_systems]
    y = [y_from_optical_system(os) for os in optical_systems]
    s = [os.eyepiece.barrel_size.diameter for os in optical_systems]
    c = [barrel_color(os.eyepiece.barrel_size).value for os in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_field_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


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

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.VIZ_FOCAL_LENGTH_MAX, fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        y_values = [y_calc_func(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        label = opt[0].label if (opt[1] == 0.0) else None
        ax.plot(fls, y_values, color=barrel_color(opt[0]).value, linestyle=opt[2], label=label)


def true_yaxis(ax, telescope, max_value, label, max_time_function, secax_functions):
    snapped_max = math.ceil(max_value / 0.5) * 0.5
    ax.set_ylim(0.0, snapped_max)
    ax.set_ylabel(label)

    secax = ax.secondary_yaxis('right', functions=secax_functions)
    secax.set_ylabel(r'$\Delta$t (s)')
    max_time = max_time_function(snapped_max)
    secax.set_yticks(np.arange(0, max_time, 60.0))
