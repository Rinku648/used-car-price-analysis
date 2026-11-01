"""Global styling, layout and UI components for AutoInsight."""
import streamlit as st

PRIMARY_COLOR = "#2563eb"
SIDEBAR_BG = "#0f172a"
PAGE_BG = "#f8fafc"
CARD_BG = "#ffffff"
TEXT_COLOR = "#0f172a"
MUTED_COLOR = "#64748b"


def inject_custom_css():
    """Inject custom CSS rules to match the AutoInsight design."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        /* Global Typography & Canvas */
        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        .stApp {
            background-color: #f8fafc;
            color: #0f172a;
        }

        /* Hide Streamlit default header decoration but keep header accessible */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            z-index: 10;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 1.2rem;
            color: #cbd5e1;
        }

        /* Sidebar Brand & Logo */
        .sidebar-brand-box {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 14px 20px 14px;
            border-bottom: 1px solid #1e293b;
            margin-bottom: 16px;
        }

        .brand-logo-icon {
            background: linear-gradient(135deg, #2563eb, #38bdf8);
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4);
        }

        .brand-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.3px;
        }

        /* Sidebar Nav Links */
        section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"] {
            gap: 4px;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
            color: #94a3b8 !important;
            font-size: 0.88rem;
            font-weight: 500;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
            border-radius: 8px;
            padding: 8px 12px;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
            background-color: #1e293b !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #2563eb !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: #ffffff !important;
            font-weight: 600;
        }

        /* Sidebar Footer */
        .sidebar-footer-box {
            margin-top: 30px;
            padding: 16px 14px 10px 14px;
            border-top: 1px solid #1e293b;
            font-size: 0.75rem;
            color: #64748b;
        }
        .sidebar-footer-title {
            color: #94a3b8;
            font-weight: 500;
        }
        .sidebar-footer-ver {
            color: #475569;
            margin-top: 2px;
        }

        /* Eyebrow badge */
        .eyebrow-tag {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #64748b;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        /* Main Headers */
        .page-header-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.6px;
            margin: 0;
            line-height: 1.2;
        }

        .page-header-subtitle {
            font-size: 1.05rem;
            font-weight: 500;
            color: #475569;
            margin-top: 6px;
            margin-bottom: 12px;
        }

        .page-header-desc {
            font-size: 0.92rem;
            color: #64748b;
            line-height: 1.5;
            max-width: 650px;
        }

        /* Cards */
        .ui-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 20px 22px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            margin-bottom: 16px;
        }

        .ui-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* Hero Container */
        .hero-banner {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 28px 32px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            margin-bottom: 24px;
        }

        /* KPI Metric Cards */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .kpi-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 94px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .kpi-card:hover {
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.07);
            border-color: #cbd5e1;
        }

        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

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

        .kpi-micro-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: 700;
            color: #475569;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .kpi-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #64748b;
            text-transform: capitalize;
        }

        .kpi-icon {
            font-size: 1.1rem;
            color: #2563eb;
            background: #eff6ff;
            width: 30px;
            height: 30px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .kpi-value {
            font-size: 1.55rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
            margin-top: 8px;
        }

        /* How to use this site step cards */
        .steps-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 14px;
        }

        .step-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        }

        .step-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }

        .step-number {
            font-size: 0.82rem;
            font-weight: 700;
            color: #2563eb;
            background: #eff6ff;
            width: 22px;
            height: 22px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .step-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #0f172a;
        }

        .step-desc {
            font-size: 0.85rem;
            color: #64748b;
            line-height: 1.4;
        }

        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-green {
            background-color: #ecfdf5;
            color: #059669;
            border: 1px solid #a7f3d0;
        }

        .badge-blue {
            background-color: #eff6ff;
            color: #2563eb;
            border: 1px solid #bfdbfe;
        }

        .badge-amber {
            background-color: #fffbeb;
            color: #d97706;
            border: 1px solid #fde68a;
        }

        /* Chart Takeaway Notes */
        .chart-takeaway {
            background-color: #f8fafc;
            border-top: 1px solid #f1f5f9;
            padding: 8px 12px;
            font-size: 0.8rem;
            color: #64748b;
            border-radius: 0 0 12px 12px;
            margin-top: -6px;
            margin-bottom: 14px;
        }

        /* Deal Verdict Visual Gauge Bar */
        .deal-gauge-wrapper {
            margin: 18px 0;
            padding: 14px;
            background: #f8fafc;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }

        .gauge-track {
            height: 12px;
            border-radius: 6px;
            display: flex;
            overflow: hidden;
            position: relative;
            margin-bottom: 8px;
        }

        .gauge-seg-under {
            flex: 1;
            background: #38bdf8;
        }

        .gauge-seg-fair {
            flex: 2;
            background: #10b981;
        }

        .gauge-seg-over {
            flex: 1;
            background: #f87171;
        }

        .gauge-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748b;
        }

        /* Buttons & Forms styling */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.2rem !important;
            border: none !important;
            transition: all 0.15s ease !important;
        }

        .stButton > button[kind="primary"] {
            background-color: #2563eb !important;
            color: white !important;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
        }

        /* Modern styled tables */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            color: #334155;
        }

        .custom-table th {
            background-color: #f8fafc;
            font-weight: 600;
            text-align: left;
            padding: 10px 14px;
            border-bottom: 1px solid #e2e8f0;
            color: #64748b;
        }

        .custom-table td {
            padding: 10px 14px;
            border-bottom: 1px solid #f1f5f9;
        }

        .custom-table tr:hover {
            background-color: #f8fafc;
        }

        /* Callout Quotes / Banner */
        .quote-banner {
            background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 22px;
            color: #1e3a8a;
            position: relative;
        }

        .quote-text {
            font-size: 0.95rem;
            line-height: 1.5;
            color: #1e3a8a;
            font-weight: 500;
            margin-bottom: 12px;
        }

        .quote-author {
            font-size: 0.82rem;
            font-weight: 700;
            color: #2563eb;
            font-style: italic;
        }

        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid #e2e8f0;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 6px 6px 0 0;
            padding: 8px 16px;
            font-weight: 600;
            color: #64748b;
        }

        .stTabs [aria-selected="true"] {
            color: #2563eb !important;
            border-bottom-color: #2563eb !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_branding():
    """Render the AutoInsight brand header and footer inside the sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="brand-logo-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="3" width="20" height="14" rx="2"></rect>
                        <line x1="8" y1="21" x2="16" y2="21"></line>
                        <line x1="12" y1="17" x2="12" y2="21"></line>
                    </svg>
                </div>
                <div>
                    <div class="brand-title">AutoInsight</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar_footer():
    """Render the sidebar bottom version footer."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-footer-box">
                <div class="sidebar-footer-title">Used Car Price Analysis</div>
                <div class="sidebar-footer-ver">v1.0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_page_header(title: str, subtitle: str, eyebrow: str = "DATA • INSIGHTS • BETTER DECISIONS"):
    """Render consistent page top headers."""
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            {f'<div class="eyebrow-tag">{eyebrow}</div>' if eyebrow else ''}
            <h1 class="page-header-title">{title}</h1>
            <div class="page-header-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(metrics: list[dict]):
    """
    Render 5 or N KPI metric cards in a row with micro-tag status dots.
    metrics: list of dict(label=str, value=str, tag=str, dot=str)
    """
    cards_html = ""
    for m in metrics:
        tag = m.get("tag", "")
        dot = m.get("dot", "blue")
        tag_html = f'<div class="kpi-micro-tag"><span class="status-dot status-dot-{dot}"></span>{tag}</div>' if tag else f'<span class="kpi-icon">{m.get("icon", "")}</span>'
        cards_html += f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">{m['label']}</span>
                {tag_html}
            </div>
            <div class="kpi-value">{m['value']}</div>
        </div>
        """
    st.markdown(f'<div class="kpi-row">{cards_html}</div>', unsafe_allow_html=True)


def render_step_cards(steps: list[dict]):
    """
    Render 'How to use this site' cards.
    steps: list of dict(num=str/int, title=str, desc=str)
    """
    cards_html = ""
    for s in steps:
        cards_html += f"""
        <div class="step-card">
            <div class="step-header">
                <div class="step-number">{s['num']}</div>
                <div class="step-title">{s['title']}</div>
            </div>
            <div class="step-desc">{s['desc']}</div>
        </div>
        """
    st.markdown(f'<div class="steps-row">{cards_html}</div>', unsafe_allow_html=True)

