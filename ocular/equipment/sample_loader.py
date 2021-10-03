from ocular.core.manufacturer import Manufacturer
from ocular.core.telescope import Telescope
from ocular.core.eyepiece import Eyepiece, BarrelSize

televue = Manufacturer('TV', 'TeleVue')
explore = Manufacturer('ES', 'Explore Scientific')
orion = Manufacturer('ORI', 'Orion')
celestron = Manufacturer('CEL', 'Celestron')
gso = Manufacturer('GSO', 'GSO')
svb = Manufacturer('SVB', 'SVBONY')
pentax = Manufacturer('PTX', 'Pentax')
awb = Manufacturer('AWB', 'Astronomers without Borders')
apetura = Manufacturer('APR', 'Apertura')


def load_telescopes(path):
    return [
        Telescope(orion, 'XX12g', 1500.0, 305.0),
        Telescope(apetura, 'AD8', 1200.0, 203.0),
        Telescope(awb, 'OneSky', 650.0, 130.0)
    ]


def load_eyepieces(path):
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
