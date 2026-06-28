"""Industrial monitoring UI components."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from components.cards import metric_card, status_card


def live_indicator(active: bool, label: str = "LIVE") -> None:
    css_class = "live-dot active" if active else "live-dot"
    st.markdown(
        f"""
        <div class="live-indicator">
            <span class="{css_class}"></span>
            <span>{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def health_indicator(label: str, healthy: bool) -> None:
    status = "ok" if healthy else "fail"
    symbol = "✓" if healthy else "✗"
    text = "Online" if healthy else "Offline"
    st.markdown(
        f"""
        <div class="health-row {status}">
            <span class="health-symbol">{symbol}</span>
            <span class="health-label">{label}</span>
            <span class="health-state">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_health_panel(snapshot: dict[str, Any]) -> None:
    st.markdown("### System Health")
    health_indicator("MQTT Connected", snapshot["connected"])
    health_indicator("Model Loaded", snapshot["model_loaded"])
    health_indicator("Scaler Loaded", snapshot["scaler_loaded"])
    health_indicator("Subscriber Running", snapshot["listener_running"] and snapshot["connected"])
    health_indicator("Dashboard Running", True)


def render_kpi_row(snapshot: dict[str, Any]) -> None:
    broker_status = "Connected" if snapshot["connected"] else "Disconnected"
    last_message = snapshot["last_message_at"]
    last_message_text = (
        last_message.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        if last_message
        else "Waiting for data"
    )

    prediction = snapshot["latest_prediction"]
    if prediction is None:
        prediction_text = "—"
        status_hint = "Awaiting first MQTT batch"
    else:
        prediction_text = "Failure" if prediction == 1 else "Healthy"
        confidence = snapshot["latest_confidence"] or 0.0
        status_hint = f"Confidence {confidence:.1%}"

    columns = st.columns(4)
    with columns[0]:
        metric_card("Broker Status", broker_status, "Topic: test/aryan/mqtt")
    with columns[1]:
        metric_card("Last Message", last_message_text, "Auto-updates on new batches")
    with columns[2]:
        metric_card(
            "Current Batch",
            str(snapshot["batch_number"]),
            f"{snapshot['message_count']} messages received",
        )
    with columns[3]:
        metric_card("Latest Prediction", prediction_text, status_hint)


def render_current_status(snapshot: dict[str, Any]) -> None:
    prediction = snapshot["latest_prediction"]
    confidence = snapshot["latest_confidence"]

    if prediction is None:
        st.info("Listening on MQTT. Start the C++ publisher to stream sensor batches.")
        return

    status_card(prediction, confidence or 0.0)


def render_sensor_table(snapshot: dict[str, Any]) -> None:
    rows = snapshot["latest_sensor_rows"]
    if not rows:
        st.caption("No sensor batch received yet.")
        return

    from config import FEATURE_COLUMNS, FEATURE_LABELS

    frame = pd.DataFrame(rows, columns=FEATURE_COLUMNS)
    frame.index = [f"Reading {index + 1}" for index in range(len(frame))]
    frame.columns = [FEATURE_LABELS[column] for column in FEATURE_COLUMNS]
    st.dataframe(frame, use_container_width=True)


def render_history_table(snapshot: dict[str, Any]) -> None:
    history = snapshot["history"]
    if not history:
        st.caption("Prediction history will appear after the first MQTT batch.")
        return

    rows = [
        {
            "Timestamp": record.timestamp.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "Batch": record.batch_number,
            "Status": record.status,
            "Prediction": record.prediction,
            "Confidence": f"{record.confidence:.1%}",
        }
        for record in history
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
