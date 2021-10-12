import math

import ocular.core.diffraction_limit_parameter as dlp
from ocular.core.eyepiece import BarrelSize, Eyepiece


class OpticalSystem:

    def __init__(self, telescope, eyepiece):
        self.telescope = telescope
        self.eyepiece = eyepiece

    @property
    def magnification(self):
        return self.telescope.magnification_for_eyepeice_focal_length(self.eyepiece.focal_length)

    @property
    def exit_pupil_diameter(self):
        return self.telescope.exit_pupil_for_eyepiece_focal_length(self.eyepiece.focal_length)

    @property
    def true_field_of_view(self):
        return self.eyepiece.apparent_field_of_view / self.magnification

    @property
    def true_angle_of_view(self):
        return math.degrees(2.0 * math.atan((self.eyepiece.field_stop_diameter / 2.0) / self.telescope.focal_length))

    @property
    def angle_of_view_magnification(self):
        """
        Calculates the magnification of the system using the true angle of view ratio instead of the paraxial approximation
        that is typically used.

        I'm not sure if this is a real thing.
        """
        return self.eyepiece.apparent_angle_of_view / self.true_angle_of_view

    def time_in_field_of_view(self, declination=0.0):
        return time_in_view(self.true_field_of_view, declination)

    def time_in_angle_of_view(self, declination=0.0):
        return time_in_view(self.true_angle_of_view, declination)

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


def sky_rotation_rate(declination=0.0):
    return (360.0 / 86400.0) * math.cos(math.radians(declination))


def time_in_view(field_angle, declination=0.0):
    return field_angle / sky_rotation_rate(declination)


def field_angle(time_in_view, declination=0.0):
    return time_in_view * sky_rotation_rate(declination)

