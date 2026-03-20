from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from smartunits import (
    Unit,
    # Dimensionless,
    # PerUnit,
    # MultUnit,
    # TimeUnit,
    # VelocityUnit,
    # Value,
    # DimensionlessUnit,
)

U = TypeVar("U", bound=Unit)  # this is the type of the measure itself
Other = TypeVar("Other", bound="Unit")
M = TypeVar("M", bound="Measure[Other]")

@dataclass(frozen=True, slots=True)
class Measure(ABC, Generic[U]):
    _magnitude: float
    _base_unit_magnitude: float
    _unit: U
    EQUIVALENCE_THRESHOLD: float = 1e-12

    def magnitude(self) -> float:
        return self._magnitude

    def base_unit_magnitude(self) -> float:
        return self._base_unit_magnitude

    def unit(self) -> U:
        return self._unit

    def in_unit(self, unit: U) -> float:
        if self._unit == unit:
            return self._magnitude
        return unit.from_base_units(self._base_unit_magnitude)

    def base_unit(self) -> U:
        return self._unit._base_unit

    # def abs(self, u: U) -> float:
    #     return abs(self.in_unit(u))

    # def copy_sign(self, other: "Measure[U]", u: U) -> float:
    #     return self.in_unit(u) * (1 if other.in_unit(u) >= 0 else -1)

    # def times_measure(self, multiplier: "Measure[Any]") -> "Measure[Any]":
    #     base_unit_result = self.base_unit_magnitude() * multiplier.base_unit_magnitude()

    #     # First try to eliminate any common units
    #     if (
    #         isinstance(self.unit(), Dimensionless)
    #     ):
    #         return self.times_dimensionless(multiplier)
    #     elif (
    #         isinstance(self.unit(), PerUnit)
    #         and multiplier.base_unit() == self.unit().denominator().base_unit()
    #     ):
    #         # PerUnit<N, D> * D -> yield N
    #         # Case 1: denominator of the PerUnit cancels out, return with just the units of the numerator
    #         return self.unit().numerator().from_base_units(base_unit_result)
    #     elif (
    #         isinstance(multiplier.base_unit(), PerUnit)
    #         and self.base_unit() == multiplier.unit().denominator().base_unit()
    #     ):
    #         # D * PerUnit<N, D> -> yield N
    #         # Case 2: Same as Case 1, just flipped between this and the multiplier
    #         return multiplier.unit().numerator().from_base_units(base_unit_result)
    #     elif (
    #         isinstance(self.unit(), PerUnit)
    #         and isinstance(multiplier.unit(), PerUnit)
    #         and self.unit().denominator().base_unit()
    #         == multiplier.unit().numerator().base_unit()
    #         and self.unit().numerator().base_unit()
    #         == multiplier.unit().denominator().base_unit()
    #     ):
    #         # multiplying eg meters per second * milliseconds per foot
    #         # return a scalar
    #         return Value.of(base_unit_result)

    #     # No common units to eliminate, is one of them dimensionless?
    #     # Note that this must come *after* the multiplier cases, otherwise
    #     # Per<U, Dimensionless> * Dimensionless will not return a U
    #     if isinstance(multiplier.unit(), DimensionlessUnit):
    #         # scalar multiplication of this
    #         return self.times_scalar(multiplier.base_unit_magnitude())
    #     elif isinstance(self.unit(), DimensionlessUnit):
    #         # scalar multiplication of multiplier
    #         return multiplier.times_scalar(self.base_unit_magnitude())

    #     return MultUnit.combine(self.unit(), multiplier.unit()).of_base_units(
    #         self.base_unit_magnitude() * multiplier.base_unit_magnitude()
    #     )

    # def times_conversion_factor(
    #     self, conversion_factor: "Measure[PerUnit[Other, U]]"
    # ) -> M:
    #     return (
    #         conversion_factor.unit()
    #         .get_base_unit()
    #         .numerator()
    #         .of_base_units(
    #             self.base_unit_magnitude() * conversion_factor.base_unit_magnitude()
    #         )
    #     )

    # def times_inverse(self, multiplier: "Measure") -> Dimensionless:
    #     return Value.of_base_units(
    #         self.base_unit_magnitude() / multiplier.base_unit_magnitude()
    #     )

    # def times_ratio(self, ratio: "Measure[PerUnit[Other, U]]") -> "Measure[Other]":
    #     return Measure.of_base_units(
    #         self.base_unit_magnitude() * ratio.base_unit_magnitude(),
    #         self.unit().numerator(),
    #     )

    # @abstractmethod
    # def divide_by_scalar(self, scalar: float) -> "Measure[U]":
    #     pass

    # @abstractmethod
    # def divide_by_dimensionless(self, divisor: Dimensionless) -> "Measure[U]":
    #     pass

    # def divide_by_measure(self, divisor: "Measure[Any]") -> "Measure[Any]":
    #     base_unit_result = self.base_unit_magnitude() / divisor.base_unit_magnitude()

    #     if (
    #         isinstance(self.unit(), PerUnit)
    #         and divisor.base_unit() == self.unit().denominator().base_unit()
    #     ):
    #         return Value.of_base_units(base_unit_result)

    #     if isinstance(divisor, Dimensionless):
    #         return self.unit().of_base_units(base_unit_result)

    #     if isinstance(divisor.unit(), Dimensionless) and isinstance(
    #         divisor.unit(), PerUnit
    #     ):
    #         return divisor.unit().reciprocal().of_base_units(base_unit_result)

    #     if (
    #         isinstance(divisor.unit(), PerUnit)
    #         and divisor.unit().numerator().get_base_unit() == self.base_unit()
    #     ):
    #         return divisor.unit().denominator().of_base_units(base_unit_result)

    #     if isinstance(divisor.unit(), TimeUnit):
    #         return VelocityUnit.combine(self.unit(), divisor.unit()).of_base_units(
    #             base_unit_result
    #         )

    #     return PerUnit.combine(self.unit(), divisor.unit()).of_base_units(
    #         base_unit_result
    #     )

    # def per(self, divisor_unit: Unit) -> "Measure[Any]":
    #     return self.divide_by_measure(divisor_unit.one())

    # def divide_by_ratio(
    #     self, divisor: "Measure[PerUnit[U, Other]]"
    # ) -> "Measure[Other]":
    #     return Measure.of_base_units(
    #         self.base_unit_magnitude() / divisor.base_unit_magnitude(),
    #         divisor.unit().denominator(),
    #     )

    def is_near_other_measure(
        self, other: "Measure[Other]", variance_threshold: float
    ) -> bool:
        if not self.unit().get_base_unit().equivalent(other.unit().get_base_unit()):
            return False

        tolerance = abs(other.base_unit_magnitude() * variance_threshold)

        return abs(self.base_unit_magnitude() - other.base_unit_magnitude()) <= tolerance

    def is_near_same_measure(
        self, other: "Measure[U]", tolerance: "Measure[U]"
    ) -> bool:
        return abs(self.base_unit_magnitude() - other.base_unit_magnitude()) <= abs(
            tolerance.base_unit_magnitude()
        )

    def is_equivalent(self, other: "Measure[Any]") -> bool:
        return (
            self.unit().get_base_unit() == other.unit().get_base_unit()
            and abs(self.base_unit_magnitude() - other.base_unit_magnitude())
            <= self.EQUIVALENCE_THRESHOLD
        )

    def compare_to(self, other: "Measure[U]") -> int:
        if not self.unit().get_base_unit().equivalent(other.unit().get_base_unit()):
            raise ValueError("Cannot compare measures with different base units")

        x = self.base_unit_magnitude() - other.base_unit_magnitude()
        if x == 0:
            return 0
        elif x < 0:
            return -1
        else:
            return 1

    def __gt__(self, other: "Measure[U]") -> bool:
        return self.compare_to(other) > 0

    def __gte__(self, other: "Measure[U]") -> bool:
        return self.compare_to(other) >= 0

    def __lt__(self, other: "Measure[U]") -> bool:
        return self.compare_to(other) < 0

    def __lte__(self, other: "Measure[U]") -> bool:
        return self.compare_to(other) <= 0

    @staticmethod
    def max(*measures: "Measure[U]") -> "Measure[U]":
        if len(measures) == 0:
            return None

        max_measure = measures[0]
        for measure in measures[1:]:
            if measure > max_measure:
                max_measure = measure

        return max_measure

    @staticmethod
    def min(*measures: "Measure[U]") -> "Measure[U]":
        if len(measures) == 0:
            return None

        min_measure = measures[0]
        for measure in measures[1:]:
            if measure < min_measure:
                min_measure = measure

        return min_measure

    def to_short_string(self) -> str:
        return f"{self.magnitude():.3e} {self.unit().symbol()}"

    def to_long_string(self) -> str:
        return f"{self.magnitude()} {self.unit().name()}"

    # def __abs__(self) -> float:
    #     return self.abs(self.unit())

    @abstractmethod
    def __neg__(self) -> "Measure[U]":
        pass

    @abstractmethod
    def __add__(self, other: "Measure[U]") -> "Measure[U]":
        pass

    @abstractmethod
    def __sub__(self, other: "Measure[U]") -> "Measure[U]":
        pass
    
    @abstractmethod
    def __mul__(self, other: float) -> "Measure[Any]":
        pass

    def __eq__(self, other: "Measure[U]") -> bool:
        return self.is_equivalent(other)

    def __str__(self) -> str:
        return self.to_long_string()
