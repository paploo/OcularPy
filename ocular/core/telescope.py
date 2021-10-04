import ocular.core.diffraction_limit_parameter as dlp
from ocular.util.tools import codeize


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
    def code(self):
        """
        Alpha-numeric identification code used to relocate this item out of a library of telescopes.

        A telescope is uniquely identifiable by the manufacturer and model, so we use this
        """
        return f"{self.manufacturer.code}-{codeize(self.model)}"

    @property
    def label(self):
        return f"{self.code}[{self.manufacturer.code} {self.model} f/{self.focal_ratio:.1f} {self.objective_diameter:.0f}mm]"


    @property
    def focal_ratio(self):
        return self.focal_length / self.objective_diameter

    @property
    def dawes_limit_arcseconds(self):
        return self.resolving_power_arcseconds(dlp.DAWES)

    def resolving_power_arcseconds(self, diffraction_limit_parameter):
        return diffraction_limit_parameter / self.objective_diameter

    def __str__(self):
        return self.label
