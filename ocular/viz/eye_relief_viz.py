import ocular.viz.common.fields_and_angles_of_view_axis as flda
import ocular.viz.common.focal_length_axis as fla
from ocular.util import tools
from ocular.viz.common.colors import Gruvbox as Color


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Eye Relief")
    fla.focal_length_xaxis(ax, telescope)
    yaxis(ax, telescope, eyepieces)
    safe_areas(ax, telescope)
    scatter(ax, telescope, eyepieces)
    ax.legend()


def yaxis(ax, telescope, eyepieces):
    snapped_max = tools.snap(tools.max_by(eyepieces, lambda ep: ep.eye_relief), 5.0)
    ax.set_ylim(0.0, snapped_max)
    ax.set_ylabel(r'Eye Relief (mm)')


def scatter(ax, telescope, eyepieces):
    flda.system_scatter(ax, telescope, eyepieces, lambda os: os.eyepiece.eye_relief)


def safe_areas(ax, telescope):
    ax.axhspan(0.0, 10.0, color=Color.RED.alpha(0.2), label=r'Too Short')
    ax.axhspan(10.0, 15.0, color=Color.ORANGE.alpha(0.1), label=r'Unsafe for Glasses')
    ax.axhspan(20.0, 50.0, color=Color.GREEN.alpha(0.1), label=r'Glasses Safe')
