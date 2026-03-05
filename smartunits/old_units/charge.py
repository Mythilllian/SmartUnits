from smartmechanismsystem.units.unit import Unit, UnitValue

__all__ = ["ChargeUnit", "ChargeValue", "coulombs", "nanocoulombs", "microcoulombs", "millicoulombs", "kilocoulombs", "ampere_hours", "nanoampere_hours", "microampere_hours", "milliampere_hours", "kiloampere_hours"]

class ChargeUnit(Unit):
    TYPE = "charge"

    def __init__(self, base_value: float = 1.0, name: str = "coulombs", abbreviation: str = "C") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class ChargeValue(UnitValue):
    unit: ChargeUnit

    def __init__(self, magnitude: float, unit: ChargeUnit = ChargeUnit()) -> None:
        super().__init__(magnitude, unit)

coulombs = ChargeUnit(base_value=1.0, name="coulombs", abbreviation="C")
nanocoulombs = ChargeUnit(base_value=1e-9, name="nanocoulombs", abbreviation="nC")
microcoulombs = ChargeUnit(base_value=1e-6, name="microcoulombs", abbreviation="µC")
millicoulombs = ChargeUnit(base_value=1e-3, name="millicoulombs", abbreviation="mC")
kilocoulombs = ChargeUnit(base_value=1e3, name="kilocoulombs", abbreviation="kC")
ampere_hours = ChargeUnit(base_value=3600.0, name="ampere hours", abbreviation="Ah")
nanoampere_hours = ChargeUnit(base_value=3.6e-6, name="nanoampere hours", abbreviation="nAh")
microampere_hours = ChargeUnit(base_value=3.6e-3, name="microampere hours", abbreviation="µAh")
milliampere_hours = ChargeUnit(base_value=3.6, name="milliampere hours", abbreviation="mAh")
kiloampere_hours = ChargeUnit(base_value=3.6e3, name="kiloampere hours", abbreviation="kAh")
