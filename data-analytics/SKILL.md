---
name: data-analytics
description: Deterministic statistical engine for exploratory data analysis, regression modeling, hypothesis testing, correlation analysis, and regression assumption diagnostics. Use this skill when strict schema-bound statistical inference is required without machine learning or stochastic behavior.
license: Apache-2.0
metadata:
  author: data-analytics-skill
  version: "2.1"
---

# Data Analytics Skill (Level 2 Deterministic Statistical Engine)

This skill provides a deterministic statistical computation engine.

All outputs strictly follow:

- schemas/input_schema.json
- schemas/output_schema.json

There is no randomness.
There is no machine learning.
There is no training state.

All results are reproducible.

---

# Supported Analysis Types

## 1) EDA

analysis_type: "eda"

Produces:

- summary_statistics
- correlation_matrix
- missing_analysis
- outlier_analysis (IQR method)

No:

- model_diagnostics
- assumption_tests
- confidence_level

---

## 2) Linear Regression (OLS)

analysis_type: "linear_regression"

Required fields:

- target_variable
- independent_variables
- confidence_level (0.8 – 0.999)

Automatically includes intercept.

Produces:

- coefficients:
  - estimate
  - p_value
  - confidence_interval
- model_metrics:
  - r_squared
  - adjusted_r_squared
  - aic
  - bic
  - rmse
  - residual_variance
- assumption_tests:
  - normality (Shapiro / D’Agostino)
  - Breusch–Pagan
  - VIF
  - Durbin–Watson

Interaction terms are supported.
Dummy encoding is deterministic.
Missing rows for required variables are dropped.

---

## 3) Logistic Regression (Binary)

analysis_type: "logistic_regression"

Required fields:

- target_variable (must be exactly {0,1})
- independent_variables
- confidence_level (0.8 – 0.999)

Produces:

- coefficients:
  - estimate
  - odds_ratio
  - p_value
- model_metrics:
  - aic
  - bic
  - pseudo_r_squared
- model_diagnostics:
  - converged (boolean)

Binary logistic only.
No multi-class support.

---

## 4) Hypothesis Testing

analysis_type: "hypothesis_test"

Required:

- test_type
- group_variable
- confidence_level (0.8 – 0.999)

Supported test_type:

- t_test_independent (exactly 2 groups)
- t_test_paired (even number of numeric observations, ≥4)
- z_test_proportion (binary 0/1)
- chi_square (≥2x2 contingency)
- anova_one_way (≥2 groups)

Produces:

- test_statistic
- p_value
- optional:
  - degrees_of_freedom
  - effect_size

---

## 5) Correlation

analysis_type: "correlation"

Required:

- independent_variables (exactly 2 variables)
- correlation_method:
  - pearson
  - spearman

Produces:

- correlation_coefficient
- p_value

No:

- confidence_level
- diagnostics

---

# Deterministic Guarantees

The engine:

- Uses pseudo-inverse for matrix stability
- Guards division by zero
- Clips probabilities safely
- Masks NaN values
- Uses sorted column ordering
- Produces JSON-serializable output
- Enforces strict schema validation
- Applies no randomness
- Stores no model state

All computations are closed-form or canonical MLE (Newton-Raphson).

---

# Input Contract

Minimum:

{
  "analysis_type": "...",
  "dataset": [...]
}

Dataset must be:

- non-empty array
- array of objects
- values limited to:
  - number
  - string
  - boolean
  - null

Conditional requirements enforced by schema and validation layer.

See:
schemas/input_schema.json

---

# Output Contract

All responses include:

{
  "analysis_type": "...",
  "results": {...},
  "interpretation": {
    "summary": "...",
    "key_findings": []
  }
}

Some analysis types additionally require:

- model_diagnostics
- assumption_tests
- confidence_level

See:
schemas/output_schema.json

---

# Preprocessing Behavior

Before computation:

- Numeric coercion applied to required variables
- Rows missing required variables are removed
- Deterministic dummy encoding (first category reference)
- Interaction terms supported (regression only)
- No stochastic imputation
- No automatic scaling

---

# Assumption Tests (Linear Regression Only)

- Residual normality
- Breusch–Pagan heteroskedasticity test
- Variance Inflation Factor (VIF)
- Durbin–Watson autocorrelation

All NaN-safe and index-safe.

---

# Limitations

Not supported:

- Time series modeling
- Cross-validation
- Regularization
- Multi-class logistic
- Non-linear regression
- Automatic feature selection
- Resampling
- Simulation

This is a deterministic statistical inference engine.

---

# Execution Flow

1. Validate payload (JSON schema + contract checks)
2. Preprocess dataset
3. Route to engine based on analysis_type
4. Compute deterministic statistics
5. Format output
6. Return schema-compliant JSON

---

# Intended Use

Use this skill when:

- You need reproducible statistical inference
- You need regression diagnostics
- You need hypothesis testing
- You require schema-bound structured output
- You must avoid ML black-box systems

Avoid this skill when:

- You need predictive ML optimization
- You need model training workflows
- You need probabilistic simulation
- You need high-dimensional ML

---

# Status

Level 2 Statistical Engine  
Deterministic  
Schema-locked  
Production-ready  
Non-ML