"""Derived features and currency formatting helpers."""
from typing import Any
import pandas as pd


def add_features(data: pd.DataFrame, reference_year: int = 2026) -> pd.DataFrame:
    """Return a copy of the dataset with standardized derived features."""
    result = data.copy()
    if "yr_mfr" in result.columns:
        result["car_age"] = reference_year - pd.to_numeric(result["yr_mfr"], errors="coerce")
    
    if "kms_run" in result.columns and "sale_price" in result.columns:
        km = pd.to_numeric(result["kms_run"], errors="coerce").replace(0, pd.NA)
        price = pd.to_numeric(result["sale_price"], errors="coerce")
        result["price_per_km"] = (price / km).fillna(0).round(2)

    if "car_age" in result.columns:
        result["age_bucket"] = pd.cut(
            result["car_age"],
            bins=[0, 5, 8, 12, 100],
            labels=["0–5 years", "6–8 years", "9–12 years", "13+ years"],
            include_lowest=True,
        )

    if "kms_run" in result.columns:
        result["km_bucket"] = pd.cut(
            result["kms_run"],
            bins=[0, 30000, 60000, 100000, float("inf")],
            labels=["Under 30k", "30k–60k", "60k–100k", "100k+"],
            include_lowest=True,
        )

    return result


def money(value: Any) -> str:
    """Format an Indian rupee amount with Indian comma placement."""
    if value is None or pd.isna(value):
        return "₹0"
    try:
        val = float(value)
        return f"₹{val:,.0f}"
    except (ValueError, TypeError):
        return f"₹{value}"


def format_lakh(value: Any) -> str:
    """Format an amount in Lakhs (e.g., 548000 -> '₹ 5.48 L')."""
    if value is None or pd.isna(value):
        return "₹ 0.00 L"
    try:
        lakhs = float(value) / 100000.0
        return f"₹ {lakhs:.2f} L"
    except (ValueError, TypeError):
        return f"₹ {value}"
