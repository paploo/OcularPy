from enum import Enum
import math
import ocular.core.manufacturer as manf
from ocular.util.tools import codeize


class BarrelSize(Enum):
    ONE_AND_A_QUARTER_INCH = ('1.25"', 31.75)
    TWO_INCH = ('2"', 50.80)

    def __init__(self, label, diameter):
        self.label = label
        self.diameter = diameter



class Eyepiece:

    def __init__(self,
                 manufacturer,
                 series,
                 focal_length,
                 apparent_field_of_view,
                 barrel_size,
                 field_stop_diameter=None,
                 eye_relief=None,
                 mass=None):
        self.manufacturer = manufacturer
        self.series = series
        self.focal_length = focal_length
        self.apparent_field_of_view = apparent_field_of_view
        self.barrel_size = barrel_size
        self.field_stop_diameter = field_stop_diameter
        self.eye_relief = eye_relief
        self.mass = mass

    @property
    def code(self):
        """
        Returns an alphanumeric identifier that can be used to identify this eyepiece from a library.

        This is derived from its data.
        """
        parts = [
            self.manufacturer.code,
            codeize(self.series),
            '{:g}'.format(self.focal_length),
            '{:.0f}'.format(self.apparent_field_of_view),
            self.barrel_size.label.replace('"', '')
        ]
        return "-".join(parts)

    @property
    def label(self):
        """
        A nice humanized label/name.
        """
        return f"{self.manufacturer.code} {self.series} {self.focal_length}mm {self.apparent_field_of_view}° {self.barrel_size.label}"

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

    def __str__(self):
        return self.label

    @classmethod
    def widest(cls,
               focal_length,
               barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
               wall_thickness=2.0):
        """
        Creates a generic eyepiece of the given focal length, with the maximum field-of-view available for the barrel size.
        :param focal_length: The target focal length in millimeters.
        :param barrel_size: The barrel size for this eyepiece (BarrelSize enum).
        :param wall_thickness: The wall thickness of the eyepiece; limits the space for the stop size
        :return: A generic eyepiece, idealized to the widest afov.
        """
        desired_stop_diameter = barrel_size.diameter - 2.0 * wall_thickness
        stop_diameter = max(desired_stop_diameter, 0.0)
        afov = math.degrees(stop_diameter / focal_length)
        return cls(manf.generic,
                   focal_length,
                   afov,
                   barrel_size,
                   field_stop_diameter=stop_diameter)

    @classmethod
    def generic(cls,
                focal_length,
                target_apparent_field_of_view,
                barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
                wall_thickness=2.0):
        """
        Creates a generic eyepiece of the given focal length and apparent field of view.

        If the barrel size doesn't allow the eyepiece to exist, then the field of view is automatically constrained.

        :param focal_length: The focal length in millimeters
        :param target_apparent_field_of_view: The apparent field of view in degrees
        :param barrel_size: The barrels size (enum value)
        :param wall_thickness: The thickness of the wall; limits the space for the stop.
        :return: The generic eyepiece.
        """
        desired_stop_diameter = math.radians(target_apparent_field_of_view) * focal_length
        max_stop_diameter = barrel_size.diameter - 2.0 * wall_thickness
        stop_diameter = min(desired_stop_diameter, max_stop_diameter)
        afov = math.degrees(stop_diameter / focal_length)
        return cls(manf.generic,
                   focal_length,
                   afov,
                   barrel_size,
                   field_stop_diameter=stop_diameter)
