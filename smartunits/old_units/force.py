from .unit import Unit, UnitValue

__all__ = ["ForceUnit", "ForceValue", "newtons", "nanonewtons", "micronewtons", "millinewtons", "kilonewtons", "pounds", "dynes", "kiloponds", "poundals"]

class ForceUnit(Unit):
    TYPE = "force"

    def __init__(self, base_value: float = 1.0, name: str = "newtons", abbreviation: str = "N") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class ForceValue(UnitValue):
    unit: ForceUnit

    def __init__(self, magnitude: float, unit: ForceUnit = ForceUnit()) -> None:
        super().__init__(magnitude, unit)

newtons = ForceUnit(base_value=1.0, name="newtons", abbreviation="N")
nanonewtons = ForceUnit(base_value=1e-9, name="nanonewtons", abbreviation="nN")
micronewtons = ForceUnit(base_value=1e-6, name="micronewtons", abbreviation="µN")
millinewtons = ForceUnit(base_value=1e-3, name="millinewtons", abbreviation="mN")
kilonewtons = ForceUnit(base_value=1e3, name="kilonewtons", abbreviation="kN")
pounds = ForceUnit(base_value=4.44822, name="pounds", abbreviation="lbf")
dynes = ForceUnit(base_value=1e-5, name="dynes", abbreviation="dyn")
kiloponds = ForceUnit(base_value=9.80665, name="kiloponds", abbreviation="kp")
poundals = ForceUnit(base_value=4.44822, name="poundals", abbreviation="pdl")