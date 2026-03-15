import stat
from typing import Generic, Type, TypeVar
from abc import ABC, abstractmethod
from . import Unit, UnaryFunction

U = TypeVar("U", bound=Unit)  # this is the type of the measure itself
UC = TypeVar("UC", bound=Unit) # this is the type of the unit constructor 

class UnitBuilder(Generic[U]):
    _base: U
    _from_base: UnaryFunction = UnaryFunction(lambda x: x)
    _to_base: UnaryFunction = UnaryFunction(lambda x: x)
    _offset: float = 0
    _name: str
    _symbol: str

    def __init__(self, base: U):
        if base is None:
            raise ValueError("Base unit cannot be None")
        self._base = base

    def offset(self, offset: float) -> "UnitBuilder[U]":
        self._offset += offset
        return self

    @staticmethod
    def map_value(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    class MappingBuilder:
        _min_input: float
        _max_input: float

        def __init__(
            self, min_input: float, max_input: float
        ):
            self._min_input = min_input
            self._max_input = max_input

        def to_output_range(self, min_output: float, max_output: float) -> "UnitBuilder[U]":
            unit_builder = getattr(self, '_unit_builder', None)
            if unit_builder is None:
                raise RuntimeError("MappingBuilder must be initialized with a reference to the parent UnitBuilder.")

            unit_builder._from_base = UnaryFunction(
                lambda x: UnitBuilder.map_value(x, self._min_input, self._max_input, min_output, max_output)
            )
            unit_builder._to_base = UnaryFunction(
                lambda y: UnitBuilder.map_value(y, min_output, max_output, self._min_input, self._max_input)
            )
            return unit_builder

    def mapping_input_range(
        self, min_base: float, max_base: float
    ) -> "UnitBuilder.MappingBuilder":
        return self.MappingBuilder(min_base, max_base)

    def set_conversion_functions(
        self, from_base: UnaryFunction, to_base: UnaryFunction
    ) -> "UnitBuilder[U]":
        self._from_base = from_base
        self._to_base = to_base
        self._offset = 0
        return self

    def set_name(self, name: str) -> "UnitBuilder[U]":
        self._name = name
        return self

    def set_symbol(self, symbol: str) -> "UnitBuilder[U]":
        self._symbol = symbol
        return self

    def split_into(self, fraction: float):
        if fraction == 0:
            return ValueError("Fraction must be nonzero")

        return self.set_conversion_functions(
            UnaryFunction(lambda b: b * fraction), UnaryFunction(lambda x: x / fraction)
        )

    def aggregate(self, aggregation: float) -> "UnitBuilder[U]":
        if aggregation == 0:
            raise ValueError("Aggregation amount must be nonzero")

        return self.set_conversion_functions(
            UnaryFunction(lambda b: b / aggregation), UnaryFunction(lambda x: x * aggregation)
        )

    class UnitConstructorFunction(ABC, Generic[UC]):
        @staticmethod
        @abstractmethod
        def create(
            base_unit: UC,
            to_base_units: UnaryFunction,
            from_base_units: UnaryFunction,
            name: str,
            symbol: str,
        ) -> UC:
            pass

    def make(self) -> U:
        if self._base is None:
            raise ValueError("Base unit must be set to create a new unit")
        if self._to_base is None or self._from_base is None:
            raise ValueError("Conversion functions must be set to create a new unit")
        if self._name is None:
            raise ValueError("New unit name must be set to create a new unit")
        if self._symbol is None:
            raise ValueError("New unit symbol must be set to create a new unit")
        return self.UnitConstructorFunction[U].create(self._base, self._to_base, self._from_base, self._name, self._symbol)