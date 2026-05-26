# diagnostics/assumption_tests.py
# Deterministic Assumption Testing Engine (Production Closed)

import numpy as np
from typing import Dict, Any
from scipy import stats


EPS = 1e-12


# =========================================================
# Public Entry
# =========================================================

def run_assumption_tests(X: np.ndarray, y: np.ndarray, y_hat: np.ndarray) -> Dict[str, Any]:

    residuals = y - y_hat

    return {
        "normality": test_normality(residuals),
        "heteroskedasticity": test_breusch_pagan(X, residuals),
        "multicollinearity": compute_vif(X),
        "autocorrelation": test_durbin_watson(residuals)
    }


# =========================================================
# Normality
# =========================================================

def test_normality(residuals: np.ndarray):

    residuals = residuals[~np.isnan(residuals)]
    n = len(residuals)

    if n < 3:
        return {"statistic": None, "p_value": None}

    try:
        if n <= 5000:
            stat, p_value = stats.shapiro(residuals)
        else:
            stat, p_value = stats.normaltest(residuals)
    except Exception:
        return {"statistic": None, "p_value": None}

    return {
        "statistic": float(stat),
        "p_value": float(p_value)
    }


# =========================================================
# Breusch–Pagan (Fully NaN Safe)
# =========================================================

def test_breusch_pagan(X: np.ndarray, residuals: np.ndarray):

    mask = ~np.isnan(residuals)
    mask &= ~np.isnan(X).any(axis=1)

    residuals = residuals[mask]
    X_aux = X[mask]

    n = len(residuals)

    if n == 0 or X_aux.shape[1] <= 1:
        return {"statistic": None, "p_value": None}

    try:
        squared_resid = residuals ** 2

        beta = np.linalg.pinv(X_aux.T @ X_aux) @ (X_aux.T @ squared_resid)
        fitted = X_aux @ beta

        sse = np.sum((squared_resid - fitted) ** 2)
        sst = np.sum((squared_resid - np.mean(squared_resid)) ** 2)

        if sst < EPS:
            return {"statistic": None, "p_value": None}

        r_squared = 1 - (sse / sst)
        lm_stat = n * r_squared

        df = X_aux.shape[1] - 1
        p_value = 1 - stats.chi2.cdf(lm_stat, df)

    except Exception:
        return {"statistic": None, "p_value": None}

    return {
        "statistic": float(lm_stat),
        "p_value": float(p_value)
    }


# =========================================================
# VIF (NaN Safe)
# =========================================================

def compute_vif(X: np.ndarray):

    if X.shape[1] <= 2:
        return {"vif": None}

    vif_values = {}

    for i in range(1, X.shape[1]):

        y_i = X[:, i]
        X_i = np.delete(X, i, axis=1)

        mask = ~np.isnan(y_i)
        mask &= ~np.isnan(X_i).any(axis=1)

        y_i = y_i[mask]
        X_i = X_i[mask]

        if len(y_i) == 0:
            vif_values[f"feature_{i}"] = None
            continue

        try:
            beta = np.linalg.pinv(X_i.T @ X_i) @ (X_i.T @ y_i)
            y_hat = X_i @ beta

            sse = np.sum((y_i - y_hat) ** 2)
            sst = np.sum((y_i - np.mean(y_i)) ** 2)

            if sst < EPS:
                vif_values[f"feature_{i}"] = None
                continue

            r_squared = 1 - (sse / sst)
            vif = 1 / (1 - r_squared + EPS)

            vif_values[f"feature_{i}"] = float(vif)

        except Exception:
            vif_values[f"feature_{i}"] = None

    return vif_values


# =========================================================
# Durbin–Watson
# =========================================================

def test_durbin_watson(residuals: np.ndarray):

    residuals = residuals[~np.isnan(residuals)]

    if len(residuals) < 2:
        return {"statistic": None}

    diff = np.diff(residuals)

    numerator = np.sum(diff ** 2)
    denominator = np.sum(residuals ** 2)

    if denominator < EPS:
        return {"statistic": None}

    dw_stat = numerator / denominator

    return {
        "statistic": float(dw_stat)
    }