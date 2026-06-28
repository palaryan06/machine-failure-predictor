"""Dark industrial theme injected once at application startup."""

import streamlit as st


def inject_theme() -> None:
    """Apply global CSS overrides for a production-inspired dark UI."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

            :root {
                --bg-primary: #0b0f14;
                --bg-secondary: #121821;
                --bg-elevated: #171f2b;
                --border-subtle: #243041;
                --text-primary: #e8edf4;
                --text-muted: #9aa7b8;
                --accent: #2dd4bf;
                --accent-soft: rgba(45, 212, 191, 0.12);
                --success: #22c55e;
                --danger: #ef4444;
                --warning: #f59e0b;
            }

            html, body, [class*="css"] {
                font-family: 'IBM Plex Sans', sans-serif;
            }

            .stApp {
                background: linear-gradient(180deg, var(--bg-primary) 0%, #0d1219 100%);
                color: var(--text-primary);
            }

            [data-testid="stSidebar"] {
                background: var(--bg-secondary);
                border-right: 1px solid var(--border-subtle);
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] label {
                color: var(--text-muted);
            }

            h1, h2, h3, h4 {
                color: var(--text-primary) !important;
                letter-spacing: -0.02em;
            }

            .dashboard-hero {
                background: linear-gradient(135deg, rgba(45, 212, 191, 0.08), rgba(23, 31, 43, 0.9));
                border: 1px solid var(--border-subtle);
                border-radius: 16px;
                padding: 1.75rem 2rem;
                margin-bottom: 1.5rem;
            }

            .dashboard-hero h1 {
                font-size: 2rem;
                margin-bottom: 0.35rem;
            }

            .dashboard-hero p {
                color: var(--text-muted);
                margin: 0;
                font-size: 1.05rem;
            }

            .metric-card {
                background: var(--bg-elevated);
                border: 1px solid var(--border-subtle);
                border-radius: 14px;
                padding: 1.1rem 1.25rem;
                min-height: 110px;
            }

            .metric-card .label {
                color: var(--text-muted);
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.35rem;
            }

            .metric-card .value {
                color: var(--text-primary);
                font-size: 1.75rem;
                font-weight: 700;
                line-height: 1.2;
            }

            .metric-card .hint {
                color: var(--text-muted);
                font-size: 0.85rem;
                margin-top: 0.35rem;
            }

            .status-card {
                border-radius: 16px;
                padding: 1.5rem;
                border: 1px solid var(--border-subtle);
                background: var(--bg-elevated);
            }

            .status-card.healthy {
                border-color: rgba(34, 197, 94, 0.45);
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.08), var(--bg-elevated));
            }

            .status-card.failure {
                border-color: rgba(239, 68, 68, 0.45);
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), var(--bg-elevated));
            }

            .status-card .title {
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-muted);
            }

            .status-card .state {
                font-size: 2rem;
                font-weight: 700;
                margin: 0.35rem 0;
            }

            .status-card.healthy .state { color: var(--success); }
            .status-card.failure .state { color: var(--danger); }

            .pipeline-step {
                background: var(--bg-elevated);
                border: 1px solid var(--border-subtle);
                border-left: 3px solid var(--accent);
                border-radius: 12px;
                padding: 1rem 1.15rem;
                margin-bottom: 0.65rem;
            }

            .pipeline-step h4 {
                margin: 0 0 0.25rem 0;
                font-size: 1rem;
            }

            .pipeline-step p {
                margin: 0;
                color: var(--text-muted);
                font-size: 0.92rem;
            }

            .pipeline-arrow {
                text-align: center;
                color: var(--accent);
                font-size: 1.25rem;
                margin: 0.15rem 0;
            }

            .section-caption {
                color: var(--text-muted);
                font-size: 0.95rem;
                margin-bottom: 1rem;
            }

            .chip-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 0.75rem;
            }

            .chip {
                background: var(--accent-soft);
                color: var(--accent);
                border: 1px solid rgba(45, 212, 191, 0.25);
                border-radius: 999px;
                padding: 0.35rem 0.75rem;
                font-size: 0.82rem;
                font-weight: 500;
            }

            div[data-testid="stMetric"] {
                background: var(--bg-elevated);
                border: 1px solid var(--border-subtle);
                border-radius: 14px;
                padding: 0.85rem 1rem;
            }

            div[data-testid="stExpander"] {
                background: var(--bg-elevated);
                border: 1px solid var(--border-subtle);
                border-radius: 12px;
            }

            .live-indicator {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(239, 68, 68, 0.12);
                border: 1px solid rgba(239, 68, 68, 0.35);
                color: #fca5a5;
                border-radius: 999px;
                padding: 0.35rem 0.8rem;
                font-size: 0.82rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                margin-bottom: 1rem;
            }

            .live-dot {
                width: 0.55rem;
                height: 0.55rem;
                border-radius: 50%;
                background: #64748b;
                display: inline-block;
            }

            .live-dot.active {
                background: #ef4444;
                box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.18);
            }

            .health-row {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                padding: 0.7rem 0.85rem;
                border-radius: 10px;
                border: 1px solid var(--border-subtle);
                background: var(--bg-elevated);
                margin-bottom: 0.55rem;
            }

            .health-row.ok {
                border-color: rgba(34, 197, 94, 0.35);
            }

            .health-row.fail {
                border-color: rgba(239, 68, 68, 0.35);
            }

            .health-symbol {
                font-weight: 700;
                width: 1rem;
            }

            .health-row.ok .health-symbol,
            .health-row.ok .health-state {
                color: var(--success);
            }

            .health-row.fail .health-symbol,
            .health-row.fail .health-state {
                color: var(--danger);
            }

            .health-label {
                flex: 1;
                color: var(--text-primary);
            }

            .health-state {
                font-size: 0.85rem;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
