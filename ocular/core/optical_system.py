import ocular.core.diffraction_limit_parameter as dlp


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

    def max_eyepiece_focal_length(self, max_pupil_diameter=7.0):
        min_mag = self.min_magnification(max_pupil_diameter)
        return self.telescope.focal_length / min_mag

    def max_eyepiece_focal_length(self,
                                  diffraction_limit_parameter=dlp.COMMON,
                                  eye_maximum_resolution_arcseconds=120.0):
        max_mag = self.max_magnification(diffraction_limit_parameter, eye_maximum_resolution_arcseconds)
        return self.telescope.focal_length / max_mag

    def min_magnification(self, max_pupil_diameter=7.0):
        return self.telescope.objective_diameter / max_pupil_diameter

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
        return eye_maximum_resolution_arcseconds / self.telescope.resolving_power_arcseconds(
            diffraction_limit_parameter)

    def image_resolution_arcseconds(self, eye_maximum_resolution_arcseconds=120.0):
        """
        Returns the smallest angle resolvable by the normal human eye for the system.

        This is determined by determining what angular size, when magnified, would be the viewer's resolution limit.
        """
        return 120.0 / self.magnification

    def __str__(self):
        return f"OpticalSystem(telescope={self.telescope}, eyepiece={self.eyepiece})"
