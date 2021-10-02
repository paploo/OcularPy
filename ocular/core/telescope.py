class Telescope:

    def __init__(self,
                 manufacturer,
                 focal_length,
                 objective_diameter):
        self.manufacturer = manufacturer
        self.focal_length = focal_length
        self.objective_diameter = objective_diameter

    @property
    def focal_ratio(self):
        return self.focal_length / self.objective_diameter

    @property
    def dawes_limit_arcseconds(self):
        return self.resolving_power_arcseconds(116.0)

    def resolving_power_arcseconds(self, limit_parameter):
        """
        Calculates the diffraction limit of the telescope in arcseconds, using a variable parameter.
        Common values of the limit_parameter include:
        Sparrow: 107
        Dawes: 116
        Common: 120
        Rayleigh Criterion @ 550nm: 138.4
        "Full gap spacing": 277 (twice rayleigh)

        :param limit_parameter: The numerator when calculating the resolving power.
        :return: The resolving power in arcseconds
        """
        return limit_parameter / self.objective_diameter

    def rayleigh_criteria_arcseconds(self, wavelength_nanometers):
        return self.resolving_power_arcseconds(0.251574581827786 * wavelength_nanometers)