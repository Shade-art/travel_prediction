import math
from typing import Optional, List, Dict, Any
from app.data.mock_taxi_data import (
    TAXI_ZONES,
    BASE_HOURLY_PATTERN,
    WEEKDAY_PATTERNS,
    BASE_ZONE_HOURLY_VOLUME,
    get_zone_by_name
)
from app.schemas.summary import SummaryResponse
from app.schemas.analytics import (
    HourlyAnalyticsResponse,
    HourlyDataPoint,
    AreaAnalyticsResponse,
    AreaDataPoint,
    WeeklyAnalyticsResponse,
    WeekdayDataPoint,
    HeatmapCell
)

class AnalyticsService:
    @staticmethod
    def get_summary() -> SummaryResponse:
        # Calculate totals across the entire simulated week
        total_pickups = 0
        hourly_totals = [0] * 24
        area_totals: Dict[str, Dict[str, Any]] = {
            z["area_id"]: {
                "name": z["area_name"],
                "borough": z["borough"],
                "total": 0
            }
            for z in TAXI_ZONES
        }

        # Simulate 7 days x 24 hours across all zones
        for day in WEEKDAY_PATTERNS:
            day_weight = day["weight"]
            is_weekend = day["day_index"] in (5, 6)

            for pattern in BASE_HOURLY_PATTERN:
                hour = pattern["hour"]
                hour_factor = pattern["weekend_factor"] if is_weekend else pattern["weekday_factor"]

                for zone in TAXI_ZONES:
                    zone_weight = zone["base_weight"]
                    # Add zone peak synergy
                    synergy = 1.2 if zone["peak_hour"] == hour else 1.0
                    pickups = int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * hour_factor * day_weight * synergy))

                    total_pickups += pickups
                    hourly_totals[hour] += pickups
                    area_totals[zone["area_id"]]["total"] += pickups

        total_hours = 7 * 24
        avg_hourly = round(total_pickups / total_hours, 1)

        # Peak demand hour
        peak_hour = max(range(24), key=lambda h: hourly_totals[h])
        peak_pickups = hourly_totals[peak_hour]
        formatted_peak = f"{peak_hour:02d}:00 ({peak_hour % 12 or 12} {'AM' if peak_hour < 12 else 'PM'})"

        # Busiest pickup area
        busiest_id = max(area_totals.keys(), key=lambda zid: area_totals[zid]["total"])
        busiest = area_totals[busiest_id]
        busiest_pct = round((busiest["total"] / total_pickups) * 100, 1) if total_pickups > 0 else 0.0

        return SummaryResponse(
            total_pickups=total_pickups,
            avg_hourly_pickups=avg_hourly,
            peak_demand_hour=peak_hour,
            peak_demand_hour_formatted=formatted_peak,
            peak_demand_hour_pickups=peak_pickups,
            busiest_pickup_area=busiest["name"],
            busiest_pickup_borough=busiest["borough"],
            busiest_area_pickups=busiest["total"],
            busiest_area_percentage=busiest_pct,
            total_monitored_zones=len(TAXI_ZONES),
            sample_date_range="Representative 7-Day NYC Transit Cycle (Simulated)",
            data_classification="Simulated NYC TLC Taxi Telemetry - Phase 1 Mock Data"
        )

    @staticmethod
    def get_hourly_analytics(area_filter: Optional[str] = None) -> HourlyAnalyticsResponse:
        active_zones = TAXI_ZONES
        matched_zone = None
        if area_filter and area_filter.lower() != "all":
            matched_zone = get_zone_by_name(area_filter)
            if matched_zone:
                active_zones = [matched_zone]

        hourly_points: List[HourlyDataPoint] = []
        total_period_pickups = 0

        # We compute aggregate or filtered hourly average
        for pattern in BASE_HOURLY_PATTERN:
            hour = pattern["hour"]
            weekday_factor = pattern["weekday_factor"]
            weekend_factor = pattern["weekend_factor"]

            hour_weekday_vol = 0
            hour_weekend_vol = 0

            for zone in active_zones:
                zone_weight = zone["base_weight"]
                synergy = 1.2 if zone["peak_hour"] == hour else 1.0

                # 5 weekdays
                wd_sum = sum(
                    int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * weekday_factor * d["weight"] * synergy))
                    for d in WEEKDAY_PATTERNS[:5]
                )
                # 2 weekend days
                we_sum = sum(
                    int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * weekend_factor * d["weight"] * synergy))
                    for d in WEEKDAY_PATTERNS[5:]
                )

                hour_weekday_vol += wd_sum
                hour_weekend_vol += we_sum

            total_hour_vol = hour_weekday_vol + hour_weekend_vol
            total_period_pickups += total_hour_vol

            # Average daily hourly count
            avg_pickups = int(round(total_hour_vol / 7))
            avg_wd = int(round(hour_weekday_vol / 5))
            avg_we = int(round(hour_weekend_vol / 2))

            formatted_hour = f"{hour:02d}:00"
            hourly_points.append(HourlyDataPoint(
                hour=hour,
                formatted_hour=formatted_hour,
                pickups=avg_pickups,
                weekday_pickups=avg_wd,
                weekend_pickups=avg_we,
                is_peak=False
            ))

        # Mark peak hour
        max_hour_val = max(p.pickups for p in hourly_points)
        for p in hourly_points:
            if p.pickups == max_hour_val:
                p.is_peak = True

        return HourlyAnalyticsResponse(
            filter_area=matched_zone["area_name"] if matched_zone else (area_filter if area_filter else "All Monitored Zones"),
            total_pickups=total_period_pickups,
            data=hourly_points
        )

    @staticmethod
    def get_area_analytics() -> AreaAnalyticsResponse:
        area_stats: List[Dict[str, Any]] = []
        grand_total = 0

        for zone in TAXI_ZONES:
            zone_total = 0
            hourly_bucket = [0] * 24

            for day in WEEKDAY_PATTERNS:
                day_weight = day["weight"]
                is_weekend = day["day_index"] in (5, 6)

                for pattern in BASE_HOURLY_PATTERN:
                    hour = pattern["hour"]
                    hour_factor = pattern["weekend_factor"] if is_weekend else pattern["weekday_factor"]
                    synergy = 1.2 if zone["peak_hour"] == hour else 1.0

                    vol = int(round(BASE_ZONE_HOURLY_VOLUME * zone["base_weight"] * hour_factor * day_weight * synergy))
                    zone_total += vol
                    hourly_bucket[hour] += vol

            grand_total += zone_total
            peak_h = max(range(24), key=lambda h: hourly_bucket[h])
            peak_fmt = f"{peak_h:02d}:00 ({peak_h % 12 or 12} {'AM' if peak_h < 12 else 'PM'})"

            area_stats.append({
                "area_id": zone["area_id"],
                "area_name": zone["area_name"],
                "borough": zone["borough"],
                "total_pickups": zone_total,
                "avg_hourly_pickups": round(zone_total / (7 * 24), 1),
                "peak_hour": peak_h,
                "peak_hour_formatted": peak_fmt,
                "zone_type": zone["zone_type"]
            })

        # Calculate percentages and sort descending by volume
        area_stats.sort(key=lambda x: x["total_pickups"], reverse=True)
        data_points: List[AreaDataPoint] = []
        for a in area_stats:
            pct = round((a["total_pickups"] / grand_total) * 100, 1) if grand_total > 0 else 0.0
            data_points.append(AreaDataPoint(
                area_id=a["area_id"],
                area_name=a["area_name"],
                borough=a["borough"],
                total_pickups=a["total_pickups"],
                percentage=pct,
                avg_hourly_pickups=a["avg_hourly_pickups"],
                peak_hour=a["peak_hour"],
                peak_hour_formatted=a["peak_hour_formatted"],
                zone_type=a["zone_type"]
            ))

        return AreaAnalyticsResponse(
            total_areas=len(data_points),
            total_pickups=grand_total,
            disclaimer="Taxis operate point-to-point without fixed transit routes. Demand is indexed by pickup zones and geographic catchment clusters.",
            data=data_points
        )

    @staticmethod
    def get_weekly_analytics(area_filter: Optional[str] = None) -> WeeklyAnalyticsResponse:
        active_zones = TAXI_ZONES
        matched_zone = None
        if area_filter and area_filter.lower() != "all":
            matched_zone = get_zone_by_name(area_filter)
            if matched_zone:
                active_zones = [matched_zone]

        weekday_totals = {d["day_index"]: 0 for d in WEEKDAY_PATTERNS}
        heatmap_matrix: List[Dict[str, Any]] = []
        total_vol = 0

        # Build 7 days x 24 hours cells
        for day in WEEKDAY_PATTERNS:
            d_idx = day["day_index"]
            d_name = day["day_name"]
            d_weight = day["weight"]
            is_weekend = d_idx in (5, 6)

            for pattern in BASE_HOURLY_PATTERN:
                hour = pattern["hour"]
                hour_factor = pattern["weekend_factor"] if is_weekend else pattern["weekday_factor"]

                cell_pickups = 0
                for zone in active_zones:
                    synergy = 1.2 if zone["peak_hour"] == hour else 1.0
                    vol = int(round(BASE_ZONE_HOURLY_VOLUME * zone["base_weight"] * hour_factor * d_weight * synergy))
                    cell_pickups += vol

                weekday_totals[d_idx] += cell_pickups
                total_vol += cell_pickups
                heatmap_matrix.append({
                    "day_index": d_idx,
                    "day_name": d_name,
                    "hour": hour,
                    "formatted_hour": f"{hour:02d}:00",
                    "pickups": cell_pickups
                })

        # Calculate heatmap intensity normalized (0-100%)
        max_cell = max(c["pickups"] for c in heatmap_matrix) if heatmap_matrix else 1
        min_cell = min(c["pickups"] for c in heatmap_matrix) if heatmap_matrix else 0
        spread = max(max_cell - min_cell, 1)

        heatmap_cells: List[HeatmapCell] = []
        for c in heatmap_matrix:
            intensity = round(((c["pickups"] - min_cell) / spread) * 100, 1)
            heatmap_cells.append(HeatmapCell(
                day_index=c["day_index"],
                day_name=c["day_name"],
                hour=c["hour"],
                formatted_hour=c["formatted_hour"],
                pickups=c["pickups"],
                intensity=intensity
            ))

        # Build weekday summary
        weekday_points: List[WeekdayDataPoint] = []
        for day in WEEKDAY_PATTERNS:
            d_idx = day["day_index"]
            tot = weekday_totals[d_idx]
            pct = round((tot / total_vol) * 100, 1) if total_vol > 0 else 0.0
            daily_avg = round(tot / 24, 1)
            weekday_points.append(WeekdayDataPoint(
                day_index=d_idx,
                day_name=day["day_name"],
                short_name=day["short_name"],
                total_pickups=tot,
                daily_average=daily_avg,
                percentage=pct
            ))

        return WeeklyAnalyticsResponse(
            filter_area=matched_zone["area_name"] if matched_zone else (area_filter if area_filter else "All Monitored Zones"),
            weekday_distribution=weekday_points,
            heatmap=heatmap_cells
        )
