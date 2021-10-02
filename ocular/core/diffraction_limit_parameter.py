
class DiffractionLimitParameter:
    SPARROW = 107.0
    DAWES = 116.0
    COMMON = 120.0
    RAYLEIGH = 138

    @staticmethod
    def rayleigh_criterion(wavelength_nanometers):
        return 0.251574581827786 * wavelength_nanometers
