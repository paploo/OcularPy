from functools import reduce, cached_property
from pathlib import Path
from ocular.equipment import csv_loader
import matplotlib.pyplot as plt

from ocular.viz import apparent_field_of_view_viz
from ocular.viz import true_angle_of_view_viz
from ocular.viz import true_field_of_view_viz
from ocular.viz import field_stop_diameter_viz
from ocular.viz import eye_relief_viz


class DevApp:

    def run(self):
        self.plot_telescopes()
        #self.plot_eye_relief()

    def plot_telescopes(self):
        charts = self.charts()
        telescopes = self.telescopes()
        eyepieces = self.selected_eyepieces()

        #plt.rcParams['figure.figsize'] = [18, 11] #16" MBP Safe
        plt.rcParams['figure.figsize'] = [30, 16] #27" iMac Safe
        plt.rcParams['figure.subplot.hspace'] = 0.40
        fig, axes = plt.subplots(len(telescopes), len(charts))
        for j, telescope in enumerate(telescopes):
            for i, chart in enumerate(charts):
                chart.make_plot(axes[j][i], telescope, eyepieces)
        plt.show()

    def plot_eye_relief(self):
        telescope = self.telescope_lib['ORI-XX12G']
        #eyepieces = self.all_eyepieces()
        eyepieces = self.selected_eyepieces()

        plt.rcParams['figure.figsize'] = [12, 9]
        plt.rcParams['figure.subplot.hspace'] = 0.40
        fig, ax = plt.subplots()
        eye_relief_viz.make_plot(ax, telescope, eyepieces)
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

    def selected_eyepieces(self):
        all_favs_lib = reduce(lambda a, b: a + b, self.favorites_lib.catalog.values())
        return self.eyepiece_lib.filter_favorites(all_favs_lib).catalog.values()

    def all_eyepieces(self):
        return self.eyepiece_lib.catalog.values()

    @cached_property
    def eyepiece_lib(self):
        return csv_loader.load_eyepiece_library(Path('./equipment/eyepieces.csv'))

    @cached_property
    def telescope_lib(self):
        return csv_loader.load_telescope_library(Path('./equipment/telescopes.csv'))

    @cached_property
    def favorites_lib(self):
        return csv_loader.load_favorites_library(Path('./equipment/favorites.csv'))
