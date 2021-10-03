"""
A collection of diffraction limit calculation parameters.

These work as numerators in diffraction limit computations. Common values include:

SPARROW

The sparrow limit parameter.

I've seen this value as both 107 and 108 arc-second-millimeters.

DAWES :
    The traditional dawes limit parameter of 116 arc-second-millimeters.
    The dawes limit is an experimentally derived quantity.

COMMON :
    A common estimate of the diffraction limit parameter is 120 arc-second-millimeters.
    This value has the added benefit of working well in equations where it gets the opportunity to cancel with the
    typically quoted 120 arcseconds of visual resolution of the human eye. As such, it is typically a good default.

RAYLEIGH :
    The parameter for the Rayleigh criterion at 550nm, rounded to the nearest integer.
    This is the separation at which, for two stars, the maximum of one's airy disc is found at the minimum of the other's.
    While this is a common mathematically derived definition of resolution, but experimental evidence indicates that
    experienced observers can resolve double stars with separation shorter than this.

GAP :
    The parameter for having a clear black space between the entities.
    This is the separation at which, for two stars, the minimum's of eachother's airy discs overlap.
    This is twice the Rayleigh criterion.
"""

SPARROW = 107.0

DAWES = 116.0

COMMON = 120.0

RAYLEIGH = 138.0

GAP = RAYLEIGH * 2.0


def rayleigh_criterion(wavelength_nanometers):
    return 0.251574581827786 * wavelength_nanometers
