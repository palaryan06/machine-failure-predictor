"""Background MQTT listener and thread-safe monitoring state."""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import paho.mqtt.client as mqtt
import streamlit as st

from config import (
    LIVE_CHART_METRICS,
    MQTT_BROKER,
    MQTT_CLIENT_ID,
    MQTT_PORT,
    MQTT_TOPIC,
    PREDICTION_HISTORY_SIZE,
    SENSOR_CHART_HISTORY_SIZE,
)
from inference.evaluate import evaluate
from inference.payload import parse_mqtt_payload
from services.model_service import load_model, load_scaler


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class PredictionRecord:
    timestamp: datetime
    batch_number: int
    prediction: int
    confidence: float
    status: str


@dataclass
class MonitoringState:
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    connected: bool = False
    listener_running: bool = False
    model_loaded: bool = False
    scaler_loaded: bool = False
    last_message_at: datetime | None = None
    batch_number: int = 0
    message_count: int = 0
    update_counter: int = 0
    latest_prediction: int | None = None
    latest_confidence: float | None = None
    latest_sensor_snapshot: dict[str, float] = field(default_factory=dict)
    latest_sensor_rows: list[list[float]] = field(default_factory=list)
    last_error: str | None = None
    history: deque[PredictionRecord] = field(
        default_factory=lambda: deque(maxlen=PREDICTION_HISTORY_SIZE)
    )
    chart_series: deque[dict[str, Any]] = field(
        default_factory=lambda: deque(maxlen=SENSOR_CHART_HISTORY_SIZE)
    )


def _handle_message(state: MonitoringState, payload_str: str) -> None:
    rows = parse_mqtt_payload(payload_str)
    if not rows:
        return

    result = evaluate(rows, load_scaler(), load_model())
    timestamp = _utc_now()

    chart_point: dict[str, Any] = {
        "timestamp": timestamp,
        "batch_number": state.batch_number + 1,
    }
    for label, column in LIVE_CHART_METRICS.items():
        chart_point[label] = result["sensor_snapshot"][column]

    record = PredictionRecord(
        timestamp=timestamp,
        batch_number=state.batch_number + 1,
        prediction=result["prediction"],
        confidence=result["confidence"],
        status="Failure" if result["prediction"] == 1 else "Healthy",
    )

    with state.lock:
        state.batch_number += 1
        state.message_count += 1
        state.last_message_at = timestamp
        state.latest_prediction = result["prediction"]
        state.latest_confidence = result["confidence"]
        state.latest_sensor_snapshot = result["sensor_snapshot"]
        state.latest_sensor_rows = result["sensor_rows"]
        state.history.appendleft(record)
        state.chart_series.append(chart_point)
        state.update_counter += 1
        state.last_error = None


class _DashboardMQTTClient:
    """Owns the MQTT client loop and writes into shared monitoring state."""

    def __init__(self, state: MonitoringState) -> None:
        self.state = state
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def start(self) -> None:
        self._preload_artifacts()
        self.client.connect_async(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()
        with self.state.lock:
            self.state.listener_running = True

    def _preload_artifacts(self) -> None:
        try:
            load_model()
            with self.state.lock:
                self.state.model_loaded = True
        except FileNotFoundError as error:
            with self.state.lock:
                self.state.model_loaded = False
                self.state.last_error = str(error)

        try:
            load_scaler()
            with self.state.lock:
                self.state.scaler_loaded = True
        except FileNotFoundError as error:
            with self.state.lock:
                self.state.scaler_loaded = False
                self.state.last_error = str(error)

    def _on_connect(self, client, userdata, flags, rc) -> None:
        with self.state.lock:
            self.state.connected = rc == 0
            if rc != 0:
                self.state.last_error = f"MQTT connect failed with code {rc}"
                return
        client.subscribe(MQTT_TOPIC)

    def _on_disconnect(self, client, userdata, rc) -> None:
        with self.state.lock:
            self.state.connected = False
            if rc != 0:
                self.state.last_error = f"MQTT disconnected with code {rc}"

    def _on_message(self, client, userdata, msg) -> None:
        payload_str = msg.payload.decode("utf-8", errors="replace")
        if not payload_str.strip():
            return

        try:
            _handle_message(self.state, payload_str)
        except Exception as error:  # noqa: BLE001 - surface parsing/inference issues in UI
            with self.state.lock:
                self.state.last_error = str(error)


@st.cache_resource(show_spinner=False)
def get_monitoring_state() -> MonitoringState:
    """Create one MQTT listener per Streamlit server process."""
    state = MonitoringState()
    listener = _DashboardMQTTClient(state)
    listener.start()
    return state


def get_state_snapshot() -> dict[str, Any]:
    """Return a thread-safe copy for UI rendering."""
    state = get_monitoring_state()
    with state.lock:
        return {
            "connected": state.connected,
            "listener_running": state.listener_running,
            "model_loaded": state.model_loaded,
            "scaler_loaded": state.scaler_loaded,
            "last_message_at": state.last_message_at,
            "batch_number": state.batch_number,
            "message_count": state.message_count,
            "update_counter": state.update_counter,
            "latest_prediction": state.latest_prediction,
            "latest_confidence": state.latest_confidence,
            "latest_sensor_snapshot": dict(state.latest_sensor_snapshot),
            "latest_sensor_rows": list(state.latest_sensor_rows),
            "last_error": state.last_error,
            "history": list(state.history),
            "chart_series": list(state.chart_series),
        }
