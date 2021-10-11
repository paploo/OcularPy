import math

import numpy as np

import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
from ocular.core.eyepiece import BarrelSize
from ocular.core.optical_system import time_in_angle_of_view_to_true_angle_of_view, \
    true_angle_of_view_to_time_in_angle_of_view


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("True Angle of View")
    fla.focal_length_xaxis(ax, telescope)
    taov_yaxis(ax, telescope)
    max_lines(ax, telescope)
    max_scatter(ax, telescope, eyepieces)
    ax.legend()


def taov_yaxis(ax, telescope):
    secax_functions = (true_angle_of_view_to_time_in_angle_of_view, time_in_angle_of_view_to_true_angle_of_view)
    flda.true_yaxis(ax,
                    telescope,
                    max_value=max_value(telescope),
                    label=r'$\Delta\theta_{taov}$ ($\degree$)',
                    max_time_function=true_angle_of_view_to_time_in_angle_of_view,
                    secax_functions=secax_functions)


def max_scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.true_angle_of_view)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.true_angle_of_view)


def max_value(telescope):
    return telescope.max_true_angle_of_view(barrel_size=BarrelSize.TWO_INCH, wall_thickness=0.0)
