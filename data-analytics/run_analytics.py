# run_analytics.py
# Data Analytics Skill – Level 2 Statistical Engine
# Deterministic Orchestration Layer (Production Closed)

import json
import sys
from typing import Dict, Any

from core.validation import validate_input_payload
from core.preprocessing import preprocess_dataset
from eda.eda_engine import run_eda
from regression.linear_regression import run_linear_regression
from regression.logistic_regression import run_logistic_regression
from hypothesis.test_selector import run_hypothesis_test
from regression.model_metrics import run_correlation_analysis
from utils.result_formatter import format_result


ENGINE_VERSION = "2.1.0"


# =========================================================
# Structured Error Builder
# =========================================================

def build_error(message: str) -> Dict[str, Any]:
    return {
        "error": True,
        "engine_version": ENGINE_VERSION,
        "message": str(message)
    }


# =========================================================
# Deterministic Dataset Normalization
# =========================================================

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:

    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary.")

    if "dataset" not in payload:
        raise ValueError("Missing 'dataset' field.")

    if not isinstance(payload["dataset"], list):
        raise ValueError("Dataset must be a list.")

    normalized_dataset = []

    for row in payload["dataset"]:
        if not isinstance(row, dict):
            raise ValueError("Each dataset row must be an object.")

        # deterministic key ordering
        normalized_dataset.append(dict(sorted(row.items())))

    payload["dataset"] = normalized_dataset
    return payload


# =========================================================
# Output Structure Guard
# =========================================================

def validate_result_structure(result: Dict[str, Any]):

    if not isinstance(result, dict):
        raise ValueError("Analysis module returned invalid structure.")

    if "results" not in result:
        raise ValueError("Output missing 'results' field.")

    if "interpretation" not in result:
        raise ValueError("Output missing 'interpretation' field.")


# =========================================================
# Dispatcher
# =========================================================

def dispatch_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:

    analysis_type = payload["analysis_type"]

    if analysis_type == "eda":
        return run_eda(payload)

    if analysis_type == "linear_regression":
        return run_linear_regression(payload)

    if analysis_type == "logistic_regression":
        return run_logistic_regression(payload)

    if analysis_type == "hypothesis_test":
        return run_hypothesis_test(payload)

    if analysis_type == "correlation":
        return run_correlation_analysis(payload)

    raise ValueError("Unsupported analysis_type.")


# =========================================================
# Public Entry
# =========================================================

def run_analytics(payload: Dict[str, Any]) -> Dict[str, Any]:

    try:
        # 1️⃣ Normalize
        payload = normalize_payload(payload)

        # 2️⃣ Validate contract
        validate_input_payload(payload)

        # 3️⃣ Deterministic preprocessing
        payload = preprocess_dataset(payload)

        # 4️⃣ Dispatch engine
        result = dispatch_analysis(payload)

        # 5️⃣ Minimal structure guard
        validate_result_structure(result)

        # 6️⃣ Attach metadata
        result["analysis_type"] = payload["analysis_type"]
        result["engine_version"] = ENGINE_VERSION

        # 7️⃣ Deterministic formatting (rounding + JSON-safe)
        result = format_result(result)

        return result

    except Exception as e:
        return build_error(str(e))


# =========================================================
# CLI Entry
# =========================================================

if _name_ == "_main_":

    if len(sys.argv) < 2:
        print(json.dumps(build_error("No input file provided.")))
        sys.exit(0)

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            payload = json.load(f)

        output = run_analytics(payload)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except Exception as e:
        print(json.dumps(build_error(str(e))))
        sys.exit(0)