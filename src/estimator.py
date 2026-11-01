"""Transparent, rule-based fair price estimation using comparable real listings.

Hard constraint: No machine learning, no regression models, no scikit-learn.
All estimations are purely based on statistical percentiles (P25 to P75) of
closely matching historical listings.
"""
from typing import Any
import pandas as pd


def estimate_price(
    data: pd.DataFrame,
    make: str,
    fuel_type: str,
    year: int,
    kms_run: int,
    transmission: str | None = None,
    asking_price: float | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """
    Find comparable real listings and calculate fair price percentiles.

    Parameters:
      data: Loaded DataFrame of used cars.
      make: Vehicle manufacturer (e.g., 'maruti', 'hyundai').
      fuel_type: Fuel category ('petrol', 'diesel', 'cng', 'other').
      year: Year of manufacture (e.g., 2018).
      kms_run: Odometer reading in kilometers.
      transmission: Optional 'manual' / 'automatic' / 'any'.
      asking_price: Optional asking price to evaluate for Deal Verdict.
      model: Optional model name (e.g., 'swift', 'i20').

    Returns:
      Dictionary with matched listings, count, price range (P25, P75, average),
      confidence rating, widening flag, and deal verdict.
    """
    if year < 1990 or year > 2026:
        raise ValueError("Please enter a valid manufacture year between 1990 and 2026.")
    if kms_run < 0:
        raise ValueError("Kilometers driven cannot be negative.")
    if asking_price is not None and asking_price <= 0:
        raise ValueError("Asking price must be a positive number.")

    empty_res: dict[str, Any] = {
        "matches": pd.DataFrame(),
        "count": 0,
        "widened": False,
        "tolerance_used": "±2 yrs, ±15,000 km",
        "p25": None,
        "p75": None,
        "average": None,
        "confidence": "Low",
        "verdict": None,
    }

    if data is None or data.empty:
        return empty_res

    # Initial filtering by brand and fuel type
    pool = data[
        (data["make"].astype(str).str.lower() == str(make).lower()) &
        (data["fuel_type"].astype(str).str.lower() == str(fuel_type).lower())
    ]

    # Filter by model if given and sufficient sample exists
    if model and model.lower() != "any" and "model" in pool.columns:
        model_subset = pool[pool["model"].astype(str).str.lower() == str(model).lower()]
        if len(model_subset) >= 5:
            pool = model_subset

    # Filter by transmission if specified
    if transmission and transmission.lower() not in ["any", "all", ""] and "transmission" in pool.columns:
        trans_subset = pool[pool["transmission"].astype(str).str.lower() == transmission.lower()]
        if len(trans_subset) >= 5:
            pool = trans_subset

    if pool.empty:
        return empty_res

    # Progressive auto-widening tolerance steps
    tolerance_levels = [
        (2, 15000, "±2 yrs, ±15,000 km"),
        (3, 25000, "±3 yrs, ±25,000 km"),
        (5, 45000, "±5 yrs, ±45,000 km"),
        (8, 70000, "±8 yrs, ±70,000 km"),
        (25, 200000, "wide brand pool"),
    ]

    matches = pd.DataFrame()
    tolerance_used = tolerance_levels[0][2]
    widened = False

    for idx, (yr_tol, km_tol, tol_label) in enumerate(tolerance_levels):
        step_matches = pool[
            (pool["yr_mfr"].astype(float) - year).abs() <= yr_tol
        ]
        step_matches = step_matches[
            (step_matches["kms_run"].astype(float) - kms_run).abs() <= km_tol
        ]

        if len(step_matches) >= 5:
            matches = step_matches.copy()
            tolerance_used = tol_label
            widened = (idx > 0)
            break
        elif idx == len(tolerance_levels) - 1:
            matches = step_matches.copy()
            tolerance_used = tol_label
            widened = True

    if matches.empty:
        return empty_res

    prices = matches["sale_price"].astype(float)
    p25 = float(prices.quantile(0.25))
    p75 = float(prices.quantile(0.75))
    avg_price = float(prices.mean())

    # Confidence based on number of close matches
    match_count = len(matches)
    if match_count >= 25:
        confidence = "High"
    elif match_count >= 8:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Deal Verdict
    verdict = None
    if asking_price is not None:
        if asking_price < p25:
            verdict = "Underpriced"
        elif asking_price > p75:
            verdict = "Overpriced"
        else:
            verdict = "Fair"

    return {
        "matches": matches,
        "count": match_count,
        "widened": widened,
        "tolerance_used": tolerance_used,
        "p25": p25,
        "p75": p75,
        "average": avg_price,
        "confidence": confidence,
        "verdict": verdict,
    }
