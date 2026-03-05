from .unit import Unit, UnitValue
import math

__all__ = ["AngleUnit", "AngleValue", "radians", "nanoradians", "microradians", "milliradians", "kiloradians", "degrees", "arcminutes", "arcseconds", "milliarcseconds", "turns", "gradians"]

class AngleUnit(Unit):
    TYPE = "angle"

    def __init__(self, base_value: float = 1.0, name: str = "radians", abbreviation: str = "rad") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class AngleValue(UnitValue):
    unit: AngleUnit

    def __init__(self, magnitude: float, unit: AngleUnit = AngleUnit()) -> None:
        super().__init__(magnitude, unit)

    def sin_of_angle(self) -> float:
        return math.sin(super().get_magnitude_in_base_unit())
    
    def cos_of_angle(self) -> float:
        return math.cos(super().get_magnitude_in_base_unit())
    
    def tan_of_angle(self) -> float:
        return math.tan(super().get_magnitude_in_base_unit())
    

radians = AngleUnit(base_value=1.0, name="radians", abbreviation="rad")
nanoradians = AngleUnit(base_value=1e-9, name="nanoradians", abbreviation="nrad")
microradians = AngleUnit(base_value=1e-6, name="microradians", abbreviation="µrad")
milliradians = AngleUnit(base_value=1e-3, name="milliradians", abbreviation="mrad")
kiloradians = AngleUnit(base_value=1e3, name="kiloradians", abbreviation="krad")
degrees = AngleUnit(base_value=0.017453292519943295, name="degrees", abbreviation="°")
arcminutes = AngleUnit(base_value=0.0002908882086657216, name="arcminutes", abbreviation="'")
arcseconds = AngleUnit(base_value=0.00000484813681109536, name="arcseconds", abbreviation='"')
milliarcseconds = AngleUnit(base_value=4.84813681109536e-9, name="milliarcseconds", abbreviation="mas")
turns = AngleUnit(base_value=6.283185307179586, name="turns", abbreviation="turn")
gradians = AngleUnit(base_value=0.015707963267948967, name="gradians", abbreviation="gon")