from .unit import Unit, UnitValue

__all__ = ["DensityUnit", "DensityValue", "kilograms_per_cubic_meter", "grams_per_milliliter", "kilograms_per_liter", "ounces_per_cubic_foot", "ounces_per_cubic_inch", "ounces_per_gallon", "pounds_per_cubic_foot", "pounds_per_cubic_inch", "pounds_per_gallon", "slugs_per_cubic_foot"]

class DensityUnit(Unit):
    TYPE = "density"

    def __init__(self, base_value: float = 1.0, name: str = "kilograms_per_cubic_meter", abbreviation: str = "kg/m³") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class DensityValue(UnitValue):
    unit: DensityUnit

    def __init__(self, magnitude: float, unit: DensityUnit = DensityUnit()) -> None:
        super().__init__(magnitude, unit)

kilograms_per_cubic_meter = DensityUnit(base_value=1.0, name="kilograms_per_cubic_meter", abbreviation="kg/m³")
grams_per_milliliter = DensityUnit(base_value=1e-3, name="grams_per_milliliter", abbreviation="g/mL")
kilograms_per_liter = DensityUnit(base_value=1.0, name="kilograms_per_liter", abbreviation="kg/L")
ounces_per_cubic_foot = DensityUnit(base_value=1.929e-5, name="ounces_per_cubic_foot", abbreviation="oz/ft³")
ounces_per_cubic_inch = DensityUnit(base_value=5.787e-8, name="ounces_per_cubic_inch", abbreviation="oz/in³")
ounces_per_gallon = DensityUnit(base_value=7.489e-4, name="ounces_per_gallon", abbreviation="oz/gal")
pounds_per_cubic_foot = DensityUnit(base_value=1.602e-5, name="pounds_per_cubic_foot", abbreviation="lb/ft³")
pounds_per_cubic_inch = DensityUnit(base_value=9.259e-8, name="pounds_per_cubic_inch", abbreviation="lb/in³")
pounds_per_gallon = DensityUnit(base_value=1.036e-3, name="pounds_per_gallon", abbreviation="lb/gal")
slugs_per_cubic_foot = DensityUnit(base_value=5.154e-4, name="slugs_per_cubic_foot", abbreviation="slug/ft³")