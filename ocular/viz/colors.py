from enum import Enum

from ocular.core.eyepiece import BarrelSize


class Gruvbox(Enum):
    BLACK = '#1d2021'
    WHITE = '#f9f5d7'

    GRAY = '#928374'
    RED = '#cc241d'
    GREEN = '#98791a'
    YELLOW = 'd79921'
    BLUE = '#458588'
    PURPLE = '#b16286'
    AQUA = '#689d6a'
    ORANGE = '#d65d0e'

    LIGHT_GRAY = '#a89984'
    LIGHT_RED = '#fb4934'
    LIGHT_GREEN = '#b8bb26'
    LIGHT_YELLOW = '#fabd2f'
    LIGHT_BLUE = '#83a598'
    LIGHT_PURPLE = '#d3869b'
    LIGHT_AQUA = '#8ec07c'
    LIGHT_ORANGE = '#fe8019'

    DARK_GRAY = '#282828'
    DARK_RED = '#9d0006'
    DARK_GREEN = '#79740e'
    DARK_YELLOW = '#b57614'
    DARK_BLUE = '#076678'
    DARK_PURPLE = '#8f3f71'
    DARK_AQUA = '#427b58'
    DARK_ORANGE = '#af3a03'

    @property
    def hex_value(self):
        return self.value

    @property
    def to_tuple(self):
        r = int(self.value[1:3], base=16) / 255.0
        g = int(self.value[3:5], base=16) / 255.0
        b = int(self.value[5:7], base=16) / 255.0
        return r, g, b

    def alpha(self, alpha=0.0):
        r, g, b = self.to_tuple
        return r, g, b, alpha


def barrel_color(barrel_size):
    if barrel_size == BarrelSize.ONE_AND_A_QUARTER_INCH:
        return Gruvbox.BLUE
    if barrel_size == BarrelSize.TWO_INCH:
        return Gruvbox.ORANGE
