from .unit import Unit, UnitValue

__all__ = ["Unit", "UnitValue"]

class Unit():
    """
    Base class for units of measurement.

    Used for the unit itself, not the value of a unit.
    """
    TYPE = "unit"

    base_value: float # how many of a base unit this unit is worth

    name: str # the name of the unit, i.e. "meters", "seconds", "kilograms"
    abbreviation: str # the abbreviation of the unit, i.e. "m", "s", "kg"

    def __init__(self, base_value: float = 1.0, name: str = "unit", abbreviation: str = "u") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

    def conversion_factor_to(self, other: "Unit") -> float:
        """
        Factor needed to convert from this unit to the other unit. 
        Multiply this unit by the conversion factor to get the other unit.

        :param other: The unit to convert to
        :return: The conversion factor from this unit to the other unit
        """
        if(self.TYPE != other.TYPE):
            raise RuntimeError("Cannot convert between different types of units.", "Cannot convert from " + str(type(self)) + " (" + self.name + ") to " + str(type(other)) + " (" + other.name + ").", "conversion_factor_to")

        return self.base_value / other.base_value
    
    def conversion_factor_from(self, other: "Unit") -> float:
        """
        Factor needed to convert from the other unit to this unit. 
        Multiply the other unit by the conversion factor to get this unit.

        :param other: The unit to convert from
        :return: The conversion factor from the other unit to this unit
        """
        if(self.TYPE != other.TYPE):
            raise RuntimeError("Cannot convert between different types of units.", "Cannot convert from " + str(type(self)) + " (" + self.name + ") to " + str(type(other)) + " (" + other.name + ").", "conversion_factor_from")

        return other.base_value / self.base_value
    
    def __str__(self) -> str:
        return self.name + " (" + self.abbreviation + ")"

class UnitValue():
    """
    Base class for a value of a unit of measurement.

    Used for the value of a unit, not the unit itself.
    """
    unit: Unit
    magnitude: float

    def __init__(self, magnitude: float, unit: Unit = Unit()) -> None:
        self.magnitude = magnitude
        self.unit = unit

    def convert(self, other_unit: Unit) -> "UnitValue":
        """
        Convert this UnitValue to another Unit of the same unit type.

        :param other_unit: The unit to convert to
        :return: A new UnitValue with the converted magnitude and the other unit
        """

        if self.unit.TYPE != other_unit.TYPE:
            raise UnitException("Cannot convert between different types of units.", "Cannot convert from " + str(type(self.unit)) + " (" + self.unit.name + ") to " + str(type(other_unit)) + " (" + other_unit.name + ").", "convert")

        conversion_factor = self.unit.conversion_factor_to(other_unit)
        return UnitValue(self.magnitude * conversion_factor, other_unit)
    
    def add(self, other: "UnitValue") -> "UnitValue":
        """
        Add this UnitValue to another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to add
        :return: A new UnitValue with the sum of the UnitValues in the unit as this UnitValue
        """
        if other.unit.TYPE != self.unit.TYPE:
            raise UnitException("Cannot add UnitValues of different unit types.", "Cannot add " + str(type(self.unit)) + " (" + self.unit.name + ") to " + str(type(other.unit)) + " (" + other.unit.name + ").", "add")
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude + converted_other.magnitude, self.unit)
    
    def subtract(self, other: "UnitValue") -> "UnitValue":
        """
        Subtract another UnitValue from this UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to subtract
        :return: A new UnitValue with the difference of the UnitValues in the unit as this UnitValue
        """
        if other.unit.TYPE != self.unit.TYPE:
            raise UnitException("Cannot subtract UnitValues of different unit types.", "Cannot subtract " + str(type(self.unit)) + " (" + self.unit.name + ") from " + str(type(other.unit)) + " (" + other.unit.name + ").", "subtract")
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude - converted_other.magnitude, self.unit)
    
    def multiply(self, other: "UnitValue") -> "UnitValue":
        """
        Multiply this UnitValue by another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to multiply by
        :return: A new UnitValue with the product of the UnitValues and a compound unit
        """
        if other.unit.TYPE != self.unit.TYPE:
            raise UnitException("Cannot multiply UnitValues of different unit types.", "Cannot multiply " + str(type(self.unit)) + " (" + self.unit.name + ") by " + str(type(other.unit)) + " (" + other.unit.name + ").", "multiply")
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude * converted_other.magnitude, self.unit)
    
    def divide(self, other: "UnitValue") -> "UnitValue":
        """
        Divide this UnitValue by another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to divide by
        :return: A new UnitValue with the quotient of the UnitValues and a compound unit
        """
        if other.unit.TYPE != self.unit.TYPE:
            raise UnitException("Cannot divide UnitValues of different unit types.", "Cannot divide " + str(type(self.unit)) + " (" + self.unit.name + ") by " + str(type(other.unit)) + " (" + other.unit.name + ").", "divide")
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude / converted_other.magnitude, self.unit)

    def get_magnitude_in_base_unit(self) -> float:
        """
        Get the magnitude of this UnitValue in the base unit.

        :return: The magnitude of this UnitValue in the base unit
        """
        return self.magnitude * self.unit.base_value
    
    def get_magnitude(self) -> float:
        """
        Get the magnitude of this UnitValue in its current unit.

        :return: The magnitude of this UnitValue in its current unit
        """
        return self.magnitude
    
    def set_magnitude_in_base_unit(self, magnitude_in_base_unit: float) -> None:
        """
        Set the magnitude of this UnitValue in the base unit.

        :param magnitude_in_base_unit: The magnitude of this UnitValue in the base unit
        """
        self.magnitude = magnitude_in_base_unit / self.unit.base_value

    def set_magnitude(self, magnitude: float) -> None:
        """
        Set the magnitude of this UnitValue in its current unit.

        :param magnitude: The magnitude of this UnitValue in its current unit
        """
        self.magnitude = magnitude

    def __str__(self) -> str:
        return str(self.magnitude) + " " + self.unit.abbreviation

units = Unit(1, "units", "u")