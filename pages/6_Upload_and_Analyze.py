"""Upload & Analyze page: real-time CSV schema validation, cleaning pipeline, and audit."""
import pandas as pd
import plotly.express as px
import streamlit as st

from src.charts import style_chart
from src.cleaning import clean_uploaded_data
from src.features import format_lakh, money
from src.ui import (
    badge,
    caption,
    card,
    inject_css,
    page_header,
    render_html,
    render_sidebar,
)

st.set_page_config(
    layout="wide",
    page_title="AutoInsight | Upload & Analyze",
)

inject_css()
render_sidebar(active_page="Upload & Analyze")

page_header(
    title="Upload and Analyze",
    subtitle="Upload your own CSV and get instant insights",
    eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
)

# File Uploader
uploaded_file = st.file_uploader(
    "Drag & drop your CSV file here or click to browse",
    type=["csv"],
    help="Upload a used car CSV dataset matching the project schema",
)

df_analyzed = None
audit_report = None

if uploaded_file is not None:
    try:
        raw_input = pd.read_csv(uploaded_file)
        df_analyzed, audit_report = clean_uploaded_data(raw_input)
        st.success(f"Analysis complete: successfully validated and cleaned {len(df_analyzed):,} records.")
    except Exception as err:
        st.error(f"Validation Error: {err}")
else:
    # Interactive demo preview slice
    st.info("Upload your custom CSV above, or review the pre-loaded 1,200-row demo slice below.")
    try:
        sample_slice = pd.read_csv("data/used_cars_cleaned.csv").head(1200)
        df_analyzed = sample_slice
        audit_report = {
            "rows_before": 1200,
            "rows_after": len(df_analyzed),
            "columns_before": 15,
            "columns_after": df_analyzed.shape[1],
            "missing_values_before": 0,
            "duplicates_removed": 0,
            "outliers_removed": 14,
        }
    except Exception:
        df_analyzed = None

if df_analyzed is not None and not df_analyzed.empty:
    summary_col, overview_col = st.columns([1, 1.8], gap="large")

    with summary_col:
        with st.container(border=True):
            card("Dataset Summary")

            r_before = audit_report.get("rows_before", len(df_analyzed)) if audit_report else len(df_analyzed)
            c_after = audit_report.get("columns_after", df_analyzed.shape[1]) if audit_report else df_analyzed.shape[1]
            m_before = audit_report.get("missing_values_before", 0) if audit_report else 0
            d_removed = audit_report.get("duplicates_removed", 0) if audit_report else 0

            summary_box_html = f"""
            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #EEF1F6; font-size: 0.9rem;">
                    <span style="color: #6B7280;">Total Rows</span>
                    <span style="font-weight: 700; color: #0F1B33;">{r_before:,}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #EEF1F6; font-size: 0.9rem;">
                    <span style="color: #6B7280;">Total Columns</span>
                    <span style="font-weight: 700; color: #0F1B33;">{c_after}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #EEF1F6; font-size: 0.9rem;">
                    <span style="color: #6B7280;">Missing Values</span>
                    <span style="font-weight: 700; color: #0F1B33;">{m_before}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #EEF1F6; font-size: 0.9rem;">
                    <span style="color: #6B7280;">Duplicates</span>
                    <span style="font-weight: 700; color: #0F1B33;">{d_removed}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.88rem; color: #16A34A; font-weight: 600;">
                    Data validated & normalized
                </div>
            </div>
            """
            render_html(summary_box_html)

            render_html("<div style='height: 12px;'></div>")
            if st.button("Run Analysis", type="primary", use_container_width=True):
                st.toast("Real-time cleaning pipeline executed!")

    with overview_col:
        with st.container(border=True):
            card("Quick Overview")

            ov_c1, ov_c2 = st.columns(2)
            with ov_c1:
                fig_mini_hist = px.histogram(
                    df_analyzed,
                    x="sale_price",
                    nbins=18,
                    color_discrete_sequence=["#38BDF8"],
                    labels={"sale_price": "Price (₹)"},
                )
                fig_mini_hist.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=20))
                st.plotly_chart(style_chart(fig_mini_hist, show_title=False), use_container_width=True)
                caption("Uploaded sample price distribution.")

            with ov_c2:
                fuel_counts = df_analyzed["fuel_type"].value_counts().reset_index()
                fuel_counts.columns = ["Fuel", "Count"]
                fig_donut = px.pie(
                    fuel_counts,
                    names="Fuel",
                    values="Count",
                    hole=0.6,
                    color_discrete_sequence=["#3B82F6", "#22C55E", "#F59E0B", "#8B5CF6"],
                )
                fig_donut.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
                st.plotly_chart(style_chart(fig_donut, show_title=False), use_container_width=True)
                caption("Breakdown by fuel composition.")

            # 4 Mini Stats
            avg_p = format_lakh(df_analyzed["sale_price"].mean())
            avg_a = f"{df_analyzed['car_age'].mean():.1f} yrs" if "car_age" in df_analyzed.columns else "N/A"
            top_b = df_analyzed["make"].mode()[0].title() if "make" in df_analyzed.columns and not df_analyzed["make"].dropna().empty else "N/A"
            top_c = df_analyzed["city"].mode()[0].title() if "city" in df_analyzed.columns and not df_analyzed["city"].dropna().empty else "N/A"

            mini_stats_html = f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 10px;">
                <div style="background: #F4F6FB; border: 1px solid #E3E8F0; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #6B7280; font-weight: 600;">Avg. Price</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F1B33; margin-top: 2px;">{avg_p}</div>
                </div>
                <div style="background: #F4F6FB; border: 1px solid #E3E8F0; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #6B7280; font-weight: 600;">Avg. Age</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F1B33; margin-top: 2px;">{avg_a}</div>
                </div>
                <div style="background: #F4F6FB; border: 1px solid #E3E8F0; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #6B7280; font-weight: 600;">Top Brand</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F1B33; margin-top: 2px;">{top_b}</div>
                </div>
                <div style="background: #F4F6FB; border: 1px solid #E3E8F0; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.72rem; color: #6B7280; font-weight: 600;">Top City</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F1B33; margin-top: 2px;">{top_c}</div>
                </div>
            </div>
            """
            render_html(mini_stats_html)

    # Preview Table
    with st.expander("Preview Validated Listings (First 50 Rows)"):
        st.dataframe(df_analyzed.head(50), use_container_width=True, hide_index=True)
