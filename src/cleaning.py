"""Data cleaning pipeline for raw and user-uploaded used car listings.

This module reproduces the 10-step cleaning pipeline used to produce
data/used_cars_cleaned.csv from data/used_cars_raw.csv. It is fully modular
and is also reused by the 'Upload & Analyze' page to audit user uploads.
"""
from typing import Any
import numpy as np
import pandas as pd

# The 13 core attributes required before computing derived features
CORE_COLUMNS = [
    "car_name",
    "make",
    "model",
    "variant",
    "yr_mfr",
    "fuel_type",
    "kms_run",
    "sale_price",
    "city",
    "registered_state",
    "body_type",
    "transmission",
    "total_owners",
]

# The final 15 columns present in used_cars_cleaned.csv
FINAL_COLUMNS = CORE_COLUMNS + ["car_age", "price_per_km"]


def clean_uploaded_data(data: pd.DataFrame, reference_year: int = 2026) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Clean and standardize a dataset of used car listings.
    
    Steps:
      1. Schema validation (ensure core columns exist)
      2. Keep relevant columns
      3. Drop duplicate rows
      4. Remove invalid prices (sale_price < 10,000 or negative kms)
      5. Impute missing transmission and body_type using mode
      6. Drop rows with missing registered_state
      7. Remove extreme IQR outliers on sale_price and kms_run
      8. Normalize text (lowercase, strip whitespace)
      9. Merge rare fuel types into 'other'
      10. Derive 'car_age' and 'price_per_km'

    Returns:
      (cleaned_df, audit_log_dict)
    """
    if data is None or data.empty:
        raise ValueError("The uploaded CSV is empty. Please provide a file with valid records.")

    # 1. Schema check
    missing_cols = [c for c in CORE_COLUMNS if c not in data.columns]
    if missing_cols:
        raise ValueError(f"Required columns missing: {', '.join(missing_cols)}")

    raw_count = len(data)
    raw_cols = len(data.columns)
    missing_vals_before = int(data[CORE_COLUMNS].isna().sum().sum())

    # 2. Subset relevant columns
    df = data[CORE_COLUMNS].copy()

    # 3. Drop exact duplicates
    dups_count = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)

    # 4. Cast numeric columns & remove sale_price < 10,000 or negative km
    df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce")
    df["kms_run"] = pd.to_numeric(df["kms_run"], errors="coerce")
    df["yr_mfr"] = pd.to_numeric(df["yr_mfr"], errors="coerce")
    df["total_owners"] = pd.to_numeric(df["total_owners"], errors="coerce")

    # Drop non-positive / invalid records
    invalid_price_or_km = (df["sale_price"] < 10000) | (df["kms_run"] < 0) | df["sale_price"].isna() | df["kms_run"].isna()
    df = df[~invalid_price_or_km].reset_index(drop=True)

    # 5. Impute transmission and body_type mode
    if df["transmission"].isna().any() and not df["transmission"].dropna().empty:
        df["transmission"] = df["transmission"].fillna(df["transmission"].mode()[0])
    if df["body_type"].isna().any() and not df["body_type"].dropna().empty:
        df["body_type"] = df["body_type"].fillna(df["body_type"].mode()[0])

    # 6. Drop missing registered_state
    df = df.dropna(subset=["registered_state"]).reset_index(drop=True)

    # 7. Lowercase and trim text columns
    text_cols = ["car_name", "make", "model", "variant", "fuel_type", "city", "registered_state", "body_type", "transmission"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace(["nan", "none", ""], pd.NA)

    # Drop any remaining NAs in text columns
    df = df.dropna(subset=text_cols).reset_index(drop=True)

    # 8. Merge rare fuel types into 'other' (e.g. electric, petrol & lpg)
    standard_fuels = {"petrol", "diesel", "cng"}
    df["fuel_type"] = df["fuel_type"].apply(lambda f: f if f in standard_fuels else "other")

    # 9. Remove IQR outliers on sale_price and kms_run (only if large enough sample)
    outliers_removed = 0
    if len(df) > 50:
        p_q1, p_q3 = df["sale_price"].quantile(0.25), df["sale_price"].quantile(0.75)
        p_iqr = p_q3 - p_q1
        p_upper = p_q3 + 2.5 * p_iqr  # Keep generous threshold for high-end cars
        p_lower = max(10000, p_q1 - 1.5 * p_iqr)

        k_q1, k_q3 = df["kms_run"].quantile(0.25), df["kms_run"].quantile(0.75)
        k_iqr = k_q3 - k_q1
        k_upper = k_q3 + 3.0 * k_iqr

        valid_mask = df["sale_price"].between(p_lower, p_upper) & (df["kms_run"] <= k_upper)
        outliers_removed = int((~valid_mask).sum())
        df = df[valid_mask].reset_index(drop=True)

    # 10. Add derived features: car_age and price_per_km
    df["car_age"] = reference_year - df["yr_mfr"].astype(int)
    safe_km = df["kms_run"].replace(0, np.nan)
    df["price_per_km"] = (df["sale_price"] / safe_km).fillna(0).round(2)

    # Reorder columns to standard final schema
    final_df = df[FINAL_COLUMNS].copy()

    audit_log = {
        "rows_before": raw_count,
        "rows_after": len(final_df),
        "columns_before": raw_cols,
        "columns_after": len(final_df.columns),
        "missing_values_before": missing_vals_before,
        "duplicates_removed": dups_count,
        "outliers_removed": outliers_removed,
        "dropped_total": raw_count - len(final_df),
    }

    return final_df, audit_log
