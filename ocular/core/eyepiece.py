from enum import Enum
import math


class Eyepiece:

    def __init__(self,
                 manufacturer,
                 focal_length,
                 apparent_field_of_view,
                 barrel_size,
                 field_stop_diameter=None,
                 eye_relief=None,
                 mass=None):
        self.manufacturer = manufacturer
        self.focal_length = focal_length
        self.apparent_field_of_view = apparent_field_of_view
        self.barrel_size = barrel_size
        self.field_stop_diameter = field_stop_diameter
        self.eye_relief = eye_relief
        self.mass = mass

    @property
    def stop_afov(self):
        """
        Calculates the AFoV from the stop diameter using the most common method.

        This matches real world numbers for AFoV better, but isn't as mathematically sound as the trig version.

        :return: The apparent field of view in degrees
        """
        return math.degrees(self.field_stop_diameter / self.focal_length)

    @property
    def apparent_angle_of_view(self):
        """
        Uses large-angle compatible trigonometry to derive the apparent field of view from the field stop diameter.

        This is defined by ISO 14132-1:2002 as teh apparent angle of view.

        This number is typically about 10% off from the reported apparent fields of view, which use the small angle approximation.
        :return: The apparent field of view in degrees
        """
        return 2.0 * math.atan(0.5 * (self.field_stop_diameter / self.focal_length))


class BarrelSize(Enum):
    ONE_AND_A_QUARTER_INCH = 31.75
    TWO_INCH = 50.80

    def __init__(self, diameter):
        self.diameter = diameter
