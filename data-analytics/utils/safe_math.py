# utils/safe_math.py
# Deterministic Safe Math Utilities (Level 2 Hardened)

import math
import numpy as np


EPS = 1e-12


# =========================================================
# Internal Numeric Guard
# =========================================================

def _to_float(x):
    try:
        return float(x)
    except Exception:
        return None


# =========================================================
# Safe Division
# =========================================================

def safe_divide(a, b, default=0.0):
    a_val = _to_float(a)
    b_val = _to_float(b)

    if a_val is None or b_val is None:
        return float(default)

    if abs(b_val) < EPS:
        return float(default)

    return float(a_val / b_val)


# =========================================================
# Safe Log
# =========================================================

def safe_log(x, default=0.0):
    x_val = _to_float(x)

    if x_val is None or x_val <= 0:
        return float(default)

    return float(math.log(x_val))


# =========================================================
# Safe Square Root
# =========================================================

def safe_sqrt(x, default=0.0):
    x_val = _to_float(x)

    if x_val is None or x_val < 0:
        return float(default)

    return float(math.sqrt(x_val))


# =========================================================
# NaN / Inf Guard
# =========================================================

def nan_to_zero(x):
    try:
        val = float(x)
        if math.isnan(val) or math.isinf(val):
            return 0.0
        return val
    except Exception:
        return 0.0


# =========================================================
# Probability Clipping
# =========================================================

def clip_probability(p):
    p_val = _to_float(p)

    if p_val is None:
        return EPS

    if p_val <= 0:
        return EPS

    if p_val >= 1:
        return 1 - EPS

    return float(p_val)


# =========================================================
# Safe Mean
# =========================================================

def safe_mean(arr, default=0.0):
    try:
        values = [float(x) for x in arr if _to_float(x) is not None]
        if len(values) == 0:
            return float(default)
        return float(np.mean(values))
    except Exception:
        return float(default)


# =========================================================
# Safe Standard Deviation
# =========================================================

def safe_std(arr, ddof=1, default=0.0):
    try:
        values = [float(x) for x in arr if _to_float(x) is not None]
        if len(values) <= ddof:
            return float(default)
        return float(np.std(values, ddof=ddof))
    except Exception:
        return float(default)