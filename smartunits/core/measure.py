from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar
from .unit import EQUIVALENCE_THRESHOLD, Unit, is_close


@dataclass(frozen=True, slots=True)
class Measure(ABC):
    _magnitude: float
    _base_unit_magnitude: float
    _unit: Unit
    EQUIVALENCE_THRESHOLD: ClassVar[float] = EQUIVALENCE_THRESHOLD

    def magnitude(self) -> float:
        return self._magnitude

    def base_unit_magnitude(self) -> float:
        return self._base_unit_magnitude

    def unit(self) -> Unit:
        return self._unit

    def into(self, unit: Unit) -> Unit:
        if unit is self._unit:
            return self._magnitude
        return unit.from_base_units(self._base_unit_magnitude)

    def in_unit(self, unit: Unit) -> float:
        if self._unit == unit:
            return self._magnitude
        return unit.from_base_units(self._base_unit_magnitude)

    def in_units(self, unit: Unit) -> float:
        if unit is self._unit:
            return self._magnitude
        return unit.from_base_units(self._base_unit_magnitude)

    def base_unit(self) -> Unit:
        return self._unit._base_unit

    def is_near_other_measure(
        self, other: "Measure", variance_threshold: float
    ) -> bool:
        if not self.unit().get_base_unit().equivalent(other.unit().get_base_unit()):
            return False

        tolerance = abs(other.base_unit_magnitude() * variance_threshold)

        return abs(self.base_unit_magnitude() - other.base_unit_magnitude()) <= tolerance

    def is_near_same_measure(
        self, other: "Measure", tolerance: "Measure"
    ) -> bool:
        return abs(self.base_unit_magnitude() - other.base_unit_magnitude()) <= abs(
            tolerance.base_unit_magnitude()
        )

    def is_equivalent(self, other: "Measure") -> bool:
        return (
            self.unit().get_base_unit() == other.unit().get_base_unit()
            and is_close(self.base_unit_magnitude(), other.base_unit_magnitude())
        )

    def compare_to(self, other: "Measure") -> int:
        if not self.unit().get_base_unit().equivalent(other.unit().get_base_unit()):
            raise ValueError("Cannot compare measures with different base units")

        if is_close(self.base_unit_magnitude(), other.base_unit_magnitude()):
            return 0

        x = self.base_unit_magnitude() - other.base_unit_magnitude()
        if x == 0:
            return 0
        elif x < 0:
            return -1
        else:
            return 1

    def __gt__(self, other: "Measure") -> bool:
        return self.compare_to(other) > 0

    def __gte__(self, other: "Measure") -> bool:
        return self.compare_to(other) >= 0

    def __lt__(self, other: "Measure") -> bool:
        return self.compare_to(other) < 0

    def __lte__(self, other: "Measure") -> bool:
        return self.compare_to(other) <= 0

    @staticmethod
    def max(*measures: "Measure") -> "Measure":
        if len(measures) == 0:
            return None

        max_measure = measures[0]
        for measure in measures[1:]:
            if measure > max_measure:
                max_measure = measure

        return max_measure

    @staticmethod
    def min(*measures: "Measure") -> "Measure":
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
    def __neg__(self) -> "Measure":
        pass

    @abstractmethod
    def __add__(self, other: "Measure") -> "Measure":
        pass

    @abstractmethod
    def __sub__(self, other: "Measure") -> "Measure":
        pass
    
    @abstractmethod
    def __mul__(self, other: float) -> "Measure":
        pass

    def __eq__(self, other: "Measure") -> bool:
        return self.is_equivalent(other)

    def __int__(self) -> int:
        return int(self.magnitude())

    def __float__(self) -> float:
        return self.magnitude()

    def __str__(self) -> str:
        return self.to_long_string()
