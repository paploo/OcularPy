import csv
import os.path
from itertools import groupby

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.manufacturer import Manufacturer
from ocular.core.telescope import Telescope
from ocular.equipment.library import Library, CatalogKind, Favorites
from ocular.util.tools import map_optional


def load_telescope_library(path, name=None):
    library = Library.with_items(name or os.path.basename(path),
                                 CatalogKind.TELESCOPE,
                                 load_by_line(path, build_telescope))
    return library


def load_eyepiece_library(path, name=None):
    library = Library.with_items(name or os.path.basename(path),
                                 CatalogKind.EYEPIECE,
                                 load_by_line(path, build_eyepiece))
    return library


def load_by_line(path, builder):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [builder(record) for record in reader]


def build_manufacturer(record):
    return Manufacturer(record['manufacturer_code'], record['manufacturer_name'])


barrel_size_string_map = {'1.25': BarrelSize.ONE_AND_A_QUARTER_INCH,
                          '2.00': BarrelSize.TWO_INCH,
                          '31.75': BarrelSize.ONE_AND_A_QUARTER_INCH,
                          '50.80': BarrelSize.TWO_INCH}


def build_barrel_size(record):
    size_str = record['barrel_diameter']
    return barrel_size_string_map[size_str]


def build_eyepiece(record):
    return Eyepiece(manufacturer=build_manufacturer(record),
                    series=record['series'],
                    focal_length=float(record['focal_length']),
                    apparent_field_of_view=float(record['apparent_field_of_view']),
                    barrel_size=build_barrel_size(record),
                    field_stop_diameter=map_optional(float, record.get('field_stop_diameter'), ),
                    eye_relief=map_optional(float, record.get('eye_relief')),
                    mass=map_optional(float, record.get('mass')))


def build_telescope(record):
    return Telescope(manufacturer=build_manufacturer(record),
                     model=record['model'],
                     focal_length=float(record['focal_length']),
                     objective_diameter=float(record['objective_diameter']))


# TODO: Allow line-by-line aggregation; this is actually better served with JSON or YAML.
def load_favorites_library(path, name=None):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    sorted_rows = sorted(rows, key=favorites_key)
    grouped_rows = {k: [r['code'] for r in g] for k, g in groupby(sorted_rows, favorites_key)}
    favs = [build_favorites(k, vs) for k, vs in grouped_rows.items()]
    return Library.with_items(name or os.path.basename(path),
                              CatalogKind.FAVORITES,
                              favs)


def favorites_code(row):
    return row['code']


def favorites_key(row):
    return row['list_code'], row['list_name'], row['kind']


def build_favorites(key, codes):
    return Favorites(code=key[0], name=key[1], kind=CatalogKind(key[2]), codes=codes)
