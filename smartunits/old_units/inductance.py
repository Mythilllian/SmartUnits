from .unit import Unit, UnitValue

__all__ = ["InductanceUnit", "InductanceValue", "henries", "nanohenries", "microhenries", "millihenries", "kilohenries"]

class InductanceUnit(Unit):
    TYPE = "inductance"

    def __init__(self, base_value: float = 1.0, name: str = "henries", abbreviation: str = "H") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class InductanceValue(UnitValue):
    unit: InductanceUnit

    def __init__(self, magnitude: float, unit: InductanceUnit = InductanceUnit()) -> None:
        super().__init__(magnitude, unit)

henries = InductanceUnit(base_value=1.0, name="henries", abbreviation="H")
nanohenries = InductanceUnit(base_value=1e-9, name="nanohenries", abbreviation="nH")
microhenries = InductanceUnit(base_value=1e-6, name="microhenries", abbreviation="µH")
millihenries = InductanceUnit(base_value=1e-3, name="millihenries", abbreviation="mH")
kilohenries = InductanceUnit(base_value=1e3, name="kilohenries", abbreviation="kH")