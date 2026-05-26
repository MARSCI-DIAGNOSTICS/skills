# regression/model_metrics.py
# Deterministic Correlation Analysis Engine (Production Closed)

import numpy as np
from typing import Dict, Any
from scipy import stats


EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_correlation_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:

    dataset = payload["dataset"]
    variables = payload["independent_variables"]
    method = payload.get("correlation_method", "pearson").lower()

    if len(variables) != 2:
        raise ValueError("Correlation analysis requires exactly two variables.")

    x, y = extract_aligned_numeric_arrays(dataset, variables[0], variables[1])

    if len(x) < 2:
        raise ValueError("At least two aligned numeric observations required.")

    if method == "pearson":
        corr_coef, p_value = compute_pearson(x, y)

    elif method == "spearman":
        corr_coef, p_value = compute_spearman(x, y)

    else:
        raise ValueError("Unsupported correlation_method.")

    return {
        "analysis_type": "correlation",
        "results": {
            "correlation_coefficient": float(corr_coef),
            "p_value": float(p_value)
        },
        "interpretation": {
            "summary": "Correlation analysis executed.",
            "key_findings": []
        }
    }


# =========================================================
# Data Alignment
# =========================================================

def extract_aligned_numeric_arrays(dataset, var1, var2):

    x_vals = []
    y_vals = []

    for row in dataset:
        v1 = row.get(var1)
        v2 = row.get(var2)

        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            x_vals.append(float(v1))
            y_vals.append(float(v2))

    return np.array(x_vals), np.array(y_vals)


# =========================================================
# Pearson Correlation
# =========================================================

def compute_pearson(x, y):

    if np.std(x, ddof=1) < EPS or np.std(y, ddof=1) < EPS:
        return 0.0, 1.0

    try:
        corr_coef, p_value = stats.pearsonr(x, y)
    except Exception:
        return 0.0, 1.0

    if np.isnan(corr_coef):
        corr_coef = 0.0

    if np.isnan(p_value):
        p_value = 1.0

    return corr_coef, p_value


# =========================================================
# Spearman Correlation
# =========================================================

def compute_spearman(x, y):

    try:
        corr_coef, p_value = stats.spearmanr(x, y)
    except Exception:
        return 0.0, 1.0

    if np.isnan(corr_coef):
        corr_coef = 0.0

    if np.isnan(p_value):
        p_value = 1.0

    return corr_coef, p_value