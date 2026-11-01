"""Statistical hypothesis tests and effect size calculations.

Implements Welch's t-test, one-way ANOVA, Tukey HSD post-hoc analysis,
Cohen's d, and eta-squared (η²) without reliance on machine learning.
"""
from typing import Any
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def run_statistical_tests(data: pd.DataFrame) -> dict[str, Any]:
    """
    Execute parametric statistical hypothesis tests on resale price.

    Returns:
      dict with:
        't_test': scipy t-test result (automatic vs manual)
        'cohens_d': float or None
        'cohens_d_label': str
        'anova': scipy f_oneway result (fuel_type)
        'eta_squared': float or None
        'eta_squared_label': str
        'tukey': statsmodels Tukey HSD result
        'correlations': dict of Pearson correlation coefficients
    """
    result: dict[str, Any] = {
        "t_test": None,
        "cohens_d": None,
        "cohens_d_label": "N/A",
        "anova": None,
        "eta_squared": None,
        "eta_squared_label": "N/A",
        "tukey": None,
        "correlations": {},
    }

    if data is None or data.empty or "sale_price" not in data.columns:
        return result

    # 1. Welch's t-test (Transmission: Automatic vs Manual)
    if "transmission" in data.columns:
        auto = data.loc[data["transmission"].str.lower() == "automatic", "sale_price"].dropna()
        manual = data.loc[data["transmission"].str.lower() == "manual", "sale_price"].dropna()

        if len(auto) > 2 and len(manual) > 2:
            # Welch's t-test does not assume equal variances
            result["t_test"] = stats.ttest_ind(auto, manual, equal_var=False)

            # Cohen's d for independent samples
            s1_sq, s2_sq = auto.var(ddof=1), manual.var(ddof=1)
            pooled_std = ((s1_sq + s2_sq) / 2.0) ** 0.5
            if pooled_std > 0:
                d = float((auto.mean() - manual.mean()) / pooled_std)
                result["cohens_d"] = d
                abs_d = abs(d)
                if abs_d < 0.2:
                    result["cohens_d_label"] = "negligible"
                elif abs_d < 0.5:
                    result["cohens_d_label"] = "small"
                elif abs_d < 0.8:
                    result["cohens_d_label"] = "medium"
                else:
                    result["cohens_d_label"] = "large"

    # 2. One-Way ANOVA (Fuel Types)
    if "fuel_type" in data.columns:
        fuel_groups = [
            group["sale_price"].dropna()
            for _, group in data.groupby("fuel_type", observed=True)
            if len(group["sale_price"].dropna()) > 2
        ]

        if len(fuel_groups) >= 2:
            result["anova"] = stats.f_oneway(*fuel_groups)

            # Compute Eta-squared (η² = SS_between / SS_total)
            grand_mean = data["sale_price"].mean()
            ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in fuel_groups)
            ss_total = sum((data["sale_price"] - grand_mean) ** 2)

            if ss_total > 0:
                eta_sq = float(ss_between / ss_total)
                result["eta_squared"] = eta_sq
                if eta_sq < 0.01:
                    result["eta_squared_label"] = "negligible"
                elif eta_sq < 0.06:
                    result["eta_squared_label"] = "small"
                elif eta_sq < 0.14:
                    result["eta_squared_label"] = "medium"
                else:
                    result["eta_squared_label"] = "large"

        # 3. Tukey HSD Post-hoc Test
        valid_fuel = data[["fuel_type", "sale_price"]].dropna()
        if valid_fuel["fuel_type"].nunique() >= 2:
            try:
                result["tukey"] = pairwise_tukeyhsd(
                    endog=valid_fuel["sale_price"],
                    groups=valid_fuel["fuel_type"],
                    alpha=0.05,
                )
            except Exception:
                result["tukey"] = None

    # 4. Pearson Correlations
    num_cols = ["car_age", "kms_run", "total_owners", "sale_price"]
    avail_num = [c for c in num_cols if c in data.columns]
    if len(avail_num) >= 2 and "sale_price" in avail_num:
        corr_series = data[avail_num].corr(numeric_only=True)["sale_price"]
        result["correlations"] = corr_series.to_dict()

    return result
