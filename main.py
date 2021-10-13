from functools import reduce
from pathlib import Path
from ocular.equipment import csv_loader
from ocular.equipment import sample_loader
import matplotlib.pyplot as plt

from ocular.viz import apparent_field_of_view_viz
from ocular.viz import true_angle_of_view_viz
from ocular.viz import true_field_of_view_viz
from ocular.viz import field_stop_diameter_viz


def main():
    eyepiece_lib = csv_loader.load_eyepiece_library(Path('./equipment/eyepieces.csv'))
    telescope_lib = csv_loader.load_telescope_library(Path('./equipment/telescopes.csv'))
    favorites_lib = csv_loader.load_favorites_library(Path('./equipment/favorites.csv'))
    all_favs_lib = reduce(lambda a, b: a + b, favorites_lib.catalog.values())

    telescope = telescope_lib['ORI-XX12G']
    #telescope = telescope_lib['APR-AD8']
    #telescope = telescope_lib['AWB-ONESKY']
    #telescope = telescope_lib['MDE-LX90']

    eyepieces = eyepiece_lib.filter_favorites(all_favs_lib).catalog.values()
    #eyepieces = eyepiece_lib.catalog.values()

    charts = [
        apparent_field_of_view_viz,
        field_stop_diameter_viz,
        true_field_of_view_viz,
        #true_angle_of_view_viz
    ]
    print(charts)

    telescopes = [
        telescope_lib['ORI-XX12G'],
        telescope_lib['APR-AD8']
    ]
    print(telescopes)

    plt.rcParams['figure.figsize'] = [18, 11]
    plt.rcParams['figure.subplot.hspace'] = 0.40
    fig, axes = plt.subplots(len(telescopes), len(charts))
    for j, telescope in enumerate(telescopes):
        for i, chart in enumerate(charts):
            chart.make_plot(axes[j][i], telescope, eyepieces)
    plt.show()

    # plt.rcParams['figure.figsize'] = [12,9]
    # fig, ax = plt.subplots()
    # apparent_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    # true_angle_of_view_viz.make_plot(ax, telescope, eyepieces)
    # true_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    # field_stop_diameter_viz.make_plot(ax, telescope, eyepieces)
    # ax.legend()
    # plt.draw() # Way to draw multple plots in different windows.
    # plt.show() # Only do this once.


if __name__ == '__main__':
    main()
