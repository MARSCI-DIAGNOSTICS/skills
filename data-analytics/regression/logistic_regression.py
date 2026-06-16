# regression/logistic_regression.py
# Deterministic Logistic Regression (Production Closed)

import numpy as np
from typing import Dict, Any
from scipy import stats


MAX_ITER = 100
TOL = 1e-6
EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_logistic_regression(payload: Dict[str, Any]) -> Dict[str, Any]:

    dataset = payload["dataset"]
    target = payload["target_variable"]
    independents = payload["independent_variables"]
    confidence_level = payload.get("confidence_level", 0.95)

    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1.")

    X, y, feature_names = build_design_matrix(dataset, independents, target)

    beta, converged = fit_logistic_mle(X, y)

    probabilities = sigmoid(X @ beta)

    metrics = compute_model_metrics(y, probabilities, X)
    coefficients = compute_coefficient_statistics(
        X, y, beta, confidence_level, feature_names
    )

    return {
        "analysis_type": "logistic_regression",
        "results": {
            "coefficients": coefficients,
            "model_metrics": metrics
        },
        "model_diagnostics": {
            "converged": bool(converged)
        },
        "assumption_tests": {},
        "confidence_level": float(confidence_level),
        "interpretation": {
            "summary": "Logistic regression executed.",
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
# Logistic Core (Newton-Raphson)
# =========================================================

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))


def fit_logistic_mle(X, y):

    n, p = X.shape
    beta = np.zeros(p)
    converged = False

    for _ in range(MAX_ITER):

        z = X @ beta
        p_hat = sigmoid(z)

        gradient = X.T @ (p_hat - y)

        w = p_hat * (1 - p_hat) + EPS
        WX = X * w[:, None]
        hessian = X.T @ WX

        try:
            delta = np.linalg.pinv(hessian) @ gradient
        except Exception:
            break

        beta_new = beta - delta

        if np.max(np.abs(beta_new - beta)) < TOL:
            beta = beta_new
            converged = True
            break

        beta = beta_new

    return beta, converged


# =========================================================
# Model Metrics
# =========================================================

def compute_model_metrics(y, p_hat, X):

    n = len(y)
    p = X.shape[1] - 1

    log_likelihood = np.sum(
        y * np.log(p_hat + EPS) +
        (1 - y) * np.log(1 - p_hat + EPS)
    )

    aic = 2 * (p + 1) - 2 * log_likelihood
    bic = np.log(n) * (p + 1) - 2 * log_likelihood

    null_prob = np.mean(y)
    null_ll = np.sum(
        y * np.log(null_prob + EPS) +
        (1 - y) * np.log(1 - null_prob + EPS)
    )

    if abs(null_ll) < EPS:
        pseudo_r2 = 0.0
    else:
        pseudo_r2 = 1 - (log_likelihood / null_ll)

    return {
        "aic": float(aic),
        "bic": float(bic),
        "pseudo_r_squared": float(pseudo_r2)
    }


# =========================================================
# Coefficient Statistics (Wald Test)
# =========================================================

def compute_coefficient_statistics(X, y, beta, confidence_level, feature_names):

    z = X @ beta
    p_hat = sigmoid(z)

    w = p_hat * (1 - p_hat) + EPS
    WX = X * w[:, None]
    fisher_info = X.T @ WX

    cov_matrix = np.linalg.pinv(fisher_info)
    standard_errors = np.sqrt(np.diagonal(cov_matrix))

    alpha = 1 - confidence_level
    z_crit = stats.norm.ppf(1 - alpha / 2)

    coefficients = {}

    for i, name in enumerate(feature_names):

        se = standard_errors[i] if standard_errors[i] > EPS else EPS
        z_score = beta[i] / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        coefficients[name] = {
            "estimate": float(beta[i]),
            "odds_ratio": float(np.exp(beta[i])),
            "p_value": float(p_value)
        }

    return coefficients