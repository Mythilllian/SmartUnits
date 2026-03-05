from .unit import Unit, UnitValue

__all__ = ["DataUnit", "DataValue", "yottabytes", "yottabits", "zettabytes", "zettabits", "exabytes", "exabits", "petabytes", "petabits", "terabytes", "terabits", "gigabytes", "gigabits", "megabytes", "megabits", "kilobytes", "kilobits", "bytes", "bits"]

class DataUnit(Unit):
    TYPE = "data"

    def __init__(self, base_value: float = 1.0, name: str = "exabytes_per_second", abbreviation: str = "EB/s") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class DataValue(UnitValue):
    unit: DataUnit

    def __init__(self, magnitude: float, unit: DataUnit = DataUnit()) -> None:
        super().__init__(magnitude, unit)

yottabytes = DataUnit(base_value=1e6, name="yottabytes", abbreviation="YB")
yottabits = DataUnit(base_value=1.25e5, name="yottabits", abbreviation="Yb")
zettabytes = DataUnit(base_value=1e3, name="zettabytes", abbreviation="ZB")
zettabits = DataUnit(base_value=125, name="zettabits", abbreviation="Zb")
exabytes = DataUnit(base_value=1.0, name="exabytes", abbreviation="EB")
exabits = DataUnit(base_value=0.125, name="exabits", abbreviation="Eb")
petabytes = DataUnit(base_value=1e-3, name="petabytes", abbreviation="PB")
petabits = DataUnit(base_value=1.25e-4, name="petabits", abbreviation="Pb")
terabytes = DataUnit(base_value=1e-6, name="terabytes", abbreviation="TB")
terabits = DataUnit(base_value=1.25e-7, name="terabits", abbreviation="Tb")
gigabytes = DataUnit(base_value=1e-9, name="gigabytes", abbreviation="GB")
gigabits = DataUnit(base_value=1.25e-10, name="gigabits", abbreviation="Gb")
megabytes = DataUnit(base_value=1e-12, name="megabytes", abbreviation="MB")
megabits = DataUnit(base_value=1.25e-13, name="megabits", abbreviation="Mb")
kilobytes = DataUnit(base_value=1e-15, name="kilobytes", abbreviation="kB")
kilobits = DataUnit(base_value=1.25e-16, name="kilobits", abbreviation="kb")
bytes = DataUnit(base_value=1e-18, name="bytes", abbreviation="B")
bits = DataUnit(base_value=1.25e-19, name="bits", abbreviation="b")