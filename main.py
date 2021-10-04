from functools import reduce
from pathlib import Path
from ocular.equipment import csv_loader
from ocular.equipment import sample_loader


def main():
    eyepiece_lib = csv_loader.load_eyepiece_library(Path('./equipment/eyepieces.csv'))
    print(eyepiece_lib)

    telescopes = csv_loader.load_telescope_library(Path('./equipment/telescopes.csv'))
    print(telescopes)

    favorites = csv_loader.load_favorites_library(Path('./equipment/favorites.csv'))
    print(favorites)

    all_favs = reduce(lambda a, b: a + b, favorites.catalog.values())
    print(all_favs)


if __name__ == '__main__':
    main()
