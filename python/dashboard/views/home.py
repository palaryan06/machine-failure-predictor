"""Home page — portfolio landing and project summary."""

import streamlit as st

from components.cards import metric_card, page_header, tech_chip_row


def render() -> None:
    page_header(
        "Machine Failure Detection",
        "Real-time predictive maintenance platform for industrial HVAC and environmental control systems.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Model", "Logistic Regression", "Scikit-learn classifier")
    with col2:
        metric_card("Transport", "MQTT", "Pub/sub streaming layer")
    with col3:
        metric_card("Simulation", "C++ Publisher", "Batch sensor replay")
    with col4:
        metric_card("Accuracy", "~86.8%", "Held-out test split")

    st.markdown("## Project Overview")
    st.markdown(
        """
        This system monitors simulated air-handling unit (AHU) sensor telemetry and predicts
        failure conditions before they escalate. Because physical hardware is unavailable in
        development, a C++ publisher replays industrial CSV batches over MQTT while a Python
        subscriber performs scaled inference using a trained Logistic Regression model.
        """
    )

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown("## Key Features")
        features = [
            "**Batch streaming pipeline** — C++ publisher emits six sensor readings per MQTT message.",
            "**Identical inference artifacts** — Dashboard and subscriber share the same scaler and model.",
            "**Majority-vote aggregation** — Six per-row predictions collapse into one operational decision.",
            "**Offline analytics** — Precision, recall, ROC, and feature importance for model transparency.",
            "**Portfolio-ready UI** — Streamlit dashboard for demos, interviews, and stakeholder walkthroughs.",
        ]
        for item in features:
            st.markdown(f"- {item}")

    with right:
        st.markdown("## Tech Stack")
        tech_chip_row(
            [
                "C++17",
                "Paho MQTT",
                "Python",
                "Pandas",
                "Scikit-learn",
                "Streamlit",
                "Plotly",
                "Joblib",
            ]
        )

        st.markdown("")
        st.markdown("## End-to-End Workflow")
        workflow = [
            "Train Logistic Regression on labeled HVAC sensor data.",
            "Start the MQTT subscriber for live batch inference.",
            "Run the C++ publisher to simulate sensor transmission.",
            "Scale features, predict each reading, and apply majority vote.",
            "Review outcomes in the terminal or this dashboard.",
        ]
        for index, step in enumerate(workflow, start=1):
            st.markdown(f"{index}. {step}")

    st.info(
        "Use **Live Monitoring** for real-time MQTT batches, **Analytics** for model performance, "
        "and **System Architecture** to explain the full pipeline during interviews."
    )
