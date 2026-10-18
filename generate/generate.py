#!/usr/bin/env python3

# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

# This script generates unit-specific interfaces and mutable and immutable
# implementations of those interfaces.
#
# Generated files will be located in wpiunits/src/generated/main/

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader


def output(output_dir, outfn: str, contents: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / outfn
    output_file.write_text(contents, encoding="utf-8", newline="\n")


def load_json_file(file_path: Path):
    with file_path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
UNIT_CONFIGURATIONS = load_json_file(SCRIPT_DIRECTORY / "unit_configurations.json")
MEASUREMENTS_BY_NAME = {
    m["name"]: m for m in load_json_file(SCRIPT_DIRECTORY / "measurement_units.json")
}


def normalize_measurement_units(measurement_configurations: list[dict]) -> list[dict]:
    normalized_configurations: list[dict] = []

    for measurement in measurement_configurations:
        normalized_units: list[dict] = []
        for unit in measurement.get("units", []):
            if "per" in unit or "mult" in unit:
                normalized_units.append(unit)
                continue

            to_base_multiplier = unit.get("to_base_multiplier", unit.get("conversion_factor", 1.0))
            to_base_offset = unit.get("to_base_offset", 0.0)

            from_base_multiplier = unit.get("from_base_multiplier")
            if from_base_multiplier is None:
                if to_base_multiplier == 0:
                    raise ValueError(f"Unit {unit['variable']} must define a non-zero conversion multiplier")
                from_base_multiplier = 1 / to_base_multiplier

            from_base_offset = unit.get("from_base_offset")
            if from_base_offset is None:
                from_base_offset = -to_base_offset * from_base_multiplier + 0.0

            normalized_units.append(
                {
                    **unit,
                    "to_base_multiplier": to_base_multiplier,
                    "to_base_offset": to_base_offset,
                    "from_base_multiplier": from_base_multiplier,
                    "from_base_offset": from_base_offset,
                }
            )

        normalized_configurations.append({**measurement, "units": normalized_units})

    return normalized_configurations



# measure-to-unit
def mtou(measure_name):
    return measure_name + "Unit"


def indent(multiline_string, indentation):
    """
    Indents a multiline string by `indentation` number of spaces
    """
    return "\n".join(
        list(map(lambda line: " " * indentation + line, multiline_string.split("\n")))
    )

def file_name(measure_name: str) -> str:
    parts = []
    for c in measure_name:
        if c.isupper() and parts:
            parts.append("_")
        parts.append(c.lower())
    return "".join(parts)

def unit_module(unit_type: str) -> str:
    return file_name(re.sub(r"Unit(\[.*\])?$", "", unit_type))


def base_unit_variable(measure_name: str) -> str:
    return MEASUREMENTS_BY_NAME[measure_name]["units"][0]["variable"]


def kind(name: str) -> str | None:
    measurement = MEASUREMENTS_BY_NAME.get(name) or MEASUREMENTS_BY_NAME[re.sub(r"Unit$", "", name)]
    return measurement.get("kind")


def measure_base(measure_name: str) -> str:
    return {"per": "Per", "mult": "Mult"}.get(kind(measure_name), "Measure")


def unit_base(measure_name: str) -> str:
    return {"per": "PerUnit", "mult": "MultUnit"}.get(kind(measure_name), "Unit")


def unit_class(unit: dict) -> str:
    return "PerUnit" if "per" in unit else "MultUnit"


def unit_parts(unit: dict) -> list[str]:
    return [ref.split(".")[-1] for ref in unit.get("per") or unit["mult"]]


def find_unit(ref: str) -> str:
    if "." in ref:
        measure_name, variable = ref.split(".")
        return file_name(measure_name)
    modules = [
        file_name(m["name"])
        for m in MEASUREMENTS_BY_NAME.values()
        if any(u["variable"] == ref for u in m["units"])
    ]
    if len(modules) != 1:
        raise ValueError(f"Unit {ref!r} is defined in {modules or 'no modules'}; write it as Quantity.{ref}")
    return modules[0]


def component_imports(measurement: dict) -> dict[str, list[str]]:
    own_module = file_name(measurement["name"])
    imports: dict[str, list[str]] = {}
    for unit in measurement["units"]:
        for ref in unit.get("per") or unit.get("mult") or ():
            module = find_unit(ref)
            variable = ref.split(".")[-1]
            if module != own_module and variable not in imports.setdefault(module, []):
                imports[module].append(variable)
    return {module: variables for module, variables in imports.items() if variables}


def generate_package_init(
    output_directory: Path,
    measurement_configurations: list[dict],
):
    lazy_imports = {
        "Measure": ("smartunits.core.measure", "Measure"),
        "Unit": ("smartunits.core.unit", "Unit"),
        "UnaryFunction": ("smartunits.core.unary_function", "UnaryFunction"),
        "Per": ("smartunits.core.per", "Per"),
        "PerUnit": ("smartunits.core.per", "PerUnit"),
        "Mult": ("smartunits.core.mult", "Mult"),
        "MultUnit": ("smartunits.core.mult", "MultUnit"),
    }

    for measurement in measurement_configurations:
        name = measurement["name"]
        module_name = f"smartunits.{file_name(name)}"

        if measurement.get("kind") != "compound":
            lazy_imports[name] = (module_name, name)
            lazy_imports[measurement["unit_type"]] = (module_name, measurement["unit_type"])
        for unit in measurement.get("units", ()):
            lazy_imports[unit["variable"]] = (module_name, unit["variable"])

    lines = [
        "from importlib import import_module",
        "from typing import TYPE_CHECKING",
        "",
        "from .core.measure import Measure",
        "from .core.unit import Unit",
        "from .core.unary_function import UnaryFunction",
        "",
        "if TYPE_CHECKING:",
    ]

    type_checking_imports: dict[str, list[str]] = {}

    for name, (module_name, attribute_name) in lazy_imports.items():
        type_checking_imports.setdefault(module_name, []).append(attribute_name)

    for module_name, attributes in type_checking_imports.items():
        relative_module = module_name.replace("smartunits.", ".")
        lines.append(f"    from {relative_module} import (")
        lines.extend(f"        {attribute}," for attribute in attributes)
        lines.append("    )")

    lines.extend(
        [
            "",
            "_LAZY_IMPORTS: dict[str, tuple[str, str]] = {",
        ]
    )

    for name, (module_name, attribute_name) in lazy_imports.items():
        lines.append(
            f'    "{name}": ("{module_name}", "{attribute_name}"),'
        )

    lines.extend(
        [
            "}",
            "",
            "",
            "def __getattr__(name: str):",
            "    try:",
            "        module_name, attribute_name = _LAZY_IMPORTS[name]",
            "    except KeyError:",
            '        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None',
            "",
            "    module = import_module(module_name)",
            "    value = getattr(module, attribute_name)",
            "",
            "    # Cache resolved values for future access.",
            "    globals()[name] = value",
            "    return value",
            "",
            "",
            "__all__ = list(_LAZY_IMPORTS)",
        ]
    )

    output(
        output_directory,
        "__init__.py",
        "\n".join(lines) + "\n",
    )

def generate_units(output_directory: Path, template_directory: Path):
    env = Environment(
        loader=FileSystemLoader(template_directory),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    quantity_template = env.get_template("quantity.py.jinja")
    script_directory = Path(__file__).resolve().parent

    math_units = load_json_file(script_directory / "unit_types.json")
    measurement_configurations = normalize_measurement_units(
        load_json_file(script_directory / "measurement_units.json")
    )

    helpers = {
        "mtou": mtou,
        "indent": indent,
        "file_name": file_name,
        "unit_module": unit_module,
        "base_unit_variable": base_unit_variable,
        "kind": kind,
        "measure_base": measure_base,
        "unit_base": unit_base,
        "unit_class": unit_class,
        "unit_parts": unit_parts,
        "component_imports": component_imports,
    }

    for measurement in measurement_configurations:
        contents = quantity_template.render(
            name=measurement["name"],
            measurement=measurement,
            math_units=math_units,
            config=UNIT_CONFIGURATIONS,
            helpers=helpers,
        )
        output(output_directory, file_name(measurement["name"]) + ".py", contents)

    generate_package_init(output_directory, measurement_configurations)


def clean_output_directories(root_directory: Path):
    """Remove generated files before generating new ones. Preserves core/, which holds the only non-generated files."""
    root_directory.mkdir(parents=True, exist_ok=True)

    for path in root_directory.iterdir():
        if path.name == "core":
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def main():
    script_path = Path(__file__).resolve()
    dirname = script_path.parent

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_directory",
        help="Optional. If set, will output the generated files to this directory, otherwise it will use a path relative to the script",
        default=dirname.parent / "smartunits",
        type=Path,
    )
    parser.add_argument(
        "--template_root",
        help="Optional. If set, will use this directory as the root for the jinja templates",
        default=dirname / "templates",
        type=Path,
    )
    args = parser.parse_args()

    clean_output_directories(args.output_directory)

    generate_units(args.output_directory, args.template_root)


if __name__ == "__main__":
    main()