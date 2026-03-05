from .unit import Unit, UnitValue

__all__ = ["FrequencyUnit", "FrequencyValue", "hertz", "nanohertz", "microhertz", "millihertz", "kilohertz"]

class FrequencyUnit(Unit):
    TYPE = "frequency"

    def __init__(self, base_value: float = 1.0, name: str = "hertz", abbreviation: str = "Hz") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class FrequencyValue(UnitValue):
    unit: FrequencyUnit

    def __init__(self, magnitude: float, unit: FrequencyUnit = FrequencyUnit()) -> None:
        super().__init__(magnitude, unit)

hertz = FrequencyUnit(base_value=1.0, name="hertz", abbreviation="Hz")
nanohertz = FrequencyUnit(base_value=1e-9, name="nanohertz", abbreviation="nHz")
microhertz = FrequencyUnit(base_value=1e-6, name="microhertz", abbreviation="µHz")
millihertz = FrequencyUnit(base_value=1e-3, name="millihertz", abbreviation="mHz")
kilohertz = FrequencyUnit(base_value=1e3, name="kilohertz", abbreviation="kHz")