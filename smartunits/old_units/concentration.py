from .unit import Unit, UnitValue

__all__ = ["ConcentrationUnit", "ConcentrationValue", "percent", "parts_per_million", "parts_per_billion", "parts_per_trillion"]

class ConcentrationUnit(Unit):
    TYPE = "concentration"

    def __init__(self, base_value: float = 1.0, name: str = "parts_per_million", abbreviation: str = "ppm") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class ConcentrationValue(UnitValue):
    unit: ConcentrationUnit

    def __init__(self, magnitude: float, unit: ConcentrationUnit = ConcentrationUnit()) -> None:
        super().__init__(magnitude, unit)

percent = ConcentrationUnit(base_value=1.0, name="percent", abbreviation="%")
parts_per_million = ConcentrationUnit(base_value=1e-6, name="parts per million", abbreviation="ppm")
parts_per_billion = ConcentrationUnit(base_value=1e-9, name="parts per billion", abbreviation="ppb")
parts_per_trillion = ConcentrationUnit(base_value=1e-12, name="parts per trillion", abbreviation="ppt")