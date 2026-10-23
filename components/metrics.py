"""
UI Metric Cards and Banner Components for Streamlit.
Provides HTML/CSS styling for transit KPI indicators and disclaimer alerts.
All HTML is stripped of leading indentation and blank lines to prevent
CommonMark markdown parsers from misinterpreting indented HTML as code blocks.
"""

from typing import Dict, Any, List
import textwrap
import streamlit as st


def render_honest_note_banner(compact: bool = False):
    """
    Renders the domain integrity callout explaining that taxis operate
    point-to-point without fixed transit routes.
    """
    pad = "12px" if compact else "16px"
    banner_html = textwrap.dedent(f"""
<div style="background: rgba(17, 24, 39, 0.85); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 10px; padding: {pad}; margin-bottom: 20px; display: flex; align-items: flex-start; gap: 12px;">
<div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 6px; padding: 6px 10px; font-size: 16px; color: #F59E0B;">📍</div>
<div style="font-size: 12.5px; line-height: 1.5; color: #CBD5E1;">
<strong style="color: #FDE68A; display: block; margin-bottom: 2px;">Transit Domain Integrity Note: Catchment Zone vs Fixed Route Analysis</strong>
Unlike fixed-guideway subways or scheduled municipal bus corridors, NYC Yellow and Green taxis operate as dynamic point-to-point vehicles without fixed routes. Demand analysis is therefore formulated honestly around <strong>Pickup Catchment Zones</strong> rather than artificial route lines.
</div>
</div>
""").strip()
    st.markdown(banner_html, unsafe_allow_html=True)


def render_mock_disclaimer_banner(is_real: bool = False):
    """
    Renders status banner indicating active prediction engine (Scikit-Learn vs Simulation).
    """
    if is_real:
        disclaimer_html = textwrap.dedent("""
<div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; border-radius: 6px; padding: 10px 14px; margin-bottom: 20px; font-size: 12px; color: #CBD5E1;">
<strong style="color: #10B981; text-transform: uppercase; letter-spacing: 0.5px;">Production ML Engine Active:</strong>
Scikit-Learn Pipeline (<strong>HistGradientBoostingRegressor</strong>, Test R² = 0.9818) fitted on 12,210,952 genuine NYC TLC yellow taxi trip records from March 2016.
</div>
""").strip()
    else:
        disclaimer_html = textwrap.dedent("""
<div style="background: rgba(30, 41, 59, 0.7); border-left: 4px solid #F59E0B; border-radius: 6px; padding: 10px 14px; margin-bottom: 20px; font-size: 12px; color: #94A3B8;">
<strong style="color: #F59E0B; text-transform: uppercase; letter-spacing: 0.5px;">Phase 1 Benchmark Simulation:</strong>
All passenger volumes and forecasts are heuristic estimates generated deterministically from baseline distributions. Toggle the Active Telemetry Engine in the sidebar to switch to genuine 12.2M NYC TLC records.
</div>
""").strip()
    st.markdown(disclaimer_html, unsafe_allow_html=True)


def render_kpi_cards(kpis: Dict[str, Any]):
    """
    Renders the 4 executive KPI metric cards for Page A (Overview Dashboard):
    1. Total Pickups
    2. Average Hourly Pickups
    3. Peak Demand Hour
    4. Busiest Pickup Area
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        c1 = textwrap.dedent(f"""
<div style="background: #111827; border: 1px solid #1F293D; border-radius: 10px; padding: 16px; min-height: 125px;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Total Pickups</div>
<div style="color: #FFFFFF; font-size: 26px; font-weight: 800; font-family: monospace; margin: 6px 0;">{kpis['total_pickups']:,}</div>
<div style="color: #64748B; font-size: 11px;">Across {kpis['total_zones']} NYC zones</div>
</div>
""").strip()
        st.markdown(c1, unsafe_allow_html=True)

    with col2:
        c2 = textwrap.dedent(f"""
<div style="background: #111827; border: 1px solid #1F293D; border-radius: 10px; padding: 16px; min-height: 125px;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Avg Hourly Demand</div>
<div style="color: #38BDF8; font-size: 26px; font-weight: 800; font-family: monospace; margin: 6px 0;">{kpis['avg_hourly_demand']:,}</div>
<div style="color: #64748B; font-size: 11px;">Trips / hour citywide</div>
</div>
""").strip()
        st.markdown(c2, unsafe_allow_html=True)

    with col3:
        c3 = textwrap.dedent(f"""
<div style="background: #111827; border: 1px solid #1F293D; border-radius: 10px; padding: 16px; min-height: 125px;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Peak Demand Hour</div>
<div style="color: #F59E0B; font-size: 22px; font-weight: 800; font-family: monospace; margin: 8px 0 6px 0;">{kpis['peak_hour_formatted']}</div>
<div style="color: #64748B; font-size: 11px;">{kpis['peak_hour_volume']:,} trips during rush</div>
</div>
""").strip()
        st.markdown(c3, unsafe_allow_html=True)

    with col4:
        c4 = textwrap.dedent(f"""
<div style="background: #111827; border: 1px solid #1F293D; border-radius: 10px; padding: 16px; min-height: 125px;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Busiest Pickup Area</div>
<div style="color: #A855F7; font-size: 18px; font-weight: 800; margin: 8px 0 6px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{kpis['busiest_area']}">{kpis['busiest_area']}</div>
<div style="color: #64748B; font-size: 11px;">{kpis['busiest_area_percentage']}% share ({kpis['busiest_borough']})</div>
</div>
""").strip()
        st.markdown(c4, unsafe_allow_html=True)


def render_prediction_result(res: Dict[str, Any]):
    """
    Renders the simulated prediction output card with volume, comparison vs average,
    and simulation factors. Formatted without leading whitespace to prevent
    markdown code-block syntax triggers.
    """
    is_positive = res["difference_percentage"] >= 0
    delta_color = "#10B981" if is_positive else "#F43F5E"
    delta_symbol = "+" if is_positive else ""
    delta_bg = "rgba(16, 185, 129, 0.15)" if is_positive else "rgba(244, 63, 94, 0.15)"

    demand_badges = {
        "Peak Surge": ("#F59E0B", "rgba(245, 158, 11, 0.15)"),
        "High": ("#38BDF8", "rgba(56, 189, 248, 0.15)"),
        "Moderate": ("#10B981", "rgba(16, 185, 129, 0.15)"),
        "Low": ("#94A3B8", "rgba(148, 163, 184, 0.15)"),
    }
    badge_fg, badge_bg = demand_badges.get(res["demand_level"], ("#F59E0B", "rgba(245, 158, 11, 0.15)"))

    drivers_html = "".join([
        f'<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #1E293D; border-radius: 6px; padding: 8px 10px; font-size: 12px; color: #CBD5E1;">✔ {d}</div>'
        for d in res["key_drivers"]
    ])

    is_mock = res.get("is_mock", True)
    forecast_title = "Simulated Demand Forecast" if is_mock else "Scikit-Learn Model Forecast"
    drivers_heading = "Simulation Model Factors & Drivers:" if is_mock else "Decision Tree Split Indicators & Environmental Signals:"
    model_tag = f"• {res.get('model_name', 'HistGradientBoosting')}" if not is_mock else "• Phase 1 Simulation"

    card_html = textwrap.dedent(f"""
<div style="background: #111827; border: 1px solid #1F293D; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="background: {badge_bg}; color: {badge_fg}; border: 1px solid {badge_fg}40; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; font-family: monospace;">{res['demand_level']}</span>
<span style="color: #94A3B8; font-size: 12px; font-family: monospace;">Confidence: {int(res['confidence_score'] * 100)}% {model_tag}</span>
</div>
<div style="color: #64748B; font-size: 11px; font-family: monospace;">{res['date']} ({res['day_name']}) • {res['formatted_hour']}</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 16px; padding-bottom: 16px; border-bottom: 1px solid #1F293D;">
<div>
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-family: monospace;">{forecast_title}</div>
<div style="color: #F59E0B; font-size: 38px; font-weight: 900; font-family: monospace; line-height: 1.1; margin-top: 4px;">{res['predicted_pickups']:,} <span style="font-size: 13px; color: #94A3B8; font-weight: 400;">pickups/hr</span></div>
<div style="color: #CBD5E1; font-size: 13px; margin-top: 2px;">📍 <strong>{res['pickup_area']}</strong> ({res['borough']} • {res['zone_type']})</div>
</div>
<div style="text-align: right;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-family: monospace;">vs Historical Baseline ({res['historical_average']:,})</div>
<div style="display: inline-block; background: {delta_bg}; color: {delta_color}; border: 1px solid {delta_color}50; padding: 4px 12px; border-radius: 6px; font-size: 16px; font-weight: 800; font-family: monospace; margin-top: 6px;">{delta_symbol}{res['difference_percentage']}%</div>
</div>
</div>
<div style="margin-top: 14px;">
<div style="color: #94A3B8; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 8px;">{drivers_heading}</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 8px;">{drivers_html}</div>
</div>
</div>
""").strip()

    st.markdown(card_html, unsafe_allow_html=True)
