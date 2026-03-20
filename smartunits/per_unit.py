from smartunits import Unit, UnaryFunction, CombinatoryUnitCache, TimeUnit, VelocityUnit, Units, Measure
from smartunits.measures import Per
from typing import Any, TypeVar, Generic, override

N = TypeVar("N", bound=Unit)  # numerator
D = TypeVar("D", bound=Unit)  # denominator

class PerUnit(Unit, Generic[N, D]):
    _cache: CombinatoryUnitCache[Unit, Unit, "PerUnit"] = CombinatoryUnitCache[N, D](lambda num, denom: PerUnit.from_fraction(num, denom))

    def __init__(
        self,
        base_unit: "PerUnit[N, D]",
        to_base_converter: UnaryFunction,
        from_base_converter: UnaryFunction,
        name: str,
        symbol: str,
        numerator: N = None,
        denominator: D = None,
    ) -> None:
        super().__init__(
            base_unit, to_base_converter, from_base_converter, name, symbol
        )
        self._numerator = numerator if numerator else self.denominator()
        self._denominator = denominator if denominator else self.denominator()

    @staticmethod
    def from_fraction(
        numerator: N, denominator: D, base_unit: "PerUnit[N, D]" = None
    ) -> "PerUnit[N, D]":
        return PerUnit[N, D](
            base_unit
            if base_unit
            else (
                None
                if numerator.is_base_unit() and denominator.is_base_unit()
                else self.combine(
                    numerator.get_base_unit(), denominator.get_base_unit()
                )
            ),
            UnaryFunction(lambda x: numerator.get_converter_to_base().apply(x) / denominator.get_converter_to_base().apply(1)),
            UnaryFunction(lambda x: numerator.get_converter_from_base().apply(x) / denominator.get_converter_from_base().apply(1)),
            numerator.name() + " per " + denominator.name(),
            numerator.symbol() + "/" + denominator.symbol(),
        )
    
    @staticmethod
    def combine(numerator: N, denominator: D) -> "PerUnit[N, D]":
        return _cache.combine(numerator, denominator)
    
    @override
    def get_base_unit(self) -> "PerUnit[N, D]":
        return super().get_base_unit()
    
    def numerator(self) -> N:
        return self._numerator
    
    def denominator(self) -> D:
        return self._denominator
    
    def reciprocal(self) -> "PerUnit[D, N]":
        if isinstance(self._numerator, TimeUnit):
            return VelocityUnit.combine(self._denominator, self._numerator)
        else:
            return self.combine(self.denominator(), self.numerator())
        
    def mult(self, denom: D) -> N:
        if denom.equivalent(self.denominator()):
            return self.numerator()
        
        return Units.derive(self.numerator()) \
            .to_base(denom.get_converter_to_base() / self.denominator().get_converter_to_base()) \
            .from_base(denom.get_converter_from_base() / self.denominator().get_converter_from_base()) \
            .named(self.name() + " " + denom.name()) \
            .symbol(self.symbol() + " " + denom.symbol()) \
            .make()
    
    @override
    def of(self, magnitude: float) -> Measure[PerUnit[N, D]]:
        return self.of_native(magnitude)
    
    @override
    def of_base_units(self, magnitude: float) -> Measure[Any]:
        return self.of_native_base_units(magnitude)
    
    def of_native(self, magnitude: float) -> Per[N, D]:
        return ImmutablePer[N, D](magnitude, self.to_base_units(magnitude), self)
    
    def of_native_base_units(self, magnitude: float) -> Per[N, D]:
        return ImmutablePer[N, D](self.to_base_units(magnitude), magnitude, self)
    
    @override
    def zero(self) -> Per[N, D]:
        return super().zero()
    
    @override
    def one(self) -> Per[N, D]:
        return super().one()

    @override
    def per(self, time: TimeUnit) -> "PerUnit[N, TimeUnit]":
        return VelocityUnit.combine(self, time)

    def convert_from(self, magnitude: float, other_unit: "PerUnit[N, D]") -> float:
        return self.from_base_units(other_unit.to_base_units(magnitude))
    
    @override
    def __eq__(self, other: object) -> bool:
        if super().__eq__(other):
            return True
        if not other or not isinstance(other, type(self)):
            return False
        
        return self.numerator() == other.numerator() and self.denominator() == other.denominator()
    
    @override
    def __hash__(self) -> int:
        return hash((super().__hash__(), self.numerator(), self.denominator()))