# hypothesis/test_selector.py
# Deterministic Hypothesis Testing Engine (Production Closed)

import numpy as np
from typing import Dict, Any
from scipy import stats


EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_hypothesis_test(payload: Dict[str, Any]) -> Dict[str, Any]:

    test_type = payload["test_type"]

    if test_type == "t_test_independent":
        return run_t_test_independent(payload)

    if test_type == "t_test_paired":
        return run_t_test_paired(payload)

    if test_type == "z_test_proportion":
        return run_z_test_proportion(payload)

    if test_type == "chi_square":
        return run_chi_square(payload)

    if test_type == "anova_one_way":
        return run_anova_one_way(payload)

    raise ValueError("Unsupported test_type.")


# =========================================================
# Utilities
# =========================================================

def extract_group_data(dataset, group_var, value_var):

    groups = {}
    for row in dataset:
        g = row.get(group_var)
        v = row.get(value_var)

        if g is None:
            continue

        if not isinstance(v, (int, float)):
            continue

        groups.setdefault(g, []).append(float(v))

    return groups


# =========================================================
# Independent t-test
# =========================================================

def run_t_test_independent(payload):

    dataset = payload["dataset"]
    group_var = payload["group_variable"]
    value_var = payload["target_variable"]

    groups = extract_group_data(dataset, group_var, value_var)

    if len(groups) != 2:
        raise ValueError("Independent t-test requires exactly two groups.")

    g1, g2 = list(groups.values())

    if len(g1) < 2 or len(g2) < 2:
        raise ValueError("Each group must contain at least two observations.")

    n1, n2 = len(g1), len(g2)
    df = n1 + n2 - 2

    mean1, mean2 = np.mean(g1), np.mean(g2)
    var1, var2 = np.var(g1, ddof=1), np.var(g2, ddof=1)

    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
    se = np.sqrt(pooled_var * (1/n1 + 1/n2))

    t_stat = (mean1 - mean2) / (se + EPS)
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

    effect_size = (mean1 - mean2) / (np.sqrt(pooled_var) + EPS)

    return build_result(payload, t_stat, p_value, df, effect_size)


# =========================================================
# Paired t-test
# =========================================================

def run_t_test_paired(payload):

    dataset = payload["dataset"]
    value_var = payload["target_variable"]

    values = [
        row[value_var]
        for row in dataset
        if isinstance(row.get(value_var), (int, float))
    ]

    if len(values) < 4 or len(values) % 2 != 0:
        raise ValueError("Paired t-test requires even number of observations (>=4).")

    half = len(values) // 2
    d = np.array(values[:half]) - np.array(values[half:])

    mean_d = np.mean(d)
    sd_d = np.std(d, ddof=1)

    df = len(d) - 1
    se = sd_d / np.sqrt(len(d))

    t_stat = mean_d / (se + EPS)
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

    effect_size = mean_d / (sd_d + EPS)

    return build_result(payload, t_stat, p_value, df, effect_size)


# =========================================================
# Z-test Proportion
# =========================================================

def run_z_test_proportion(payload):

    dataset = payload["dataset"]
    value_var = payload["target_variable"]

    values = [
        row[value_var]
        for row in dataset
        if row.get(value_var) in [0, 1]
    ]

    n = len(values)

    if n == 0:
        raise ValueError("No valid binary observations.")

    p_hat = np.mean(values)

    p0 = payload.get("null_proportion", 0.5)

    if not (0 < p0 < 1):
        raise ValueError("null_proportion must be between 0 and 1.")

    se = np.sqrt(p0 * (1 - p0) / n)

    z_stat = (p_hat - p0) / (se + EPS)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return build_result(payload, z_stat, p_value, None, None)


# =========================================================
# Chi-square
# =========================================================

def run_chi_square(payload):

    dataset = payload["dataset"]
    group_var = payload["group_variable"]
    value_var = payload["target_variable"]

    groups = sorted({row[group_var] for row in dataset if group_var in row})
    values = sorted({row[value_var] for row in dataset if value_var in row})

    if len(groups) < 2 or len(values) < 2:
        raise ValueError("Chi-square requires at least 2x2 contingency table.")

    group_index = {g: i for i, g in enumerate(groups)}
    value_index = {v: j for j, v in enumerate(values)}

    matrix = np.zeros((len(groups), len(values)))

    for row in dataset:
        g = row.get(group_var)
        v = row.get(value_var)

        if g in group_index and v in value_index:
            matrix[group_index[g], value_index[v]] += 1

    chi_stat, p_value, df, _ = stats.chi2_contingency(matrix)

    return build_result(payload, chi_stat, p_value, int(df), None)


# =========================================================
# One-way ANOVA
# =========================================================

def run_anova_one_way(payload):

    dataset = payload["dataset"]
    group_var = payload["group_variable"]
    value_var = payload["target_variable"]

    groups = extract_group_data(dataset, group_var, value_var)

    if len(groups) < 2:
        raise ValueError("ANOVA requires at least two groups.")

    arrays = []

    for vals in groups.values():
        if len(vals) < 2:
            raise ValueError("Each group must contain at least two observations.")
        arrays.append(np.array(vals))

    f_stat, p_value = stats.f_oneway(*arrays)

    df_between = len(groups) - 1
    df_within = sum(len(v) for v in groups.values()) - len(groups)
    df_total = df_between + df_within

    return build_result(payload, f_stat, p_value, int(df_total), None)


# =========================================================
# Result Builder (Schema Compliant)
# =========================================================

def build_result(payload, test_stat, p_value, df, effect_size):

    result = {
        "analysis_type": "hypothesis_test",
        "results": {
            "test_statistic": float(test_stat),
            "p_value": float(p_value)
        },
        "confidence_level": float(payload.get("confidence_level", 0.95)),
        "interpretation": {
            "summary": "Hypothesis test executed.",
            "key_findings": []
        }
    }

    if df is not None:
        result["results"]["degrees_of_freedom"] = int(df)

    if effect_size is not None:
        result["results"]["effect_size"] = float(effect_size)

    return result