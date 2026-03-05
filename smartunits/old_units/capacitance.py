from .unit import Unit, UnitValue

__all__ = ["CapitanceUnit", "CapitanceValue", "farads", "nanofarads", "microfarads", "millifarads", "kilofarads"]

class CapitanceUnit(Unit):
    TYPE = "capacitance"

    def __init__(self, base_value: float = 1.0, name: str = "farads", abbreviation: str = "F") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class CapitanceValue(UnitValue):
    unit: CapitanceUnit

    def __init__(self, magnitude: float, unit: CapitanceUnit = CapitanceUnit()) -> None:
        super().__init__(magnitude, unit)

farads = CapitanceUnit(base_value=1.0, name="farads", abbreviation="F")
nanofarads = CapitanceUnit(base_value=1e-9, name="nanofarads", abbreviation="nF")
microfarads = CapitanceUnit(base_value=1e-6, name="microfarads", abbreviation="µF")
millifarads = CapitanceUnit(base_value=1e-3, name="millifarads", abbreviation="mF")
kilofarads = CapitanceUnit(base_value=1e3, name="kilofarads", abbreviation="kF")
