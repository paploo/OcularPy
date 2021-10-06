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
    def name(self):
        return f"{self.code}[{self.manufacturer.code} {self.model} f/{self.focal_ratio:.1f} {self.objective_diameter:.0f}mm]"


    @property
    def focal_ratio(self):
        return self.focal_length / self.objective_diameter

    @property
    def dawes_limit_arcseconds(self):
        return self.resolving_power_arcseconds(dlp.DAWES)

    def resolving_power_arcseconds(self, diffraction_limit_parameter):
        return diffraction_limit_parameter / self.objective_diameter

    def min_magnification(self, max_pupil_diameter=7.0):
        return self.objective_diameter / max_pupil_diameter

    def max_magnification(self,
                          diffraction_limit_parameter=dlp.COMMON,
                          eye_maximum_resolution_arcseconds=120.0):
        """
        Returns the maximum useful magnification of this optical system due to diffraction limiting.

        In reality, this can be affected by up-to a factor of 2 due to limits due to atmosphere, and the
        comfort of zooming higher than the diffraction limit.

        :param diffraction_limit_parameter: The resolution parameter used to calculate the diffraction limit.
        :param eye_maximum_resolution_arcseconds: The maximum resolution of the viewer's eye in arc-seconds.
        :return: The maximum magnification.
        """
        return eye_maximum_resolution_arcseconds / self.resolving_power_arcseconds(
            diffraction_limit_parameter)

    def magnification_for_eyepeice_focal_length(self, eyepiece_focal_length):
        return self.focal_length / eyepiece_focal_length

    def eyepiece_focal_length_for_magnification(self, magnification):
        return self.focal_length / magnification

    def exit_pupil_for_eyepiece_focal_length(self, eyepiece_focal_length):
        return eyepiece_focal_length / self.focal_ratio

    def eyepiece_focal_length_for_exit_pupil(self, exit_pupil):
        return exit_pupil * self.focal_ratio

    def __str__(self):
        return self.name
