# regression/linear_regression.py
# Deterministic OLS Regression Engine (Production Closed)

import numpy as np
from typing import Dict, Any
from scipy import stats
from diagnostics.assumption_tests import run_assumption_tests


EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_linear_regression(payload: Dict[str, Any]) -> Dict[str, Any]:

    dataset = payload["dataset"]
    target = payload["target_variable"]
    independents = payload["independent_variables"]
    confidence_level = payload.get("confidence_level", 0.95)

    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1.")

    X, y, feature_names = build_design_matrix(dataset, independents, target)

    beta = compute_ols_coefficients(X, y)
    predictions = X @ beta

    metrics = compute_model_metrics(y, predictions, X)
    coefficients = compute_coefficient_statistics(
        X, y, beta, confidence_level, feature_names
    )

    assumption_results = run_assumption_tests(X, y, predictions)

    return {
        "analysis_type": "linear_regression",
        "results": {
            "coefficients": coefficients,
            "model_metrics": metrics
        },
        "model_diagnostics": {},
        "assumption_tests": assumption_results,
        "confidence_level": float(confidence_level),
        "interpretation": {
            "summary": "Linear regression executed.",
            "key_findings": []
        }
    }


# =========================================================
# Design Matrix
# =========================================================

def build_design_matrix(dataset, independents, target):

    n = len(dataset)
    k = len(independents)

    if n == 0:
        raise ValueError("Dataset is empty.")

    X = np.ones((n, k + 1))
    y = np.zeros(n)

    for i, row in enumerate(dataset):
        y[i] = float(row[target])
        for j, var in enumerate(independents):
            X[i, j + 1] = float(row[var])

    feature_names = ["intercept"] + independents
    return X, y, feature_names


# =========================================================
# OLS Core
# =========================================================

def compute_ols_coefficients(X, y):

    XtX = X.T @ X
    XtX_inv = np.linalg.pinv(XtX)
    XtY = X.T @ y

    beta = XtX_inv @ XtY
    return beta


# =========================================================
# Model Metrics
# =========================================================

def compute_model_metrics(y, y_hat, X):

    n = len(y)
    p = X.shape[1] - 1

    residuals = y - y_hat
    sse = np.sum(residuals ** 2)
    sst = np.sum((y - np.mean(y)) ** 2)

    if sst < EPS:
        r_squared = 0.0
    else:
        r_squared = 1 - (sse / sst)

    df = n - p - 1

    if df > 0:
        adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / df
        mse = sse / df
    else:
        adjusted_r_squared = 0.0
        mse = 0.0

    rmse = np.sqrt(mse)

    safe_mse = mse if mse > EPS else EPS
    log_likelihood = -n / 2 * (np.log(2 * np.pi * safe_mse) + 1)

    aic = 2 * (p + 1) - 2 * log_likelihood
    bic = np.log(n) * (p + 1) - 2 * log_likelihood

    return {
        "r_squared": float(r_squared),
        "adjusted_r_squared": float(adjusted_r_squared),
        "aic": float(aic),
        "bic": float(bic),
        "rmse": float(rmse),
        "residual_variance": float(mse)
    }


# =========================================================
# Coefficient Statistics
# =========================================================

def compute_coefficient_statistics(X, y, beta, confidence_level, feature_names):

    n = len(y)
    p = X.shape[1]

    residuals = y - X @ beta
    df = n - p

    if df <= 0:
        raise ValueError("Insufficient degrees of freedom.")

    mse = np.sum(residuals ** 2) / df

    XtX_inv = np.linalg.pinv(X.T @ X)
    var_beta = mse * XtX_inv
    standard_errors = np.sqrt(np.diagonal(var_beta))

    alpha = 1 - confidence_level
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    coefficients = {}

    for i, name in enumerate(feature_names):

        se = standard_errors[i] if standard_errors[i] > EPS else EPS
        t_value = beta[i] / se
        p_value = 2 * (1 - stats.t.cdf(abs(t_value), df))

        lower = beta[i] - t_crit * se
        upper = beta[i] + t_crit * se

        coefficients[name] = {
            "estimate": float(beta[i]),
            "p_value": float(p_value),
            "confidence_interval": [
                float(lower),
                float(upper)
            ]
        }

    return coefficients