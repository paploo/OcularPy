import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
from ocular.core.eyepiece import BarrelSize


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Field Stop Diameter")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope)
    max_lines(ax, telescope)
    scatter(ax, telescope, eyepieces)
    ax.legend()


def yaxis(ax, telescope):
    #TODO: Need to build the right conversion functions and then this should work.
    pass
    secax_functions = (true_field_of_view_to_time_in_field_of_view, time_in_field_of_view_to_true_field_of_view)
    flda.true_yaxis(ax,
                    telescope,
                    max_value=BarrelSize.TWO_INCH.value,
                    label=r'$\Delta\theta_{tfov}$ ($\degree$)',
                    max_time_function=true_field_of_view_to_time_in_field_of_view,
                    secax_functions=secax_functions)


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.eyepiece.field_stop_diameter)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.eyepiece.field_stop_diameter)

def stop_diameter_to_time_in_field_of_view(stop_diameter, telescope):
    pass