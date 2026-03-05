from .unit import Unit, UnitValue

__all__ = ["LuminousFluxUnit", "LuminousFluxValue", "lumens", "nanolumens", "microlumens", "millilumens", "kilolumens"]

class LuminousFluxUnit(Unit):
    TYPE = "luminous_flux"

    def __init__(self, base_value: float = 1.0, name: str = "lumens", abbreviation: str = "lm") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class LuminousFluxValue(UnitValue):
    unit: LuminousFluxUnit

    def __init__(self, magnitude: float, unit: LuminousFluxUnit = LuminousFluxUnit()) -> None:
        super().__init__(magnitude, unit)

lumens = LuminousFluxUnit(base_value=1.0, name="lumens", abbreviation="lm")
nanolumens = LuminousFluxUnit(base_value=1e-9, name="nanolumens", abbreviation="nlm")
microlumens = LuminousFluxUnit(base_value=1e-6, name="microlumens", abbreviation="µlm")
millilumens = LuminousFluxUnit(base_value=1e-3, name="millilumens", abbreviation="mlm")
kilolumens = LuminousFluxUnit(base_value=1e3, name="kilolumens", abbreviation="klm")