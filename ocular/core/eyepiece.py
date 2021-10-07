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
    def name(self):
        """
        A nice humanized name.
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
        rads = 2.0 * math.atan(0.5 * (self.field_stop_diameter / self.focal_length))
        return math.degrees(rads)

    def __str__(self):
        return self.name

    @classmethod
    def generic(cls,
                focal_length,
                target_apparent_field_of_view=None,
                barrel_size=BarrelSize.ONE_AND_A_QUARTER_INCH,
                wall_thickness=2.0):
        """
        Creates a generic eyepiece of the given focal length.

        If no field of view is given, it attempts to give the widest possible field of view.

        If the barrel size doesn't allow the eyepiece to exist, then the field of view is automatically constrained.

        :param focal_length: The focal length in millimeters
        :param target_apparent_field_of_view: The apparent field of view in degrees; if None, then auto generates the widest possible.
        :param barrel_size: The barrels size (enum value)
        :param wall_thickness: The thickness of the wall; limits the space for the stop.
        :return: The generic eyepiece.
        """
        if target_apparent_field_of_view is None:
            desired_stop_diameter = barrel_size.diameter - 2.0 * wall_thickness
        else:
            desired_stop_diameter = math.radians(target_apparent_field_of_view) * focal_length

        max_stop_diameter = barrel_size.diameter - 2.0 * wall_thickness
        min_stop_diameter = 0.0
        stop_diameter = max(min(desired_stop_diameter, max_stop_diameter), min_stop_diameter)

        afov = math.degrees(stop_diameter / focal_length)

        # afov is a standard mathematical construction, but it totally breaks-down at large FoVs,
        # so we insert some sanity for the purpose of our visualizations.
        afov = min(afov, 180.0)

        return cls(manf.generic,
                   "Generic",
                   focal_length,
                   afov,
                   barrel_size,
                   field_stop_diameter=stop_diameter)


def degrees_to_arcseconds(degrees):
    return degrees * 3600.0


def arcseconds_to_degrees(arcseconds):
    return arcseconds / 3600.0


def degrees_to_arcminutes(degrees):
    return degrees * 60.0


def arcminutes_to_degrees(arcminutes):
    return arcminutes / 60.0
