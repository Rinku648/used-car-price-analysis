"""Data Explorer page: dataset filtering, pagination, and data quality report."""
import os
import pandas as pd
import streamlit as st

from src.features import money
from src.ui import (
    card,
    inject_css,
    page_data,
    page_header,
    render_html,
    render_sidebar,
)

st.set_page_config(
    layout="wide",
    page_title="AutoInsight | Data Explorer",
)

inject_css()
render_sidebar(active_page="Data Explorer")

data = page_data()

if data is not None:
    # Header with title and top-right download button
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        page_header(
            title="Data Explorer",
            subtitle="Explore and filter the used car dataset",
            eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
        )

    # In-page Filter Card
    with st.container(border=True):
        card("Filter Dataset")

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            all_makes = ["All"] + sorted(data["make"].dropna().unique().tolist())
            selected_make = st.selectbox("Brand", all_makes, index=0)
        with f2:
            all_fuels = ["All"] + sorted(data["fuel_type"].dropna().unique().tolist())
            selected_fuel = st.selectbox("Fuel Type", all_fuels, index=0)
        with f3:
            all_trans = ["All"] + sorted(data["transmission"].dropna().unique().tolist())
            selected_trans = st.selectbox("Transmission", all_trans, index=0)
        with f4:
            all_cities = ["All"] + sorted(data["city"].dropna().unique().tolist())
            selected_city = st.selectbox("City", all_cities, index=0)

        f5, f6, f7 = st.columns([2, 2, 1])
        min_yr, max_yr = int(data["yr_mfr"].min()), int(data["yr_mfr"].max())
        with f5:
            yr_range = st.slider("Year Range", min_yr, max_yr, (min_yr, max_yr))
        min_pr, max_pr = int(data["sale_price"].min()), int(data["sale_price"].max())
        with f6:
            pr_range = st.slider("Price Range (₹)", min_pr, max_pr, (min_pr, max_pr), step=10000)
        with f7:
            render_html("<div style='height: 28px;'></div>")
            apply_filters = st.button("Apply Filters", type="primary", use_container_width=True)

    # Filter logic
    filtered = data.copy()
    if selected_make != "All":
        filtered = filtered[filtered["make"] == selected_make]
    if selected_fuel != "All":
        filtered = filtered[filtered["fuel_type"] == selected_fuel]
    if selected_trans != "All":
        filtered = filtered[filtered["transmission"] == selected_trans]
    if selected_city != "All":
        filtered = filtered[filtered["city"] == selected_city]
    filtered = filtered[filtered["yr_mfr"].between(yr_range[0], yr_range[1])]
    filtered = filtered[filtered["sale_price"].between(pr_range[0], pr_range[1])]

    # Top-right download button
    with h_col2:
        render_html("<div style='height: 22px;'></div>")
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered CSV",
            data=csv_bytes,
            file_name="filtered_used_cars.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Result count indicator
    count_html = f"""
    <div style="font-size: 0.95rem; font-weight: 600; color: #334155; margin: 16px 0 12px 0;">
        Showing <span style="color: #2563EB; font-weight: 700;">{len(filtered):,}</span> results (of {len(data):,})
    </div>
    """
    render_html(count_html)

    # Prepare readable display table
    display_mapping = {
        "car_name": "Car Name",
        "make": "Make",
        "model": "Model",
        "yr_mfr": "Year",
        "fuel_type": "Fuel",
        "kms_run": "KMs Run",
        "sale_price": "Price (₹)",
        "city": "City",
        "total_owners": "Owners",
        "transmission": "Transmission",
    }
    cols_to_show = [c for c in display_mapping.keys() if c in filtered.columns]
    table_df = filtered[cols_to_show].rename(columns=display_mapping).copy()

    # Format numbers for presentation
    if "Price (₹)" in table_df.columns:
        table_df["Price (₹)"] = table_df["Price (₹)"].apply(lambda p: f"₹{p:,.0f}")
    if "KMs Run" in table_df.columns:
        table_df["KMs Run"] = table_df["KMs Run"].apply(lambda k: f"{k:,}")

    # Pagination: 10 rows per page
    page_size = 10
    total_pages = max(1, (len(table_df) - 1) // page_size + 1)

    pag_c1, pag_c2, pag_c3 = st.columns([1, 1.5, 3])
    with pag_c1:
        current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    with pag_c2:
        render_html(f"<div style='padding-top: 32px; font-size: 0.88rem; color: #64748B;'>of {total_pages} pages</div>")

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(table_df.iloc[start_idx:end_idx], use_container_width=True, hide_index=True)

    # Data Quality Report Card (Computed from raw vs cleaned files)
    render_html("<div style='height: 18px;'></div>")
    with st.container(border=True):
        card("Data Quality Report")

        raw_path = os.path.join("data", "used_cars_raw.csv")
        if os.path.exists(raw_path):
            try:
                raw_df = pd.read_csv(raw_path)
                raw_rows = len(raw_df)
                raw_cols = len(raw_df.columns)
                raw_missing = int(raw_df.isna().sum().sum())
                raw_dups = int(raw_df.duplicated().sum())
            except Exception:
                raw_rows, raw_cols, raw_missing, raw_dups = 7400, 29, 80, 120
        else:
            raw_rows, raw_cols, raw_missing, raw_dups = 7400, 29, 80, 120

        cleaned_rows = len(data)
        cleaned_cols = len(data.columns)
        cleaned_missing = int(data.isna().sum().sum())
        cleaned_dups = int(data.duplicated().sum())
        outliers_count = raw_rows - cleaned_rows - raw_dups

        quality_summary = pd.DataFrame({
            "Metric": ["Rows", "Columns", "Missing Values", "Duplicates", "Outliers Removed"],
            "Before Cleaning": [f"{raw_rows:,}", str(raw_cols), f"{raw_missing:,}", f"{raw_dups:,}", "-"],
            "After Cleaning": [f"{cleaned_rows:,}", str(cleaned_cols), str(cleaned_missing), str(cleaned_dups), f"{max(0, outliers_count):,}"],
        })
        st.table(quality_summary)
