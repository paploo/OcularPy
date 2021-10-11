import numpy as np

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.optical_system import OpticalSystem
from ocular.viz.common.colors import barrel_color
import ocular.viz.common.focal_length_axis as fla


def make_plot(ax, telescope, eyepieces):
    ax.grid(True)
    ax.set_title("Apparent Field of View")
    fla.focal_length_xaxis(ax, telescope)
    afov_yaxis(ax, telescope)
    afov_max_lines(ax, telescope)
    afov_scatter(ax, telescope, eyepieces)
    ax.legend()


def afov_yaxis(ax, telescope):
    ax.set_ylim([40, 120])
    ax.set_ylabel(r'$\Delta\theta_{ep}$ ($\degree$)')


def afov_scatter(ax, telescope, eyepieces):
    optical_systems = OpticalSystem.combinations(telescope, eyepieces)
    x = [s.eyepiece.focal_length for s in optical_systems]
    y = [s.eyepiece.apparent_field_of_view for s in optical_systems]
    s = [s.eyepiece.barrel_size.diameter for s in optical_systems]
    c = [barrel_color(s.eyepiece.barrel_size).value for s in optical_systems]
    ax.scatter(x, y, s=s, c=c)

    for os in optical_systems:
        ax.annotate(os.eyepiece.manufacturer.code,
                    (os.eyepiece.focal_length, os.eyepiece.apparent_field_of_view),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


def afov_max_lines(ax, telescope):
    def afov(focal_length, barrel_size, wall_thickness):
        eyepiece = Eyepiece.generic(focal_length,
                                    barrel_size=barrel_size,
                                    wall_thickness=wall_thickness)
        return eyepiece.apparent_field_of_view

    options = [
        (BarrelSize.TWO_INCH, 0.0, None),
        (BarrelSize.TWO_INCH, 2.0, 'dashed'),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 0.0, None),
        (BarrelSize.ONE_AND_A_QUARTER_INCH, 2.0, 'dashed')
    ]

    fls = np.arange(fla.VIZ_FOCAL_LENGTH_DELTA, fla.VIZ_FOCAL_LENGTH_MAX, fla.VIZ_FOCAL_LENGTH_DELTA)

    for opt in options:
        afovs = [afov(fl, barrel_size=opt[0], wall_thickness=opt[1]) for fl in fls]
        label = opt[0].label if (opt[1] == 0.0) else None
        ax.plot(fls, afovs, color=barrel_color(opt[0]).value, linestyle=opt[2], label=label)
