from .unit import Unit, UnitValue

__all__ = ["RadiationUnit", "RadiationValue", "becquerels", "nanobecquerels", "microbecquerels", "millibecquerels", "kilobecquerels", "grays", "nanograys", "micrograys", "milligrays", "kilograys", "sieverts", "nanosieverts", "microsieverts", "millisieverts", "kilosieverts", "curies", "rutherfords", "rads"]

class RadiationUnit(Unit):
    TYPE = "radiation"

    def __init__(self, base_value: float = 1.0, name: str = "becquerels", abbreviation: str = "Bq") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class RadiationValue(UnitValue):
    unit: RadiationUnit

    def __init__(self, magnitude: float, unit: RadiationUnit = RadiationUnit()) -> None:
        super().__init__(magnitude, unit)

becquerels = RadiationUnit(base_value=1.0, name="becquerels", abbreviation="Bq")
nanobecquerels = RadiationUnit(base_value=1e-9, name="nanobecquerels", abbreviation="nBq")
microbecquerels = RadiationUnit(base_value=1e-6, name="microbecquerels", abbreviation="µBq")
millibecquerels = RadiationUnit(base_value=1e-3, name="millibecquerels", abbreviation="mBq")
kilobecquerels = RadiationUnit(base_value=1e3, name="kilobecquerels", abbreviation="kBq")
grays = RadiationUnit(base_value=1.0, name="grays", abbreviation="Gy")
nanograys = RadiationUnit(base_value=1e-9, name="nanograys", abbreviation="nGy")
micrograys = RadiationUnit(base_value=1e-6, name="micrograys", abbreviation="µGy")
milligrays = RadiationUnit(base_value=1e-3, name="milligrays", abbreviation="mGy")
kilograys = RadiationUnit(base_value=1e3, name="kilograys", abbreviation="kGy")
sieverts = RadiationUnit(base_value=1.0, name="sieverts", abbreviation="Sv")
nanosieverts = RadiationUnit(base_value=1e-9, name="nanosieverts", abbreviation="nSv")
microsieverts = RadiationUnit(base_value=1e-6, name="microsieverts", abbreviation="µSv")
millisieverts = RadiationUnit(base_value=1e-3, name="millisieverts", abbreviation="mSv")
kilosieverts = RadiationUnit(base_value=1e3, name="kilosieverts", abbreviation="kSv")
curies = RadiationUnit(base_value=3.7e10, name="curies", abbreviation="Ci")
rutherfords = RadiationUnit(base_value=1e6, name="rutherfords", abbreviation="R")
rads = RadiationUnit(base_value=1e-2, name="rads", abbreviation="rad")