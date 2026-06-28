"""About page — motivation, design decisions, and roadmap."""

import streamlit as st

from components.cards import page_header


def render() -> None:
    page_header(
        "About",
        "Context, engineering decisions, and planned enhancements.",
    )

    motivation, decisions = st.columns(2, gap="large")

    with motivation:
        st.markdown("## Project Motivation")
        st.markdown(
            """
            Industrial HVAC and air-handling systems operate in environments where downtime is
            costly — semiconductor fabs, pharmaceutical clean rooms, and large manufacturing plants
            depend on stable environmental control.

            This project demonstrates how **edge-style sensor data** can be streamed, scored, and
            interpreted in near real time using a lightweight ML stack. The focus is not raw model
            complexity, but **production-shaped architecture**: clear boundaries, reproducible
            artifacts, and an interface suitable for operators and interviewers alike.
            """
        )

        st.markdown("## Target Use Case")
        st.markdown(
            """
            - Predict failure conditions from multi-sensor AHU telemetry
            - Simulate IoT ingestion when hardware is unavailable
            - Present results through both CLI streaming and a visual dashboard
            """
        )

    with decisions:
        st.markdown("## Design Decisions")
        design_points = [
            (
                "Logistic Regression baseline",
                "Interpretable coefficients, fast inference, and stable behavior on tabular sensor data.",
            ),
            (
                "MQTT transport",
                "Industry-standard pub/sub decouples the C++ simulator from Python inference.",
            ),
            (
                "Batch + majority vote",
                "Mirrors six-reading acquisition windows and reduces single-sample noise.",
            ),
            (
                "Shared model artifacts",
                "Dashboard and subscriber load identical scaler/model files — no duplicate training logic.",
            ),
            (
                "Modular Streamlit app",
                "Separate views, services, and components keep the portfolio UI maintainable.",
            ),
        ]
        for title, detail in design_points:
            st.markdown(f"**{title}**  \n{detail}")
            st.markdown("")

    st.markdown("## Future Improvements")
    improvements = [
        "Deploy inference behind a FastAPI service with health checks and versioning.",
        "Replace public Mosquitto with a dedicated broker and TLS authentication.",
        "Integrate live MQTT batches into the dashboard via a background listener.",
        "Add drift monitoring and automated retraining triggers.",
        "Connect real IoT hardware or OPC-UA gateways for field validation.",
        "Extend models with anomaly detection and model explainability (SHAP).",
    ]
    for item in improvements:
        st.markdown(f"- {item}")

    st.markdown("")
    st.markdown("---")
    st.caption(
        "Machine Failure Detection · Predictive maintenance portfolio project · "
        "C++ · MQTT · Python · Scikit-learn · Streamlit"
    )
