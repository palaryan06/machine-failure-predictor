"""Reusable HTML and layout components."""

import streamlit as st


def page_header(title: str, subtitle: str) -> None:
    """Consistent page heading block."""
    st.markdown(
        f"""
        <div class="dashboard-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, hint: str = "") -> None:
    """Render a styled metric card."""
    hint_html = f'<div class="hint">{hint}</div>' if hint else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {hint_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_card(prediction: int, confidence: float) -> None:
    """Render operational status for live inference."""
    is_failure = prediction == 1
    css_class = "failure" if is_failure else "healthy"
    state = "Failure Detected" if is_failure else "Healthy"
    detail = (
        "Immediate inspection recommended."
        if is_failure
        else "System operating within expected parameters."
    )

    st.markdown(
        f"""
        <div class="status-card {css_class}">
            <div class="title">Operational Status</div>
            <div class="state">{state}</div>
            <div class="hint">Confidence: {confidence:.1%} · {detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tech_chip_row(items: list[str]) -> None:
    """Render technology badges."""
    chips = "".join(f'<span class="chip">{item}</span>' for item in items)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)
