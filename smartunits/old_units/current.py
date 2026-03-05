from .unit import Unit, UnitValue

__all__ = ["CurrentUnit", "CurrentValue", "amperes", "nanoamperes", "microamperes", "milliamperes", "kiloamperes"]

class CurrentUnit(Unit):
    TYPE = "current"

    def __init__(self, base_value: float = 1.0, name: str = "amperes", abbreviation: str = "A") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class CurrentValue(UnitValue):
    unit: CurrentUnit

    def __init__(self, magnitude: float, unit: CurrentUnit = CurrentUnit()) -> None:
        super().__init__(magnitude, unit)
    
amperes = CurrentUnit(base_value=1.0, name="amperes", abbreviation="A")
nanoamperes = CurrentUnit(base_value=1e-9, name="nanoamperes", abbreviation="nA")
microamperes = CurrentUnit(base_value=1e-6, name="microamperes", abbreviation="µA")
milliamperes = CurrentUnit(base_value=1e-3, name="milliamperes", abbreviation="mA")
kiloamperes = CurrentUnit(base_value=1e3, name="kiloamperes", abbreviation="kA")