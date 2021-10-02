from ocular.core.DiffractionLimitParameter import DiffractionLimitParameter


class OpticalSystem:

    def __init__(self, telescope, eyepiece):
        self.telescope = telescope
        self.eyepiece = eyepiece

    @property
    def magnification(self):
        return self.telescope.focal_length / self.eyepiece.focal_length

    @property
    def exit_pupil_diameter(self):
        return self.telescope.objective_diameter / self.magnification

    @property
    def true_field_of_view(self):
        return self.eyepiece.apparent_field_of_view / self.magnification

    @property
    def true_angle_of_view(self):
        return self.eyepiece.apparent_angle_of_view / self.magnification

    def magnification_min(self, max_pupil_diameter=7.0):
        return self.telescope.objective_diameter / max_pupil_diameter

    def magnification_max(self,
                          atmospheric_magnification_limit=300.0,
                          diffraction_limit_parameter=DiffractionLimitParameter.COMMON,
                          eye_maximum_resolution_arcseconds=120.0):
        """
        Returns the maximum useful magnification of this optical system.
        :param atmospheric_magnification_limit: The maximum magnification the atmosphere will allow.
        :param diffraction_limit_parameter: The resolution parameter used to calculate the diffraction limit.
        :param eye_maximum_resolution_arcseconds: The maximum resolution of the viewer's eye in arc-seconds.
        :return: The maximum magnification.
        """
        return eye_maximum_resolution_arcseconds / self.telescope.resolving_power_arcseconds(diffraction_limit_parameter)

    def image_resolution_arcseconds(self, eye_maximum_resolution_arcseconds=120.0):
        """
        Returns the smallest angle resolvable by the normal human eye for the system.

        This is determined by determining what angular size, when magnified, would be the viewer's resolution limit.
        """
        return 120.0 / self.magnification
