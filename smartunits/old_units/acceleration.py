from .unit import Unit, UnitValue

__all__ = ["AccelerationUnit", "AccelerationValue", "meters_per_second_squared", "feet_per_second_squared", "standard_gravity"]

class AccelerationUnit(Unit):
    TYPE = "acceleration"

    def __init__(self, base_value: float = 1.0, name: str = "meters per second squared", abbreviation: str = "m/s^2") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class AccelerationValue(UnitValue):
    unit: AccelerationUnit

    def __init__(self, magnitude: float, unit: AccelerationUnit = AccelerationUnit()) -> None:
        super().__init__(magnitude, unit)

meters_per_second_squared = AccelerationUnit(base_value=1.0, name="meters per second squared", abbreviation="m/s^2")
feet_per_second_squared = AccelerationUnit(base_value=0.3048, name="feet per second squared", abbreviation="ft/s^2")
standard_gravity = AccelerationUnit(base_value=9.80665, name="standard gravity", abbreviation="g")