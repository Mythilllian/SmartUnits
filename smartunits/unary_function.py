from operator import add
from typing import Callable


class UnaryFunction:
    def __init__(self, func: Callable[[float], float]) -> None:
        self.identity: Callable[[float], float] = func

    @staticmethod
    def from_multiplier(value: float) -> tuple["UnaryFunction", "UnaryFunction"]:
        return UnaryFunction(lambda x: x * value), UnaryFunction(lambda x: x / value)

    @staticmethod
    def from_divisor(value: float) -> tuple["UnaryFunction", "UnaryFunction"]:
        return UnaryFunction(lambda x: x / value), UnaryFunction(lambda x: x * value)

    @staticmethod
    def from_offset(value: float) -> tuple["UnaryFunction", "UnaryFunction"]:
        return UnaryFunction(lambda x: x + value), UnaryFunction(lambda x: x - value)

    @staticmethod
    def from_exponent(value: float) -> tuple["UnaryFunction", "UnaryFunction"]:
        return UnaryFunction(lambda x: x**value), UnaryFunction(lambda x: x ** (1 / value))

    # @staticmethod
    # def multiply_pair(func, inverse_func, multiplier: float) -> tuple["UnaryFunction", "UnaryFunction"]:
    #     return UnaryFunction(lambda x: func(x) * multiplier), UnaryFunction(lambda x: inverse_func(x) / multiplier)
    
    # @staticmethod
    # def divide_pair(func, inverse_func, divisor: float) -> tuple["UnaryFunction", "UnaryFunction"]:
    #     return UnaryFunction(lambda x: func(x) / divisor), UnaryFunction(lambda x: inverse_func(x) * divisor)
    
    # @staticmethod
    # def offset_pair(func, inverse_func, offset: float) -> tuple["UnaryFunction", "UnaryFunction"]:
    #     return UnaryFunction(lambda x: func(x) + offset), UnaryFunction(lambda x: inverse_func(x) - offset)
    
    # @staticmethod
    # def exponentiate_pair(func, inverse_func, exponent: float) -> tuple["UnaryFunction", "UnaryFunction"]:
    #     return UnaryFunction(lambda x: func(x) ** exponent), UnaryFunction(lambda x: inverse_func(x) ** (1 / exponent))

    def add_function(self, other: "UnaryFunction") -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) + other.apply(x))
    
    def subtract_function(self, other: "UnaryFunction") -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) - other.apply(x))

    def multiply_by_scalar(self, multiplier: float) -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) * multiplier)

    def divide_by_scalar(self, divisor: float) -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) / divisor)

    def multiply_by_function(self, other: "UnaryFunction") -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) * other.apply(x))
    
    def divide_by_function(self, other: "UnaryFunction") -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) / other.apply(x))

    def offset(self, offset: float) -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) + offset)

    def exponentiate(self, exponent: float) -> "UnaryFunction":
        return UnaryFunction(lambda x: self.apply(x) ** exponent)

    def from_offset_and_multiplier(
        self, offset: float, multiplier: float
    ) -> tuple["UnaryFunction", "UnaryFunction"]:

        return UnaryFunction(lambda x: (x + offset) * multiplier), UnaryFunction(lambda x: (x / multiplier) - offset)

    def apply(self, value: float) -> float:
        return self.identity(value)

    def pipe_to(self, next_func: "UnaryFunction") -> "UnaryFunction":
        if not next_func:
            raise ValueError("Next function must be provided")

        return UnaryFunction(lambda x: next_func.apply(self.apply(x)))

    def __add__(self, other) -> "UnaryFunction":
        if isinstance(other, (int, float)):
            return self.multiply_by_scalar(other)
        elif isinstance(other, UnaryFunction):
            return self.add_function(other)
        else:
            raise TypeError("Unsupported type for addition with UnaryFunction")

    def __sub__(self, other) -> "UnaryFunction":
        if isinstance(other, (int, float)):
            return self.multiply_by_scalar(-other)
        elif isinstance(other, UnaryFunction):
            return self.subtract_function(other)
        else:
            raise TypeError("Unsupported type for subtraction with UnaryFunction")

    def __mul__(self, other) -> "UnaryFunction":
        if isinstance(other, (int, float)):
            return self.multiply_by_scalar(other)
        elif isinstance(other, UnaryFunction):
            return self.multiply_by_function(other)
        else:
            raise TypeError("Unsupported type for multiplication with UnaryFunction")

    def __truediv__(self, other) -> "UnaryFunction":
        if isinstance(other, (int, float)):
            return self.divide_by_scalar(other)
        elif isinstance(other, UnaryFunction):
            return self.divide_by_function(other)
        else:
            raise TypeError("Unsupported type for division with UnaryFunction")

    def __abs__(self) -> "UnaryFunction":
        return UnaryFunction(lambda x: abs(self.apply(x)))
    
    def __call__(self, value: float) -> float:
        return self.apply(value)
