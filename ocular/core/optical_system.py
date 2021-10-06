import ocular.core.diffraction_limit_parameter as dlp
from ocular.core.eyepiece import BarrelSize, Eyepiece


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

    # def max_eyepiece_focal_length(self, max_pupil_diameter=7.0):
    #     min_mag = self.min_magnification(max_pupil_diameter)
    #     return self.telescope.focal_length / min_mag
    #
    # def max_eyepiece_focal_length(self,
    #                               diffraction_limit_parameter=dlp.COMMON,
    #                               eye_maximum_resolution_arcseconds=120.0):
    #     max_mag = self.max_magnification(diffraction_limit_parameter, eye_maximum_resolution_arcseconds)
    #     return self.telescope.focal_length / max_mag


    def image_resolution_arcseconds(self, eye_maximum_resolution_arcseconds=120.0):
        """
        Returns the smallest angle resolvable by the normal human eye for the system.

        This is determined by determining what angular size, when magnified, would be the viewer's resolution limit.
        """
        return 120.0 / self.magnification

    def __str__(self):
        return f"OpticalSystem(telescope={self.telescope}, eyepiece={self.eyepiece})"

    @classmethod
    def combinations(cls, telescope, eyepieces):
        return [cls(telescope, ep) for ep in eyepieces]

    @classmethod
    def matched_exit_pupil_diameter(cls,
                                    telescope,
                                    exit_pupil_diameter,
                                    target_apparent_field_of_view=None,
                                    barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
                                    wall_thickness=2.0):
        """
        Creates a system with the given telescope, and an eyepiece that matches the requested exit pupil.
        """
        target_focal_length = exit_pupil_diameter * telescope.focal_ratio
        eyepiece = Eyepiece.generic(target_focal_length, target_apparent_field_of_view, barrel_size, wall_thickness)
        return OpticalSystem(telescope, eyepiece)

def focal_length_to_exit_pupil(telescope, focal_length):
    # This works out to be focal_length / telescope.focal_ratio, but with encapsulation.
    # optsys = OpticalSystem(telescope, Eyepiece.generic(focal_length))
    # return optsys.exit_pupil_diameter
    return focal_length / telescope.focal_ratio

# def focal_length_to_exit_pupil(telescope):
#     """
#     Returns a function that maps a focal length into an exit pupil for the given telescope.
#     """
#     def exit_pupil_func(focal_length):
#         # This works out to be focal_length / telescope.focal_ratio, but with encapsulation.
#         # optsys = OpticalSystem(telescope, Eyepiece.generic(focal_length))
#         # return optsys.exit_pupil_diameter
#         return focal_length / telescope.focal_ratio
#     return exit_pupil_func


def exit_pupil_to_focal_length(telescope):
    """
    Returns a function that maps an exit pupil into a focal elngth for the given telescope.
    """
    def focal_length_func(exit_pupil):
        # This works out to be exit_pupil * telescope.focal_ratio, but with encapsulation.
        # optsys = OpticalSystem.matched_exit_pupil_diameter(telescope, exit_pupil)
        # return optsys.eyepiece.focal_length
        return exit_pupil * telescope.focal_ratio
    return focal_length_func

def focal_length_to_magnification(telescope):
    def magnification(focal_length):
        return focal_length