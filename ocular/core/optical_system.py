
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

    def magnification_minmax(self,
                             max_pupil_diameter=7.0,
                             atmospheric_magnification_limit=300.0,
                             eye_maximum_resolution_arcseconds=116.0):
        """
        Returns a tuple of the minimum and maximum magnifications for the system.

        The min is determined by the maximum pupil diameter.

        The max is determined by when the dawes limit of the telescope is magnified to match the eye's resolution.
        In other words, when  dawes_limit * M = eye_res.

        Note that in common calculations, the eye's resolution is taken to be the same as the parameter for the dawes limit,
        effectively giving the magnification that matches the telescope objective diameter in millimeters!

        :param max_pupil_diameter: The maximum diameter of the viewer's dark-adjusted pupil.
        :param atmospheric_magnification_limit: The maximum magnification allowed by atmospheric conditions.
        :param eye_maximum_resolution_arcseconds: The smallest angle the eye is able to resolve. For the classical approximation, use the dawes limit parameter of 116.
        :return:
        """
        return (self.telescope.objective_diameter / max_pupil_diameter,
                eye_maximum_resolution_arcseconds / self.telescope.dawes_limit_arcseconds)

    def image_resolution_arcseconds(self, limit_parameter=116.0):
        """
        Returns the smallest angle resolvable by the normal human eye.

        This uses the Dawes Limit numerator of 116 for resolution calculation.

        :param limit_parameter: 116 for the Dawes Limit, 120 for standard approximation, 138.4 for Rayleigh @ 550nm
        """
        return limit_parameter / self.magnification
