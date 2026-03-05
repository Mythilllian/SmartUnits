from .unit import Unit, UnitValue

__all__ = ["LengthUnit", "LengthValue", "meters", "nanometers", "micrometers", "millimeters", "centimeters", "kilometers", "feet", "mils", "inches", "miles", "nautical_miles", "astronomical_units", "lightyears", "parsecs", "angstroms", "cubits", "fathoms", "chains", "furlongs", "hands", "leagues", "nautical_leagues", "yards"]

class LengthUnit(Unit):
    TYPE = "length"

    def __init__(self, base_value: float = 1.0, name: str = "meters", abbreviation: str = "m") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class LengthValue(UnitValue):
    unit: LengthUnit

    def __init__(self, magnitude: float, unit: LengthUnit = LengthUnit()) -> None:
        super().__init__(magnitude, unit)

meters = LengthUnit(base_value=1.0, name="meters", abbreviation="m")
nanometers = LengthUnit(base_value=1e-9, name="nanometers", abbreviation="nm")
micrometers = LengthUnit(base_value=1e-6, name="micrometers", abbreviation="µm")
millimeters = LengthUnit(base_value=1e-3, name="millimeters", abbreviation="mm")
centimeters = LengthUnit(base_value=1e-2, name="centimeters", abbreviation="cm")
kilometers = LengthUnit(base_value=1e3, name="kilometers", abbreviation="km")
feet = LengthUnit(base_value=0.3048, name="feet", abbreviation="ft")
mils = LengthUnit(base_value=0.0254, name="mils", abbreviation="mil")
inches = LengthUnit(base_value=0.0254, name="inches", abbreviation="in")
miles = LengthUnit(base_value=1609.344, name="miles", abbreviation="mi")
nautical_miles = LengthUnit(base_value=1852.0, name="nautical miles", abbreviation="nmi")
astronomical_units = LengthUnit(base_value=149597870700.0, name="astronomical units", abbreviation="AU")
lightyears = LengthUnit(base_value=9460730472580800.0, name="light years", abbreviation="ly")
parsecs = LengthUnit(base_value=3.08567758149137e+16, name="parsecs", abbreviation="pc")
angstroms = LengthUnit(base_value=1e-10, name="angstroms", abbreviation="Å")
cubits = LengthUnit(base_value=0.4572, name="cubits", abbreviation="cbt")
fathoms = LengthUnit(base_value=1.8288, name="fathoms", abbreviation="fth")
chains = LengthUnit(base_value=20.1168, name="chains", abbreviation="ch")
furlongs = LengthUnit(base_value=201.168, name="furlongs", abbreviation="fur")
hands = LengthUnit(base_value=0.1016, name="hands", abbreviation="hnd")
leagues = LengthUnit(base_value=4828.032, name="leagues", abbreviation="lea")
nautical_leagues = LengthUnit(base_value=5556.0, name="nautical leagues", abbreviation="nlea")
yards = LengthUnit(base_value=0.9144, name="yards", abbreviation="yd")