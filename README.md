# SmartUnits

A flexible Python unit system inspired by the WPILibJ units system that includes every unit used within that as well as the (rudimentary) Python WPILib unit libary.

SmartUnits provides strongly structured units and measurements with support for conversions, arithmetic, temperature offsets, compound units, and a large collection of physical measurement types.

The library is designed to make unit-aware calculations readable:

```
from smartunits.distance import feet, inches, meters  
  
distance = feet.of(1) + inches.of(12)  
  
print(distance.in\_unit(feet))  
\# 2.0  
  
print(distance.in\_unit(meters))  
\# 0.6096
```


## Features

- Large collection of physical measurement types

- Simple unit conversion

- Unit-aware measurement arithmetic

- Temperature units with offset conversions

- Linear and angular measurements

- Electrical units

- SI and imperial units

- Compound and derived units

- Python-friendly API

- Inspired by the Java WPILib units system

- Designed for robotics, science, engineering, and general-purpose calculations


# Installation

## Clone the repository

Clone the repository using Git:

```
git clone https://github.com/Mythilllian/SmartUnits.git
```

Move into the project directory:

```
cd SmartUnits
```

## Install SmartUnits

Install the package locally:

```
pip install .
```

Alternatively, install it in editable mode while developing:

```
pip install -e .
```


# Using SmartUnits

SmartUnits separates units into modules based on their measurement type.

For example:

```
from smartunits.distance import meters, feet, inches
```

Each unit provides an `.of()` method for creating a measurement.

```
distance = meters.of(10)
```

This creates a measurement representing:

```
10 meters
```

You can convert the measurement into another compatible unit with `.in\_unit()`.

```
from smartunits.distance import meters, feet  
  
distance = meters.of(10)  
  
print(distance.in\_unit(feet))
```


# Basic Examples

## Creating Measurements

Create a measurement using a unit's `.of()` method:

```
from smartunits.distance import meters  
  
distance = meters.of(5)
```

This creates a measurement representing 5 meters.

Another example:

```
from smartunits.temperature import celsius  
  
temperature = celsius.of(25)
```


## Converting Units

Measurements can be converted between compatible units.

```
from smartunits.distance import meters, feet  
  
distance = meters.of(1)  
  
print(distance.in\_unit(feet))  
\# 3.28084...
```

Another example:

```
from smartunits.distance import inches, feet  
  
distance = inches.of(12)  
  
print(distance.in\_unit(feet))  
\# 1.0
```


## Measurement Arithmetic

Measurements of compatible units can be used in arithmetic operations.

```
from smartunits.distance import feet, inches  
  
distance = feet.of(1) + inches.of(12)  
  
print(distance.in\_unit(feet))  
\# 2.0
```

The measurements are automatically converted as necessary.

You can also perform calculations and then convert the result:

```
from smartunits.distance import meters, feet  
  
distance = meters.of(10)  
  
result = distance.in\_unit(feet)  
  
print(result)
```


# Measurement Types

SmartUnits currently includes the following measurement categories.

## Motion and Mechanics

### Acceleration

- meters per second squared

- feet per second squared

- inches per second squared

- G

- standard gravity

### Linear Acceleration

- meters per second squared

- feet per second squared

- inches per second squared

- G

### Velocity

- meters per second

- feet per second

- inches per second

- miles per hour

- kilometers per hour

- knots

### Linear Velocity

- meters per second

- feet per second

- inches per second

### Angular Velocity

- radians per second

- revolutions per second

- rotations per second

- rotations per minute

- degrees per second

- turns per second

- revolutions per minute

- milliarcseconds per year

### Angular Acceleration

- radians per second squared

- rotations per second squared

- degrees per second squared

- turns per second squared

### Force

- newtons

- pound-force

- ounce-force

- nanonewtons

- micronewtons

- millinewtons

- kilonewtons

- pounds

- dynes

- kiloponds

- poundals

### Torque

- newton meters

- pound-feet

- pound-inches

- ounce-inches

- foot-poundals

- inch-pounds

- meter-kilograms

### Linear Momentum

- kilogram meters per second

- pound inches per second

### Angular Momentum

- kilogram meter squared per second

- pound inch squared per second

### Moment of Inertia

- kilogram square meters

- pound square inches


# Distance

- meters

- millimeters

- centimeters

- kilometers

- inches

- feet

- yards

- miles

- nautical miles

- astronomical units

- lightyears

- parsecs

- nanometers

- micrometers

- angstroms

- mils

- cubits

- fathoms

- chains

- furlongs

- hands

- leagues

- nautical leagues


# Angle

- radians

- degrees

- revolutions

- rotations

- turns

- gradians

- nanoradians

- microradians

- milliradians

- kiloradians

- arcminutes

- arcseconds

- milliarcseconds


# Area

- square meters

- square feet

- square inches

- square miles

- square kilometers

- hectares

- acres


# Volume

- cubic meters

- cubic millimeters

- cubic kilometers

- liters

- nanoliters

- microliters

- milliliters

- kiloliters

- cubic inches

- cubic feet

- cubic yards

- cubic miles

- gallons

- quarts

- pints

- cups

- fluid ounces

- barrels

- bushels

- tablespoons

- teaspoons

- pinches

- dashes

- drops

- fifths

- drams

- gills

- pecks

- sacks

- shots

- strikes


# Time

- seconds

- milliseconds

- microseconds

- nanoseconds

- minutes

- hours

- kiloseconds

- days

- weeks

- years

- Julian years

- Gregorian years


# Mass

- kilograms

- grams

- pounds

- ounces

- nanograms

- micrograms

- milligrams

- metric tons

- long tons

- short tons

- stone

- carats

- slugs


# Temperature

- kelvin

- Celsius

- Fahrenheit

- Réaumur

- Rankine


# Energy

- joules

- millijoules

- kilojoules

- nanojoules

- microjoules

- calories

- nanocalories

- microcalories

- millicalories

- kilocalories

- watt-hours

- kilowatt-hours

- British thermal units

- therms

- foot-pounds


# Power

- watts

- milliwatts

- nanowatts

- microwatts

- kilowatts

- horsepower


# Frequency

- hertz

- millihertz

- nanohertz

- microhertz

- kilohertz


# Electrical Units

## Current

- amps

- milliamps

- amperes

- nanoamperes

- microamperes

- milliamperes

- kiloamperes

## Voltage

- volts

- millivolts

- nanovolts

- microvolts

- kilovolts

- statvolts

- abvolts

## Resistance

- ohms

- kiloohms

- milliohms

- nanoohms

- microohms

## Capacitance

- farads

- nanofarads

- microfarads

- millifarads

- kilofarads

## Conductance

- siemens

- nanosiemens

- microsiemens

- millisiemens

- kilosiemens

## Charge

- coulombs

- nanocoulombs

- microcoulombs

- millicoulombs

- kilocoulombs

- ampere-hours

- nanoampere-hours

- microampere-hours

- milliampere-hours

- kiloampere-hours

## Inductance

- henries

- nanohenries

- microhenries

- millihenries

- kilohenries


# Pressure

- pascals

- nanopascals

- micropascals

- millipascals

- kilopascals

- bars

- millibars

- atmospheres

- pounds per square inch

- torr


# Density

- kilograms per cubic meter

- grams per milliliter

- kilograms per liter

- ounces per cubic foot

- ounces per cubic inch

- ounces per gallon

- pounds per cubic foot

- pounds per cubic inch

- pounds per gallon

- slugs per cubic foot


# Light and Photometry

## Illuminance

- lux

- nanolux

- microlux

- millilux

- kilolux

- footcandles

- lumens per square inch

- phots

## Luminous Flux

- lumens

- nanolumens

- microlumens

- millilumens

- kilolumens

## Luminous Intensity

- candelas

- nanocandelas

- microcandelas

- millicandelas

- kilocandelas


# Magnetism

## Magnetic Flux

- webers

- nanowebers

- microwebers

- milliwebers

- kilowebers

- maxwells

## Magnetic Strength

- teslas

- nanoteslas

- microteslas

- milliteslas

- kiloteslas

- gauss


# Radiation

## Radioactivity

- becquerels

- nanobecquerels

- microbecquerels

- millibecquerels

- kilobecquerels

- curies

- rutherfords

## Absorbed Dose

- grays

- nanograys

- micrograys

- milligrays

- kilograys

- rads

## Equivalent Dose

- sieverts

- nanosieverts

- microsieverts

- millisieverts

- kilosieverts


# Other Measurement Types

SmartUnits also includes support for:

- dimensionless values

- percentages

- concentration

- parts per million

- parts per billion

- parts per trillion

- data

- data transfer rates

- solid angles

- steradians

- substance

- moles

- compound units

- multiplication units

- division/per units


# WPILib

SmartUnits is inspired by the Java WPILib units system (edu.wpi.first.units) and contains portions of code used in it.

SmartUnits is not affiliated with or endorsed by FIRST or WPILib.

See the project's LICENSE.md and attribution files for complete licensing information regarding WPILib-derived code.


# License

See the repository's license files for licensing information.

Some portions of SmartUnits are derived from or inspired by WPILib and retain the required attribution and licensing notices.

