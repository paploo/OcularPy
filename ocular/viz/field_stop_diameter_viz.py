import numpy as np

import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
from ocular.core.eyepiece import BarrelSize
from ocular.core.optical_system import true_angle_of_view_to_time_in_angle_of_view, \
    time_in_angle_of_view_to_true_angle_of_view


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Field Stop Diameter")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope)
    max_lines(ax, telescope)
    scatter(ax, telescope, eyepieces)
    ax.legend()


def yaxis(ax, telescope):
    # TODO: Need to build the right conversion functions and then this should work.
    pass
    secax_functions = (field_stop_diameter_to_time_in_angle_of_view(telescope),
                       time_in_angle_of_view_to_field_stop_diameter(telescope))
    flda.true_yaxis(ax,
                    telescope,
                    max_value=BarrelSize.TWO_INCH.diameter,
                    label=r'$\Delta D_{stop}$ (mm)',
                    max_time_function=field_stop_diameter_to_time_in_angle_of_view(telescope),
                    secax_functions=secax_functions,
                    max_granularity=5.0)


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.eyepiece.field_stop_diameter)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.eyepiece.field_stop_diameter)


def field_stop_diameter_to_time_in_angle_of_view(telescope):
    def taov(field_stop_diameter):
        return telescope.true_angle_of_view(field_stop_diameter, BarrelSize.TWO_INCH, wall_thickness=0.0)

    def f(field_stop_diameter):
        return true_angle_of_view_to_time_in_angle_of_view(taov(field_stop_diameter))

    return np.vectorize(f, otypes=[float])


def time_in_angle_of_view_to_field_stop_diameter(telescope):
    def f(time_in_aov):
        return telescope.field_stop_diameter(
            time_in_angle_of_view_to_true_angle_of_view(time_in_aov),
            BarrelSize.TWO_INCH,
            wall_thickness=0.0
        )

    return np.vectorize(f, otypes=[float])
