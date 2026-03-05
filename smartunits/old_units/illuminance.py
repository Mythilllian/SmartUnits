from .unit import Unit, UnitValue

__all__ = ["IlluminanceUnit", "IlluminanceValue", "luxes", "nanoluxes", "microluxes", "milliluxes", "kiloluxes", "footcandles", "lumens_per_square_inch", "phots"]

class IlluminanceUnit(Unit):
    TYPE = "illuminance"

    def __init__(self, base_value: float = 1.0, name: str = "lux", abbreviation: str = "lx") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class IlluminanceValue(UnitValue):
    unit: IlluminanceUnit

    def __init__(self, magnitude: float, unit: IlluminanceUnit = IlluminanceUnit()) -> None:
        super().__init__(magnitude, unit)

luxes = IlluminanceUnit(base_value=1.0, name="lux", abbreviation="lx")
nanoluxes = IlluminanceUnit(base_value=1e-9, name="nanoluxes", abbreviation="nlx")
microluxes = IlluminanceUnit(base_value=1e-6, name="microluxes", abbreviation="µlx")
milliluxes = IlluminanceUnit(base_value=1e-3, name="milliluxes", abbreviation="mlx")
kiloluxes = IlluminanceUnit(base_value=1e3, name="kiloluxes", abbreviation="klx")
footcandles = IlluminanceUnit(base_value=10.7639, name="footcandles", abbreviation="fc")
lumens_per_square_inch = IlluminanceUnit(base_value=1550.0031, name="lumens per square inch", abbreviation="lm/in²")
phots = IlluminanceUnit(base_value=10000.0, name="phots", abbreviation="ph")