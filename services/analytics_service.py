"""
Analytics Service Module.
Performs data filtering, KPI extraction, and aggregations using Pandas and NumPy.
All analytical metrics in the dashboard are computed dynamically from the underlying dataset.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import date
import pandas as pd
import numpy as np


class AnalyticsService:
    @staticmethod
    def filter_data(
        df: pd.DataFrame,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        selected_areas: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Filters the dataset by date range and selected pickup areas.
        """
        filtered = df.copy()

        if start_date is not None:
            filtered = filtered[filtered["date_dt"] >= start_date]

        if end_date is not None:
            filtered = filtered[filtered["date_dt"] <= end_date]

        if selected_areas and len(selected_areas) > 0 and "All Zones" not in selected_areas:
            filtered = filtered[filtered["pickup_area"].isin(selected_areas)]

        return filtered

    @staticmethod
    def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Computes executive KPI metrics for Page A (Overview Dashboard):
        - Total pickups
        - Average hourly demand
        - Peak demand hour
        - Busiest pickup area
        """
        if df.empty:
            return {
                "total_pickups": 0,
                "avg_hourly_demand": 0.0,
                "peak_hour": 0,
                "peak_hour_formatted": "N/A",
                "peak_hour_volume": 0,
                "busiest_area": "N/A",
                "busiest_borough": "N/A",
                "busiest_area_volume": 0,
                "busiest_area_percentage": 0.0,
                "total_zones": 0,
                "date_range_str": "No records in filter",
            }

        total_pickups = int(df["pickups"].sum())

        # Group by hour to find peak demand hour
        hourly_totals = df.groupby("hour")["pickups"].sum()
        peak_hour = int(hourly_totals.idxmax())
        peak_hour_volume = int(hourly_totals.max())
        peak_formatted = f"{peak_hour:02d}:00 ({peak_hour % 12 or 12} {'AM' if peak_hour < 12 else 'PM'})"

        # Unique hours in filtered dataset
        unique_timestamps = df["timestamp"].nunique()
        avg_hourly_demand = round(total_pickups / max(1, unique_timestamps), 1)

        # Busiest pickup area
        area_totals = df.groupby(["pickup_area", "borough"])["pickups"].sum().reset_index()
        busiest_row = area_totals.sort_values(by="pickups", ascending=False).iloc[0]
        busiest_area = busiest_row["pickup_area"]
        busiest_borough = busiest_row["borough"]
        busiest_vol = int(busiest_row["pickups"])
        busiest_pct = round((busiest_vol / max(1, total_pickups)) * 100, 1)

        # Date range string
        min_date = df["date_dt"].min()
        max_date = df["date_dt"].max()
        date_range_str = f"{min_date.strftime('%b %d, %Y')} – {max_date.strftime('%b %d, %Y')}"

        return {
            "total_pickups": total_pickups,
            "avg_hourly_demand": avg_hourly_demand,
            "peak_hour": peak_hour,
            "peak_hour_formatted": peak_formatted,
            "peak_hour_volume": peak_hour_volume,
            "busiest_area": busiest_area,
            "busiest_borough": busiest_borough,
            "busiest_area_volume": busiest_vol,
            "busiest_area_percentage": busiest_pct,
            "total_zones": int(df["pickup_area"].nunique()),
            "date_range_str": date_range_str,
        }

    @staticmethod
    def get_hourly_trend(df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes 24-hour demand profile across the filtered dataset:
        Returns DataFrame with: hour, formatted_hour, total_pickups, avg_pickups,
        weekday_avg, weekend_avg, is_peak
        """
        if df.empty:
            return pd.DataFrame()

        # Unique dates to normalize averages
        weekday_dates = df[~df["is_weekend"]]["date_dt"].nunique() or 1
        weekend_dates = df[df["is_weekend"]]["date_dt"].nunique() or 1
        total_dates = df["date_dt"].nunique() or 1

        rows = []
        for hour in range(24):
            hour_df = df[df["hour"] == hour]
            tot = int(hour_df["pickups"].sum())
            avg = round(tot / total_dates, 1)

            wd_df = hour_df[~hour_df["is_weekend"]]
            we_df = hour_df[hour_df["is_weekend"]]

            wd_avg = round(wd_df["pickups"].sum() / weekday_dates, 1) if not wd_df.empty else 0.0
            we_avg = round(we_df["pickups"].sum() / weekend_dates, 1) if not we_df.empty else 0.0

            rows.append({
                "hour": hour,
                "formatted_hour": f"{hour:02d}:00",
                "total_pickups": tot,
                "avg_pickups": avg,
                "weekday_avg": wd_avg,
                "weekend_avg": we_avg,
                "is_peak": False,
            })

        result = pd.DataFrame(rows)
        if not result.empty:
            max_avg = result["avg_pickups"].max()
            result["is_peak"] = result["avg_pickups"] == max_avg

        return result

    @staticmethod
    def get_weekday_vs_weekend_hourly(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns average hourly demand comparing Weekday vs Weekend.
        """
        if df.empty:
            return pd.DataFrame()

        weekday_dates = df[~df["is_weekend"]]["date_dt"].nunique() or 1
        weekend_dates = df[df["is_weekend"]]["date_dt"].nunique() or 1

        hourly_wd = (
            df[~df["is_weekend"]]
            .groupby("hour")["pickups"]
            .sum()
            .div(weekday_dates)
            .round(1)
            .reset_index(name="weekday_avg")
        )
        hourly_we = (
            df[df["is_weekend"]]
            .groupby("hour")["pickups"]
            .sum()
            .div(weekend_dates)
            .round(1)
            .reset_index(name="weekend_avg")
        )

        merged = pd.merge(hourly_wd, hourly_we, on="hour", how="outer").fillna(0)
        merged["formatted_hour"] = merged["hour"].apply(lambda h: f"{int(h):02d}:00")
        merged = merged.sort_values(by="hour")
        return merged

    @staticmethod
    def get_weekday_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups passenger pickups by Day of Week (Monday to Sunday).
        """
        if df.empty:
            return pd.DataFrame()

        total_pickups = df["pickups"].sum()
        grouped = (
            df.groupby(["day_of_week", "day_name", "day_short", "is_weekend"])
            .agg(
                total_pickups=("pickups", "sum"),
                unique_days=("date_dt", "nunique")
            )
            .reset_index()
        )

        grouped["daily_average"] = (grouped["total_pickups"] / grouped["unique_days"]).round(1)
        grouped["percentage"] = ((grouped["total_pickups"] / max(1, total_pickups)) * 100).round(1)
        grouped = grouped.sort_values(by="day_of_week")
        return grouped

    @staticmethod
    def get_area_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes passenger pickup volume ranking by Pickup Area.
        """
        if df.empty:
            return pd.DataFrame()

        total_pickups = df["pickups"].sum()
        unique_hours = df["timestamp"].nunique() or 1

        grouped = (
            df.groupby(["pickup_area", "borough", "zone_type"])
            .agg(total_pickups=("pickups", "sum"))
            .reset_index()
        )

        grouped["percentage"] = ((grouped["total_pickups"] / max(1, total_pickups)) * 100).round(1)
        grouped["avg_hourly_pickups"] = (grouped["total_pickups"] / unique_hours).round(1)

        # Compute peak hour for each area
        area_peak_hours = {}
        for area, sub_df in df.groupby("pickup_area"):
            h_tot = sub_df.groupby("hour")["pickups"].sum()
            if not h_tot.empty:
                pk_h = int(h_tot.idxmax())
                area_peak_hours[area] = f"{pk_h:02d}:00"
            else:
                area_peak_hours[area] = "N/A"

        grouped["peak_hour"] = grouped["pickup_area"].map(area_peak_hours)
        grouped = grouped.sort_values(by="total_pickups", ascending=False)
        return grouped

    @staticmethod
    def get_heatmap_matrix(df: pd.DataFrame) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Builds a 7-day x 24-hour matrix for heatmap visualization.
        Returns:
            matrix (7x24 np.ndarray): normalized or mean pickup volume per cell
            days (list): ['Monday', 'Tuesday', ..., 'Sunday']
            hours (list): ['00:00', '01:00', ..., '23:00']
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = [f"{h:02d}:00" for h in range(24)]

        if df.empty:
            return np.zeros((7, 24)), days, hours

        # Calculate average volume per day_of_week and hour
        # Normalize by count of occurrences of that day/hour to represent typical hourly rate
        agg = (
            df.groupby(["day_of_week", "hour"])
            .agg(total=("pickups", "sum"), count=("date_dt", "nunique"))
            .reset_index()
        )
        agg["mean_pickups"] = (agg["total"] / agg["count"].replace(0, 1)).round(1)

        pivot = agg.pivot(index="day_of_week", columns="hour", values="mean_pickups").fillna(0)

        # Ensure all 7 rows and 24 columns exist
        for d in range(7):
            if d not in pivot.index:
                pivot.loc[d] = 0.0
        for h in range(24):
            if h not in pivot.columns:
                pivot[h] = 0.0

        pivot = pivot.sort_index().reindex(columns=range(24))
        matrix = pivot.to_numpy()

        return matrix, days, hours
