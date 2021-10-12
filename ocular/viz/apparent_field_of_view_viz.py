import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Apparent Field of View")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope)
    max_lines(ax, telescope)
    scatter(ax, telescope, eyepieces)


def yaxis(ax, telescope):
    ax.set_ylim([40, 120])
    ax.set_ylabel(r'$\Delta\theta_{ep}$ ($\degree$)')


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax,
                        telescope,
                        eyepieces,
                        lambda os: os.eyepiece.apparent_field_of_view,
                        label_func=lambda os: os.eyepiece.manufacturer.code)


def max_lines(ax, telescope):
    flda.system_field_stop_lines(ax, telescope, lambda os: os.eyepiece.apparent_field_of_view)
