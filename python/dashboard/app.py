"""
Machine Failure Detection — Streamlit dashboard entry point.

Run from the project root:
    streamlit run python/dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure dashboard modules resolve when Streamlit executes this file directly.
DASHBOARD_DIR = Path(__file__).resolve().parent
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import streamlit as st

from config import APP_TAGLINE, APP_TITLE
from styles import inject_theme
from views import about, analytics, architecture, home, live_monitoring, manual_testing


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

pages = [
    st.Page(live_monitoring.render, title="Live Monitoring", icon="📡", default=True, url_path="live-monitoring"),
    st.Page(manual_testing.render, title="Manual Testing", icon="🧪", url_path="manual-testing"),
    st.Page(home.render, title="Home", icon="🏠", url_path="home"),
    st.Page(analytics.render, title="Analytics", icon="📊", url_path="analytics"),
    st.Page(architecture.render, title="System Architecture", icon="🧩", url_path="architecture"),
    st.Page(about.render, title="About", icon="ℹ️", url_path="about"),
]

with st.sidebar:
    st.markdown(f"## {APP_TITLE}")
    st.caption(APP_TAGLINE)
    st.divider()

navigation = st.navigation(pages, position="sidebar")
navigation.run()

with st.sidebar:
    st.divider()
    st.caption("MQTT listener starts automatically on Live Monitoring.")
