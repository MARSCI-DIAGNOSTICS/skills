# core/preprocessing.py
# Deterministic Preprocessing Layer (Final Production Closed)

from typing import List, Dict, Any
import copy
import math


def preprocess_dataset(payload: Dict[str, Any]) -> Dict[str, Any]:

    new_payload = copy.deepcopy(payload)
    dataset = new_payload["dataset"]

    target = new_payload.get("target_variable")
    independents = list(new_payload.get("independent_variables", []))
    interaction_terms = new_payload.get("interaction_terms", [])

    required_columns = set(independents)
    if target:
        required_columns.add(target)

    dataset = coerce_numeric(dataset, required_columns)
    dataset = drop_missing_required(dataset, required_columns)

    dataset, independents = apply_dummy_encoding(dataset, independents)

    dataset = apply_interactions(dataset, interaction_terms)

    new_payload["dataset"] = dataset
    new_payload["independent_variables"] = independents

    return new_payload


def coerce_numeric(dataset: List[Dict[str, Any]], columns: set):

    for row in dataset:
        for col in columns:
            value = row.get(col)

            if value is None or isinstance(value, bool):
                continue

            try:
                row[col] = float(value)
            except Exception:
                pass

    return dataset


def drop_missing_required(dataset: List[Dict[str, Any]], required_columns: set):

    clean_rows = []

    for row in dataset:
        valid = True

        for col in required_columns:
            val = row.get(col)

            if val is None:
                valid = False
                break

            if isinstance(val, float) and math.isnan(val):
                valid = False
                break

        if valid:
            clean_rows.append(row)

    return clean_rows


def apply_dummy_encoding(dataset: List[Dict[str, Any]], independents: List[str]):

    if not dataset:
        return dataset, independents

    new_independents = []

    for col in independents:

        values = sorted({
            row.get(col)
            for row in dataset
            if row.get(col) is not None
            and not isinstance(row.get(col), (int, float, bool))
        })

        if len(values) <= 1:
            new_independents.append(col)
            continue

        dummy_columns = []

        for category in values[1:]:
            new_col = f"{col}_{category}"
            dummy_columns.append(new_col)

            for row in dataset:
                val = row.get(col)
                row[new_col] = 1.0 if val == category else 0.0

        for row in dataset:
            row.pop(col, None)

        new_independents.extend(dummy_columns)

    return dataset, new_independents


def apply_interactions(dataset: List[Dict[str, Any]], interaction_terms: List[List[str]]):

    if not interaction_terms:
        return dataset

    for pair in interaction_terms:

        if not isinstance(pair, list) or len(pair) != 2:
            continue

        var1, var2 = pair
        new_col = f"{var1}_x_{var2}"

        for row in dataset:
            if var1 not in row or var2 not in row:
                row[new_col] = 0.0
                continue

            try:
                row[new_col] = float(row[var1]) * float(row[var2])
            except Exception:
                row[new_col] = 0.0

    return dataset