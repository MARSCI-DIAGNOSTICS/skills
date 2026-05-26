# core/validation.py
# Data Analytics Skill – Validation Layer
# Deterministic & Hardened Contract Enforcement (Production Closed)

import json
import os
from typing import Dict, Any, List, Set

try:
    import jsonschema
except ImportError:
    jsonschema = None


SCHEMA_PATH = os.path.join("schemas", "input_schema.json")


# =========================================================
# Public Entry
# =========================================================

def validate_input_payload(payload: Dict[str, Any]) -> None:

    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary.")

    validate_json_schema(payload)

    dataset = payload["dataset"]
    validate_dataset_structure(dataset)

    analysis_type = payload["analysis_type"]

    if analysis_type in ["linear_regression", "logistic_regression", "hypothesis_test"]:
        if "confidence_level" not in payload:
            raise ValueError("confidence_level is required for this analysis_type.")
        validate_confidence_level(payload["confidence_level"])

    if analysis_type in ["linear_regression", "logistic_regression"]:
        validate_regression_variables(payload, dataset)

    if analysis_type == "logistic_regression":
        validate_logistic_binary_target(payload, dataset)

    if analysis_type == "hypothesis_test":
        validate_hypothesis_structure(payload, dataset)

    if analysis_type == "correlation":
        validate_correlation_structure(payload, dataset)


# =========================================================
# JSON Schema Validation
# =========================================================

def validate_json_schema(payload: Dict[str, Any]) -> None:

    if jsonschema is None:
        return

    if not os.path.exists(SCHEMA_PATH):
        raise ValueError("input_schema.json not found.")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    jsonschema.validate(instance=payload, schema=schema)


# =========================================================
# Dataset Validation
# =========================================================

def validate_dataset_structure(dataset: List[Dict[str, Any]]) -> None:

    if not isinstance(dataset, list) or len(dataset) == 0:
        raise ValueError("Dataset must be a non-empty array.")

    for row in dataset:
        if not isinstance(row, dict):
            raise ValueError("Each dataset row must be an object.")


def extract_columns(dataset: List[Dict[str, Any]]) -> Set[str]:
    all_columns = set()
    for row in dataset:
        all_columns.update(row.keys())
    return all_columns


def is_numeric_column(dataset: List[Dict[str, Any]], column: str) -> bool:
    for row in dataset:
        value = row.get(column)
        if value is None:
            continue
        if not isinstance(value, (int, float)):
            return False
    return True


# =========================================================
# Regression Validation
# =========================================================

def validate_regression_variables(payload: Dict[str, Any], dataset: List[Dict[str, Any]]):

    columns = extract_columns(dataset)

    target = payload.get("target_variable")
    independents = payload.get("independent_variables", [])

    if target not in columns:
        raise ValueError(f"Target variable '{target}' not found in dataset.")

    for var in independents:
        if var not in columns:
            raise ValueError(f"Independent variable '{var}' not found in dataset.")

    if target in independents:
        raise ValueError("Target variable cannot be included in independent variables.")

    if not is_numeric_column(dataset, target):
        raise ValueError("Target variable must be numeric for regression.")

    for var in independents:
        if not is_numeric_column(dataset, var):
            raise ValueError(f"Independent variable '{var}' must be numeric for regression.")


def validate_logistic_binary_target(payload: Dict[str, Any], dataset: List[Dict[str, Any]]):

    target = payload["target_variable"]
    values = set(row[target] for row in dataset if row.get(target) is not None)

    if values != {0, 1}:
        raise ValueError("Logistic regression target must be binary {0,1}.")


# =========================================================
# Hypothesis Validation
# =========================================================

def validate_hypothesis_structure(payload: Dict[str, Any], dataset: List[Dict[str, Any]]):

    columns = extract_columns(dataset)

    group_var = payload.get("group_variable")
    test_type = payload.get("test_type")

    if group_var not in columns:
        raise ValueError(f"Group variable '{group_var}' not found in dataset.")

    if test_type is None:
        raise ValueError("test_type must be specified for hypothesis testing.")


# =========================================================
# Correlation Validation
# =========================================================

def validate_correlation_structure(payload: Dict[str, Any], dataset: List[Dict[str, Any]]):

    columns = extract_columns(dataset)
    independents = payload.get("independent_variables", [])

    if len(independents) != 2:
        raise ValueError("Correlation analysis requires exactly two variables.")

    for var in independents:
        if var not in columns:
            raise ValueError(f"Correlation variable '{var}' not found in dataset.")

        if not is_numeric_column(dataset, var):
            raise ValueError(f"Correlation variable '{var}' must be numeric.")


# =========================================================
# Confidence Level Validation
# =========================================================

def validate_confidence_level(value: Any):

    if not isinstance(value, (int, float)):
        raise ValueError("confidence_level must be numeric.")

    if not (0.8 <= float(value) <= 0.999):
        raise ValueError("confidence_level must be between 0.8 and 0.999.")