# eda/eda_engine.py
# Deterministic EDA Engine (Production Closed)

import numpy as np
from typing import Dict, Any, List


EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_eda(payload: Dict[str, Any]) -> Dict[str, Any]:

    dataset = payload["dataset"]

    summary_stats = compute_summary_statistics(dataset)
    correlation_matrix = compute_correlation_matrix(dataset)
    missing_analysis = compute_missing_analysis(dataset)
    outlier_analysis = compute_outlier_analysis(dataset)

    return {
        "analysis_type": "eda",
        "results": {
            "summary_statistics": summary_stats,
            "correlation_matrix": correlation_matrix,
            "missing_analysis": missing_analysis,
            "outlier_analysis": outlier_analysis
        },
        "interpretation": {
            "summary": "Exploratory data analysis completed.",
            "key_findings": []
        }
    }


# =========================================================
# Utilities
# =========================================================

def extract_columns(dataset: List[Dict[str, Any]]) -> List[str]:
    columns = set()
    for row in dataset:
        columns.update(row.keys())
    return sorted(columns)


def is_numeric_column(dataset: List[Dict[str, Any]], column: str) -> bool:
    for row in dataset:
        value = row.get(column)
        if value is None:
            continue
        if not isinstance(value, (int, float)):
            return False
    return True


def get_numeric_array(dataset: List[Dict[str, Any]], column: str):
    values = []
    for row in dataset:
        value = row.get(column)
        if isinstance(value, (int, float)):
            values.append(float(value))
    return np.array(values)


def get_aligned_numeric_arrays(dataset, col1, col2):
    x_vals = []
    y_vals = []

    for row in dataset:
        v1 = row.get(col1)
        v2 = row.get(col2)

        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            x_vals.append(float(v1))
            y_vals.append(float(v2))

    return np.array(x_vals), np.array(y_vals)


# =========================================================
# Summary Statistics
# =========================================================

def compute_summary_statistics(dataset):

    columns = extract_columns(dataset)
    summary = {}

    for col in columns:

        if not is_numeric_column(dataset, col):
            continue

        values = get_numeric_array(dataset, col)
        n = len(values)

        if n == 0:
            continue

        std_val = float(np.std(values, ddof=1)) if n > 1 else 0.0
        iqr_val = float(np.percentile(values, 75) - np.percentile(values, 25))

        summary[col] = {
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "std": std_val,
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "iqr": iqr_val,
            "count": int(n)
        }

    return summary


# =========================================================
# Correlation Matrix (Deterministic + Safe)
# =========================================================

def compute_correlation_matrix(dataset):

    columns = extract_columns(dataset)
    numeric_columns = [col for col in columns if is_numeric_column(dataset, col)]

    matrix = {}

    for col1 in numeric_columns:

        matrix[col1] = {}

        for col2 in numeric_columns:

            x, y = get_aligned_numeric_arrays(dataset, col1, col2)

            if len(x) < 2:
                matrix[col1][col2] = 0.0
                continue

            if np.std(x, ddof=1) < EPS or np.std(y, ddof=1) < EPS:
                matrix[col1][col2] = 0.0
                continue

            corr = np.corrcoef(x, y)[0, 1]

            if np.isnan(corr):
                corr = 0.0

            matrix[col1][col2] = float(corr)

    return matrix


# =========================================================
# Missing Analysis
# =========================================================

def compute_missing_analysis(dataset):

    total_rows = len(dataset)
    columns = extract_columns(dataset)

    missing_summary = {}

    for col in columns:

        missing_count = sum(
            1 for row in dataset if row.get(col) is None
        )

        missing_percentage = (
            float(missing_count / total_rows)
            if total_rows > 0 else 0.0
        )

        missing_summary[col] = {
            "missing_count": int(missing_count),
            "missing_percentage": missing_percentage
        }

    return missing_summary


# =========================================================
# Outlier Detection (IQR Method)
# =========================================================

def compute_outlier_analysis(dataset):

    columns = extract_columns(dataset)
    outliers = {}

    for col in columns:

        if not is_numeric_column(dataset, col):
            continue

        values = get_numeric_array(dataset, col)
        n = len(values)

        if n < 4:
            continue

        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1

        if iqr < EPS:
            outliers[col] = {
                "lower_bound": float(q1),
                "upper_bound": float(q3),
                "outlier_count": 0
            }
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = int(
            np.sum((values < lower_bound) | (values > upper_bound))
        )

        outliers[col] = {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "outlier_count": outlier_count
        }

    return outliers