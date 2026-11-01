"""Unit tests for the data cleaning pipeline."""
import os
import pandas as pd
import pytest

from src.cleaning import FINAL_COLUMNS, clean_uploaded_data


def sample_valid_record() -> pd.DataFrame:
    """Return a single valid listing row with uncleaned formatting."""
    return pd.DataFrame([{
        "car_name": "  Maruti Swift VXi  ",
        "make": " MARUTI ",
        "model": " SWIFT ",
        "variant": " vxi ",
        "yr_mfr": 2018,
        "fuel_type": "PETROL",
        "kms_run": 35000,
        "sale_price": 450000,
        "city": " Pune ",
        "registered_state": " MH ",
        "body_type": "Hatchback",
        "transmission": "Manual",
        "total_owners": 1,
    }])


def test_cleaning_normalizes_text_and_derives_features() -> None:
    """Verify that strings are trimmed, lowercased, and derived features added."""
    cleaned, report = clean_uploaded_data(sample_valid_record())
    assert cleaned.loc[0, "make"] == "maruti"
    assert cleaned.loc[0, "fuel_type"] == "petrol"
    assert cleaned.loc[0, "car_age"] == 2026 - 2018
    assert cleaned.loc[0, "price_per_km"] > 0
    assert report["rows_after"] == 1


def test_cleaning_rejects_missing_columns() -> None:
    """A DataFrame missing mandatory attributes raises a helpful ValueError."""
    bad_df = pd.DataFrame([{"car_name": "Incomplete Car", "sale_price": 500000}])
    with pytest.raises(ValueError, match="Required columns missing"):
        clean_uploaded_data(bad_df)


def test_cleaning_handles_empty_dataframe() -> None:
    """An empty DataFrame triggers a clean validation exception."""
    with pytest.raises(ValueError, match="empty"):
        clean_uploaded_data(pd.DataFrame())


def test_cleaning_matches_cleaned_dataset_schema() -> None:
    """Verify that cleaning produces the exact 15-column schema."""
    cleaned_file = os.path.join("data", "used_cars_cleaned.csv")
    if os.path.exists(cleaned_file):
        df_cleaned = pd.read_csv(cleaned_file)
        cleaned_out, report = clean_uploaded_data(df_cleaned)
        assert len(cleaned_out.columns) == 15
        assert list(cleaned_out.columns) == FINAL_COLUMNS
