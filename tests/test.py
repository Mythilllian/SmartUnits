import unittest

import math

import smartunits
from smartunits import *

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
		self.assertAlmostEqual(radians.conversion_to(degrees).apply(3.14159), 180.0, places=2)
		self.assertAlmostEqual(radians.conversion_from(degrees).apply(180), 3.14159, places=2)

class UnaryFunctionTests(unittest.TestCase):
	def test_constructors(self) -> None:
		self.assertEqual(UnaryFunction.from_multiplier(3).apply(2), 6)
		self.assertEqual(UnaryFunction.from_divisor(4).apply(2), 0.5)
		self.assertEqual(UnaryFunction.from_offset(5).apply(2), 7)
		self.assertEqual(UnaryFunction.from_exponent(3).apply(2), 8)

	def test_pairs_are_inverses(self) -> None:
		for pair in (
			UnaryFunction.pair_from_multiplier(3),
			UnaryFunction.pair_from_divisor(4),
			UnaryFunction.pair_from_offset(5),
			UnaryFunction.pair_from_exponent(3),
		):
			forward, inverse = pair
			self.assertAlmostEqual(inverse.apply(forward.apply(2)), 2)

	def test_combinators(self) -> None:
		double = UnaryFunction.from_multiplier(2)
		plus_one = UnaryFunction.from_offset(1)
		self.assertEqual(double.add_function(plus_one).apply(3), 10)
		self.assertEqual(double.subtract_function(plus_one).apply(3), 2)
		self.assertEqual(double.multiply_by_scalar(5).apply(3), 30)
		self.assertEqual(double.divide_by_scalar(4).apply(3), 1.5)
		self.assertEqual(double.multiply_by_function(plus_one).apply(3), 24)
		self.assertEqual(double.divide_by_function(plus_one).apply(3), 1.5)
		self.assertEqual(double.offset(1).apply(3), 7)
		self.assertEqual(double.exponentiate(2).apply(3), 36)
		self.assertEqual(double.pipe_to(plus_one).apply(3), 7)
		self.assertEqual(plus_one.pipe_to(double).apply(3), 8)

	def test_operators(self) -> None:
		double = UnaryFunction.from_multiplier(2)
		plus_one = UnaryFunction.from_offset(1)
		self.assertEqual((double + plus_one)(3), 10)
		self.assertEqual((double - plus_one)(3), 2)
		self.assertEqual((double * plus_one)(3), 24)
		self.assertEqual((double / plus_one)(3), 1.5)
		self.assertEqual((double * 5)(3), 30)
		self.assertEqual((double / 4)(3), 1.5)
		self.assertEqual(abs(UnaryFunction.from_multiplier(-2))(3), 6)
		with self.assertRaises(TypeError):
			double + "a"


class UnitTests(unittest.TestCase):
	def test_name_and_symbol(self) -> None:
		self.assertEqual(meters.name(), "meter")
		self.assertEqual(meters.symbol(), "m")
		self.assertEqual(str(meters), "meter")

	def test_base_units(self) -> None:
		self.assertTrue(meters.is_base_unit())
		self.assertFalse(feet.is_base_unit())
		self.assertIs(meters.get_base_unit(), meters)
		self.assertIs(feet.get_base_unit(), meters)
		self.assertEqual(feet.base_scale(), 0.3048)

	def test_to_and_from_base_units(self) -> None:
		self.assertAlmostEqual(feet.to_base_units(1), 0.3048)
		self.assertAlmostEqual(feet.from_base_units(0.3048), 1)
		self.assertAlmostEqual(feet.conversion_to_base_units().apply(1), 0.3048)
		self.assertAlmostEqual(feet.conversion_from_base_units().apply(0.3048), 1)

	def test_convert_between_units(self) -> None:
		self.assertAlmostEqual(feet.convert_from(12, inches), 1)
		self.assertAlmostEqual(feet.convert_to(1, inches), 12)
		self.assertAlmostEqual(feet.conversion_from(inches).apply(12), 1)
		self.assertAlmostEqual(feet.conversion_to(inches).apply(1), 12)

	def test_equality_and_hash(self) -> None:
		self.assertEqual(meters, meters)
		self.assertNotEqual(meters, feet)
		self.assertTrue(meters.equivalent(meters))
		self.assertFalse(meters.equivalent(seconds))
		self.assertEqual(len({meters, meters, feet}), 2)

	def test_temperature_base_scale_ignores_offset(self) -> None:
		self.assertAlmostEqual(celsius.base_scale(), 1)
		self.assertAlmostEqual(fahrenheit.base_scale(), 5 / 9)


class MeasureTests(unittest.TestCase):
	def test_accessors(self) -> None:
		length = feet.of(2)
		self.assertEqual(length.magnitude(), 2)
		self.assertAlmostEqual(length.base_unit_magnitude(), 0.6096)
		self.assertIs(length.unit(), feet)
		self.assertIs(length.base_unit(), meters)
		self.assertIsInstance(length, Distance)
		self.assertIsInstance(length, Measure)

	def test_of_base_units(self) -> None:
		self.assertAlmostEqual(feet.of_base_units(0.3048).magnitude(), 1)
		self.assertAlmostEqual(Distance.of_base_units(0.3048, feet).magnitude(), 1)
		self.assertAlmostEqual(Distance.of(1, feet).base_unit_magnitude(), 0.3048)

	def test_in_unit(self) -> None:
		self.assertAlmostEqual(feet.of(1).in_unit(inches), 12)
		self.assertAlmostEqual(feet.of(1).in_units(inches), 12)
		self.assertEqual(feet.of(1).in_unit(feet), 1)

	def test_into(self) -> None:
		self.assertEqual(feet.of(3).into(feet), 3)

	def test_arithmetic(self) -> None:
		self.assertAlmostEqual((feet.of(1) + inches.of(12)).in_unit(feet), 2)
		self.assertAlmostEqual((feet.of(3) - inches.of(12)).in_unit(feet), 2)
		self.assertEqual((-feet.of(3)).magnitude(), -3)
		self.assertEqual((feet.of(3) * 2).magnitude(), 6)
		self.assertEqual((2 * feet.of(3)).magnitude(), 6)
		self.assertEqual((feet.of(3) / 2).magnitude(), 1.5)

	def test_same_unit_arithmetic_keeps_unit(self) -> None:
		total = feet.of(1) + feet.of(2)
		self.assertIs(total.unit(), feet)
		self.assertAlmostEqual(total.in_unit(feet), 3)
		self.assertAlmostEqual(total.base_unit_magnitude(), 0.9144)

	def test_divide_same_quantity_gives_ratio(self) -> None:
		self.assertAlmostEqual(feet.of(6) / inches.of(12), 6)

	def test_dimensionless_scaling(self) -> None:
		self.assertAlmostEqual((feet.of(4) * percent.of(50)).in_unit(feet), 2)
		self.assertAlmostEqual((feet.of(4) / value.of(2)).in_unit(feet), 2)

	def test_comparisons(self) -> None:
		self.assertTrue(feet.of(1) < meters.of(1))
		self.assertTrue(meters.of(1) > feet.of(1))
		self.assertEqual(meters.of(1).compare_to(centimeters.of(100)), 0)
		self.assertEqual(feet.of(1).compare_to(meters.of(1)), -1)
		self.assertEqual(meters.of(1).compare_to(feet.of(1)), 1)
		with self.assertRaises(ValueError):
			meters.of(1).compare_to(seconds.of(1))

	def test_equivalence(self) -> None:
		self.assertTrue(feet.of(1).is_equivalent(inches.of(12)))
		self.assertFalse(feet.of(1).is_equivalent(inches.of(11)))

	def test_shared_tolerance(self) -> None:
		self.assertEqual(feet.of(1).compare_to(inches.of(12)), 0)
		self.assertTrue(lightyears.of(1).is_equivalent(meters.of(9460730472580800.0 * (1 + 1e-15))))
		self.assertFalse(lightyears.of(1).is_equivalent(meters.of(9460730472580800.0 * (1 + 1e-9))))
		self.assertTrue(meters.of(0).is_equivalent(meters.of(1e-13)))
		self.assertIs(Measure.EQUIVALENCE_THRESHOLD, smartunits.core.unit.EQUIVALENCE_THRESHOLD)
		self.assertTrue(feet_per_second.of(1).is_equivalent(inches_per_second.of(12)))
		self.assertEqual(pound_feet.of(1).compare_to(pound_inches.of(12)), 0)

	def test_equality_operator_uses_equivalence(self) -> None:
		self.assertTrue(feet.of(1) == inches.of(12))

	def test_nearness(self) -> None:
		self.assertTrue(meters.of(1).is_near_other_measure(meters.of(1.05), 0.1))
		self.assertFalse(meters.of(1).is_near_other_measure(meters.of(1.5), 0.1))
		self.assertFalse(meters.of(1).is_near_other_measure(seconds.of(1), 0.1))
		self.assertTrue(meters.of(1).is_near_same_measure(feet.of(3), centimeters.of(10)))
		self.assertFalse(meters.of(1).is_near_same_measure(feet.of(3), centimeters.of(5)))

	def test_max_and_min(self) -> None:
		measures = (feet.of(1), meters.of(1), inches.of(1))
		self.assertIs(Measure.max(*measures), measures[1])
		self.assertIs(Measure.min(*measures), measures[2])
		self.assertIsNone(Measure.max())
		self.assertIsNone(Measure.min())

	def test_strings(self) -> None:
		self.assertEqual(str(meters.of(2)), "2.000e+00 m")
		self.assertEqual(meters.of(2).to_short_string(), "2.000e+00 m")
		self.assertEqual(meters.of(2).to_long_string(), "2 meter")

	def test_number_conversion(self) -> None:
		self.assertEqual(int(meters.of(2.7)), 2)
		self.assertEqual(float(meters.of(2.5)), 2.5)


class ConversionTests(unittest.TestCase):
	def test_time(self) -> None:
		self.assertAlmostEqual(hours.of(1).in_unit(minutes), 60)
		self.assertAlmostEqual(days.of(1).in_unit(seconds), 86400)
		self.assertAlmostEqual(milliseconds.of(1500).in_unit(seconds), 1.5)

	def test_mass(self) -> None:
		self.assertAlmostEqual(kilograms.of(1).in_unit(grams), 1000)
		self.assertAlmostEqual(Mass.of(1, smartunits.mass.pounds).in_unit(kilograms), 0.45359237)

	def test_angle(self) -> None:
		self.assertAlmostEqual(rotations.of(1).in_unit(degrees), 360)
		self.assertAlmostEqual(degrees.of(90).in_unit(radians), math.pi / 2)

	def test_area_and_volume(self) -> None:
		self.assertAlmostEqual(square_feet.of(1).in_unit(square_inches), 144)
		self.assertAlmostEqual(liters.of(1).in_unit(milliliters), 1000)
		self.assertAlmostEqual(cubic_meters.of(1).in_unit(liters), 1000)

	def test_electrical(self) -> None:
		self.assertAlmostEqual(kilovolts.of(1).in_unit(volts), 1000)
		self.assertAlmostEqual(kilo_ohms.of(1).in_unit(ohms), 1000)
		self.assertAlmostEqual(kilowatts.of(1).in_unit(watts), 1000)

	def test_energy_and_force(self) -> None:
		self.assertAlmostEqual(kilojoules.of(1).in_unit(joules), 1000)
		self.assertAlmostEqual(pounds_force.of(1).in_unit(newtons), 4.4482216152605)

	def test_temperature_offsets(self) -> None:
		self.assertAlmostEqual(celsius.of(-40).in_unit(fahrenheit), -40)
		self.assertAlmostEqual(kelvin.of(0).in_unit(celsius), -273.15)


class PerUnitTests(unittest.TestCase):
	def test_named_per_units_are_typed(self) -> None:
		self.assertIsInstance(meters_per_second, LinearVelocityUnit)
		self.assertIsInstance(meters_per_second, PerUnit)
		self.assertIsInstance(radians_per_second, AngularVelocityUnit)
		self.assertIsInstance(meters_per_second_squared, LinearAccelerationUnit)
		self.assertIsInstance(radians_per_second_squared, AngularAccelerationUnit)
		self.assertIsInstance(exabytes_per_second, DataTransferUnit)
		self.assertIsInstance(kilograms_per_cubic_meter, DensityUnit)

	def test_components(self) -> None:
		self.assertIs(meters_per_second.numerator(), meters)
		self.assertIs(meters_per_second.denominator(), seconds)
		self.assertIs(meters_per_second_squared.numerator(), meters_per_second)

	def test_per_returns_named_unit(self) -> None:
		self.assertIs(meters.per(seconds), meters_per_second)
		self.assertIs(radians.per(seconds), radians_per_second)
		self.assertIs(meters_per_second.per(seconds), meters_per_second_squared)
		self.assertIs(radians_per_second.per(seconds), radians_per_second_squared)
		self.assertIs(feet.per(seconds), feet_per_second)
		self.assertIs(meters / seconds, meters_per_second)

	def test_per_is_cached(self) -> None:
		self.assertIs(volts.per(meters), volts.per(meters))
		self.assertIs(feet.per(minutes), feet.per(minutes))

	def test_unnamed_per_unit(self) -> None:
		unit = volts.per(meters)
		self.assertIs(type(unit), PerUnit)
		self.assertEqual(unit.name(), "volt per meter")
		self.assertEqual(unit.symbol(), "V/m")

	def test_unnamed_typed_per_unit(self) -> None:
		unit = feet.per(minutes)
		self.assertIsInstance(unit, LinearVelocityUnit)
		self.assertIs(unit.get_base_unit(), meters_per_second)
		self.assertAlmostEqual(unit.of(60).in_unit(feet_per_second), 1)

	def test_base_units(self) -> None:
		self.assertTrue(meters_per_second.is_base_unit())
		self.assertIs(feet_per_second.get_base_unit(), meters_per_second)
		self.assertIs(gs.get_base_unit(), meters_per_second_squared)
		self.assertFalse(gs.is_base_unit())

	def test_conversions(self) -> None:
		self.assertAlmostEqual(feet_per_second.base_scale(), 0.3048)
		self.assertAlmostEqual(miles_per_hour.of(1).in_unit(meters_per_second), 0.44704)
		self.assertAlmostEqual(knots.of(1).in_unit(kilometers_per_hour), 1.852)
		self.assertAlmostEqual(rotations_per_minute.of(60).in_unit(rotations_per_second), 1)
		self.assertAlmostEqual(rotations_per_second.of(1).in_unit(radians_per_second), 2 * math.pi)
		self.assertAlmostEqual(gs.of(1).in_unit(meters_per_second_squared), 9.80665)
		self.assertAlmostEqual(standard_gravity.of(1).in_unit(gs), 1)
		self.assertAlmostEqual(degrees_per_second_squared.of(360).in_unit(rotations_per_second_squared), 1)
		self.assertAlmostEqual(exabits_per_second.of(8).in_unit(exabytes_per_second), 1)
		self.assertAlmostEqual(grams_per_milliliter.of(1).in_unit(kilograms_per_cubic_meter), 1000)
		self.assertAlmostEqual(feet_per_second.convert_to(1, inches_per_second), 12)
		self.assertAlmostEqual(feet_per_second.conversion_from(inches_per_second).apply(12), 1)

	def test_reciprocal(self) -> None:
		inverse = meters_per_second.reciprocal()
		self.assertIs(inverse.numerator(), seconds)
		self.assertIs(inverse.denominator(), meters)
		self.assertEqual(inverse.symbol(), "s/m")

	def test_unit_cancellation(self) -> None:
		self.assertIs(meters_per_second * seconds, meters)
		self.assertIs(meters_per_second.mult(seconds), meters)


class MultUnitTests(unittest.TestCase):
	def test_named_mult_units_are_typed(self) -> None:
		self.assertIsInstance(newton_meters, TorqueUnit)
		self.assertIsInstance(newton_meters, MultUnit)
		self.assertIsInstance(kilogram_square_meters, MomentOfInertiaUnit)
		self.assertIsInstance(kilogram_meters_per_second, LinearMomentumUnit)
		self.assertIsInstance(kilogram_meters_squared_per_second, AngularMomentumUnit)

	def test_components(self) -> None:
		self.assertIs(newton_meters.unit_a(), newtons)
		self.assertIs(newton_meters.unit_b(), meters)

	def test_mult_returns_named_unit(self) -> None:
		self.assertIs(newtons.mult(meters), newton_meters)
		self.assertIs(newtons * meters, newton_meters)
		self.assertIs(kilograms.mult(meters_per_second), kilogram_meters_per_second)

	def test_unnamed_mult_unit(self) -> None:
		unit = volts * meters
		self.assertIs(type(unit), MultUnit)
		self.assertEqual(unit.name(), "volt meter")
		self.assertEqual(unit.symbol(), "V*m")
		self.assertIs(unit, volts * meters)

	def test_conversions(self) -> None:
		self.assertAlmostEqual(pound_feet.of(1).in_unit(newton_meters), 1.3558179483314)
		self.assertAlmostEqual(pound_feet.of(1).in_unit(pound_inches), 12)
		self.assertAlmostEqual(meter_kilograms.of(1).in_unit(newton_meters), 9.80665)
		self.assertAlmostEqual(pound_square_inches.of(1).in_unit(kilogram_square_meters), 0.0002926396534292)
		self.assertAlmostEqual(pound_inches_per_second.of(1).in_unit(kilogram_meters_per_second), 0.45359237 * 0.0254)

	def test_unit_cancellation(self) -> None:
		self.assertIs(newton_meters.per(meters), newtons)
		self.assertIs(newton_meters / newtons, meters)


class ScalarUnitDerivingTests(unittest.TestCase):
	def test_per_table_finds_existing_unit(self) -> None:
		self.assertIs(watts.per(volts), amps)
		self.assertIs(watts.per(amps), volts)
		self.assertIs(volts.per(ohms), amps)
		self.assertIs(newton_meters.per(meters), newtons)

	def test_multiply_table_finds_existing_unit(self) -> None:
		self.assertIs(amps * volts, watts)
		self.assertIs(volts * amps, watts)

	def test_derive_makes_new_unit_when_missing(self) -> None:
		unit = watts.per(millivolts)
		self.assertIsInstance(unit, CurrentUnit)
		self.assertAlmostEqual(unit.to_base_units(1), 1000)
		self.assertIs(unit.get_base_unit(), amps)

	def test_derive(self) -> None:
		self.assertIs(CurrentUnit.derive(0.001, "x", "x"), milliamps)
		self.assertEqual(CurrentUnit.derive(0.5, "half amp", "hA").name(), "half amp")


class PerMeasureTests(unittest.TestCase):
	def test_divide_measures(self) -> None:
		velocity = meters.of(10) / seconds.of(2)
		self.assertIsInstance(velocity, LinearVelocity)
		self.assertIsInstance(velocity, Per)
		self.assertAlmostEqual(velocity.in_unit(meters_per_second), 5)

	def test_divide_velocity_by_time(self) -> None:
		acceleration = meters_per_second.of(10) / seconds.of(2)
		self.assertIsInstance(acceleration, LinearAcceleration)
		self.assertAlmostEqual(acceleration.in_unit(meters_per_second_squared), 5)

	def test_multiply_by_denominator(self) -> None:
		self.assertAlmostEqual((feet_per_second.of(3) * seconds.of(2)).in_unit(feet), 6)
		self.assertAlmostEqual((seconds.of(2) * feet_per_second.of(3)).in_unit(feet), 6)
		self.assertAlmostEqual((meters_per_second.of(1) * minutes.of(1)).in_unit(meters), 60)

	def test_times_divisor(self) -> None:
		self.assertAlmostEqual(meters_per_second.of(5).times_divisor(minutes.of(1)).in_unit(meters), 300)

	def test_reciprocal(self) -> None:
		self.assertAlmostEqual(meters_per_second.of(4).reciprocal().in_unit(seconds.per(meters)), 0.25)

	def test_components(self) -> None:
		velocity = Per.of(1, volts.per(meters))
		self.assertIs(velocity.numerator(), volts)
		self.assertIs(velocity.denominator(), meters)

	def test_arithmetic(self) -> None:
		self.assertAlmostEqual((meters_per_second.of(1) + feet_per_second.of(1)).in_unit(meters_per_second), 1.3048)
		self.assertAlmostEqual((meters_per_second.of(3) - meters_per_second.of(1)).in_unit(meters_per_second), 2)
		self.assertEqual((-meters_per_second.of(2)).magnitude(), -2)
		self.assertEqual((meters_per_second.of(2) * 3).magnitude(), 6)
		self.assertEqual((3 * meters_per_second.of(2)).magnitude(), 6)
		self.assertEqual((meters_per_second.of(6) / 3).magnitude(), 2)

	def test_generic_per_arithmetic(self) -> None:
		field = volts.per(meters).of(10)
		self.assertIs(type(field), Per)
		self.assertEqual((field * 2).magnitude(), 20)
		self.assertEqual((field / 2).magnitude(), 5)
		self.assertEqual((-field).magnitude(), -10)
		self.assertAlmostEqual((field + field).magnitude(), 20)
		self.assertAlmostEqual((field * meters.of(2)).in_unit(volts), 20)

	def test_angular_velocity(self) -> None:
		self.assertAlmostEqual((rotations.of(1) / seconds.of(1)).in_unit(radians_per_second), 2 * math.pi)

	def test_angular_velocity_as_frequency(self) -> None:
		self.assertAlmostEqual(rotations_per_second.of(1).as_frequency().in_unit(hertz), 1)

	def test_string(self) -> None:
		self.assertEqual(str(radians_per_second.of(3)), "3.000e+00 rad/s")


class MultMeasureTests(unittest.TestCase):
	def test_divide_by_component(self) -> None:
		self.assertAlmostEqual((pound_feet.of(10) / feet.of(2)).in_unit(pounds_force), 5)
		self.assertAlmostEqual((newton_meters.of(10) / newtons.of(2)).in_unit(meters), 5)

	def test_generic_mult_arithmetic(self) -> None:
		amount = (volts * seconds).of(4)
		self.assertIs(type(amount), Mult)
		self.assertIs(amount.unit_a(), volts)
		self.assertIs(amount.unit_b(), seconds)
		self.assertEqual((amount * 2).magnitude(), 8)
		self.assertEqual((amount / 2).magnitude(), 2)
		self.assertEqual((-amount).magnitude(), -4)
		self.assertAlmostEqual((amount + amount).magnitude(), 8)
		self.assertAlmostEqual((amount / seconds.of(2)).in_unit(volts), 2)

	def test_multiply_measures(self) -> None:
		momentum = kilograms.of(2) * meters_per_second.of(3)
		self.assertAlmostEqual(momentum.base_unit_magnitude(), 6)

	def test_string(self) -> None:
		self.assertEqual(str(newton_meters.of(3)), "3.000e+00 N m")


class QuantityTableTests(unittest.TestCase):
	def test_multiply_tables(self) -> None:
		self.assertAlmostEqual((amps.of(2) * volts.of(3)).in_unit(watts), 6)
		self.assertAlmostEqual((watts.of(2) * seconds.of(3)).in_unit(joules), 6)
		self.assertAlmostEqual((kilograms.of(2) * meters_per_second_squared.of(3)).in_unit(newtons), 6)
		self.assertAlmostEqual((hertz.of(2) * seconds.of(3)).in_unit(value), 6)

	def test_divide_tables(self) -> None:
		self.assertAlmostEqual((watts.of(6) / volts.of(3)).in_unit(amps), 2)
		self.assertAlmostEqual((joules.of(6) / seconds.of(3)).in_unit(watts), 2)
		self.assertAlmostEqual((volts.of(6) / ohms.of(3)).in_unit(amps), 2)

	def test_time_as_frequency(self) -> None:
		self.assertAlmostEqual(seconds.of(4).as_frequency().in_unit(hertz), 0.25)

	def test_frequency_as_period(self) -> None:
		self.assertAlmostEqual(hertz.of(4).as_period().in_unit(seconds), 0.25)


class CompoundTests(unittest.TestCase):
	def test_compound_units(self) -> None:
		self.assertIs(type(volt_seconds), MultUnit)
		self.assertIs(type(radians_per_meter), PerUnit)
		self.assertIs(volt_seconds.unit_a(), volts)
		self.assertIs(volt_seconds_squared.unit_a(), volt_seconds)
		self.assertAlmostEqual(volt_seconds_per_feet.of(1).in_unit(volt_seconds_per_meter), 3.280839895013123)
		self.assertAlmostEqual(units_per_second.of(1).in_unit(value.per(minutes)), 60)


class PackageTests(unittest.TestCase):
	def test_lazy_exports(self) -> None:
		self.assertIs(smartunits.Per, Per)
		self.assertIs(smartunits.PerUnit, PerUnit)
		self.assertIs(smartunits.Mult, Mult)
		self.assertIs(smartunits.MultUnit, MultUnit)
		self.assertIs(smartunits.meters_per_second, smartunits.linear_velocity.meters_per_second)
		with self.assertRaises(AttributeError):
			smartunits.not_a_unit

	def test_quantity_modules(self) -> None:
		from smartunits import area
		self.assertIn("Area", area.__all__)
		self.assertIn("AreaUnit", area.__all__)
		self.assertIn("acres", area.__all__)
		namespace: dict = {}
		exec("from smartunits.linear_velocity import *", namespace)
		self.assertIn("meters_per_second", namespace)
		self.assertIn("LinearVelocity", namespace)
		self.assertNotIn("meters", namespace)

	def test_removed_quantities(self) -> None:
		self.assertFalse(hasattr(smartunits, "Velocity"))
		self.assertFalse(hasattr(smartunits, "Acceleration"))
		self.assertFalse(hasattr(smartunits, "Compound"))

class UnitDerivationTests(unittest.TestCase):
	def test_derive_new_unit(self) -> None:
		new_unit = DistanceUnit.derive(0.5, "half meter", "hm")
		self.assertIsInstance(new_unit, DistanceUnit)
		self.assertAlmostEqual(new_unit.to_base_units(1), 0.5)
		self.assertEqual(new_unit.name(), "half meter")
		self.assertEqual(new_unit.symbol(), "hm")
		self.assertIs(new_unit.get_base_unit(), meters)

class ReverseMultiplicationTests(unittest.TestCase):
	def test_reverse_multiplication(self) -> None:
		self.assertEqual((2 * feet.of(3)).magnitude(), 6)
		self.assertEqual((3 * meters_per_second.of(2)).magnitude(), 6)
		self.assertEqual((4 * newton_meters.of(2)).magnitude(), 8)
		volts_per_meter = volts.per(meters)
		self.assertEqual((5 * volts_per_meter.of(2)).magnitude(), 10)

class TestLinearVelocity(unittest.TestCase):
    def test_linear_velocity(self) -> None:
        import smartunits.linear_velocity
        self.assertIsNotNone(smartunits.linear_velocity)
        self.assertEqual(int(smartunits.linear_velocity.meters_per_second.of(5113)), 5113)
        amount: LinearVelocity = smartunits.linear_velocity.meters_per_second.of(5113)
        self.assertEqual(int(amount), 5113)

if __name__ == "__main__":
	unittest.main()