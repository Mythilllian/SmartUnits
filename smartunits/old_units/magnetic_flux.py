from .unit import Unit, UnitValue

__all__ = ["MagneticFluxUnit", "MagneticFluxValue", "webers", "nanowebers", "microwebers", "milliwebers", "kilowebers", "maxwells"]

class MagneticFluxUnit(Unit):
    TYPE = "magnetic_flux"

    def __init__(self, base_value: float = 1.0, name: str = "webers", abbreviation: str = "Wb") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class MagneticFluxValue(UnitValue):
    unit: MagneticFluxUnit

    def __init__(self, magnitude: float, unit: MagneticFluxUnit = MagneticFluxUnit()) -> None:
        super().__init__(magnitude, unit)

webers = MagneticFluxUnit(base_value=1.0, name="webers", abbreviation="Wb")
nanowebers = MagneticFluxUnit(base_value=1e-9, name="nanowebers", abbreviation="nWb")
microwebers = MagneticFluxUnit(base_value=1e-6, name="microwebers", abbreviation="µWb")
milliwebers = MagneticFluxUnit(base_value=1e-3, name="milliwebers", abbreviation="mWb")
kilowebers = MagneticFluxUnit(base_value=1e3, name="kilowebers", abbreviation="kWb")
maxwells = MagneticFluxUnit(base_value=1e-8, name="maxwells", abbreviation="Mx")