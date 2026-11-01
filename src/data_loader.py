"""Load and validate the project's used car data."""
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

REQUIRED_COLUMNS = [
    "car_name", "make", "model", "variant", "yr_mfr", "fuel_type", "kms_run",
    "sale_price", "city", "registered_state", "body_type", "transmission",
    "total_owners", "car_age", "price_per_km",
]
NUMERIC_COLUMNS = ["yr_mfr", "kms_run", "sale_price", "total_owners", "car_age", "price_per_km"]
TEXT_COLUMNS = [column for column in REQUIRED_COLUMNS if column not in NUMERIC_COLUMNS]


def validate_schema(data: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> list[str]:
    """Return a list of required columns missing from a data frame."""
    return [column for column in required if column not in data.columns]


@st.cache_data(show_spinner=False)
def load_data(path: str = "data/used_cars_cleaned.csv") -> pd.DataFrame:
    """Read the bundled CSV using a path relative to the project root."""
    file_path = Path(__file__).resolve().parent.parent / path
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    data = pd.read_csv(file_path)
    missing = validate_schema(data)
    if missing:
        raise ValueError("Dataset is missing required columns: " + ", ".join(missing))
    return data
