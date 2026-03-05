from .unit import Unit, UnitValue

__all__ = ["MagneticStrengthUnit", "MagneticStrengthValue", "teslas", "nanoteslas", "microteslas", "milliteslas", "kiloteslas", "gauss"]

class MagneticStrengthUnit(Unit):
    TYPE = "magnetic_strength"

    def __init__(self, base_value: float = 1.0, name: str = "teslas", abbreviation: str = "T") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class MagneticStrengthValue(UnitValue):
    unit: MagneticStrengthUnit

    def __init__(self, magnitude: float, unit: MagneticStrengthUnit = MagneticStrengthUnit()) -> None:
        super().__init__(magnitude, unit)

teslas = MagneticStrengthUnit(base_value=1.0, name="teslas", abbreviation="T")
nanoteslas = MagneticStrengthUnit(base_value=1e-9, name="nanoteslas", abbreviation="nT")
microteslas = MagneticStrengthUnit(base_value=1e-6, name="microteslas", abbreviation="µT")
milliteslas = MagneticStrengthUnit(base_value=1e-3, name="milliteslas", abbreviation="mT")
kiloteslas = MagneticStrengthUnit(base_value=1e3, name="kiloteslas", abbreviation="kT")
gauss = MagneticStrengthUnit(base_value=1e-4, name="gauss", abbreviation="G")