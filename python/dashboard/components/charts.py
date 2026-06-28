"""Plotly chart builders with a shared dark theme."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#e8edf4", "family": "IBM Plex Sans, sans-serif"},
        "xaxis": {
            "gridcolor": "#243041",
            "zerolinecolor": "#243041",
            "linecolor": "#243041",
        },
        "yaxis": {
            "gridcolor": "#243041",
            "zerolinecolor": "#243041",
            "linecolor": "#243041",
        },
        "legend": {"bgcolor": "rgba(0,0,0,0)"},
        "margin": {"l": 24, "r": 24, "t": 48, "b": 24},
    }
}


def _theme_layout(**overrides: Any) -> dict[str, Any]:
    """Merge shared dark-theme layout settings with per-chart overrides."""
    layout = {**PLOTLY_TEMPLATE["layout"], **overrides}
    for axis in ("xaxis", "yaxis"):
        base = PLOTLY_TEMPLATE["layout"].get(axis, {})
        extra = overrides.get(axis, {})
        if extra:
            layout[axis] = {**base, **extra}
    return layout


def confusion_matrix_figure(matrix: np.ndarray) -> go.Figure:
    """Interactive confusion matrix heatmap."""
    labels = ["Normal (0)", "Failure (1)"]
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=labels,
            y=labels,
            text=matrix,
            texttemplate="%{text}",
            colorscale=[[0, "#171f2b"], [0.5, "#2dd4bf"], [1, "#ef4444"]],
            showscale=False,
        )
    )
    fig.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted label",
        yaxis_title="Actual label",
        **PLOTLY_TEMPLATE["layout"],
    )
    return fig


def roc_curve_figure(fpr: np.ndarray, tpr: np.ndarray, roc_auc: float) -> go.Figure:
    """ROC curve with diagonal reference."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"ROC (AUC = {roc_auc:.3f})",
            line={"color": "#2dd4bf", "width": 3},
            fill="tozeroy",
            fillcolor="rgba(45, 212, 191, 0.12)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random baseline",
            line={"color": "#9aa7b8", "dash": "dash"},
        )
    )
    fig.update_layout(
        title="ROC Curve",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        **PLOTLY_TEMPLATE["layout"],
    )
    return fig


def feature_importance_figure(importance_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of normalized coefficient magnitudes."""
    fig = px.bar(
        importance_df,
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale=["#243041", "#2dd4bf"],
    )
    fig.update_layout(
        title="Feature Importance (|coefficient| normalized)",
        xaxis_title="Relative importance",
        yaxis_title="",
        coloraxis_showscale=False,
        **PLOTLY_TEMPLATE["layout"],
    )
    return fig


def probability_distribution_figure(y_proba: np.ndarray, y_test: np.ndarray) -> go.Figure:
    """Histogram of predicted failure probabilities by actual class."""
    frame = pd.DataFrame(
        {
            "failure_probability": y_proba,
            "actual_label": np.where(y_test == 1, "Failure", "Normal"),
        }
    )
    fig = px.histogram(
        frame,
        x="failure_probability",
        color="actual_label",
        nbins=20,
        barmode="overlay",
        opacity=0.75,
        color_discrete_map={"Normal": "#22c55e", "Failure": "#ef4444"},
    )
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text="Decision threshold (0.5)",
        annotation_position="top right",
    )
    fig.update_layout(
        title="Prediction Probability Distribution (Test Set)",
        xaxis_title="Predicted probability of failure",
        yaxis_title="Count",
        **PLOTLY_TEMPLATE["layout"],
    )
    return fig


def live_probability_figure(
    probability_normal: float,
    probability_failure: float,
) -> go.Figure:
    """Bar chart for a single live inference result."""
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Normal", "Failure"],
                y=[probability_normal, probability_failure],
                marker_color=["#22c55e", "#ef4444"],
                text=[f"{probability_normal:.1%}", f"{probability_failure:.1%}"],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        title="Class Probabilities",
        yaxis_title="Probability",
        **_theme_layout(yaxis={"range": [0, 1.05]}),
    )
    return fig


def prediction_timeline_figure(history: list[Any]) -> go.Figure:
    """Timeline of recent batch predictions."""
    if not history:
        fig = go.Figure()
        fig.update_layout(
            title="Prediction Timeline",
            annotations=[
                {
                    "text": "Waiting for MQTT batches...",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"color": "#9aa7b8", "size": 14},
                }
            ],
            **PLOTLY_TEMPLATE["layout"],
        )
        return fig

    frame = pd.DataFrame(
        [
            {
                "timestamp": record.timestamp,
                "batch_number": record.batch_number,
                "prediction": record.prediction,
                "confidence": record.confidence,
                "status": record.status,
            }
            for record in reversed(history)
        ]
    )

    colors = frame["status"].map({"Healthy": "#22c55e", "Failure": "#ef4444"})
    fig = go.Figure(
        data=[
            go.Scatter(
                x=frame["timestamp"],
                y=frame["prediction"],
                mode="lines+markers",
                marker={
                    "size": 10 + frame["confidence"] * 12,
                    "color": colors,
                    "line": {"width": 1, "color": "#e8edf4"},
                },
                line={"color": "#2dd4bf", "width": 2},
                text=frame["status"],
                hovertemplate=(
                    "Batch %{customdata[0]}<br>"
                    "Status: %{text}<br>"
                    "Confidence: %{customdata[1]:.1%}<br>"
                    "Time: %{x}<extra></extra>"
                ),
                customdata=frame[["batch_number", "confidence"]].values,
            )
        ]
    )
    fig.update_layout(
        title="Prediction Timeline (Last 20 Batches)",
        xaxis_title="Timestamp (UTC)",
        yaxis_title="Prediction Class",
        **_theme_layout(
            yaxis={"tickmode": "array", "tickvals": [0, 1], "ticktext": ["Healthy", "Failure"]}
        ),
    )
    return fig


def live_sensor_figure(chart_series: list[dict[str, Any]], metric_label: str) -> go.Figure:
    """Single live sensor trend chart."""
    if not chart_series or metric_label not in chart_series[0]:
        fig = go.Figure()
        fig.update_layout(
            title=metric_label,
            annotations=[
                {
                    "text": "No data",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"color": "#9aa7b8", "size": 12},
                }
            ],
            **_theme_layout(),
        )
        return fig

    frame = pd.DataFrame(chart_series)
    fig = go.Figure(
        data=[
            go.Scatter(
                x=frame["batch_number"],
                y=frame[metric_label],
                mode="lines+markers",
                line={"color": "#2dd4bf", "width": 2},
                marker={"size": 6},
                name=metric_label,
            )
        ]
    )
    fig.update_layout(
        title=metric_label,
        xaxis_title="Batch",
        yaxis_title="Sensor value",
        **_theme_layout(),
    )
    return fig
