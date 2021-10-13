import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
import ocular.core.optical_system as optsys

# TODO: Add the field stop diameter as a third axis.
# https://matplotlib.org/stable/gallery/axisartist/demo_parasite_axes.html
# Or maybe they are better implemented using twinx?
# https://matplotlib.org/stable/gallery/ticks_and_spines/multiple_yaxis_with_spines.html


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("True Field of View")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope)
    max_lines(ax, telescope)
    afov_lines(ax, telescope)
    scatter(ax, telescope, eyepieces)


def yaxis(ax, telescope):
    secax_functions = (optsys.time_in_view, optsys.field_angle)
    flda.true_yaxis(ax,
                    telescope,
                    max_value=max_value(telescope),
                    label=r'$\Delta\theta_{tfov}$ ($\degree$)',
                    max_time_function=optsys.time_in_view,
                    secax_functions=secax_functions)


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.true_field_of_view)


def afov_lines(ax, telescope):
    flda.system_afov_lines(ax, telescope, lambda os: os.true_field_of_view)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.true_field_of_view)


def max_value(telescope):
    return telescope.max_true_field_of_view(barrel_size=telescope.barrel_size, wall_thickness=0.0)
