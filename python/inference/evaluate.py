"""
Canonical batch inference used by subscriber.py and the dashboard.

Logic is extracted from python/mqtt/subscriber.py without changing behavior.
"""

from __future__ import annotations

from statistics import mode
from typing import Any

import numpy as np
import pandas as pd

from inference.config import FEATURE_COLUMNS


def evaluate(data: list[list[float]], scaler: Any, model: Any) -> dict[str, Any]:
    """
    Scale sensor rows, predict each reading, and aggregate with majority vote.

    Returns the final prediction plus optional metadata for visualization layers.
    """
    frame = pd.DataFrame(
        data,
        columns=["footfall", "tempMode", "AQ", "USS", "CS", "VOC", "RP", "IP", "Temperature"],
    )
    scaled = scaler.transform(frame)
    prediction = model.predict(scaled)
    probability = model.predict_proba(scaled)

    final_prediction = np.mean(prediction, axis=0)
    final_prediction = int(mode(prediction))

    class_probabilities = probability.mean(axis=0)
    confidence = float(class_probabilities[final_prediction])
    snapshot = frame.mean(numeric_only=True)

    return {
        "final_prediction": final_prediction,
        "prediction": final_prediction,
        "confidence": confidence,
        "row_predictions": prediction.tolist(),
        "probabilities": probability.tolist(),
        "sensor_snapshot": {column: float(snapshot[column]) for column in FEATURE_COLUMNS},
        "sensor_rows": frame.values.tolist(),
    }
