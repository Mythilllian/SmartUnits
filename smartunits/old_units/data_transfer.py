from .unit import Unit, UnitValue

__all__ = ["DataTransferUnit", "DataTransferValue", "exabytes_per_second", "exabits_per_second"]

class DataTransferUnit(Unit):
    TYPE = "data_transfer"

    def __init__(self, base_value: float = 1.0, name: str = "exabytes_per_second", abbreviation: str = "EB/s") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class DataTransferValue(UnitValue):
    unit: DataTransferUnit

    def __init__(self, magnitude: float, unit: DataTransferUnit = DataTransferUnit()) -> None:
        super().__init__(magnitude, unit)
    

yottabytes_per_second = DataTransferUnit(base_value=1e6, name="yottabytes_per_second", abbreviation="YB/s")
yottabits_per_second = DataTransferUnit(base_value=1.25e5, name="yottabits_per_second", abbreviation="Yb/s")
zettabytes_per_second = DataTransferUnit(base_value=1e3, name="zettabytes_per_second", abbreviation="ZB/s")
zettabits_per_second = DataTransferUnit(base_value=125, name="zettabits_per_second", abbreviation="Zb/s")
exabytes_per_second = DataTransferUnit(base_value=1.0, name="exabytes_per_second", abbreviation="EB/s")
exabits_per_second = DataTransferUnit(base_value=0.125, name="exabits_per_second", abbreviation="Eb/s")
petabytes_per_second = DataTransferUnit(base_value=1e-3, name="petabytes_per_second", abbreviation="PB/s")
petabits_per_second = DataTransferUnit(base_value=1.25e-4, name="petabits_per_second", abbreviation="Pb/s")
terabytes_per_second = DataTransferUnit(base_value=1e-6, name="terabytes_per_second", abbreviation="TB/s")
terabits_per_second = DataTransferUnit(base_value=1.25e-7, name="terabits_per_second", abbreviation="Tb/s")
gigabytes_per_second = DataTransferUnit(base_value=1e-9, name="gigabytes_per_second", abbreviation="GB/s")
gigabits_per_second = DataTransferUnit(base_value=1.25e-10, name="gigabits_per_second", abbreviation="Gb/s")
megabytes_per_second = DataTransferUnit(base_value=1e-12, name="megabytes_per_second", abbreviation="MB/s")
megabits_per_second = DataTransferUnit(base_value=1.25e-13, name="megabits_per_second", abbreviation="Mb/s")
kilobytes_per_second = DataTransferUnit(base_value=1e-15, name="kilobytes_per_second", abbreviation="kB/s")
kilobits_per_second = DataTransferUnit(base_value=1.25e-16, name="kilobits_per_second", abbreviation="kb/s")
bytes_per_second = DataTransferUnit(base_value=1e-18, name="bytes_per_second", abbreviation="B/s")
bits_per_second = DataTransferUnit(base_value=1.25e-19, name="bits_per_second", abbreviation="b/s")