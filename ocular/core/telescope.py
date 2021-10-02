from ocular.core.DiffractionLimitParameter import DiffractionLimitParameter


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
        return self.resolving_power_arcseconds(DiffractionLimitParameter.DAWES)

    def resolving_power_arcseconds(self, diffraction_limit_parameter):
        return diffraction_limit_parameter / self.objective_diameter
