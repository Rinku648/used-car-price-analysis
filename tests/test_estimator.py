"""Tests for the transparent comparable-listing estimator."""
import pandas as pd
import pytest

from src.estimator import estimate_price


def sample_data() -> pd.DataFrame:
    """Build a small deterministic set of comparable cars."""
    return pd.DataFrame({
        "make": ["brand"] * 8,
        "model": ["model"] * 8,
        "fuel_type": ["petrol"] * 8,
        "transmission": ["manual"] * 8,
        "yr_mfr": [2015, 2015, 2016, 2016, 2016, 2017, 2017, 2017],
        "kms_run": [40000, 45000, 50000, 52000, 55000, 48000, 60000, 62000],
        "sale_price": [300000, 320000, 330000, 350000, 360000, 370000, 390000, 410000],
    })


def test_estimator_returns_percentile_range() -> None:
    """A close set produces a range, mean and match count."""
    result = estimate_price(sample_data(), "brand", "petrol", 2016, 50000, model="model")
    assert result["count"] >= 5
    assert result["p25"] <= result["average"] <= result["p75"]
    assert result["confidence"] in {"Low", "Medium", "High"}


def test_estimator_widens_tolerance_when_needed() -> None:
    """Listings outside the initial band can be included after widening."""
    data = sample_data().assign(yr_mfr=2012, kms_run=90000)
    result = estimate_price(data, "brand", "petrol", 2016, 50000)
    assert result["count"] == 8
    assert result["widened"] is True


def test_estimator_handles_empty_results() -> None:
    """A brand with no comparable listings returns an empty result safely."""
    result = estimate_price(sample_data(), "unknown", "petrol", 2016, 50000)
    assert result["count"] == 0
    assert result["p25"] is None


def test_estimator_rejects_invalid_input() -> None:
    """Invalid year, mileage and asking prices raise friendly validation errors."""
    with pytest.raises(ValueError):
        estimate_price(sample_data(), "brand", "petrol", 2030, 50000)
    with pytest.raises(ValueError):
        estimate_price(sample_data(), "brand", "petrol", 2016, -1)
    with pytest.raises(ValueError):
        estimate_price(sample_data(), "brand", "petrol", 2016, 50000, asking_price=0)
