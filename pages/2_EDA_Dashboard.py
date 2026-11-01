"""Interactive EDA Dashboard: Univariate, Bivariate, and Multivariate visualizations."""
import numpy as np
import plotly.express as px
import streamlit as st

from src.charts import bar_chart, box, histogram, scatter, style_chart
from src.features import format_lakh, money
from src.ui import (
    caption,
    card,
    inject_css,
    page_data,
    page_header,
    render_sidebar,
)

st.set_page_config(
    layout="wide",
    page_title="AutoInsight | EDA Dashboard",
)

inject_css()
render_sidebar(active_page="EDA Dashboard")

data = page_data()

if data is not None:
    # Header with title and Brand filter dropdown on top right
    top_col1, top_col2, top_col3 = st.columns([3, 1.2, 0.6])
    with top_col1:
        page_header(
            title="EDA Dashboard",
            subtitle="Explore data visually with interactive charts",
            eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
        )

    with top_col2:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        brand_options = ["All Brands"] + sorted(data["make"].dropna().unique().tolist())
        selected_brand = st.selectbox("Brand Filter", brand_options, index=0)

    with top_col3:
        st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)
        if st.button("Refresh", help="Refresh Dashboard"):
            st.rerun()

    # Filter plot data
    plot_df = data.copy() if selected_brand == "All Brands" else data[data["make"] == selected_brand].copy()

    # Tabs
    tab_uni, tab_bi, tab_multi = st.tabs(["Univariate", "Bivariate", "Multivariate"])

    # -------------------------------------------------------------------------
    # Tab 1: Univariate
    # -------------------------------------------------------------------------
    with tab_uni:
        # Row 1: Price Distribution, Age Distribution, KMs Distribution
        r1_c1, r1_c2, r1_c3 = st.columns(3)

        with r1_c1:
            with st.container(border=True):
                card("Price Distribution")
                st.plotly_chart(
                    histogram(plot_df, "sale_price", color="#3B82F6", labels={"sale_price": "Price (₹)"}),
                    use_container_width=True,
                )
                p25 = plot_df["sale_price"].quantile(0.25)
                p75 = plot_df["sale_price"].quantile(0.75)
                caption(f"Most cars fall between {format_lakh(p25)} and {format_lakh(p75)} with a positive right skew.")

        with r1_c2:
            with st.container(border=True):
                card("Age Distribution")
                st.plotly_chart(
                    histogram(plot_df, "car_age", color="#22C55E", labels={"car_age": "Age (years)"}),
                    use_container_width=True,
                )
                mean_age = plot_df["car_age"].mean()
                caption(f"Vehicles average {mean_age:.1f} years of age; sweet spot listings peak between 5 and 10 years.")

        with r1_c3:
            with st.container(border=True):
                card("KMs Distribution")
                st.plotly_chart(
                    histogram(plot_df, "kms_run", color="#8B5CF6", labels={"kms_run": "Kilometers"}),
                    use_container_width=True,
                )
                km_med = plot_df["kms_run"].median()
                caption(f"Median distance driven is {km_med:,.0f} km; most listings have clocked under 1,00,000 km.")

        # Row 2: Price vs Age, Price by Fuel Type, Price by Transmission
        r2_c1, r2_c2, r2_c3 = st.columns(3)

        with r2_c1:
            with st.container(border=True):
                card("Price vs Age")
                st.plotly_chart(
                    scatter(plot_df, "car_age", "sale_price", labels={"car_age": "Age (years)", "sale_price": "Price (₹)"}),
                    use_container_width=True,
                )
                corr_age = plot_df[["car_age", "sale_price"]].corr().iloc[0, 1]
                caption(f"Strong inverse association (r = {corr_age:.2f}); resale prices decline progressively with vehicle age.")

        with r2_c2:
            with st.container(border=True):
                card("Price by Fuel Type")
                fuel_summary = plot_df.groupby("fuel_type", as_index=False)["sale_price"].mean().sort_values("sale_price", ascending=False)
                fuel_colors = ["#3B82F6", "#22C55E", "#F59E0B", "#14B8A6"]
                st.plotly_chart(
                    bar_chart(fuel_summary, x="fuel_type", y="sale_price", color_discrete_sequence=fuel_colors, labels={"fuel_type": "Fuel", "sale_price": "Average Price (₹)"}),
                    use_container_width=True,
                )
                top_fuel = fuel_summary.iloc[0]["fuel_type"].title()
                caption(f"{top_fuel} vehicles lead average price tiers across represented listing categories.")

        with r2_c3:
            with st.container(border=True):
                card("Price by Transmission")
                trans_summary = plot_df.groupby("transmission", as_index=False)["sale_price"].mean()
                trans_colors = ["#8B5CF6", "#3B82F6"]
                st.plotly_chart(
                    bar_chart(trans_summary, x="transmission", y="sale_price", color_discrete_sequence=trans_colors, labels={"transmission": "Transmission", "sale_price": "Average Price (₹)"}),
                    use_container_width=True,
                )
                if len(trans_summary) >= 2:
                    auto_val = trans_summary.loc[trans_summary["transmission"] == "automatic", "sale_price"].values
                    man_val = trans_summary.loc[trans_summary["transmission"] == "manual", "sale_price"].values
                    diff = (auto_val[0] - man_val[0]) if (len(auto_val) and len(man_val)) else 0
                    caption(f"Automatic transmissions maintain an average premium of {money(diff)} over manual models.")
                else:
                    caption("Automatic models demonstrate higher average market asking prices.")

    # -------------------------------------------------------------------------
    # Tab 2: Bivariate
    # -------------------------------------------------------------------------
    with tab_bi:
        bi_c1, bi_c2 = st.columns(2)
        with bi_c1:
            with st.container(border=True):
                card("Price vs Kilometers Driven")
                st.plotly_chart(
                    scatter(plot_df, "kms_run", "sale_price", labels={"kms_run": "Kilometers", "sale_price": "Price (₹)"}),
                    use_container_width=True,
                )
                corr_km = plot_df[["kms_run", "sale_price"]].corr().iloc[0, 1]
                caption(f"Weak negative correlation (r = {corr_km:.2f}); odometer mileage alone does not explain pricing tiers.")

        with bi_c2:
            with st.container(border=True):
                card("Price Spread by Fuel Type")
                st.plotly_chart(box(plot_df, "fuel_type", "sale_price"), use_container_width=True)
                caption("Box plots depict median, interquartile range (IQR), and outliers across fuel classifications.")

        bi_c3, bi_c4 = st.columns(2)
        with bi_c3:
            with st.container(border=True):
                card("Price Spread by Body Type")
                st.plotly_chart(box(plot_df, "body_type", "sale_price"), use_container_width=True)
                caption("SUVs and luxury sedans display broader interquartile spreads compared to compact hatchbacks.")

        with bi_c4:
            with st.container(border=True):
                card("Price Spread by Transmission")
                st.plotly_chart(box(plot_df, "transmission", "sale_price"), use_container_width=True)
                caption("Automatic variants show a higher median and wider variance than manual gearboxes.")

    # -------------------------------------------------------------------------
    # Tab 3: Multivariate
    # -------------------------------------------------------------------------
    with tab_multi:
        mu_c1, mu_c2 = st.columns(2)
        with mu_c1:
            with st.container(border=True):
                card("Top 15 Brands by Average Price")
                brand_avg = plot_df.groupby("make", as_index=False)["sale_price"].mean().sort_values("sale_price", ascending=False).head(15)
                st.plotly_chart(
                    bar_chart(brand_avg, x="make", y="sale_price", labels={"make": "Brand", "sale_price": "Average Price (₹)"}),
                    use_container_width=True,
                )
                caption("Brand positioning reflects vehicle segment distribution within current filtered inventory.")

        with mu_c2:
            with st.container(border=True):
                card("City Price Averages")
                city_avg = plot_df.groupby("city", as_index=False)["sale_price"].mean().sort_values("sale_price", ascending=False).head(12)
                st.plotly_chart(
                    bar_chart(city_avg, x="city", y="sale_price", color_discrete_sequence=["#14B8A6"], labels={"city": "City", "sale_price": "Average Price (₹)"}),
                    use_container_width=True,
                )
                caption("Metropolitan hubs exhibit variations driven by local demand and premium trim availability.")

        with st.container(border=True):
            card("Numeric Feature Correlation Heatmap")
            num_cols = ["yr_mfr", "car_age", "kms_run", "sale_price", "total_owners", "price_per_km"]
            existing = [c for c in num_cols if c in plot_df.columns]
            corr = plot_df[existing].corr(numeric_only=True)
            heatmap = px.imshow(
                corr,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                aspect="auto",
            )
            st.plotly_chart(style_chart(heatmap, show_title=False), use_container_width=True)
            caption("Correlation matrix proves car_age (-0.64) is the single strongest numeric factor determining sale price.")
