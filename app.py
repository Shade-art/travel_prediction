"""
Public Transportation Demand Analysis and Passenger Prediction System.
Main Streamlit Application & Routing Entrypoint.
Streamlined for clear, high-impact faculty presentations.
"""

import streamlit as st
import pandas as pd
import importlib
try:
    from data.mock_data import load_dataset, get_dataset_metadata, DATA_DISCLAIMER
except ImportError:
    import data.mock_data
    importlib.reload(data.mock_data)
    from data.mock_data import load_dataset, get_dataset_metadata, DATA_DISCLAIMER
from services.analytics_service import AnalyticsService
from components.metrics import (
    render_honest_note_banner,
    render_kpi_cards
)
from components.charts import (
    create_hourly_trend_chart,
    create_area_distribution_chart
)
from components.filters import render_sidebar_filters

# Global Page Configuration
st.set_page_config(
    page_title="NYC Transit Demand Analysis & Prediction",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared Custom Transit Theme CSS
SHARED_CSS = """
<style>
/* Metric numbers tabular font */
div[data-testid="stMetricValue"] {
    font-family: monospace;
    font-weight: 800;
}
/* Main container spacing - clears top header bar completely */
.block-container {
    padding-top: 5.2rem !important;
    padding-bottom: 3rem;
}
/* Sleek translucent top header navbar */
header[data-testid="stHeader"] {
    background: rgba(11, 15, 25, 0.92) !important;
    backdrop-filter: blur(8px);
}
/* Hide the Streamlit Deploy button to keep the header clean */
.stDeployButton {
    display: none !important;
}
/* Remove Streamlit top decoration stripe */
[data-testid="stDecoration"] {
    display: none !important;
}
/* Page header typography */
.page-header-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #F8FAFC;
    margin-bottom: 2px;
}
.page-header-subtitle {
    font-size: 13px;
    color: #94A3B8;
    margin-bottom: 18px;
}
</style>
"""


def render_overview_page():
    """Renders Page A: Overview Dashboard (Streamlined for faculty presentation)."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)

    # Load centralized mock dataset (cached)
    raw_df = load_dataset()

    # Render sidebar filters
    start_date, end_date, selected_areas = render_sidebar_filters(raw_df)

    # Filter dataset based on user selection
    df = AnalyticsService.filter_data(
        raw_df,
        start_date=start_date,
        end_date=end_date,
        selected_areas=selected_areas
    )

    # Top Title Banner
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(
            """
            <div class="page-header-title">🚕 NYC Taxi Transit Demand Overview</div>
            <div class="page-header-subtitle">
                Executive mobility indicators and spatial-temporal distributions across NYC TLC zones
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_badge:
        meta = get_dataset_metadata()
        badge_bg = "rgba(16, 185, 129, 0.15)" if meta["is_real"] else "rgba(245, 158, 11, 0.15)"
        badge_border = "rgba(16, 185, 129, 0.4)" if meta["is_real"] else "rgba(245, 158, 11, 0.4)"
        badge_color = "#6EE7B7" if meta["is_real"] else "#FDE68A"
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 6px;">
                <span style="
                    background: {badge_bg};
                    border: 1px solid {badge_border};
                    color: {badge_color};
                    padding: 4px 10px;
                    border-radius: 6px;
                    font-size: 11px;
                    font-family: monospace;
                    font-weight: 700;
                ">
                    {meta['badge']}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Domain integrity banner: Taxis vs fixed-route transit
    render_honest_note_banner(compact=True)

    # Check for empty filter results
    if df.empty:
        st.warning("⚠️ No transit records found for the selected date window and zone filters. Please expand your filters in the sidebar.")
        return

    # Compute & render executive KPI metrics (4 clean cards)
    kpis = AnalyticsService.compute_kpis(df)
    render_kpi_cards(kpis)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Visualizations: 2 high-impact charts side-by-side
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        hourly_trend_df = AnalyticsService.get_hourly_trend(df)
        fig_hourly = create_hourly_trend_chart(
            hourly_trend_df,
            title="Hourly Passenger Demand (24-Hour Cycle)"
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

    with col_chart2:
        area_df = AnalyticsService.get_area_distribution(df)
        fig_area = create_area_distribution_chart(
            area_df,
            limit=10
        )
        st.plotly_chart(fig_area, use_container_width=True)

    # Footer disclaimer
    meta = get_dataset_metadata()
    st.markdown("---")
    st.markdown(
        f"<div style='font-size: 11px; color: #64748B; text-align: center;'>{meta['disclaimer']}</div>",
        unsafe_allow_html=True
    )


# Explicit Page Definitions for Clean Multi-Page Navigation
overview_page = st.Page(
    render_overview_page,
    title="Overview Dashboard",
    icon="🚕",
    default=True
)

analytics_page = st.Page(
    "pages/1_Demand_Analytics.py",
    title="Demand Analytics",
    icon="📈"
)

prediction_page = st.Page(
    "pages/2_Demand_Prediction.py",
    title="Demand Prediction",
    icon="🔮"
)

# Initialize st.navigation
pg = st.navigation([overview_page, analytics_page, prediction_page])

# Run active page
pg.run()
