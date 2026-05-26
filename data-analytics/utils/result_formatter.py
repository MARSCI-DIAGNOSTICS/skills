# utils/result_formatter.py
# Deterministic Result Formatter (Final Hardened Production)

import math
import numpy as np


DEFAULT_PRECISION = 6


def format_result(data, precision=DEFAULT_PRECISION):

    if not isinstance(precision, int) or precision < 0:
        precision = DEFAULT_PRECISION

    return _format_recursive(data, precision)


def _format_recursive(obj, precision):

    if obj is None:
        return None

    if isinstance(obj, bool):
        return obj

    if isinstance(obj, dict):
        # Deterministic key order
        return {
            str(key): _format_recursive(obj[key], precision)
            for key in sorted(obj.keys(), key=str)
        }

    if isinstance(obj, list):
        return [_format_recursive(item, precision) for item in obj]

    if isinstance(obj, tuple):
        return [_format_recursive(item, precision) for item in obj]

    if isinstance(obj, np.ndarray):
        return [_format_recursive(item, precision) for item in obj.tolist()]

    if isinstance(obj, np.generic):
        return _format_number(float(obj), precision)

    if isinstance(obj, int):
        return obj  # preserve integer type

    if isinstance(obj, float):
        return _format_number(obj, precision)

    if isinstance(obj, str):
        return obj

    return None


def _format_number(value, precision):

    try:
        val = float(value)

        if math.isnan(val) or math.isinf(val):
            return 0.0

        rounded = round(val, precision)
        return float(rounded)

    except Exception:
        return 0.0