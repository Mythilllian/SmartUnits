from .unit import Unit, UnitValue

__all__ = ["MomentOfInertiaUnit", "MomentOfInertiaValue", "kilogram_square_meters", "gram_square_centimeters", "pound_square_feet", "ounce_square_inches"]

class MomentOfInertiaUnit(Unit):
    TYPE = "moment_of_inertia"

    def __init__(self, base_value: float = 1.0, name: str = "kilogram square meters", abbreviation: str = "kg·m²") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class MomentOfInertiaValue(UnitValue):
    unit: MomentOfInertiaUnit

    def __init__(self, magnitude: float, unit: MomentOfInertiaUnit = MomentOfInertiaUnit()) -> None:
        super().__init__(magnitude, unit)

kilogram_square_meters = MomentOfInertiaUnit(base_value=1.0, name="kilogram square meters", abbreviation="kg·m²")
gram_square_centimeters = MomentOfInertiaUnit(base_value=1e-7, name="gram square centimeters", abbreviation="g·cm²")
pound_square_feet = MomentOfInertiaUnit(base_value=0.04214011, name="pound square feet", abbreviation="lb·ft²")
ounce_square_inches = MomentOfInertiaUnit(base_value=0.00064516, name="ounce square inches", abbreviation="oz·in²")