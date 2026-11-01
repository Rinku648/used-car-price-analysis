# AutoInsight: Used Car Price Analysis

> **A Data-Driven Study of Resale Value Trends in the Indian Used Car Market**  
> *Major Project & CV Portfolio Piece | BTech CSE (Data Science & Machine Learning)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Problem Statement

Buyers and sellers of used cars in the Indian automotive market lack an objective, transparent, and data-backed mechanism to determine whether a listed price is fair. Price listings vary wildly across metropolitan cities, vehicle ages, fuel categories, and transmission choices. 

**AutoInsight** bridges this gap by analyzing **6,814 real used-car listings** across 22 brands and 13 cities. Rather than relying on opaque "black-box" machine learning algorithms, the platform employs **transparent exploratory data analysis, formal parametric hypothesis testing, and rule-based comparable-listing estimation** to assist buyers and sellers in making confident, data-backed decisions.

---

## Key Features

1. **Executive Overview (Home):**
   - Live KPI metrics computed directly from dataset records (Total Listings, Mean Price in Lakhs, Vehicle Age, Brands, Cities).
   - Modern analytics SaaS interface with custom dark navy sidebar (`#0B1B3A`) and Inter typography.
2. **Interactive Data Explorer:**
   - Multi-parameter filtering by Brand, Fuel Type, Transmission, City, Year, and Price Range.
   - Client-side pagination (10 rows per page) and CSV export of filtered subsets.
   - Comprehensive **Data Quality Report** auditing raw (7,400 rows) vs. cleaned (6,814 rows) records.
3. **Exploratory Data Analysis (EDA) Dashboard:**
   - **Univariate:** Distribution histograms with dynamic takeaway captions for Sale Price, Vehicle Age, and Kilometers Driven.
   - **Bivariate:** Scatter plots with OLS regression trendlines, box plots illustrating interquartile spreads by fuel, body type, and gearbox.
   - **Multivariate:** Full Pearson correlation matrix heatmap and city/brand valuation rankings.
4. **Statistical Hypothesis Testing:**
   - **Welch’s Two-Sample t-Test:** Comparing automatic vs. manual transmissions without assuming equal variances.
   - **One-Way ANOVA:** Testing variance between fuel types ($p < 0.05$).
   - **Tukey HSD Post-Hoc Analysis:** Pairwise comparisons identifying significant fuel category price gaps.
   - **Effect Size Metrics:** Standardized Cohen's $d$ and Eta-Squared ($\eta^2$) to assess practical significance beyond $p$-values.
5. **Fair Price Estimator & Deal Checker (Strictly Non-ML):**
   - Filters exact real comparable listings matching Make, Fuel Type, and Model.
   - Progressive auto-widening tolerances if fewer than 5 close matches are found.
   - Rule-based valuation band using the Interquartile Range (**P25 to P75**).
   - Three-tier visual **Deal Verdict bar** (`Underpriced` < P25, `Fair` P25–P75, `Overpriced` > P75).
6. **Brand Depreciation & Value Retention:**
   - Empirical cohort depreciation comparing younger vehicles (3–6 yrs) against mature cohorts (8–12 yrs).
   - Value retention leaderboard and non-linear depreciation trajectory curves.
7. **Upload & Analyze (Real-Time Live Feature):**
   - Drag-and-drop CSV upload with instant schema validation and 10-step data cleaning execution.
   - Live audit report detailing missing values, duplicate removal, and outlier exclusions.
8. **Actionable Insights & Recommendations:**
   - Data-backed takeaways for buyers (depreciation sweet spot at 3–6 years) and sellers (defending asking prices with service logs).

---

## Tech Stack & Engineering Architecture

- **Language:** Python 3.12
- **Framework:** Streamlit (Multi-page architecture via `pages/`)
- **Data Manipulation:** pandas 2.x, NumPy 1.26+
- **Data Visualization:** Plotly Express & Plotly Graph Objects (Interactive SVG/WebGL)
- **Inferential Statistics:** SciPy (stats), statsmodels (multicomp)
- **Automated Testing:** pytest 8.x

### Folder Structure

```text
used-car-eda/
├── app.py                                # Home / Overview page
├── pages/
│   ├── 1_Data_Explorer.py                # Table filters, pagination & quality audit
│   ├── 2_EDA_Dashboard.py                # Univariate, Bivariate & Multivariate distributions
│   ├── 3_Statistical_Tests.py            # Welch's t-test, ANOVA, Tukey HSD & effect sizes
│   ├── 4_Fair_Price_Estimator.py         # Rule-based comparable-listing estimation & deal checker
│   ├── 5_Brand_Depreciation.py           # Annual depreciation & retention rate ranking (no ML)
│   ├── 6_Upload_and_Analyze.py           # Real-time CSV upload, validation, cleaning & audit
│   └── 7_Insights_and_Recommendations.py # Data-driven buyer/seller takeaways & market synthesis
├── src/
│   ├── __init__.py
│   ├── ui.py                             # Design system: CSS injection, custom sidebar, cards & banners
│   ├── data_loader.py                    # Cached data loading (@st.cache_data) & schema validation
│   ├── cleaning.py                       # 10-step raw-to-cleaned pipeline & upload auditor with log
│   ├── features.py                       # Derived metrics: car_age, price_per_km, age/km buckets, money()
│   ├── stats_tests.py                    # Hypothesis testing: t-test, ANOVA, post-hoc, effect sizes
│   ├── estimator.py                      # Rule-based range finder with auto-widening tolerances
│   └── charts.py                         # Plotly layout template & reusable chart builders
├── assets/
│   ├── hero_car.png                      # Studio sedan hero render
│   └── logo.svg                          # AutoInsight brand vector logo
├── data/
│   ├── used_cars_cleaned.csv             # 6,814 rows × 15 columns (ground truth)
│   └── used_cars_raw.csv                 # 7,400 rows × 29 columns (for data quality audit)
├── tests/
│   ├── test_cleaning.py                  # Pytest verification of pipeline integrity & edge cases
│   └── test_estimator.py                 # Pytest verification of tolerances, quantiles & verdicts
├── .streamlit/
│   └── config.toml                       # Theme palette, headless mode & server configuration
├── requirements.txt                      # Project dependency specification
└── README.md                             # Project documentation & viva guide
```

---

## How to Run Locally

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/used-car-eda.git
cd used-car-eda

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Application

```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
python -m pytest -v
```

All 8 tests verify:
- Pipeline schema conformance (15 standardized columns).
- Edge cases in the price estimator (tolerance auto-widening, empty results, zero-division guards).
- Handling of malformed, corrupted, or missing upload columns.

---

## Key Findings from the Dataset

- **Age is King:** Vehicle age is the single strongest negative predictor of resale price ($r = -0.64$).
- **Mileage is Secondary:** Kilometers driven exhibits only a modest correlation ($r = -0.18$), meaning age and condition heavily outweigh odometer mileage.
- **Ownership Penalty:** Each subsequent owner adds an average markdown ($r = -0.20$).
- **Automatic Premium:** Automatic transmissions command a statistically significant premium over manuals ($t = 2.95, p = 0.0032$, Cohen's $d = 0.42$).
- **Fuel Hierarchy:** ANOVA confirms significant price variance across fuels ($F = 24.1, p < 0.001$), with diesel retaining highest average resale values.
- **Brand Hierarchy:** Among top-10 volume brands, Mahindra commands the highest average listing price (skewed by SUV trims), whereas Tata records the lowest average price point.

---

## Limitations & Ethical Considerations

1. **Asking Prices vs. Transaction Prices:** Listings represent asking prices, which may be negotiated downward by 5% to 15% in actual physical sales.
2. **Unobserved Vehicle Condition:** Cosmetic scratches, tire tread depth, battery health, and accident history are not captured in tabular listing datasets.
3. **Cross-Sectional Depreciation:** Brand depreciation is measured using cross-sectional cohorts rather than tracking a single vehicle longitudinally over a decade.

---

## Future Scope

While machine learning was strictly excluded from this project to prioritize transparency and statistical rigor, future extensions could incorporate:
- Supervised ML regression (e.g., CatBoost or LightGBM) with SHAP value explanations.
- Computer vision trim/damage assessment from vehicle photos.
- Geolocation-based real-time localized negotiation factor calculations.

---

## Viva Q&A Guide (For BTech Project Evaluation)

**Q1: Why did you not use a Machine Learning Regression Model (like XGBoost or Random Forest)?**  
*Answer:* "In used car sales, ML models frequently suffer from the 'black-box' dilemma where buyers and sellers cannot see *why* a particular price was generated. Furthermore, used car datasets have noisy outliers and uncaptured qualitative variables (paint condition, accident history). Our rule-based comparable-listing algorithm provides 100% transparency by showing the exact real matching cars, their interquartile range (P25 to P75), and the sample size confidence level."

**Q2: What is the difference between statistical significance ($p$-value) and practical significance (effect size)?**  
*Answer:* "With large datasets ($N = 6,814$), even tiny, negligible differences can produce $p < 0.05$. Therefore, we calculated Cohen's $d$ ($0.42$) for transmissions and Eta-Squared ($\eta^2 = 0.08$) for fuel types to quantify the actual magnitude of the gap, proving that transmission choice has a medium practical impact on resale price."

**Q3: How do you handle cases where very few similar cars exist?**  
*Answer:* "We engineered a progressive auto-widening algorithm. It starts strictly at $\pm 2$ years and $\pm 15,000$ km. If fewer than 5 matches exist, it steps incrementally up to $\pm 5$ years and $\pm 45,000$ km, flagging the widening to the user and downgrading the confidence rating from High to Medium/Low."
