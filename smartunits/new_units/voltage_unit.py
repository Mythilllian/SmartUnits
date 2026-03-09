from typing import override
from . import Unit


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
        return self._base_unit

    # def mult(self, current: CurrentUnit, name: str, symbol: str) -> PowerUnit:
    #     # TODO: implement the classes and check
    #     return (
    #         Units.derive(PowerUnit.combine(self, current))
    #         .with_name(name)
    #         .with_symbol(symbol)
    #         .make()
    #     )

    @override
    def of(self, magnitude: float) -> "VoltageMeasure":
        return ImmutableVoltage(magnitude, self.to_base_units(magnitude), self)

    @override
    def of_base_units(self, magnitude: float):
        return super().of_base_units(magnitude)

    # TODO finish
