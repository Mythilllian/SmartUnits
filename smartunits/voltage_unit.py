from typing import override

from smartunits.measure import Measure

from smartunits import *
from smartunits.measures import Voltage, ImmutableVoltage, MutVoltage


class VoltageUnit(Unit):
    def __init__(
        self,
        base_unit: "VoltageUnit",
        base_unit_equivalent: float,
        name: str,
        symbol: str,
    ) -> None:
        to_base_converter, from_base_converter = self.base_unit_equivalent_converters(
            base_unit_equivalent
        )
        super().__init__(
            base_unit, to_base_converter, from_base_converter, name, symbol
        )

    def get_base_unit(self) -> "VoltageUnit":
        return self.get_base_unit()

    # def mult(self, current: CurrentUnit, name: str, symbol: str) -> PowerUnit:
    #     # TODO: implement the classes and check
    #     return (
    #         Units.derive(PowerUnit.combine(self, current))
    #         .with_name(name)
    #         .with_symbol(symbol)
    #         .make()
    #     )

    @override
    def of(self, magnitude: float) -> Voltage:
        return ImmutableVoltage(magnitude, self.to_base_units(magnitude), self)

    @override
    def of_base_units(self, magnitude: float) -> Voltage:
        return super().of_base_units(magnitude)

    @override
    def zero(self) -> Voltage:
        return super().zero()
    
    @override
    def one(self) -> Voltage:
        return super().one()
    
    @override
    def mutable(self, magnitude: float) -> MutVoltage:
        return MutVoltage(magnitude, self.to_base_units(magnitude), self)
    
    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        if t is TimeUnit:
            return VelocityUnit.combine(self, other)
        if t is CurrentUnit:
            return PowerUnit.combine(self, other)
        return PerUnit[VoltageUnit, t].combine(self, other)


    def convert_from(self, magnitude: float, other_unit: "VoltageUnit") -> float:
        return self.from_base_units(other_unit.to_base_units(magnitude))
    
    def convert_to(self, magnitude: float, other_unit: "VoltageUnit") -> float:
        return other_unit.from_base_units(self.to_base_units(magnitude))