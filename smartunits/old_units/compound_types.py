# TODO: add more support for different types of compound units

from .unit import Unit, UnitValue
from .__init__ import *

__all__ = ["PerUnit", "Per"]

class PerUnit(Unit):
    numerator: Unit
    denominator: Unit

    def __init__(self, base_value: float, numerator: Unit, denominator: Unit, name: str = None, abbreviation: str = None) -> None:
        if name is None:
            name = numerator.name + " per " + denominator.name.removesuffix("s")
        if abbreviation is None:
            abbreviation = numerator.abbreviation + "/" + denominator.abbreviation

        super().__init__(base_value, name, abbreviation)
        self.numerator = numerator
        self.denominator = denominator
        self.TYPE = self.numerator.TYPE + "_per_" + self.denominator.TYPE

class Per(UnitValue):
    def __init__(self, magnitude: float, unit: PerUnit) -> None:
        super().__init__(magnitude, unit)

    def __str__(self) -> str:
        return self.unit.name

# radians_per_meter = float
# radians_per_second_per_volt = float
# units_per_second = float
# units_per_second_squared = float
# volt_seconds = float
# volt_seconds_squared = float
# volt_seconds_per_meter = float
# volt_seconds_squared_per_meter = float
# volt_seconds_per_feet = float
# volt_seconds_squared_per_feet = float
# volt_seconds_per_radian = float
# volt_seconds_squared_per_radian = float
# unit_seconds_squared_per_unit = float
# meters_per_second_squared_per_volt = float