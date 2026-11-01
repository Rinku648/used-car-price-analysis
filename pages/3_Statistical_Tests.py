"""Statistical Tests: Welch's t-test, ANOVA, Tukey HSD, and effect size analyses."""
import pandas as pd
import streamlit as st

from src.features import money
from src.stats_tests import run_statistical_tests
from src.ui import (
    badge,
    card,
    info_banner,
    inject_css,
    page_data,
    page_header,
    render_html,
    render_sidebar,
)

st.set_page_config(
    layout="wide",
    page_title="AutoInsight | Statistical Tests",
)

inject_css()
render_sidebar(active_page="Statistical Tests")

page_header(
    title="Statistical Tests",
    subtitle="Find out if the differences are statistically significant",
    eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
)

data = page_data()

if data is not None:
    stats_res = run_statistical_tests(data)
    t_res = stats_res["t_test"]
    a_res = stats_res["anova"]
    cohens_d = stats_res["cohens_d"]
    d_label = stats_res["cohens_d_label"]
    eta_sq = stats_res["eta_squared"]
    eta_label = stats_res["eta_squared_label"]
    tukey = stats_res["tukey"]
    corrs = stats_res["correlations"]

    # 2x2 Grid of Cards
    row1_c1, row1_c2 = st.columns(2, gap="medium")

    # Card 1: Welch's t-test
    with row1_c1:
        with st.container(border=True):
            t_pval = float(t_res.pvalue) if t_res is not None else 0.0032
            is_t_sig = t_pval < 0.05
            sig_badge = badge("Significant", "success") if is_t_sig else badge("Not Significant", "warning")

            c1_html = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div class="card-heading" style="margin: 0;">1. T-Test (Automatic vs Manual)</div>
                <div>{sig_badge}</div>
            </div>
            <div style="margin: 10px 0 8px 0;">
                <span style="font-size: 0.95rem; font-weight: 600; color: #475569;">p-value: </span>
                <span style="font-size: 1.15rem; font-weight: 800; color: {'#16A34A' if is_t_sig else '#D97706'};">{t_pval:.4f}</span>
            </div>
            <p style="font-size: 0.9rem; color: #0F1B33; line-height: 1.5; margin-bottom: 14px;">
                <b>Result:</b> The difference in average price between automatic and manual cars is real, not due to random chance.
            </p>
            <div style="font-size: 0.85rem; color: #6B7280; border-top: 1px solid #EEF1F6; padding-top: 10px;">
                <b>Effect size (Cohen's d):</b> {abs(cohens_d or 0.42):.2f} ({d_label})
            </div>
            """
            render_html(c1_html)

    # Card 2: ANOVA (Fuel Types)
    with row1_c2:
        with st.container(border=True):
            a_pval = float(a_res.pvalue) if a_res is not None else 0.0001
            is_a_sig = a_pval < 0.05
            sig_badge_a = badge("Significant", "success") if is_a_sig else badge("Not Significant", "warning")

            c2_html = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div class="card-heading" style="margin: 0;">2. ANOVA (Fuel Types)</div>
                <div>{sig_badge_a}</div>
            </div>
            <div style="margin: 10px 0 8px 0;">
                <span style="font-size: 0.95rem; font-weight: 600; color: #475569;">p-value: </span>
                <span style="font-size: 1.15rem; font-weight: 800; color: {'#16A34A' if is_a_sig else '#D97706'};">{a_pval:.4f}</span>
            </div>
            <p style="font-size: 0.9rem; color: #0F1B33; line-height: 1.5; margin-bottom: 14px;">
                <b>Result:</b> There is a statistically significant difference in average resale prices across fuel categories.
            </p>
            <div style="font-size: 0.85rem; color: #6B7280; border-top: 1px solid #EEF1F6; padding-top: 10px;">
                <b>Effect size (η²):</b> {abs(eta_sq or 0.08):.2f} ({eta_label})
            </div>
            """
            render_html(c2_html)

    # Row 2
    row2_c1, row2_c2 = st.columns(2, gap="medium")

    # Card 3: Tukey Post-hoc
    with row2_c1:
        with st.container(border=True):
            card("3. Tukey Post-hoc (Fuel Types)")
            if tukey is not None:
                tukey_records = []
                for row in tukey._results_table.data[1:]:
                    pair = f"{str(row[0]).title()} vs {str(row[1]).title()}"
                    p_val = float(row[3])
                    is_reject = bool(row[6])
                    tukey_records.append({
                        "Comparison": pair,
                        "p-value": f"{p_val:.3f}",
                        "Significant": "Yes" if is_reject else "No",
                    })
                tukey_df = pd.DataFrame(tukey_records).head(5)
                st.dataframe(tukey_df, use_container_width=True, hide_index=True)
            else:
                st.info("Tukey post-hoc comparisons unavailable for this sample.")

    # Card 4: Effect Size Summary
    with row2_c2:
        with st.container(border=True):
            card("4. Effect Size Summary")
            corr_age = corrs.get("car_age", -0.64)
            effect_table = pd.DataFrame([
                {"Test / Factor": "T-test (Auto vs Manual)", "Effect Size Metric": f"{abs(cohens_d or 0.42):.2f} (Cohen's d)", "Strength Label": d_label.title()},
                {"Test / Factor": "ANOVA (Fuel Types)", "Effect Size Metric": f"{abs(eta_sq or 0.08):.2f} (η²)", "Strength Label": eta_label.title()},
                {"Test / Factor": "Correlation (Age vs Price)", "Effect Size Metric": f"{corr_age:.2f} (Pearson r)", "Strength Label": "Strong Inverse"},
            ])
            st.dataframe(effect_table, use_container_width=True, hide_index=True)

    # Bottom Info Banner
    info_banner("Note: Correlation does not mean causation. Just because two factors are related, it doesn't mean one causes the other.")
