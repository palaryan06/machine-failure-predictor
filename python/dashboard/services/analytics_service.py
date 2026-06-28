"""Offline evaluation metrics computed from the original training dataset."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

from config import FEATURE_COLUMNS, RANDOM_STATE, TEST_SIZE, TRAINING_DATA_PATH
from services.model_service import load_model, load_scaler


@st.cache_data(show_spinner="Computing model analytics...")
def get_evaluation_bundle() -> dict[str, Any]:
    """
    Reproduce the notebook train/test split and derive dashboard metrics.

    Split parameters match Machine_failure_predict_model_training.ipynb exactly.
    """
    if not TRAINING_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training data not found at {TRAINING_DATA_PATH}."
        )

    data = pd.read_csv(TRAINING_DATA_PATH)
    features = data[FEATURE_COLUMNS]
    labels = data["fail"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    scaler = load_scaler()
    model = load_model()

    x_test_scaled = scaler.transform(x_test)
    y_pred = model.predict(x_test_scaled)
    y_proba = model.predict_proba(x_test_scaled)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)

    coefficients = model.coef_[0]
    importance = np.abs(coefficients)
    importance = importance / importance.sum()

    return {
        "x_test": x_test,
        "y_test": y_test.to_numpy(),
        "y_pred": y_pred,
        "y_proba": y_proba,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "confusion_matrix": cm,
        "roc": {
            "fpr": fpr,
            "tpr": tpr,
            "thresholds": thresholds,
            "auc": auc(fpr, tpr),
        },
        "feature_importance": pd.DataFrame(
            {
                "feature": FEATURE_COLUMNS,
                "importance": importance,
                "coefficient": coefficients,
            }
        ).sort_values("importance", ascending=True),
        "support": {
            "train_samples": len(x_train),
            "test_samples": len(x_test),
            "total_samples": len(data),
        },
    }
