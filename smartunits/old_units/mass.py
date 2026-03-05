from .unit import Unit, UnitValue

__all__ = ["MassUnit", "MassValue", "grams", "nanograms", "micrograms", "milligrams", "kilograms", "metric_tons", "pounds", "long_tons", "short_tons", "stone", "ounces", "carats", "slugs"]

class MassUnit(Unit):
    TYPE = "mass"

    def __init__(self, base_value: float = 1.0, name: str = "kilograms", abbreviation: str = "kg") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class MassValue(UnitValue):
    unit: MassUnit

    def __init__(self, magnitude: float, unit: MassUnit = MassUnit()) -> None:
        super().__init__(magnitude, unit)

kilograms = MassUnit(base_value=1.0, name="kilograms", abbreviation="kg")
grams = MassUnit(base_value=1e-3, name="grams", abbreviation="g")
nanograms = MassUnit(base_value=1e-9, name="nanograms", abbreviation="ng")
micrograms = MassUnit(base_value=1e-6, name="micrograms", abbreviation="µg")
milligrams = MassUnit(base_value=1e-3, name="milligrams", abbreviation="mg")
metric_tons = MassUnit(base_value=1e3, name="metric_tons", abbreviation="t")
pounds = MassUnit(base_value=0.453592, name="pounds", abbreviation="lb")
long_tons = MassUnit(base_value=1016.047, name="long_tons", abbreviation="lt")
short_tons = MassUnit(base_value=907.185, name="short_tons", abbreviation="st")
stone = MassUnit(base_value=6.35029, name="stone", abbreviation="st")
ounces = MassUnit(base_value=28.3495, name="ounces", abbreviation="oz")
carats = MassUnit(base_value=0.2, name="carats", abbreviation="ct")
slugs = MassUnit(base_value=14.5939, name="slugs", abbreviation="slug")