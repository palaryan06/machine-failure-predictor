"""Shared path and schema configuration for inference."""

from pathlib import Path

PYTHON_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = PYTHON_DIR.parent

MODEL_PATH = PYTHON_DIR / "model" / "failure_model.pkl"
SCALER_PATH = PYTHON_DIR / "model" / "scaler.pkl"

FEATURE_COLUMNS = [
    "footfall",
    "tempMode",
    "AQ",
    "USS",
    "CS",
    "VOC",
    "RP",
    "IP",
    "Temperature",
]
