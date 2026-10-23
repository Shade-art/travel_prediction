"""
Interactive Filters Component.
Provides sidebar controls for active dataset engine, date ranges, and catchment area selections.
"""

from typing import Tuple, List
from datetime import date
import streamlit as st
import pandas as pd
import importlib
try:
    from data.mock_data import get_all_areas, get_dataset_metadata
except ImportError:
    import data.mock_data
    importlib.reload(data.mock_data)
    from data.mock_data import get_all_areas, get_dataset_metadata


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[date, date, List[str]]:
    """
    Renders sidebar filters for dataset engine, date range, and pickup area selection.
    Returns:
        start_date (date)
        end_date (date)
        selected_areas (list of str)
    """
    st.sidebar.markdown(
        """
        <div style="margin-bottom: 8px;">
            <span style="font-size: 11px; text-transform: uppercase; font-family: monospace; color: #F59E0B; letter-spacing: 1px; font-weight: 700;">
                Data Source & Scope
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Global Dataset Engine Selector
    current_source = st.session_state.get("dataset_source", "real")
    source_options = [
        "🚕 NYC TLC Real Data (March 2016 • 12.2M Trips)",
        "🎲 Simulated Benchmark (Deterministic Seed 42)"
    ]
    current_index = 0 if current_source == "real" else 1

    selected_source_label = st.sidebar.selectbox(
        "Active Telemetry Engine",
        options=source_options,
        index=current_index,
        help="Switch between genuine 12.2M NYC TLC yellow taxi trips (March 2016) and the deterministic simulation baseline."
    )

    new_source = "real" if "Real Data" in selected_source_label else "mock"
    if new_source != current_source:
        st.session_state["dataset_source"] = new_source
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Observation Filters")

    # Date Range Filter
    min_available_date = df["date_dt"].min()
    max_available_date = df["date_dt"].max()

    date_range = st.sidebar.date_input(
        "Observation Date Window",
        value=(min_available_date, max_available_date),
        min_value=min_available_date,
        max_value=max_available_date,
        help="Select start and end dates to filter analytics observations."
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_available_date, max_available_date

    # Pickup Area Filter
    all_areas = ["All Zones"] + get_all_areas()
    selected_areas = st.sidebar.multiselect(
        "Pickup Catchment Areas",
        options=all_areas,
        default=["All Zones"],
        help="Select one or more catchment zones to isolate telemetry."
    )

    meta = get_dataset_metadata(new_source)
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="font-size: 11px; color: #64748B; line-height: 1.5;">
            <strong style="color: #94A3B8;">{meta['name']}</strong><br>
            • Volume: <span style="font-family: monospace; color: #CBD5E1;">{meta['trip_count_str']}</span><br>
            • Range: <span style="font-family: monospace; color: #CBD5E1;">{meta['observation_window']}</span><br>
            • ML Engine: <span style="font-family: monospace; color: #10B981;">HistGradientBoosting</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return start_date, end_date, selected_areas
