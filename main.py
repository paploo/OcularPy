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
    eyepieces = eyepiece_lib.filter_favorites(all_favs).catalog.values()

    plt.rcParams['figure.figsize'] = [12,9]
    print(plt.rcParams.get('figure.figsize'))

    fig, ax = plt.subplots()
    #apparent_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    #true_angle_of_view_viz.make_plot(ax, telescope, eyepieces)
    #true_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    field_stop_diameter_viz.make_plot(ax, telescope, eyepieces)
    ax.legend()
    plt.draw()

    fig, ax = plt.subplots()
    apparent_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    #true_angle_of_view_viz.make_plot(ax, telescope, eyepieces)
    #true_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    #field_stop_diameter_viz.make_plot(ax, telescope, eyepieces)
    ax.legend()
    plt.draw()

    plt.show()


if __name__ == '__main__':
    main()
