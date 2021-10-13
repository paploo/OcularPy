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
    print(eyepiece_lib)

    telescopes = csv_loader.load_telescope_library(Path('./equipment/telescopes.csv'))
    print(telescopes)

    favorites = csv_loader.load_favorites_library(Path('./equipment/favorites.csv'))
    print(favorites)

    all_favs = reduce(lambda a, b: a + b, favorites.catalog.values())
    print(all_favs)

    telescope = telescopes.catalog['ORI-XX12G']
    #telescope = telescopes.catalog['APR-AD8']
    #telescope = telescopes.catalog['AWB-ONESKY']
    #telescope = telescopes.catalog['MDE-LX90']

    eyepieces = eyepiece_lib.filter_favorites(all_favs).catalog.values()
    #eyepieces = eyepiece_lib.catalog.values()

    plt.rcParams['figure.figsize'] = [16, 11]
    plt.rcParams['figure.subplot.hspace'] = 0.40
    fig, axes = plt.subplots(2, 2)
    apparent_field_of_view_viz.make_plot(axes[0][0], telescope, eyepieces)
    field_stop_diameter_viz.make_plot(axes[0][1], telescope, eyepieces)
    true_field_of_view_viz.make_plot(axes[1][0], telescope, eyepieces)
    true_angle_of_view_viz.make_plot(axes[1][1], telescope, eyepieces)
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
