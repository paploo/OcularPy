import ocular.core.diffraction_limit_parameter as dlp


class Telescope:

    def __init__(self,
                 manufacturer,
                 model,
                 focal_length,
                 objective_diameter):
        self.manufacturer = manufacturer
        self.model = model
        self.focal_length = focal_length
        self.objective_diameter = objective_diameter

    @property
    def focal_ratio(self):
        return self.focal_length / self.objective_diameter

    @property
    def dawes_limit_arcseconds(self):
        return self.resolving_power_arcseconds(dlp.DAWES)

    def resolving_power_arcseconds(self, diffraction_limit_parameter):
        return diffraction_limit_parameter / self.objective_diameter

    def __str__(self):
        return f"{self.manufacturer.code} {self.model} f/{self.focal_ratio:.1f} {self.objective_diameter:.0f}mm"
