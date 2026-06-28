"""Manual Testing page — optional single-row inference for experiments."""

import streamlit as st

from components.cards import page_header, status_card
from components.charts import live_probability_figure
from config import FEATURE_COLUMNS, FEATURE_LABELS, TRAINING_DATA_PATH
from services.model_service import predict_single


def _default_values() -> dict[str, float]:
    """Use dataset medians as sensible form defaults."""
    if TRAINING_DATA_PATH.exists():
        import pandas as pd

        data = pd.read_csv(TRAINING_DATA_PATH)
        return {col: float(data[col].median()) for col in FEATURE_COLUMNS}

    return {
        "footfall": 50.0,
        "tempMode": 3.0,
        "AQ": 4.0,
        "USS": 3.0,
        "CS": 5.0,
        "VOC": 2.0,
        "RP": 45.0,
        "IP": 4.0,
        "Temperature": 12.0,
    }


def render() -> None:
    page_header(
        "Manual Testing",
        "Experiment with custom sensor values using the same scaler and model artifacts.",
    )

    st.info(
        "This page is for manual experiments only. "
        "Use **Live Monitoring** for the real-time MQTT pipeline."
    )

    defaults = _default_values()

    with st.form("manual_prediction_form", clear_on_submit=False):
        st.markdown("### Sensor Inputs")
        st.caption("All nine features must match the training schema.")

        inputs: dict[str, float] = {}
        columns = st.columns(3)

        for index, feature in enumerate(FEATURE_COLUMNS):
            with columns[index % 3]:
                inputs[feature] = st.number_input(
                    FEATURE_LABELS[feature],
                    min_value=0.0,
                    value=defaults[feature],
                    step=1.0,
                    key=f"manual_input_{feature}",
                )

        submitted = st.form_submit_button("Run Prediction", type="primary", use_container_width=True)

    if submitted:
        result = predict_single(inputs)

        st.markdown("### Results")
        result_left, result_right = st.columns([1, 1.2], gap="large")

        with result_left:
            status_card(result["prediction"], result["confidence"])
            st.markdown("")
            st.metric("Predicted Class", str(result["prediction"]))
            st.metric("Confidence Score", f"{result['confidence']:.1%}")

        with result_right:
            st.plotly_chart(
                live_probability_figure(
                    result["probability_normal"],
                    result["probability_failure"],
                ),
                use_container_width=True,
            )
