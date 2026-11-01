"""Shared Plotly styling and reusable chart builders matching the SaaS design system."""
import plotly.express as px
import plotly.graph_objects as go

# Design system primary palette: Blue, Green, Purple, Amber, Teal
CHART_PALETTE = ["#3B82F6", "#22C55E", "#8B5CF6", "#F59E0B", "#14B8A6", "#EC4899", "#64748B"]


def style_chart(fig: go.Figure, show_title: bool = False, title_text: str | None = None) -> go.Figure:
    """
    Apply shared analytics SaaS styling to any Plotly chart:
    - Transparent/white paper and plot background
    - Inter font family
    - Light gridlines (#EEF1F6)
    - Legend oriented horizontally at the bottom
    - Clean margins and subtle axis lines
    """
    fig.update_layout(
        template="plotly_white",
        colorway=CHART_PALETTE,
        title=dict(
            text=f"<b>{title_text}</b>" if (show_title and title_text) else None,
            font=dict(size=14, color="#0F1B33", family="Inter, sans-serif"),
            x=0.02,
            y=0.96,
        ) if show_title else None,
        margin=dict(l=24, r=24, t=30 if show_title else 15, b=35),
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#6B7280", family="Inter, sans-serif"),
        ),
        font=dict(family="Inter, sans-serif", color="#0F1B33", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            gridcolor="#EEF1F6",
            linecolor="#E3E8F0",
            tickfont=dict(color="#6B7280", size=11),
            title_font=dict(color="#475569", size=12),
        ),
        yaxis=dict(
            gridcolor="#EEF1F6",
            linecolor="#E3E8F0",
            tickfont=dict(color="#6B7280", size=11),
            title_font=dict(color="#475569", size=12),
        ),
    )
    return fig


# Backward-compatible alias
style = style_chart


def histogram(data, column: str, title: str | None = None, color: str = "#3B82F6", labels: dict | None = None, nbins: int = 30):
    """Generate a clean styled histogram."""
    fig = px.histogram(
        data,
        x=column,
        nbins=nbins,
        labels=labels,
        color_discrete_sequence=[color],
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color="#FFFFFF")))
    return style_chart(fig, show_title=False)


def scatter(data, x: str, y: str, title: str | None = None, color: str | None = None, labels: dict | None = None):
    """Generate a scatter plot with an OLS regression trendline."""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        opacity=0.6,
        trendline="ols",
        trendline_color_override="#DC2626",
        labels=labels,
        color_discrete_sequence=CHART_PALETTE,
    )
    fig.update_traces(marker=dict(size=6))
    return style_chart(fig, show_title=False)


def box(data, x: str, y: str, title: str | None = None):
    """Generate category box plots showing median and spread."""
    fig = px.box(data, x=x, y=y, points="outliers", color=x, color_discrete_sequence=CHART_PALETTE)
    return style_chart(fig, show_title=False)


def bar_chart(data, x: str, y: str, title: str | None = None, color: str | None = None, color_discrete_sequence: list | None = None, labels: dict | None = None):
    """Generate a clean category bar chart."""
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color or x,
        labels=labels,
        color_discrete_sequence=color_discrete_sequence or CHART_PALETTE,
    )
    fig.update_layout(showlegend=False)
    return style_chart(fig, show_title=False)
