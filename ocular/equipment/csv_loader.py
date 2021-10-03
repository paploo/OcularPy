import csv

from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.core.manufacturer import Manufacturer
from ocular.core.telescope import Telescope
from ocular.util.tools import map_optional


def load_telescopes(path):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [build_telescope(record) for record in reader]


def load_eyepieces(path):
    with path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [build_eyepiece(record) for record in reader]


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
