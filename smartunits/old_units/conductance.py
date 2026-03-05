from .unit import Unit, UnitValue

__all__ = ["ConductanceUnit", "ConductanceValue", "siemens", "nanosiemens", "microsiemens", "millisiemens", "kilosiemens"]

class ConductanceUnit(Unit):
    TYPE = "conductance"

    def __init__(self, base_value: float = 1.0, name: str = "siemens", abbreviation: str = "S") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class ConductanceValue(UnitValue):
    unit: ConductanceUnit

    def __init__(self, magnitude: float, unit: ConductanceUnit = ConductanceUnit()) -> None:
        super().__init__(magnitude, unit)
    
siemens = ConductanceUnit(base_value=1.0, name="siemens", abbreviation="S")
nanosiemens = ConductanceUnit(base_value=1e-9, name="nanosiemens", abbreviation="nS")
microsiemens = ConductanceUnit(base_value=1e-6, name="microsiemens", abbreviation="µS")
millisiemens = ConductanceUnit(base_value=1e-3, name="millisiemens", abbreviation="mS")
kilosiemens = ConductanceUnit(base_value=1e3, name="kilosiemens", abbreviation="kS")