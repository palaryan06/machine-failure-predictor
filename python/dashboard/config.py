"""Central configuration and path resolution for the Streamlit dashboard."""

import sys
from pathlib import Path

# Resolve project paths relative to this file (no hardcoded user directories).
DASHBOARD_DIR = Path(__file__).resolve().parent
PYTHON_DIR = DASHBOARD_DIR.parent
PROJECT_ROOT = PYTHON_DIR.parent

if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from inference.config import FEATURE_COLUMNS, MODEL_PATH, SCALER_PATH  # noqa: E402

TRAINING_DATA_PATH = PROJECT_ROOT / "mqtt_c++" / "data" / "data.csv"
STREAM_DATA_PATH = PROJECT_ROOT / "test_data.csv"

FEATURE_LABELS = {
    "footfall": "Footfall (load)",
    "tempMode": "Temperature mode",
    "AQ": "Air quality",
    "USS": "Ultrasonic sensor",
    "CS": "Current sensor",
    "VOC": "VOC level",
    "RP": "Rotational parameter",
    "IP": "Input pressure",
    "Temperature": "System temperature",
}

# MQTT settings — must match mqtt_c++/main.cpp and python/mqtt/subscriber.py.
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "test/aryan/mqtt"
MQTT_CLIENT_ID = "aryan_dashboard_monitor_001"

# Live monitoring limits.
PREDICTION_HISTORY_SIZE = 20
SENSOR_CHART_HISTORY_SIZE = 40

# Industrial chart labels mapped to project sensor columns.
LIVE_CHART_METRICS = {
    "Temperature": "Temperature",
    "Torque": "CS",
    "Air Temperature": "tempMode",
    "Process Temperature": "AQ",
    "Rotational Speed": "RP",
    "Tool Wear": "USS",
}

# Match the training notebook split for consistent offline metrics.
RANDOM_STATE = 42
TEST_SIZE = 0.2

APP_TITLE = "Machine Failure Detection"
APP_TAGLINE = "Real-time predictive maintenance for industrial HVAC systems"
