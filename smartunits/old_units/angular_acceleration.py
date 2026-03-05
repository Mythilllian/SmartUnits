from .unit import Unit, UnitValue

__all__ = ["AngularAccelerationUnit", "AngularAccelerationValue", "radians_per_second_squared", "degrees_per_second_squared", "turns_per_second_squared"]

class AngularAccelerationUnit(Unit):
    TYPE = "angular_acceleration"

    def __init__(self, base_value: float = 1.0, name: str = "radians per second squared", abbreviation: str = "rad/s^2") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class AngularAccelerationValue(UnitValue):
    unit: AngularAccelerationUnit

    def __init__(self, magnitude: float, unit: AngularAccelerationUnit = AngularAccelerationUnit()) -> None:
        super().__init__(magnitude, unit)

radians_per_second_squared = AngularAccelerationUnit(base_value=1.0, name="radians per second squared", abbreviation="rad/s^2")
degrees_per_second_squared = AngularAccelerationUnit(base_value=0.017453292519943295, name="degrees per second squared", abbreviation="°/s^2")
turns_per_second_squared = AngularAccelerationUnit(base_value=6.283185307179586, name="turns per second squared", abbreviation="turn/s^2")