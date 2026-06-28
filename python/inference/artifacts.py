"""Load serialized model artifacts using relative project paths."""

from __future__ import annotations

from typing import Any

import joblib

from inference.config import MODEL_PATH, SCALER_PATH


def load_scaler() -> Any:
    """Load the fitted StandardScaler."""
    return joblib.load(SCALER_PATH)


def load_model() -> Any:
    """Load the serialized Logistic Regression classifier."""
    return joblib.load(MODEL_PATH)
