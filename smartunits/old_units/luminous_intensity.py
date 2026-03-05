from .unit import Unit, UnitValue

__all__ = ["LuminousIntensityUnit", "LuminousIntensityValue", "candelas", "nanocandelas", "microcandelas", "millicandelas", "kilocandelas"]

class LuminousIntensityUnit(Unit):
    TYPE = "luminous_intensity"

    def __init__(self, base_value: float = 1.0, name: str = "candelas", abbreviation: str = "cd") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class LuminousIntensityValue(UnitValue):
    unit: LuminousIntensityUnit

    def __init__(self, magnitude: float, unit: LuminousIntensityUnit = LuminousIntensityUnit()) -> None:
        super().__init__(magnitude, unit)

candelas = LuminousIntensityUnit(base_value=1.0, name="candelas", abbreviation="cd")
nanocandelas = LuminousIntensityUnit(base_value=1e-9, name="nanocandelas", abbreviation="ncd")
microcandelas = LuminousIntensityUnit(base_value=1e-6, name="microcandelas", abbreviation="µcd")
millicandelas = LuminousIntensityUnit(base_value=1e-3, name="millicandelas", abbreviation="mcd")
kilocandelas = LuminousIntensityUnit(base_value=1e3, name="kilocandelas", abbreviation="kcd")