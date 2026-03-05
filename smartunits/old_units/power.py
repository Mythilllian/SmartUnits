from .unit import Unit, UnitValue

__all__ = ["PowerUnit", "PowerValue", "watts", "nanowatts", "microwatts", "milliwatts", "kilowatts", "horsepower"]

class PowerUnit(Unit):
    TYPE = "power"

    def __init__(self, base_value: float = 1.0, name: str = "watts", abbreviation: str = "W") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class PowerValue(UnitValue):
    unit: PowerUnit

    def __init__(self, magnitude: float, unit: PowerUnit = PowerUnit()) -> None:
        super().__init__(magnitude, unit)

watts = PowerUnit(base_value=1.0, name="watts", abbreviation="W")
nanowatts = PowerUnit(base_value=1e-9, name="nanowatts", abbreviation="nW")
microwatts = PowerUnit(base_value=1e-6, name="microwatts", abbreviation="µW")
milliwatts = PowerUnit(base_value=1e-3, name="milliwatts", abbreviation="mW")
kilowatts = PowerUnit(base_value=1e3, name="kilowatts", abbreviation="kW")
horsepower = PowerUnit(base_value=745.7, name="horsepower", abbreviation="hp")