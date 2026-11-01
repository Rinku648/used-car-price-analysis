"""Design system components, layout helpers, and dataset access for AutoInsight."""
import base64
import os
from typing import Any
import pandas as pd
import streamlit as st

from src.data_loader import load_data


# -----------------------------------------------------------------------------
# Safe HTML Renderer (Prevents Markdown 4-space code block interpretation)
# -----------------------------------------------------------------------------

def render_html(html_str: str) -> None:
    """
    Render HTML safely.
    Strips leading whitespace from every line to ensure Markdown never
    accidentally interprets indentation as a <pre><code> block.
    """
    cleaned_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown("\n".join(cleaned_lines), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Dataset Access Helpers
# -----------------------------------------------------------------------------

def page_data() -> pd.DataFrame | None:
    """Load the bundled dataset and show a friendly error if it is unavailable."""
    try:
        return load_data()
    except Exception as error:
        st.error(f"Could not load the project dataset: {error}")
        st.info("Check that data/used_cars_cleaned.csv exists and has the expected columns.")
        return None


def sidebar_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Show interactive filters and return matching rows (backward compatibility)."""
    st.sidebar.markdown("### Filters")
    result = data.copy()
    makes = sorted(result["make"].dropna().unique().tolist())
    selected = st.sidebar.multiselect("Brand", makes, default=makes)
    if selected:
        result = result[result["make"].isin(selected)]
    for label, column in [("Fuel", "fuel_type"), ("Transmission", "transmission"), ("City", "city")]:
        options = sorted(result[column].dropna().unique().tolist())
        values = st.sidebar.multiselect(label, options, default=options)
        if values:
            result = result[result[column].isin(values)]
    low_year, high_year = int(data["yr_mfr"].min()), int(data["yr_mfr"].max())
    years = st.sidebar.slider("Manufacture year", low_year, high_year, (low_year, high_year))
    result = result[result["yr_mfr"].between(years[0], years[1])]
    low_price, high_price = int(data["sale_price"].min()), int(data["sale_price"].max())
    prices = st.sidebar.slider("Sale price (₹)", low_price, high_price, (low_price, high_price), step=10000)
    return result[result["sale_price"].between(prices[0], prices[1])]


# -----------------------------------------------------------------------------
# Global CSS Injection
# -----------------------------------------------------------------------------

def inject_css() -> None:
    """
    Inject global styles matching the AutoInsight design specification:
    - Dark navy sidebar (#0B1B3A) with crisp white/silver text (NO black text!)
    - Active nav pill (#2F6FEB) with pure white text
    - Light grey canvas (#F4F6FB)
    - White rounded cards (#FFFFFF, radius 12px, border #E3E8F0, shadow)
    - Heading text (#0F1B33), muted text (#6B7280), primary blue (#2563EB)
    - Inter font family from Google Fonts
    - Hide default Streamlit navigation, footer, and hamburger menu
    """
    css_content = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

    /* Base Typography & Canvas */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #F4F6FB !important;
        color: #0F1B33 !important;
    }

    /* Preserve Material Symbols so ligature words render as icons */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [data-testid="stIconMaterial"],
    span[data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] * {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 20px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Hide Streamlit Default UI Chrome */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 10 !important;
    }

    /* Hide Default Streamlit Sidebar Auto-Navigation */
    [data-testid="stSidebarNav"] { display: none !important; }
    ul[data-testid="stSidebarNavItems"] { display: none !important; }

    /* =========================================================================
       SIDEBAR STYLING & HIGH-CONTRAST TEXT (NO BLACK TEXT IN SIDEBAR)
       ========================================================================= */
    section[data-testid="stSidebar"] {
        background-color: #0B1B3A !important;
        border-right: 1px solid #16284F !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding: 1.0rem 0.8rem !important;
        background-color: #0B1B3A !important;
    }

    /* Hide the raw collapse button text at the top of the sidebar */
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Force all base sidebar elements to light silver/white */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] a {
        color: #E2E8F0 !important;
    }

    /* Sidebar Brand Header */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 8px 18px 8px;
        margin-bottom: 14px;
        border-bottom: 1px solid #16284F;
    }

    .brand-logo-img {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: block;
    }

    .brand-title {
        font-size: 1.20rem;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: -0.3px;
    }

    /* Inactive Sidebar Links */
    [data-testid="stSidebar"] a {
        border-radius: 8px !important;
        padding: 8px 14px !important;
        transition: all 0.15s ease-in-out !important;
        background-color: transparent !important;
        text-decoration: none !important;
    }

    [data-testid="stSidebar"] a *,
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] * {
        color: #CBD5E1 !important;
        fill: #CBD5E1 !important;
        font-size: 0.90rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] a:hover {
        background-color: #16284F !important;
    }

    [data-testid="stSidebar"] a:hover *,
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Active Nav Pill: Vibrant blue with PURE WHITE TEXT (#FFFFFF) */
    .nav-pill-active,
    .nav-pill-active a,
    .nav-pill-active [data-testid="stPageLink-NavLink"],
    .nav-pill-active a[data-testid="stPageLink-NavLink"] {
        background-color: #2F6FEB !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(47, 111, 235, 0.45) !important;
    }

    .nav-pill-active *,
    .nav-pill-active a *,
    .nav-pill-active [data-testid="stPageLink-NavLink"] *,
    .nav-pill-active a[data-testid="stPageLink-NavLink"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar Footer */
    .sidebar-footer-box {
        margin-top: 28px;
        padding: 14px 8px 4px 8px;
        border-top: 1px solid #16284F;
        font-size: 0.75rem;
    }
    .sidebar-footer-title {
        color: #94A3B8 !important;
        font-weight: 500 !important;
    }
    .sidebar-footer-ver {
        color: #64748B !important;
        margin-top: 2px !important;
    }

    /* =========================================================================
       PAGE HEADERS & HERO STYLING
       ========================================================================= */
    /* Status Dots and Micro-Badges */
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
    }
    .status-dot-green {
        background-color: #10B981;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
    }
    .status-dot-blue {
        background-color: #2563EB;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25);
    }
    .status-dot-purple {
        background-color: #7C3AED;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.25);
    }
    .status-dot-amber {
        background-color: #F59E0B;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25);
    }
    .status-dot-teal {
        background-color: #0D9488;
        box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.25);
    }
    .status-dot-red {
        background-color: #DC2626;
        box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.25);
    }

    .eyebrow-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #2563EB;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .page-header-title {
        font-size: 28px;
        font-weight: 800;
        color: #0F1B33;
        letter-spacing: -0.6px;
        margin: 0;
        line-height: 1.2;
    }

    .page-header-subtitle {
        font-size: 1.02rem;
        font-weight: 500;
        color: #475569;
        margin-top: 6px;
        margin-bottom: 12px;
    }

    .page-header-desc {
        font-size: 0.92rem;
        color: #6B7280;
        line-height: 1.55;
        max-width: 680px;
    }

    /* Cards & Border Wrappers */
    .ui-card {
        background: #FFFFFF;
        border: 1px solid #E3E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(15, 27, 51, 0.06);
        margin-bottom: 16px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #E3E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(15, 27, 51, 0.06) !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
    }

    .card-heading {
        font-size: 16px;
        font-weight: 600;
        color: #0F1B33;
        margin-bottom: 10px;
    }

    /* KPI Cards in One Row */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin: 22px 0;
    }

    .kpi-card-box {
        background: #FFFFFF;
        border: 1px solid #E3E8F0;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(15, 27, 51, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 90px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi-card-box:hover {
        box-shadow: 0 4px 12px rgba(15, 27, 51, 0.08);
        border-color: #CBD5E1;
    }

    .kpi-card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }

    .kpi-micro-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 2px 6px;
        font-size: 10px;
        font-weight: 700;
        color: #475569;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .kpi-label-text {
        font-size: 0.8rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: capitalize;
    }

    .kpi-val-text {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0F1B33;
        letter-spacing: -0.5px;
        margin-top: 6px;
    }

    /* Step Cards */
    .steps-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-top: 14px;
    }

    .step-card-box {
        background: #FFFFFF;
        border: 1px solid #E3E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 27, 51, 0.05);
    }

    .step-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }

    .step-num-badge {
        font-size: 0.82rem;
        font-weight: 700;
        color: #2563EB;
        background: #EFF6FF;
        width: 22px;
        height: 22px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .step-title-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0F1B33;
    }

    .step-desc-text {
        font-size: 0.85rem;
        color: #6B7280;
        line-height: 1.45;
    }

    /* Badges */
    .ui-badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-success {
        background-color: #DCFCE7;
        color: #16A34A;
        border: 1px solid #BBF7D0;
    }

    .badge-primary {
        background-color: #DBEAFE;
        color: #2563EB;
        border: 1px solid #BFDBFE;
    }

    .badge-warning {
        background-color: #FEF3C7;
        color: #D97706;
        border: 1px solid #FDE68A;
    }

    .badge-danger {
        background-color: #FEE2E2;
        color: #DC2626;
        border: 1px solid #FECACA;
    }

    /* Info Banner */
    .ui-info-banner {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 16px 0;
        color: #1E40AF;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    /* Small Muted Caption Under Charts */
    .chart-caption-muted {
        font-size: 12px;
        color: #6B7280;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* Buttons Styling */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #0B1B3A !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1B3A !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #16284F !important;
        border-color: #16284F !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid #E3E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        font-weight: 600;
        color: #6B7280;
    }

    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 2px solid #2563EB !important;
    }
    </style>
    """
    render_html(css_content)


# -----------------------------------------------------------------------------
# Custom Navigation Sidebar (Clean, Professional Text Links - No Emojis)
# -----------------------------------------------------------------------------

def render_sidebar(active_page: str = "Home") -> None:
    """
    Render the custom AutoInsight dark navy sidebar with:
    - Vector SVG Logo + Brand name at top
    - Professional clean text navigation links (no emojis)
    - Active highlight pill
    - Version info at bottom
    """
    with st.sidebar:
        logo_path = os.path.join("assets", "logo.svg")
        logo_html = ""
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "r", encoding="utf-8") as f:
                    svg_content = f.read()
                    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
                    logo_html = f'<img src="data:image/svg+xml;base64,{encoded}" class="brand-logo-img" alt="AutoInsight Logo" />'
            except Exception:
                logo_html = '<div style="width: 28px; height: 28px; background: #2563EB; border-radius: 6px;"></div>'
        else:
            logo_html = '<div style="width: 28px; height: 28px; background: #2563EB; border-radius: 6px;"></div>'

        brand_html = f"""
        <div class="sidebar-brand-box">
            {logo_html}
            <div class="brand-title">AutoInsight</div>
        </div>
        """
        render_html(brand_html)

        # Navigation links without emojis
        nav_items = [
            ("Home", "app.py"),
            ("Data Explorer", "pages/1_Data_Explorer.py"),
            ("EDA Dashboard", "pages/2_EDA_Dashboard.py"),
            ("Statistical Tests", "pages/3_Statistical_Tests.py"),
            ("Fair Price Estimator", "pages/4_Fair_Price_Estimator.py"),
            ("Brand Depreciation", "pages/5_Brand_Depreciation.py"),
            ("Upload & Analyze", "pages/6_Upload_and_Analyze.py"),
            ("Insights & Recommendations", "pages/7_Insights_and_Recommendations.py"),
        ]

        for label, page_target in nav_items:
            is_active = (label.lower() == active_page.lower())
            wrapper_class = "nav-pill-active" if is_active else "nav-pill-normal"
            render_html(f'<div class="{wrapper_class}">')
            try:
                st.page_link(page_target, label=label)
            except Exception:
                render_html(f'<div style="padding: 8px 14px; color: #FFFFFF;">{label}</div>')
            render_html("</div>")

        footer_html = """
        <div class="sidebar-footer-box">
            <div class="sidebar-footer-title">Used Car Price Analysis</div>
            <div class="sidebar-footer-ver">v1.0</div>
        </div>
        """
        render_html(footer_html)


# -----------------------------------------------------------------------------
# Reusable Design System UI Elements
# -----------------------------------------------------------------------------

def page_header(title: str, subtitle: str, eyebrow: str = "DATA · INSIGHTS · BETTER DECISIONS") -> None:
    """Render consistent page headers with a clean indicator dot."""
    eyebrow_content = f'<div class="eyebrow-tag"><span class="status-dot status-dot-blue"></span>{eyebrow}</div>' if eyebrow else ''
    header_html = f"""
    <div style="margin-bottom: 20px;">
        {eyebrow_content}
        <h1 class="page-header-title">{title}</h1>
        <div class="page-header-subtitle">{subtitle}</div>
    </div>
    """
    render_html(header_html)


def kpi_card(label: str, value: str, tag: str = "", dot: str = "blue") -> str:
    """Generate clean HTML for a single professional KPI card with micro-tag status dot."""
    tag_html = ""
    if tag:
        tag_html = f'<div class="kpi-micro-tag"><span class="status-dot status-dot-{dot}"></span>{tag}</div>'
    return f"""
    <div class="kpi-card-box">
        <div class="kpi-card-top">
            <span class="kpi-label-text">{label}</span>
            {tag_html}
        </div>
        <div class="kpi-val-text">{value}</div>
    </div>
    """


def render_kpi_row(metrics: list[dict[str, str]]) -> None:
    """Render an array of KPI cards in a 5-column responsive row."""
    inner_cards = "".join([
        kpi_card(
            m["label"],
            m["value"],
            m.get("tag", ""),
            m.get("dot", "blue")
        ) for m in metrics
    ])
    full_html = f'<div class="kpi-row">{inner_cards}</div>'
    render_html(full_html)


def card(title: str) -> None:
    """Render a card heading inside a container."""
    render_html(f'<div class="card-heading">{title}</div>')


def badge(text: str, kind: str = "success", show_dot: bool = True) -> str:
    """Generate HTML for a status badge with an indicator dot."""
    badge_class = f"badge-{kind}"
    dot_map = {
        "success": "green",
        "primary": "blue",
        "warning": "amber",
        "danger": "red",
        "purple": "purple",
    }
    dot_color = dot_map.get(kind, "blue")
    dot_html = f'<span class="status-dot status-dot-{dot_color}" style="margin-right: 5px;"></span>' if show_dot else ""
    return f'<span class="ui-badge {badge_class}">{dot_html}{text}</span>'


def info_banner(text: str) -> None:
    """Render a clean informational callout banner."""
    render_html(f'<div class="ui-info-banner">{text}</div>')


def caption(text: str) -> None:
    """Render small muted caption text under a chart or figure."""
    render_html(f'<div class="chart-caption-muted">{text}</div>')
