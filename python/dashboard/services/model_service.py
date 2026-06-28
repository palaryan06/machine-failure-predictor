"""Cached access to shared inference artifacts for the dashboard."""

from __future__ import annotations

from typing import Any

import streamlit as st

from config import FEATURE_COLUMNS, MODEL_PATH, SCALER_PATH
from inference.artifacts import load_model as _load_model
from inference.artifacts import load_scaler as _load_scaler
from inference.evaluate import evaluate


@st.cache_resource(show_spinner="Loading trained model...")
def load_scaler() -> Any:
    """Load the fitted StandardScaler used during training."""
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler not found at {SCALER_PATH}. Run the training notebook first."
        )
    return _load_scaler()


@st.cache_resource(show_spinner=False)
def load_model() -> Any:
    """Load the serialized Logistic Regression classifier."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run the training notebook first."
        )
    return _load_model()


def predict_single(features: dict[str, float]) -> dict[str, float | int]:
    """
    Run manual single-row inference through the shared evaluate() implementation.
    """
    row = [[features[column] for column in FEATURE_COLUMNS]]
    result = evaluate(row, load_scaler(), load_model())
    row_probabilities = result["probabilities"][0]

    return {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "probability_normal": float(row_probabilities[0]),
        "probability_failure": float(row_probabilities[1]),
    }
