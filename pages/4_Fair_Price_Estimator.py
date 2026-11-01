"""Fair Price Estimator + Deal Checker (Rule-based, strictly non-ML)."""
import plotly.express as px
import streamlit as st

from src.charts import style_chart
from src.estimator import estimate_price
from src.features import money
from src.ui import (
    badge,
    card,
    caption,
    info_banner,
    inject_css,
    page_data,
    page_header,
    render_html,
    render_sidebar,
)

st.set_page_config(
    layout="wide",
    page_title="AutoInsight | Fair Price Estimator",
)

inject_css()
render_sidebar(active_page="Fair Price Estimator")

page_header(
    title="Fair Price Estimator + Deal Checker",
    subtitle="Check if a car's price is fair using real listings",
    eyebrow="DATA · INSIGHTS · BETTER DECISIONS",
)

data = page_data()

if data is not None:
    left_col, right_col = st.columns([1, 1.25], gap="large")

    with left_col:
        with st.container(border=True):
            card("Car Details")

            all_makes = sorted(data["make"].unique())
            default_make_idx = all_makes.index("maruti") if "maruti" in all_makes else 0
            make = st.selectbox("Brand", all_makes, index=default_make_idx)

            brand_models = sorted(data.loc[data["make"] == make, "model"].unique())
            default_mod_idx = brand_models.index("swift") if "swift" in brand_models else 0
            model = st.selectbox("Model", brand_models, index=default_mod_idx)

            fuel_types = sorted(data["fuel_type"].unique())
            default_fuel_idx = fuel_types.index("petrol") if "petrol" in fuel_types else 0
            fuel = st.selectbox("Fuel Type", fuel_types, index=default_fuel_idx)

            trans_options = ["Any"] + sorted(data["transmission"].unique())
            transmission = st.selectbox("Transmission (optional)", trans_options, index=trans_options.index("manual") if "manual" in trans_options else 0)

            year = st.number_input("Year of Manufacture", min_value=1995, max_value=2026, value=2018, step=1)
            kms = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=45000, step=1000)
            asking = st.number_input("Asking Price (optional, ₹)", min_value=0, value=520000, step=10000)

            render_html("<div style='height: 8px;'></div>")
            submitted = st.button("Find Fair Price", type="primary", use_container_width=True)

    with right_col:
        with st.container(border=True):
            card("Estimation Results")

            asking_val = float(asking) if asking > 0 else None
            est_res = estimate_price(
                data=data,
                make=make,
                fuel_type=fuel,
                year=int(year),
                kms_run=int(kms),
                transmission=transmission,
                asking_price=asking_val,
                model=model,
            )

            if est_res["count"] == 0:
                st.warning("No comparable listings found for this exact criteria. Try setting Transmission to 'Any'.")
            else:
                if est_res["widened"]:
                    st.info(f"Fewer than 5 close matches were found; tolerance was widened to: {est_res['tolerance_used']}.")

                # Top Metrics: Similar Listings Found & Confidence Level
                c_stat1, c_stat2 = st.columns(2)
                with c_stat1:
                    stat1_html = f"""
                    <div style="font-size: 0.8rem; font-weight: 600; color: #6B7280;">Similar Listings Found</div>
                    <div style="font-size: 1.55rem; font-weight: 800; color: #0F1B33;">{est_res['count']}</div>
                    """
                    render_html(stat1_html)

                with c_stat2:
                    conf = est_res["confidence"]
                    conf_kind = "success" if conf == "High" else ("primary" if conf == "Medium" else "warning")
                    stat2_html = f"""
                    <div style="font-size: 0.8rem; font-weight: 600; color: #6B7280;">Confidence Level</div>
                    <div style="margin-top: 4px;">{badge(conf, conf_kind)}</div>
                    """
                    render_html(stat2_html)

                render_html("<div style='height: 12px;'></div>")

                # Estimated Price Range (P25 - Average - P75)
                range_html = f"""
                <div style="background: #F4F6FB; border: 1px solid #E3E8F0; border-radius: 10px; padding: 14px; margin-bottom: 16px;">
                    <div style="font-size: 0.76rem; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">Estimated Price Range (₹)</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; text-align: center;">
                        <div>
                            <div style="font-size: 0.75rem; color: #6B7280;">P25 (Low)</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #0F1B33;">{money(est_res['p25'])}</div>
                        </div>
                        <div style="font-size: 1.2rem; color: #94A3B8;">—</div>
                        <div>
                            <div style="font-size: 0.75rem; color: #2563EB; font-weight: 600;">Average</div>
                            <div style="font-size: 1.3rem; font-weight: 800; color: #2563EB;">{money(est_res['average'])}</div>
                        </div>
                        <div style="font-size: 1.2rem; color: #94A3B8;">—</div>
                        <div>
                            <div style="font-size: 0.75rem; color: #6B7280;">P75 (High)</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #0F1B33;">{money(est_res['p75'])}</div>
                        </div>
                    </div>
                </div>
                """
                render_html(range_html)

                # Deal Verdict Bar
                if est_res["verdict"] and asking_val:
                    verdict = est_res["verdict"]
                    v_kind = "success" if verdict == "Fair" else ("primary" if verdict == "Underpriced" else "danger")
                    verdict_html = f"""
                    <div style="margin: 12px 0 6px 0;">
                        <span style="font-size: 0.9rem; font-weight: 600; color: #0F1B33;">Deal Verdict (for asking price {money(asking_val)}):</span>
                        <span style="margin-left: 6px;">{badge(verdict, v_kind)}</span>
                    </div>
                    <div style="margin: 8px 0 14px 0;">
                        <div style="height: 10px; border-radius: 6px; display: flex; overflow: hidden; background: #E3E8F0;">
                            <div style="flex: 1; background: #38BDF8;" title="Underpriced"></div>
                            <div style="flex: 2; background: #16A34A;" title="Fair"></div>
                            <div style="flex: 1; background: #DC2626;" title="Overpriced"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #6B7280; margin-top: 4px; font-weight: 600;">
                            <span>Underpriced (&lt; {money(est_res['p25'])})</span>
                            <span style="color: #16A34A;">Fair Band</span>
                            <span>Overpriced (&gt; {money(est_res['p75'])})</span>
                        </div>
                    </div>
                    """
                    render_html(verdict_html)

                # Price Distribution Histogram with "Your Price" Line
                fig_hist = px.histogram(
                    est_res["matches"],
                    x="sale_price",
                    nbins=16,
                    color_discrete_sequence=["#93C5FD"],
                    labels={"sale_price": "Price (₹)"},
                )
                fig_hist.update_traces(marker=dict(line=dict(width=0.5, color="#FFFFFF")))

                # Fair range rectangle
                fig_hist.add_vrect(
                    x0=est_res["p25"],
                    x1=est_res["p75"],
                    fillcolor="#16A34A",
                    opacity=0.15,
                    line_width=0,
                    annotation_text="Fair Range",
                    annotation_position="top left",
                )

                # Vertical line for asking price
                if asking_val:
                    fig_hist.add_vline(
                        x=asking_val,
                        line_color="#DC2626",
                        line_width=2.5,
                        line_dash="dash",
                        annotation_text=f"Your Price: {money(asking_val)}",
                        annotation_position="top right",
                    )

                st.plotly_chart(style_chart(fig_hist, show_title=False), use_container_width=True)
                caption("Shaded green region represents the interquartile fair range (P25 to P75) of comparable listings.")

                with st.expander(f"View Matched Listings ({est_res['count']})"):
                    show_cols = ["car_name", "yr_mfr", "fuel_type", "kms_run", "sale_price", "city"]
                    valid_cols = [c for c in show_cols if c in est_res["matches"].columns]
                    st.dataframe(est_res["matches"][valid_cols].sort_values("sale_price"), use_container_width=True, hide_index=True)
