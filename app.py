"""Home / Overview page for AutoInsight Used Car Price Analysis."""
import streamlit as st

from src.features import format_lakh
from src.ui import (
    inject_css,
    page_data,
    page_header,
    render_html,
    render_kpi_row,
    render_sidebar,
)

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="AutoInsight | Used Car Price Analysis",
)

# Inject design system stylesheet and render custom sidebar navigation
inject_css()
render_sidebar(active_page="Home")

# -----------------------------------------------------------------------------
# Hero Section
# -----------------------------------------------------------------------------
page_header(
    title="Used Car Price Analysis",
    subtitle="A Data-Driven Study of Resale Value Trends in the Indian Used Car Market",
    eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
)
desc_html = """
<div class="page-header-desc" style="max-width: 850px; margin-bottom: 24px;">
    This platform analyzes ~6,800 real used-car listings, shows which factors (age, kilometers, 
    fuel type, transmission, brand, owners, city) influence resale price, proves the findings 
    statistically, and helps you check whether a car's price is fair.
</div>
"""
render_html(desc_html)

# -----------------------------------------------------------------------------
# Live Dataset KPIs (Calculated dynamically, never hardcoded)
# -----------------------------------------------------------------------------
data = page_data()

if data is not None:
    total_listings = f"{len(data):,}"
    avg_price_lakh = format_lakh(data["sale_price"].mean())
    avg_age = f"{data['car_age'].mean():.1f} years"
    total_brands = str(data["make"].nunique())
    total_cities = str(data["city"].nunique())

    kpi_metrics = [
        {"label": "Total Listings", "value": total_listings, "tag": "ACTIVE", "dot": "green"},
        {"label": "Average Price", "value": avg_price_lakh, "tag": "INR", "dot": "blue"},
        {"label": "Average Age", "value": avg_age, "tag": "YEARS", "dot": "purple"},
        {"label": "Total Brands", "value": total_brands, "tag": "MAKES", "dot": "amber"},
        {"label": "Total Cities", "value": total_cities, "tag": "METROS", "dot": "teal"},
    ]
    render_kpi_row(kpi_metrics)

# -----------------------------------------------------------------------------
# "How to use this site" Steps Section
# -----------------------------------------------------------------------------
section_title = """
<div style="margin-top: 28px; margin-bottom: 8px;">
    <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F1B33; margin-bottom: 4px;">How to use this site</h3>
</div>
"""
render_html(section_title)

steps_html = """
<div class="steps-row">
    <div class="step-card-box">
        <div class="step-header">
            <div class="step-num-badge">1</div>
            <div class="step-title-text">Explore data</div>
        </div>
        <div class="step-desc-text">Use filters to find the cars you're interested in and view real listing records.</div>
    </div>
    <div class="step-card-box">
        <div class="step-header">
            <div class="step-num-badge">2</div>
            <div class="step-title-text">Analyze</div>
        </div>
        <div class="step-desc-text">Check EDA charts and statistics to understand resale value trends across groups.</div>
    </div>
    <div class="step-card-box">
        <div class="step-header">
            <div class="step-num-badge">3</div>
            <div class="step-title-text">Get insights</div>
        </div>
        <div class="step-desc-text">Use the estimator and recommendations to make better buying or selling decisions.</div>
    </div>
</div>
"""
render_html(steps_html)
