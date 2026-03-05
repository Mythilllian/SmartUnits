from .unit import Unit, UnitValue

__all__ = ["EnergyUnit", "EnergyValue", "joules", "nanojoules", "microjoules", "millijoules", "kilojoules", "calories", "nanocalories", "microcalories", "millicalories", "kilocalories", "kilowatt_hours", "watt_hours", "british_thermal_units", "british_thermal_units_iso", "british_thermal_units_59", "therms", "foot_pounds"]

class EnergyUnit(Unit):
    TYPE = "energy"

    def __init__(self, base_value: float = 1.0, name: str = "joules", abbreviation: str = "J") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class EnergyValue(UnitValue):
    unit: EnergyUnit

    def __init__(self, magnitude: float, unit: EnergyUnit = EnergyUnit()) -> None:
        super().__init__(magnitude, unit)

joules = EnergyUnit(base_value=1.0, name="joules", abbreviation="J")
nanojoules = EnergyUnit(base_value=1e-9, name="nanojoules", abbreviation="nJ")
microjoules = EnergyUnit(base_value=1e-6, name="microjoules", abbreviation="µJ")
millijoules = EnergyUnit(base_value=1e-3, name="millijoules", abbreviation="mJ")
kilojoules = EnergyUnit(base_value=1e3, name="kilojoules", abbreviation="kJ")
calories = EnergyUnit(base_value=4.184, name="calories", abbreviation="cal")
nanocalories = EnergyUnit(base_value=4.184e-9, name="nanocalories", abbreviation="ncal")
microcalories = EnergyUnit(base_value=4.184e-6, name="microcalories", abbreviation="µcal")
millicalories = EnergyUnit(base_value=4.184e-3, name="millicalories", abbreviation="mcal")
kilocalories = EnergyUnit(base_value=4.184e3, name="kilocalories", abbreviation="kcal")
kilowatt_hours = EnergyUnit(base_value=3.6e6, name="kilowatt hours", abbreviation="kWh")
watt_hours = EnergyUnit(base_value=3600.0, name="watt hours", abbreviation="Wh")
british_thermal_units = EnergyUnit(base_value=1055.06, name="british thermal units", abbreviation="BTU")
british_thermal_units_iso = EnergyUnit(base_value=1055.05585262, name="british thermal units (ISO)", abbreviation="BTU(ISO)")
british_thermal_units_59 = EnergyUnit(base_value=1054.350264, name="british thermal units (59°F)", abbreviation="BTU(59°F)")
therms = EnergyUnit(base_value=1.055e8, name="therms", abbreviation="thm")
foot_pounds = EnergyUnit(base_value=1.3558179483314004, name="foot-pounds", abbreviation="ft·lbf")