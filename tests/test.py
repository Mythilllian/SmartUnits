from smartunits import DistanceUnit, Measure, Distance
EQUIVALENCE_THRESHOLD = Measure.EQUIVALENCE_THRESHOLD

m = DistanceUnit(None, 1, "meter", "m")
f = DistanceUnit(m, 0.3048, "foot", "ft")
inch = DistanceUnit(m, 0.0254, "inch", "in")
cm = DistanceUnit(m, 0.01, "centimeter", "cm")

EQUIVALENCE_THRESHOLD = 1e-12

x = inch.of(12)
y = f.of(1)
print(abs(inch.of(12) / f.of(1) - 1) < EQUIVALENCE_THRESHOLD)
print(abs((cm.of(500).base_unit_magnitude() / m.of(5).base_unit_magnitude()) - 1) < EQUIVALENCE_THRESHOLD)