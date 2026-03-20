from smartunits import DistanceUnit

m = DistanceUnit(None, 1, "meter", "m")
f = DistanceUnit(m, 0.3048, "foot", "ft")
inch = DistanceUnit(m, 0.0254, "inch", "in")
cm = DistanceUnit(m, 0.01, "centimeter", "cm")

assert m.of(1) == f.of_base_units(1)

print(inch.conversion_to(f)(1))
print(cm.of(5).base_unit_magnitude() / m.of(5).base_unit_magnitude())