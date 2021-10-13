import numpy as np

import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
import ocular.core.optical_system as optsys
from ocular.core.telescope import true_angle_of_view, field_stop_diameter


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Field Stop Diameter")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope)
    afov_lines(ax, telescope)
    max_lines(ax, telescope)
    scatter(ax, telescope, eyepieces)


def yaxis(ax, telescope):
    secax_functions = (time_in_view(telescope),
                       stop_diameter_for_time(telescope))
    flda.true_yaxis(ax,
                    telescope,
                    max_value=telescope.barrel_size.diameter,
                    label=r'$\Delta D_{stop}$ (mm)',
                    max_time_function=time_in_view(telescope),
                    secax_functions=secax_functions,
                    max_granularity=5.0)


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.eyepiece.field_stop_diameter)


def afov_lines(ax, telescope):
    flda.system_afov_lines(ax, telescope, lambda os: os.eyepiece.field_stop_diameter)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.eyepiece.field_stop_diameter)


def time_in_view(telescope):
    def f(stop_diameter):
        taov = true_angle_of_view(telescope.focal_length, stop_diameter)
        return optsys.time_in_view(taov)

    return np.vectorize(f, otypes=[float])


def stop_diameter_for_time(telescope):
    def f(time_in_fov):
        taov = optsys.field_angle(time_in_fov)
        return field_stop_diameter(telescope.focal_length, taov)

    return np.vectorize(f, otypes=[float])
