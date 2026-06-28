"""Analytics page — offline model performance and interpretability."""

import pandas as pd
import streamlit as st

from components.cards import metric_card, page_header
from components.charts import (
    confusion_matrix_figure,
    feature_importance_figure,
    probability_distribution_figure,
    roc_curve_figure,
)
from services.analytics_service import get_evaluation_bundle


def render() -> None:
    page_header(
        "Analytics",
        "Offline evaluation metrics reproduced from the original training split.",
    )

    try:
        bundle = get_evaluation_bundle()
    except FileNotFoundError as error:
        st.error(str(error))
        return

    support = bundle["support"]
    st.caption(
        f"Evaluation set: {support['test_samples']} samples · "
        f"Training set: {support['train_samples']} · "
        f"Total dataset: {support['total_samples']}"
    )

    metrics = st.columns(4)
    metric_values = [
        ("Accuracy", bundle["accuracy"]),
        ("Precision", bundle["precision"]),
        ("Recall", bundle["recall"]),
        ("F1 Score", bundle["f1"]),
    ]

    for column, (label, value) in zip(metrics, metric_values):
        with column:
            metric_card(label, f"{value:.1%}", "Test split · random_state=42")

    st.markdown("")

    top_row_left, top_row_right = st.columns(2, gap="large")
    with top_row_left:
        st.plotly_chart(
            confusion_matrix_figure(bundle["confusion_matrix"]),
            use_container_width=True,
        )
    with top_row_right:
        roc = bundle["roc"]
        st.plotly_chart(
            roc_curve_figure(roc["fpr"], roc["tpr"], roc["auc"]),
            use_container_width=True,
        )

    bottom_row_left, bottom_row_right = st.columns(2, gap="large")
    with bottom_row_left:
        st.plotly_chart(
            feature_importance_figure(bundle["feature_importance"]),
            use_container_width=True,
        )
    with bottom_row_right:
        st.plotly_chart(
            probability_distribution_figure(bundle["y_proba"], bundle["y_test"]),
            use_container_width=True,
        )

    with st.expander("Classification summary"):
        st.markdown(
            f"""
            | Metric | Value |
            |--------|-------|
            | Accuracy | {bundle['accuracy']:.4f} |
            | Precision | {bundle['precision']:.4f} |
            | Recall | {bundle['recall']:.4f} |
            | F1 Score | {bundle['f1']:.4f} |
            | ROC AUC | {bundle['roc']['auc']:.4f} |
            """
        )

        st.markdown("**Confusion matrix (rows = actual, columns = predicted)**")
        cm_df = pd.DataFrame(
            bundle["confusion_matrix"],
            index=["Actual Normal", "Actual Failure"],
            columns=["Pred Normal", "Pred Failure"],
        )
        st.dataframe(cm_df, use_container_width=True)

        st.markdown("**Feature coefficients**")
        st.dataframe(
            bundle["feature_importance"].sort_values("importance", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
