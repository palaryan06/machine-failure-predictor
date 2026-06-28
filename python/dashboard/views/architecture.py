"""System Architecture page — pipeline documentation for interviews."""

import streamlit as st

from components.cards import page_header, tech_chip_row
from config import PROJECT_ROOT


def render() -> None:
    page_header(
        "System Architecture",
        "End-to-end data flow from simulated sensors to dashboard visualization.",
    )

    st.markdown("### Pipeline Overview")
    st.caption("Each stage is independently runnable and maps to a concrete repository component.")

    pipeline = [
        (
            "C++ Sensor Simulation",
            "mqtt_demo.exe reads test_data.csv, buffers six readings into student2.csv, "
            "and publishes the batch as one MQTT payload.",
        ),
        (
            "MQTT Broker",
            "Public Mosquitto broker (test.mosquitto.org) routes messages on topic test/aryan/mqtt.",
        ),
        (
            "Python Subscriber",
            "subscriber.py listens for batches, parses CSV rows, and invokes the evaluate() path.",
        ),
        (
            "Feature Scaling",
            "StandardScaler transforms nine sensor features using training-time statistics.",
        ),
        (
            "Logistic Regression",
            "A serialized classifier predicts failure (1) or normal operation (0) per row.",
        ),
        (
            "Majority Vote",
            "Six row-level predictions are aggregated with mode() into one batch decision.",
        ),
        (
            "Dashboard",
            "The Streamlit Live Monitoring page subscribes to the same MQTT topic, "
            "applies the identical batch inference path, and visualizes health, history, and sensor trends.",
        ),
    ]

    for title, description in pipeline:
        st.markdown(
            f"""
            <div class="pipeline-step">
                <h4>{title}</h4>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if title != "Dashboard":
            st.markdown('<div class="pipeline-arrow">↓</div>', unsafe_allow_html=True)

    st.markdown("")

    diagram_col, detail_col = st.columns([1.1, 0.9], gap="large")

    with diagram_col:
        st.markdown("### Architecture Diagram")
        st.graphviz_chart(
            """
            digraph pipeline {
                graph [rankdir=TB, bgcolor="#0b0f14", fontname="Helvetica", nodesep=0.45];
                node [shape=box, style="rounded,filled", fillcolor="#171f2b",
                      fontcolor="#e8edf4", color="#243041", fontname="Helvetica"];
                edge [color="#2dd4bf", penwidth=1.4];

                csv [label="test_data.csv"];
                cpp [label="C++ Publisher\\nmqtt_c++/main.cpp"];
                broker [label="MQTT Broker\\ntest.mosquitto.org"];
                sub [label="Python Subscriber\\nsubscriber.py"];
                scale [label="StandardScaler"];
                model [label="Logistic Regression"];
                vote [label="Majority Vote"];
                dash [label="Streamlit Dashboard"];

                csv -> cpp -> broker -> sub -> scale -> model -> vote -> dash;
            }
            """
        )

    with detail_col:
        st.markdown("### Repository Mapping")
        mapping = {
            "Publisher source": "mqtt_c++/main.cpp",
            "Training notebook": "python/Machine_failure_predict_model_training.ipynb",
            "Model artifacts": "python/model/failure_model.pkl, scaler.pkl",
            "Live subscriber": "python/mqtt/subscriber.py",
            "Labeled dataset": "mqtt_c++/data/data.csv",
            "Stream replay data": "test_data.csv",
            "Dashboard entry": "python/dashboard/app.py",
        }
        for label, path in mapping.items():
            st.markdown(f"**{label}**  \n`{path}`")

        st.markdown("")
        st.markdown("### Integration Contract")
        st.markdown(
            """
            - **Features:** 9 numeric columns in fixed order (no label in MQTT payload)
            - **Batch size:** 6 rows per MQTT message
            - **Topic:** `test/aryan/mqtt`
            - **Decision rule:** Majority vote across six predictions
            """
        )

        tech_chip_row(["C++17", "Paho MQTT", "Python", "Scikit-learn", "Streamlit"])

    st.markdown("")
    st.code(
        f"Project root: {PROJECT_ROOT}",
        language="text",
    )
