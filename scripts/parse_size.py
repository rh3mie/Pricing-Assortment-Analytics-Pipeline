from __future__ import annotations

import re
from fractions import Fraction
from typing import Any


UNIT_ALIASES = {
    "oz": "oz",
    "fl oz": "fl_oz",
    "fluid ounce": "fl_oz",
    "fluid ounces": "fl_oz",
    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",
    "gal": "gal",
    "gallon": "gal",
    "gallons": "gal",
    "qt": "qt",
    "quart": "qt",
    "pt": "pt",
    "pint": "pt",
    "l": "l",
    "liter": "l",
    "liters": "l",
    "ml": "ml",
    "ct": "ct",
    "count": "ct",
    "ea": "ea",
    "each": "ea",
    "pack": "pack",
}


def _parse_number(value: str) -> float | None:
    value = value.strip()
    try:
        if "/" in value:
            return float(Fraction(value))
        return float(value)
    except Exception:
        return None


def parse_size(size: Any) -> tuple[float | None, str | None]:
    if size is None:
        return None, None

    text = str(size).strip().lower()
    if not text:
        return None, None

    pattern = r"^(\d+(?:\.\d+)?|\d+/\d+)\s*([a-z ]+)$"
    match = re.match(pattern, text)

    if not match:
        return None, None

    raw_num = match.group(1).strip()
    raw_unit = match.group(2).strip()

    num = _parse_number(raw_num)
    unit = UNIT_ALIASES.get(raw_unit, raw_unit)

    return num, unit


def convert_to_base_unit(unit_size: float | None, unit_type: str | None) -> tuple[float | None, str | None]:
    if unit_size is None or unit_type is None:
        return None, None

    if unit_type == "gal":
        return unit_size * 128, "fl_oz"
    if unit_type == "qt":
        return unit_size * 32, "fl_oz"
    if unit_type == "pt":
        return unit_size * 16, "fl_oz"
    if unit_type == "l":
        return unit_size * 33.814, "fl_oz"
    if unit_type == "ml":
        return unit_size / 29.5735, "fl_oz"
    if unit_type == "lb":
        return unit_size * 16, "oz"

    return unit_size, unit_type