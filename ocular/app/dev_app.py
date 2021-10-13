from functools import reduce, cached_property
from pathlib import Path
from ocular.equipment import csv_loader
import matplotlib.pyplot as plt

from ocular.viz import apparent_field_of_view_viz
from ocular.viz import true_angle_of_view_viz
from ocular.viz import true_field_of_view_viz
from ocular.viz import field_stop_diameter_viz


class DevApp:

    def run(self):
        charts = self.charts()
        telescopes = self.telescopes()
        eyepieces = self.eyepieces()

        plt.rcParams['figure.figsize'] = [18, 11]
        plt.rcParams['figure.subplot.hspace'] = 0.40
        fig, axes = plt.subplots(len(telescopes), len(charts))
        for j, telescope in enumerate(telescopes):
            for i, chart in enumerate(charts):
                chart.make_plot(axes[j][i], telescope, eyepieces)
        plt.show()

    def charts(self):
        return [
            apparent_field_of_view_viz,
            field_stop_diameter_viz,
            true_field_of_view_viz,
            # true_angle_of_view_viz
        ]

    def telescopes(self):
        return [
            self.telescope_lib['ORI-XX12G'],
            self.telescope_lib['APR-AD8'],
            self.telescope_lib['AWB-ONESKY']
        ]

    def eyepieces(self):
        all_favs_lib = reduce(lambda a, b: a + b, self.favorites_lib.catalog.values())
        return self.eyepiece_lib.filter_favorites(all_favs_lib).catalog.values()

    @cached_property
    def eyepiece_lib(self):
        return csv_loader.load_eyepiece_library(Path('./equipment/eyepieces.csv'))

    @cached_property
    def telescope_lib(self):
        return csv_loader.load_telescope_library(Path('./equipment/telescopes.csv'))

    @cached_property
    def favorites_lib(self):
        return csv_loader.load_favorites_library(Path('./equipment/favorites.csv'))
