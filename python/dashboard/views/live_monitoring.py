"""Live Monitoring page — real-time MQTT visualization."""

from __future__ import annotations

from datetime import timedelta

import streamlit as st

from components.cards import page_header
from components.charts import live_sensor_figure, prediction_timeline_figure
from components.monitoring import (
    live_indicator,
    render_current_status,
    render_health_panel,
    render_history_table,
    render_kpi_row,
    render_sensor_table,
)
from config import LIVE_CHART_METRICS, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from services.mqtt_service import get_monitoring_state, get_state_snapshot


def _render_live_dashboard(snapshot: dict) -> None:
    header_left, header_right = st.columns([3, 1])
    with header_left:
        page_header(
            "Live Monitoring",
            "Real-time machine health visualization from MQTT sensor batches.",
        )
    with header_right:
        live_indicator(snapshot["connected"], "LIVE")

    render_kpi_row(snapshot)

    if snapshot["last_error"]:
        st.warning(snapshot["last_error"])

    status_col, health_col = st.columns([2.2, 1], gap="large")
    with status_col:
        st.markdown("### Current Machine Status")
        render_current_status(snapshot)

        st.markdown("### Current Sensor Batch")
        render_sensor_table(snapshot)

    with health_col:
        render_health_panel(snapshot)
        st.markdown("")
        st.caption(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
        st.caption(f"Topic: {MQTT_TOPIC}")

    st.markdown("### Live Sensor Trends")
    chart_rows = list(LIVE_CHART_METRICS.keys())
    for row_start in range(0, len(chart_rows), 3):
        columns = st.columns(3)
        for column, metric_label in zip(columns, chart_rows[row_start : row_start + 3]):
            with column:
                st.plotly_chart(
                    live_sensor_figure(snapshot["chart_series"], metric_label),
                    use_container_width=True,
                    key=f"sensor_chart_{metric_label}_{snapshot['update_counter']}",
                )

    st.markdown("### Prediction History")
    history_left, history_right = st.columns([1.1, 1], gap="large")
    with history_left:
        render_history_table(snapshot)
    with history_right:
        st.plotly_chart(
            prediction_timeline_figure(snapshot["history"]),
            use_container_width=True,
            key=f"timeline_chart_{snapshot['update_counter']}",
        )


@st.fragment(run_every=timedelta(seconds=1))
def _auto_refresh_panel() -> None:
    get_monitoring_state()
    snapshot = get_state_snapshot()
    _render_live_dashboard(snapshot)


def render() -> None:
    _auto_refresh_panel()
