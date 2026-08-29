import unittest

import smartunits
from smartunits import DistanceUnit, Measure, TemperatureUnit, UnaryFunction, Unit, radians, degrees
from smartunits.current import amps, milliamps
from smartunits.distance import feet, inches, meters, miles
from smartunits.temperature import celsius, fahrenheit, kelvin
from smartunits.voltage import millivolts, volts


class DistanceTests(unittest.TestCase):
	def test_linear_distance_conversions(self) -> None:
		self.assertAlmostEqual(feet.of(1).in_unit(meters), 0.3048)
		self.assertAlmostEqual(inches.of(12).in_unit(feet), 1.0)
		self.assertAlmostEqual(miles.of(1).in_unit(feet), 5280.0)

	def test_distance_measure_arithmetic(self) -> None:
		total = feet.of(1) + inches.of(12)
		self.assertAlmostEqual(total.in_unit(feet), 2.0)


class TemperatureTests(unittest.TestCase):
	def test_temperature_offset_conversions(self) -> None:
		self.assertAlmostEqual(celsius.of(0).in_unit(kelvin), 273.15)
		self.assertAlmostEqual(fahrenheit.of(32).in_unit(celsius), 0.0)
		self.assertAlmostEqual(kelvin.of(300).in_unit(fahrenheit), 80.33, places=2)

	def test_temperature_measure_round_trip(self) -> None:
		boiling_point = celsius.of(100)
		self.assertAlmostEqual(boiling_point.in_unit(fahrenheit), 212.0)
		self.assertAlmostEqual(fahrenheit.of(212).in_unit(kelvin), 373.15)


class ElectricalUnitTests(unittest.TestCase):
	def test_current_and_voltage_conversions(self) -> None:
		self.assertAlmostEqual(milliamps.of(1500).in_unit(amps), 1.5)
		self.assertAlmostEqual(millivolts.of(1000).in_unit(volts), 1.0)


class PackageSurfaceTests(unittest.TestCase):
	def test_public_exports_are_lazy(self) -> None:
		self.assertIs(smartunits.DistanceUnit, DistanceUnit)
		self.assertIs(smartunits.TemperatureUnit, TemperatureUnit)
		self.assertIs(smartunits.Unit, Unit)
		self.assertIs(smartunits.UnaryFunction, UnaryFunction)
		self.assertAlmostEqual(Measure.EQUIVALENCE_THRESHOLD, 1e-12)
		self.assertTrue(hasattr(smartunits, "Distance"))
		self.assertTrue(hasattr(smartunits, "Temperature"))

class AngleTests(unittest.TestCase):
	def test_angle_conversions(self) -> None:
		self.assertAlmostEqual(radians.of(3.14159).in_unit(degrees), 180.0, places=2)
		self.assertAlmostEqual(degrees.of(180).in_unit(radians), 3.14159, places=2)

if __name__ == "__main__":
	unittest.main()