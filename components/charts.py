"""
Plotly Chart Generators for NYC Transit Telemetry Dashboard.
Provides consistent styling with high-contrast transit dark theme:
Slate background, Taxi Amber (#F59E0B), Cyan (#38BDF8), Emerald (#10B981).
"""

from typing import List
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Styling constants
CHART_BG = "rgba(17, 24, 39, 0.75)"  # Dark slate #111827
GRID_COLOR = "#1F293D"
TEXT_COLOR = "#94A3B8"
ACCENT_AMBER = "#F59E0B"
ACCENT_BLUE = "#38BDF8"
ACCENT_PURPLE = "#A855F7"
ACCENT_EMERALD = "#10B981"


def apply_transit_theme(fig: go.Figure, height: int = 360) -> go.Figure:
    """Applies unified dark transportation styling to a Plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CHART_BG,
        font=dict(color=TEXT_COLOR, family="sans-serif", size=12),
        margin=dict(l=45, r=20, t=50, b=55),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#E2E8F0"),
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR, size=11),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR, size=11),
        ),
    )
    return fig


def create_hourly_trend_chart(hourly_df: pd.DataFrame, title: str = "24-Hour Passenger Demand Trend") -> go.Figure:
    """Creates a 24-hour hourly demand curve with optional weekday/weekend breakdown."""
    fig = go.Figure()

    if hourly_df.empty:
        return apply_transit_theme(fig)

    # Main aggregate hourly volume line with gradient area
    fig.add_trace(
        go.Scatter(
            x=hourly_df["formatted_hour"],
            y=hourly_df["avg_pickups"],
            name="Average Hourly Demand",
            mode="lines+markers",
            line=dict(color=ACCENT_AMBER, width=3),
            marker=dict(size=5, color=ACCENT_AMBER),
            fill="tozeroy",
            fillcolor="rgba(245, 158, 11, 0.12)",
            hovertemplate="<b>%{x}</b><br>Average Pickups: %{y:,.0f}<extra></extra>",
        )
    )

    if "weekday_avg" in hourly_df.columns and "weekend_avg" in hourly_df.columns:
        fig.add_trace(
            go.Scatter(
                x=hourly_df["formatted_hour"],
                y=hourly_df["weekday_avg"],
                name="Weekday Avg",
                mode="lines",
                line=dict(color=ACCENT_BLUE, width=1.8, dash="dot"),
                hovertemplate="Weekday Avg: %{y:,.0f}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hourly_df["formatted_hour"],
                y=hourly_df["weekend_avg"],
                name="Weekend Avg",
                mode="lines",
                line=dict(color=ACCENT_PURPLE, width=1.8, dash="dash"),
                hovertemplate="Weekend Avg: %{y:,.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(text=title, font=dict(color="#F8FAFC", size=14)),
        xaxis_title="Hour of Day",
        yaxis_title="Pickups / Hour",
    )
    return apply_transit_theme(fig, height=350)


def create_weekday_vs_weekend_chart(hourly_df: pd.DataFrame) -> go.Figure:
    """Creates a grouped comparison between weekday and weekend 24-hour demand."""
    fig = go.Figure()

    if hourly_df.empty:
        return apply_transit_theme(fig)

    fig.add_trace(
        go.Bar(
            x=hourly_df["formatted_hour"],
            y=hourly_df["weekday_avg"],
            name="Weekday Demand",
            marker_color=ACCENT_BLUE,
            marker_line_width=0,
            opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Weekday Avg: %{y:,.0f} trips<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=hourly_df["formatted_hour"],
            y=hourly_df["weekend_avg"],
            name="Weekend Demand",
            marker_color=ACCENT_AMBER,
            marker_line_width=0,
            opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Weekend Avg: %{y:,.0f} trips<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Weekday vs Weekend Hourly Comparison", font=dict(color="#F8FAFC", size=14)),
        barmode="group",
        xaxis_title="Hour of Day",
        yaxis_title="Average Pickups",
    )
    return apply_transit_theme(fig, height=350)


def create_weekday_distribution_chart(weekday_df: pd.DataFrame) -> go.Figure:
    """Creates a bar chart of pickup volume across days of week (Mon-Sun)."""
    fig = go.Figure()

    if weekday_df.empty:
        return apply_transit_theme(fig)

    max_val = weekday_df["total_pickups"].max()
    colors = [
        ACCENT_AMBER if v == max_val else ACCENT_BLUE
        for v in weekday_df["total_pickups"]
    ]

    fig.add_trace(
        go.Bar(
            x=weekday_df["day_name"],
            y=weekday_df["total_pickups"],
            marker_color=colors,
            text=weekday_df["percentage"].apply(lambda p: f"{p}%"),
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=11),
            hovertemplate="<b>%{x}</b><br>Total Pickups: %{y:,.0f}<br>Share: %{text}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Demand by Day of Week", font=dict(color="#F8FAFC", size=14)),
        xaxis_title="Day of Week",
        yaxis_title="Total Pickups",
        showlegend=False,
    )
    return apply_transit_theme(fig, height=330)


def create_area_distribution_chart(area_df: pd.DataFrame, limit: int = 10) -> go.Figure:
    """Creates a horizontal bar chart ranking pickup areas by demand."""
    fig = go.Figure()

    if area_df.empty:
        return apply_transit_theme(fig)

    df_slice = area_df.head(limit).iloc[::-1]  # Reverse for descending horizontal bars

    fig.add_trace(
        go.Bar(
            x=df_slice["total_pickups"],
            y=df_slice["pickup_area"],
            orientation="h",
            marker=dict(
                color=df_slice["total_pickups"],
                colorscale=[[0, "#0284C7"], [0.5, "#38BDF8"], [1, "#F59E0B"]],
                showscale=False,
            ),
            text=df_slice["percentage"].apply(lambda p: f"{p}%"),
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=10),
            hovertemplate="<b>%{y}</b><br>Total Pickups: %{x:,.0f}<br>Share: %{text}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Pickup Area Demand Ranking", font=dict(color="#F8FAFC", size=14)),
        xaxis_title="Total Pickups",
        yaxis_title="",
        showlegend=False,
    )
    return apply_transit_theme(fig, height=360)


def create_heatmap_chart(
    matrix: np.ndarray,
    days: List[str],
    hours: List[str],
    title: str = "Passenger Demand Heatmap (Hour × Weekday)"
) -> go.Figure:
    """Creates an interactive 7x24 heatmap grid using Plotly."""
    custom_colorscale = [
        [0.0, "#0B1120"],
        [0.2, "#1E293B"],
        [0.4, "#0369A1"],
        [0.6, "#0284C7"],
        [0.8, "#F59E0B"],
        [1.0, "#FBBF24"],
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=hours,
            y=days,
            colorscale=custom_colorscale,
            colorbar=dict(
                title=dict(text="Pickups / Hr", font=dict(color=TEXT_COLOR, size=11)),
                tickfont=dict(color=TEXT_COLOR, size=10),
                thickness=12,
                len=0.8,
            ),
            hovertemplate="<b>%{y}</b> at <b>%{x}</b><br>Average Pickups: %{z:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(color="#F8FAFC", size=14)),
        xaxis_title="Hour of Day",
        yaxis_title="Weekday",
        yaxis=dict(autorange="reversed"),
    )
    return apply_transit_theme(fig, height=380)


def create_prediction_comparison_chart(
    hourly_curve_df: pd.DataFrame,
    target_hour: int,
    predicted_val: int,
    historical_val: int,
) -> go.Figure:
    """
    Creates a 24-hour comparative line chart showing historical baseline
    vs predicted scenario, highlighting the target prediction window.
    """
    fig = go.Figure()

    if hourly_curve_df.empty:
        return apply_transit_theme(fig)

    target_hour_fmt = f"{target_hour:02d}:00"

    # Historical average curve
    fig.add_trace(
        go.Scatter(
            x=hourly_curve_df["formatted_hour"],
            y=hourly_curve_df["historical_baseline"],
            name="Historical Baseline",
            mode="lines",
            line=dict(color="#64748B", width=2, dash="dash"),
            hovertemplate="Historical Baseline: %{y:,.0f}<extra></extra>",
        )
    )

    # Simulated prediction curve
    fig.add_trace(
        go.Scatter(
            x=hourly_curve_df["formatted_hour"],
            y=hourly_curve_df["predicted_volume"],
            name="Simulated Forecast Curve",
            mode="lines+markers",
            line=dict(color=ACCENT_AMBER, width=2.5),
            marker=dict(size=4, color=ACCENT_AMBER),
            hovertemplate="Forecast Profile: %{y:,.0f}<extra></extra>",
        )
    )

    # Highlight target hour predicted point
    fig.add_trace(
        go.Scatter(
            x=[target_hour_fmt],
            y=[predicted_val],
            name=f"Target Hour ({target_hour_fmt})",
            mode="markers+text",
            marker=dict(size=14, color=ACCENT_AMBER, line=dict(color="#FFFFFF", width=2)),
            text=[f"{predicted_val:,.0f}"],
            textposition="top center",
            textfont=dict(color="#FFFFFF", size=12, family="monospace"),
            hovertemplate="<b>Target Window (%{x})</b><br>Forecast: %{y:,.0f} pickups<extra></extra>",
        )
    )

    # Vertical reference line at target hour
    fig.add_vline(
        x=target_hour_fmt,
        line_width=1.5,
        line_dash="dot",
        line_color=ACCENT_AMBER,
        opacity=0.6,
    )

    fig.update_layout(
        title=dict(
            text=f"24-Hour Profile Comparison (Target: {target_hour_fmt})",
            font=dict(color="#F8FAFC", size=14)
        ),
        xaxis_title="Hour of Day",
        yaxis_title="Pickups / Hour",
    )
    return apply_transit_theme(fig, height=360)
