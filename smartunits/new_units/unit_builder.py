from typing import Callable, Generic, Type, TypeVar
from abc import ABC, abstractmethod
from . import Unit

U = TypeVar("U", bound=Unit)  # this is the type of the measure itself


class UnitBuilder(Generic[U]):
    _base: U
    _from_base: Callable[[float], float] = lambda x: x
    _to_base: Callable[[float], float] = lambda x: x
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

    def map_value(
        value: float, in_min: float, in_max: float, out_min: float, out_max: float
    ) -> float:
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    class MappingBuilder:
        _min_input: float
        _max_input: float
        _unit_builder: "UnitBuilder[U]"

        def __init__(
            self, unit_builder: "UnitBuilder[U]", min_input: float, max_input: float
        ):
            self._min_input = min_input
            self._max_input = max_input
            self._unit_builder = unit_builder

        def to_output_range(
            self, min_output: float, max_output: float
        ) -> "UnitBuilder.MappingBuilder":
            self._unit_builder._from_base = lambda x: self._unit_builder.map_value(
                x, self._min_input, self._max_input, min_output, max_output
            )
            self._unit_builder._to_base = lambda x: self._unit_builder.map_value(
                x, min_output, max_output, self._min_input, self._max_input
            )
            self._unit_builder._offset = 0
            return self

    def mapping_input_range(
        self, min_base: float, max_base: float
    ) -> "UnitBuilder.MappingBuilder":
        return self.MappingBuilder(self, min_base, max_base)

    def set_conversion_functions(
        self, from_base: Callable[[float], float], to_base: Callable[[float], float]
    ) -> "UnitBuilder[U]":
        if not callable(from_base) or not callable(to_base):
            raise ValueError("Conversion functions must be callable")
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
            lambda b: b * fraction, lambda x: x / fraction
        )

    def aggregate(self, aggregation: float) -> "UnitBuilder[U]":
        if aggregation == 0:
            raise ValueError("Aggregation amount must be nonzero")

        return self.set_conversion_functions(
            lambda b: b / aggregation, lambda x: x * aggregation
        )

    class UnitConstructorFunction(ABC, Generic[U]):
        @abstractmethod
        def create(
            base_unit: U,
            to_base_units: Callable[[float], float],
            from_base_units: Callable[[float], float],
            name: str,
            symbol: str,
        ):
            pass

    def make(self, constructor: UnitConstructorFunction[U] = None) -> Type[U]:
        if constructor is None:
            unit: Type[U] = self.get_unit_type(self.get_base_unit())
            constructor = unit(
                self._base, self._to_base, self._from_base, self._name, self._symbol
            )

        if not callable(self._from_base):
            raise ValueError("from_base function was not to a function")
        if not callable(self._to_base):
            raise ValueError("to_base function was not to a function")
        if not self._name:
            raise ValueError("New unit name was not set")
        if not self._symbol:
            raise ValueError("New unit symbol was not set")

        return constructor.create(
            self._base.get_base_unit(),
            lambda x: self._base.get_converter_to_base(self._to_base(x)),
            lambda y: self._from_base(self._base.get_converter_from_base(y)),
            self._name,
            self._symbol,
        )

    @staticmethod
    def get_unit_type(base_unit: U) -> Type[U]:
        return type(base_unit)
