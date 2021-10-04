from ocular.core.manufacturer import Manufacturer
from ocular.core.telescope import Telescope
from ocular.core.eyepiece import Eyepiece, BarrelSize
from ocular.equipment.favorites import Favorites
from ocular.equipment.library import CatalogKind, Library

televue = Manufacturer('TV', 'TeleVue')
explore = Manufacturer('ES', 'Explore Scientific')
orion = Manufacturer('ORI', 'Orion')
celestron = Manufacturer('CEL', 'Celestron')
gso = Manufacturer('GSO', 'GSO')
svb = Manufacturer('SVB', 'SVBONY')
pentax = Manufacturer('PTX', 'Pentax')
awb = Manufacturer('AWB', 'Astronomers without Borders')
apetura = Manufacturer('APR', 'Apertura')


def sample_telescope_library(name=None):
    return Library.with_items(name or 'Sample Telescopes',
                              CatalogKind.TELESCOPE,
                              sample_telescopes())


def sample_eyepiece_library(name=None):
    return Library.with_items(name or 'Sample Telescopes',
                              CatalogKind.EYEPIECE,
                              sample_eyepieces())


def sample_favorites_library(name=None):
    return Library.with_items(name or 'Sample Favorites',
                              CatalogKind.FAVORITES,
                              [sample_owned_eyepieces(), sample_wishlist()])


def sample_telescopes():
    return [
        Telescope(orion, 'XX12g', 1500.0, 305.0),
        Telescope(apetura, 'AD8', 1200.0, 203.0),
        Telescope(awb, 'OneSky', 650.0, 130.0)
    ]


def sample_eyepieces():
    return [
        Eyepiece(gso,
                 series='SuperPlossl',
                 focal_length=32.0,
                 apparent_field_of_view=52.0,
                 barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
                 field_stop_diameter=28.6,
                 eye_relief=22,
                 mass=123)
    ]


def sample_owned_eyepieces(name=None):
    codes = [
        'SVB-GOLDLINE-6-66-1.25',
        'SVB-GOLDLINE-9-66-1.25',
        'SVB-GOLDLINE-15-66-1.25',
        'SVB-GOLDLINE-20-66-1.25',
        'GSO-SUPERPLOSSL-32-52-1.25',
        'GSO-SUPERVIEW-30-68-2',
        'ES-82-4.7-82-1.25',
        'ORI-DEEPVIEW-28-56-2'
    ]
    return Favorites('OWNED', name or 'Owned', CatalogKind.EYEPIECE, codes)


def sample_wishlist(name=None):
    codes = [
        'TV-DELITE-5-62-1.25',
        'TV-DELITE-13-62-1.25',
        'TV-DELITE-18.2-62-1.25',
        'TV-PANOPTIC-24-68-1.25'
    ]
    return Favorites('WISHLIST', name or 'Wishlist', CatalogKind.EYEPIECE, codes)
