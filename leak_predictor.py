import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & GOOGLE MATERIAL DESIGN 3.0 (M3) LIGHT TOKENS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gas Company • Network Integrity Console",
    page_icon="https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/sensors/default/24px.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0');

    :root {
        color-scheme: light;
        --md-background: #F6F8FC;
        --md-surface: #FFFFFF;
        --md-surface-container: #EEF2F8;
        --md-surface-container-low: #F8FAFD;
        --md-surface-container-high: #E4EAF3;

        --md-primary: #0B57D0;
        --md-on-primary: #FFFFFF;
        --md-primary-container: #D3E3FD;
        --md-on-primary-container: #041E49;

        --md-text-primary: #192B45;
        --md-text-secondary: #64748B;
        --md-outline: #CBD5E1;
        --md-outline-variant: #E2E8F0;

        --md-error: #B3261E;
        --md-error-container: #FCE8E6;
        --md-on-error-container: #7F1D1D;

        --md-warning: #A15C00;
        --md-warning-container: #FFF3D6;
        --md-on-warning-container: #713F12;

        --md-success: #137333;
        --md-success-container: #E6F4EA;
        --md-on-success-container: #14532D;

        --md-elevation-1: 0 1px 2px rgba(25, 43, 69, 0.05), 0 1px 3px rgba(25, 43, 69, 0.04);
        --md-elevation-2: 0 4px 14px rgba(25, 43, 69, 0.08), 0 1px 3px rgba(25, 43, 69, 0.04);
    }

    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
        background-color: var(--md-background) !important;
        color: var(--md-text-primary) !important;
        font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0 !important;
    }

    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }

    .m3-icon {
        font-family: 'Material Symbols Outlined';
        font-weight: normal;
        font-style: normal;
        font-size: 20px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        vertical-align: middle;
    }

    /* A. Top Application Bar */
    .m3-appbar {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        justify-content: space-between;
        align-items: center;
        box-shadow: var(--md-elevation-1);
    }
    .m3-brand-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .m3-brand-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background-color: var(--md-primary-container);
        color: var(--md-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .m3-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: var(--md-text-primary) !important;
        letter-spacing: -0.015em;
        margin: 0 !important;
        line-height: 1.3 !important;
    }
    .m3-subtitle {
        font-size: 13px;
        color: var(--md-text-secondary);
        margin-top: 2px;
        font-weight: 400;
    }
    .m3-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }
    .m3-chip {
        background-color: var(--md-surface-container);
        border: 1px solid var(--md-outline-variant);
        color: var(--md-text-primary);
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 12.5px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--md-success);
        box-shadow: 0 0 0 3px var(--md-success-container);
        display: inline-block;
    }

    /* B. Filter & Control Card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--md-surface) !important;
        border: 1px solid var(--md-outline-variant) !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
        box-shadow: var(--md-elevation-1) !important;
        margin-bottom: 16px !important;
    }

    .stSelectbox label, .stSlider label, .stRadio label {
        color: var(--md-text-primary) !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--md-surface-container-low) !important;
        border: 1px solid var(--md-outline) !important;
        border-radius: 12px !important;
        color: var(--md-text-primary) !important;
        min-height: 44px !important;
        font-size: 14px !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: var(--md-primary) !important;
        background-color: var(--md-surface) !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: var(--md-surface) !important;
        border: 1px solid var(--md-outline-variant) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="popover"] li {
        color: var(--md-text-primary) !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--md-primary) !important;
        border: 2px solid var(--md-surface) !important;
        box-shadow: 0 1px 4px rgba(11, 87, 208, 0.4) !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"],
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p {
        color: var(--md-text-secondary) !important;
        font-size: 12px !important;
    }

    /* Primary & Secondary M3 Buttons */
    div.stButton > button[kind="primary"] {
        background-color: var(--md-primary) !important;
        color: var(--md-on-primary) !important;
        border: none !important;
        border-radius: 999px !important;
        min-height: 44px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 1px 3px rgba(11, 87, 208, 0.28) !important;
        transition: all 0.18s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #0842A0 !important;
        box-shadow: 0 4px 10px rgba(11, 87, 208, 0.35) !important;
        transform: translateY(-1px);
    }
    div.stButton > button[kind="secondary"],
    div[data-testid="stDownloadButton"] > button {
        background-color: var(--md-surface-container) !important;
        color: var(--md-primary) !important;
        border: 1px solid var(--md-outline) !important;
        border-radius: 999px !important;
        min-height: 40px !important;
        padding: 0.45rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    div.stButton > button[kind="secondary"]:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: var(--md-primary-container) !important;
        border-color: var(--md-primary) !important;
    }

    /* Pre-Scan Readiness Hero Card */
    .m3-readiness-card {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: 18px;
        padding: 32px 36px;
        box-shadow: var(--md-elevation-1);
        margin-top: 4px;
    }
    .m3-readiness-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: var(--md-primary-container);
        color: var(--md-on-primary-container);
        padding: 5px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 14px;
    }
    .m3-readiness-title {
        font-size: 22px;
        font-weight: 700;
        color: var(--md-text-primary);
        margin-bottom: 8px;
        letter-spacing: -0.015em;
    }
    .m3-readiness-desc {
        font-size: 14.5px;
        color: var(--md-text-secondary);
        line-height: 1.65;
        max-width: 780px;
        margin-bottom: 24px;
    }
    .m3-mini-stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }
    .m3-mini-stat {
        background-color: var(--md-surface-container-low);
        border: 1px solid var(--md-outline-variant);
        border-radius: 14px;
        padding: 16px 18px;
    }
    .m3-mini-stat-label {
        font-size: 12px;
        font-weight: 600;
        color: var(--md-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .m3-mini-stat-val {
        font-size: 20px;
        font-weight: 700;
        color: var(--md-text-primary);
        margin-top: 4px;
    }

    /* C. KPI Cards */
    .m3-kpi-card {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: 16px;
        padding: 20px 22px;
        height: 158px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: var(--md-elevation-1);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .m3-kpi-card:hover {
        box-shadow: var(--md-elevation-2);
        transform: translateY(-2px);
    }
    .m3-kpi-card:has(.pill-critical) {
        background: linear-gradient(180deg, #FFFBFB 0%, #FFFFFF 100%);
        border-color: #F5C2C0;
    }
    .m3-kpi-card:has(.pill-warning) {
        background: linear-gradient(180deg, #FFFDF7 0%, #FFFFFF 100%);
        border-color: #F3D999;
    }
    .m3-kpi-card:has(.pill-safe) {
        background: linear-gradient(180deg, #F8FCF9 0%, #FFFFFF 100%);
        border-color: #BCE3C6;
    }
    .m3-kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
    }
    .m3-kpi-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--md-text-secondary);
    }
    .m3-kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--md-text-primary);
        letter-spacing: -0.025em;
        font-variant-numeric: tabular-nums;
        margin: 6px 0 4px 0;
        line-height: 1.15;
    }
    .m3-kpi-meta {
        font-size: 13px;
        font-weight: 500;
        color: var(--md-text-secondary);
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* M3 Semantic Status Pills */
    .pill-critical {
        background-color: var(--md-error-container);
        color: var(--md-on-error-container);
        border: 1px solid rgba(179, 38, 30, 0.16);
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
    }
    .pill-warning {
        background-color: var(--md-warning-container);
        color: var(--md-on-warning-container);
        border: 1px solid rgba(161, 92, 0, 0.18);
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
    }
    .pill-safe {
        background-color: var(--md-success-container);
        color: var(--md-on-success-container);
        border: 1px solid rgba(19, 115, 51, 0.18);
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* F. AI Insights & Diagnostic Assessment Card */
    .m3-verdict-card {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-left: 4px solid var(--md-primary);
        border-radius: 16px;
        padding: 18px 24px;
        margin: 16px 0 18px 0;
        box-shadow: var(--md-elevation-1);
    }
    .m3-verdict-header {
        font-size: 14px;
        font-weight: 700;
        color: var(--md-primary);
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .m3-verdict-text {
        font-size: 14px;
        line-height: 1.65;
        color: var(--md-text-primary);
    }

    /* D & E. Section Cards */
    .m3-section-card {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: var(--md-elevation-1);
        margin-bottom: 20px;
        overflow-x: auto;
    }
    .m3-section-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--md-text-primary);
        letter-spacing: -0.01em;
        margin-bottom: 3px;
    }
    .m3-section-sub {
        font-size: 13px;
        color: var(--md-text-secondary);
        margin-bottom: 14px;
    }

    /* E. Enterprise Data Table */
    .m3-table {
        width: 100%;
        min-width: 640px;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13.5px;
        text-align: left;
    }
    .m3-table th {
        background-color: var(--md-surface-container);
        color: var(--md-text-secondary);
        font-weight: 600;
        font-size: 11.5px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 11px 14px;
        border-top: 1px solid var(--md-outline-variant);
        border-bottom: 1px solid var(--md-outline-variant);
    }
    .m3-table th:first-child {
        border-left: 1px solid var(--md-outline-variant);
        border-top-left-radius: 10px;
    }
    .m3-table th:last-child {
        border-right: 1px solid var(--md-outline-variant);
        border-top-right-radius: 10px;
    }
    .m3-table td {
        padding: 13px 14px;
        border-bottom: 1px solid var(--md-outline-variant);
        color: var(--md-text-primary);
        vertical-align: middle;
        transition: background-color 0.12s ease;
    }
    .m3-table tr:last-child td {
        border-bottom: none;
    }
    .m3-table tbody tr:hover td {
        background-color: var(--md-surface-container-low);
    }
    .mono {
        font-family: 'Roboto Mono', monospace;
        font-size: 13px;
        font-weight: 600;
        color: var(--md-primary);
        white-space: nowrap;
    }

    .risk-bar-bg {
        width: 68px;
        height: 7px;
        background-color: var(--md-surface-container-high);
        border-radius: 999px;
        display: inline-block;
        margin-right: 8px;
        vertical-align: middle;
        overflow: hidden;
    }
    .risk-bar-fill {
        height: 100%;
        border-radius: 999px;
        display: block;
    }

    /* G. Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: 14px;
        padding: 6px 10px;
        gap: 8px;
        margin-bottom: 16px;
        box-shadow: var(--md-elevation-1);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 10px !important;
        color: var(--md-text-secondary) !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        padding: 8px 16px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--md-surface-container-low) !important;
        color: var(--md-text-primary) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--md-primary-container) !important;
        color: var(--md-on-primary-container) !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--md-outline-variant);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STRUCTURED PYDANTIC SCHEMA
# -----------------------------------------------------------------------------
class SegmentAssessment(BaseModel):
    segment_id: str
    zone: str
    material: str
    age_years: int
    pressure_drop_mbar: float
    leak_probability_pct: int = Field(description="0 to 100 risk score")
    risk_tier: str = Field(description="CRITICAL, ELEVATED, or NORMAL")
    estimated_hours_to_breach: str = Field(description="e.g., '18-24 hrs' or 'Stable'")
    recommended_action: str = Field(description="Specific preventive field engineering action")

class NetworkForecast(BaseModel):
    highest_risk_segment: str = Field(description="Segment ID only, e.g. 'CAD-EE-7734'")
    highest_risk_zone_and_prob: str = Field(description="e.g. 'East of England • 92% probability'")
    secondary_watchlist_segment: str = Field(description="Segment ID only, e.g. 'CAD-NW-4012'")
    secondary_zone_and_prob: str = Field(description="e.g. 'North West • 84% probability'")
    prevented_incidents_est: str = Field(description="e.g. '3 Critical Mains'")
    prevented_subtext: str = Field(description="e.g. 'Flagged 36h prior to odor threshold'")
    chief_engineer_verdict: str = Field(description="3-4 sentence diagnostic summary explaining material fatigue, pressure decay, and proactive dispatch priority before customer complaints occur")
    segment_assessments: list[SegmentAssessment]

# -----------------------------------------------------------------------------
# 3. SIMULATED SCADA & ASSET REGISTRY TELEMETRY
# -----------------------------------------------------------------------------
def get_pipeline_telemetry(zone_filter: str) -> pd.DataFrame:
    data = [
        {"Segment_ID": "CAD-EE-7734", "Zone": "East of England", "Material": "Cast Iron (Spun)", "Age_Yrs": 63, "Soil_Corrosion": "High (Moisture)", "Nominal_mbar": 75.0, "Live_mbar": 59.8, "Night_Flow_Anomaly_pct": 22.0},
        {"Segment_ID": "CAD-NW-4012", "Zone": "North West", "Material": "Cast Iron (Grey)", "Age_Yrs": 58, "Soil_Corrosion": "High (Clay/Acidic)", "Nominal_mbar": 75.0, "Live_mbar": 61.4, "Night_Flow_Anomaly_pct": 18.5},
        {"Segment_ID": "CAD-WM-3304", "Zone": "West Midlands", "Material": "Cast Iron (Grey)", "Age_Yrs": 54, "Soil_Corrosion": "High (Traffic Load)", "Nominal_mbar": 75.0, "Live_mbar": 64.0, "Night_Flow_Anomaly_pct": 15.4},
        {"Segment_ID": "CAD-WM-1189", "Zone": "West Midlands", "Material": "Ductile Iron", "Age_Yrs": 41, "Soil_Corrosion": "Moderate", "Nominal_mbar": 75.0, "Live_mbar": 68.2, "Night_Flow_Anomaly_pct": 11.2},
        {"Segment_ID": "CAD-NL-2095", "Zone": "North London", "Material": "MDPE (Polyethylene)", "Age_Yrs": 12, "Soil_Corrosion": "Low", "Nominal_mbar": 75.0, "Live_mbar": 74.6, "Night_Flow_Anomaly_pct": 1.1},
        {"Segment_ID": "CAD-NW-8821", "Zone": "North West", "Material": "HDPE (PE100)", "Age_Yrs": 6, "Soil_Corrosion": "Low", "Nominal_mbar": 75.0, "Live_mbar": 74.9, "Night_Flow_Anomaly_pct": 0.4},
    ]
    df = pd.DataFrame(data)
    df["Pressure_Drop_mbar"] = (df["Nominal_mbar"] - df["Live_mbar"]).round(2)
    if zone_filter != "All Regions (500,000+ Assets)":
        df = df[df["Zone"] == zone_filter]
    return df

# Session State Initialization
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None
if "scan_params" not in st.session_state:
    st.session_state.scan_params = None
if "dispatched_crews" not in st.session_state:
    st.session_state.dispatched_crews = set()

# -----------------------------------------------------------------------------
# 4. MATERIAL DESIGN 3 LIGHT TOP APP BAR
# -----------------------------------------------------------------------------
st.markdown("""
<div class="m3-appbar">
    <div class="m3-brand-group">
        <div class="m3-brand-icon">
            <span class="m3-icon" style="font-size:24px;">sensors</span>
        </div>
        <div>
            <h1 class="m3-title">Cadent Gas • Network Integrity Console</h1>
            <div class="m3-subtitle">Predictive Pipeline Leakage Intelligence • Material Health &amp; SCADA Pressure Decay</div>
        </div>
    </div>
    <div class="m3-chip-row">
        <span class="m3-chip"><span class="live-dot"></span> 5,12,480 Mains Monitored</span>
        <span class="m3-chip"><span class="m3-icon" style="font-size:16px; color:#0B57D0;">verified_user</span> LangSmith Traced</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. ALIGNED FILTER & ACTION TOOLBAR
# -----------------------------------------------------------------------------
with st.container(border=True):
    f1, f2, f3 = st.columns([1.45, 1.55, 1.0], vertical_alignment="bottom")
    with f1:
        region = st.selectbox(
            "Distribution Operating Zone",
            ["All Regions (500,000+ Assets)", "East of England", "North West", "West Midlands", "North London"],
            key="zone_select"
        )
    with f2:
        scada_window = st.slider(
            "Minimum Night Flow (MNF) Lookback Window (Hours)",
            min_value=6, max_value=72, value=24,
            key="window_slider"
        )
    with f3:
        run_btn = st.button("Run Predictive Scan", type="primary", use_container_width=True, key="run_scan_btn")

telemetry_df = get_pipeline_telemetry(region)

# Trigger AI Scan on Button Click & Persist in Session State
if run_btn:
    with st.spinner("Correlating pipe metallurgy, soil corrosivity, and overnight SCADA pressure decay..."):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        structured_llm = llm.with_structured_output(NetworkForecast)

        prompt = f"""
        You are the Principal Gas Network Integrity Engineer for Cadent Gas (managing 500,000+ distribution pipelines).
        Predict micro-leaks BEFORE customer odor complaints or life-threatening incidents occur.

        Evaluate this {scada_window}-hour SCADA pressure telemetry and pipe material registry:
        {telemetry_df.to_csv(index=False)}

        Classification rules:
        - Cast Iron (>50 yrs) + Pressure Drop > 10 mbar + Night Flow Anomaly > 15% -> CRITICAL
        - Ductile Iron or Cast Iron with 6-10 mbar drop -> ELEVATED
        - MDPE / HDPE polymer pipes with < 2 mbar drop -> NORMAL
        Return structured assessments for every row.
        """
        st.session_state.scan_result = structured_llm.invoke(prompt)
        st.session_state.scan_params = (region, scada_window)

# -----------------------------------------------------------------------------
# 6. NAVIGATION TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "Predictive Risk & Dispatch",
    "SCADA Sensor Telemetry",
    "Preventive Methodology"
])

with tab1:
    # Show results ONLY after clicking 'Run Predictive Scan'
    if st.session_state.scan_result is not None:
        result: NetworkForecast = st.session_state.scan_result

        # Alert banner if filters changed since last scan
        if st.session_state.scan_params != (region, scada_window):
            st.info(f"Parameters updated to **{region}** ({scada_window}h). Click **Run Predictive Scan** to refresh AI predictions.")

        # C. M3 3-Column Elevated KPI Grid
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
            <div class="m3-kpi-card">
                <div class="m3-kpi-top">
                    <span class="m3-kpi-label">Primary Pre-Breach Risk</span>
                    <span class="pill-critical">Critical</span>
                </div>
                <div class="m3-kpi-value">{result.highest_risk_segment}</div>
                <div class="m3-kpi-meta">
                    <span class="m3-icon" style="font-size:17px; color:#B3261E;">warning</span>
                    {result.highest_risk_zone_and_prob}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="m3-kpi-card">
                <div class="m3-kpi-top">
                    <span class="m3-kpi-label">Secondary Watchlist</span>
                    <span class="pill-warning">Elevated</span>
                </div>
                <div class="m3-kpi-value">{result.secondary_watchlist_segment}</div>
                <div class="m3-kpi-meta">
                    <span class="m3-icon" style="font-size:17px; color:#A15C00;">schedule</span>
                    {result.secondary_zone_and_prob}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
            <div class="m3-kpi-card">
                <div class="m3-kpi-top">
                    <span class="m3-kpi-label">Proactive Interventions</span>
                    <span class="pill-safe">Prevented</span>
                </div>
                <div class="m3-kpi-value">{result.prevented_incidents_est}</div>
                <div class="m3-kpi-meta">
                    <span class="m3-icon" style="font-size:17px; color:#137333;">shield</span>
                    {result.prevented_subtext}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # F. Chief Engineer Diagnostic Banner
        st.markdown(f"""
        <div class="m3-verdict-card">
            <div class="m3-verdict-header">
                <span class="m3-icon">engineering</span> Chief Network Integrity Assessment
            </div>
            <div class="m3-verdict-text">{result.chief_engineer_verdict}</div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Tier Filter & CSV Export Bar
        ctrl_left, ctrl_right = st.columns([2.2, 1.0], vertical_alignment="center")
        with ctrl_left:
            tier_filter = st.radio(
                "Filter Results by Risk Tier",
                ["All Assets", "CRITICAL", "ELEVATED", "NORMAL"],
                horizontal=True,
                key="tier_radio"
            )
        with ctrl_right:
            export_df = pd.DataFrame([item.model_dump() for item in result.segment_assessments])
            st.download_button(
                label="Download Dispatch CSV",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name="cadent_preventive_dispatch.csv",
                mime="text/csv",
                use_container_width=True
            )

        filtered_assessments = [
            item for item in result.segment_assessments
            if tier_filter == "All Assets" or item.risk_tier == tier_filter
        ]

        # D & E. Interactive Plotly Chart + Prioritized Dispatch Matrix
        chart_col, table_col = st.columns([1.15, 1.85], vertical_alignment="top")

        with chart_col:
            with st.container(border=True):
                st.markdown('<div class="m3-section-title">Overnight Pressure Decay (Δ mbar)</div>', unsafe_allow_html=True)
                st.markdown('<div class="m3-section-sub">Minimum Night Flow (02:00–04:00) drop by asset</div>', unsafe_allow_html=True)

                if filtered_assessments:
                    df_sorted = pd.DataFrame([item.model_dump() for item in filtered_assessments]).sort_values("pressure_drop_mbar", ascending=True)
                    colors = [
                        "#B3261E" if t == "CRITICAL" else ("#A15C00" if t == "ELEVATED" else "#0B57D0")
                        for t in df_sorted["risk_tier"]
                    ]

                    fig = go.Figure(go.Bar(
                        x=df_sorted["pressure_drop_mbar"],
                        y=df_sorted["segment_id"],
                        orientation="h",
                        marker=dict(color=colors, cornerradius=6),
                        text=[f"{v:.1f} mbar" for v in df_sorted["pressure_drop_mbar"]],
                        textposition="outside",
                        textfont=dict(family="Inter", size=12, color="#192B45"),
                        hovertemplate="<b>%{y}</b><br>Pressure Drop: %{x:.2f} mbar<extra></extra>",
                        cliponaxis=False
                    ))
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=52, t=6, b=6),
                        height=350,
                        xaxis=dict(
                            title=dict(text="Pressure Drop (mbar)", font=dict(size=12, color="#64748B")),
                            gridcolor="#E2E8F0",
                            zeroline=False,
                            color="#64748B",
                            tickfont=dict(size=11.5)
                        ),
                        yaxis=dict(
                            color="#192B45",
                            tickfont=dict(family="Roboto Mono", size=12, color="#192B45")
                        ),
                        font=dict(family="Inter", size=12, color="#192B45"),
                        hoverlabel=dict(
                            bgcolor="#FFFFFF",
                            bordercolor="#CBD5E1",
                            font=dict(family="Inter", size=12.5, color="#192B45")
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                else:
                    st.info("No assets match the selected severity tier.")

        with table_col:
            rows_list = []
            for item in filtered_assessments:
                if item.risk_tier == "CRITICAL":
                    badge = '<span class="pill-critical">CRITICAL</span>'
                    bar_color = "#B3261E"
                elif item.risk_tier == "ELEVATED":
                    badge = '<span class="pill-warning">ELEVATED</span>'
                    bar_color = "#A15C00"
                else:
                    badge = '<span class="pill-safe">NORMAL</span>'
                    bar_color = "#137333"

                dispatched_tag = (
                    '<br><span style="font-size:11px; color:#137333; font-weight:600;">✓ Crew Dispatched</span>'
                    if item.segment_id in st.session_state.dispatched_crews else ""
                )

                row_html = (
                    f'<tr>'
                    f'<td class="mono">{item.segment_id}{dispatched_tag}</td>'
                    f'<td><strong style="color:#192B45;">{item.material}</strong><br><span style="font-size:12px; color:#64748B;">{item.zone} • {item.age_years} yrs</span></td>'
                    f'<td style="white-space:nowrap;"><div class="risk-bar-bg"><span class="risk-bar-fill" style="width:{item.leak_probability_pct}%; background:{bar_color};"></span></div><strong style="color:#192B45;">{item.leak_probability_pct}%</strong></td>'
                    f'<td>{badge}</td>'
                    f'<td style="font-weight:600; color:#192B45; white-space:nowrap;">{item.estimated_hours_to_breach}</td>'
                    f'<td style="font-size:12.5px; color:#475569; line-height:1.45;">{item.recommended_action}</td>'
                    f'</tr>'
                )
                rows_list.append(row_html)

            table_card_html = (
                '<div class="m3-section-card">'
                '<div class="m3-section-title">Prioritized Preventive Dispatch Schedule</div>'
                '<div class="m3-section-sub">Field work orders prioritized ahead of public gas odor complaints</div>'
                '<table class="m3-table">'
                '<thead><tr>'
                '<th>Asset ID</th>'
                '<th>Metallurgy &amp; Zone</th>'
                '<th>Leak Risk</th>'
                '<th>Status</th>'
                '<th>Est. Window</th>'
                '<th>Preventive Work Order</th>'
                '</tr></thead>'
                f'<tbody>{"".join(rows_list)}</tbody>'
                '</table>'
                '</div>'
            )
            st.markdown(table_card_html, unsafe_allow_html=True)

        # Interactive Asset Drill-Down & Crew Dispatch Simulator
        with st.container(border=True):
            st.markdown('<div class="m3-section-title">Interactive Asset Drill-Down &amp; Field Dispatch Action</div>', unsafe_allow_html=True)
            st.markdown('<div class="m3-section-sub">Select a pipeline segment to inspect its 24-hour pressure decay curve and authorize preventive crew dispatch</div>', unsafe_allow_html=True)

            d1, d2 = st.columns([1.1, 1.9], vertical_alignment="top")
            all_ids = [item.segment_id for item in result.segment_assessments]
            with d1:
                selected_id = st.selectbox("Select Pipeline Segment", all_ids, key="drilldown_asset")
                selected_asset = next(i for i in result.segment_assessments if i.segment_id == selected_id)

                st.markdown(f"""
                <div style="background:#F8FAFD; border:1px solid #E2E8F0; border-radius:12px; padding:14px 16px; margin-bottom:12px;">
                    <div style="font-size:12px; color:#64748B; font-weight:600;">METALLURGY &amp; AGE</div>
                    <div style="font-size:15px; font-weight:700; color:#192B45; margin-bottom:8px;">{selected_asset.material} ({selected_asset.age_years} yrs)</div>
                    <div style="font-size:12px; color:#64748B; font-weight:600;">RECOMMENDED INTERVENTION</div>
                    <div style="font-size:13.5px; color:#192B45; line-height:1.45;">{selected_asset.recommended_action}</div>
                </div>
                """, unsafe_allow_html=True)

                if selected_id in st.session_state.dispatched_crews:
                    st.success(f"Preventive engineering crew dispatched to **{selected_id}**.")
                else:
                    if st.button(f"Authorize Crew Dispatch for {selected_id}", type="primary", use_container_width=True, key="dispatch_btn"):
                        st.session_state.dispatched_crews.add(selected_id)
                        st.rerun()

            with d2:
                hours = [f"{h:02d}:00" for h in range(0, 24, 2)]
                nominal_series = [75.0] * len(hours)
                drop = selected_asset.pressure_drop_mbar
                # Simulate realistic pressure dip during 02:00-06:00 Minimum Night Flow window
                decay_curve = [
                    round(75.0 - drop * (0.25 if h < 2 else (1.0 if h <= 6 else 0.72)), 2)
                    for h in range(0, 24, 2)
                ]

                trend_fig = go.Figure()
                trend_fig.add_trace(go.Scatter(
                    x=hours, y=nominal_series, name="Nominal Line Pressure (75 mbar)",
                    line=dict(color="#94A3B8", width=2, dash="dash")
                ))
                trend_fig.add_trace(go.Scatter(
                    x=hours, y=decay_curve, name=f"{selected_id} Live Telemetry",
                    mode="lines+markers",
                    line=dict(color="#B3261E" if selected_asset.risk_tier == "CRITICAL" else "#0B57D0", width=3),
                    marker=dict(size=7)
                ))
                trend_fig.update_layout(
                    title=dict(text=f"24-Hour Pressure Profile • {selected_id} ({selected_asset.zone})", font=dict(size=13.5, color="#192B45")),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=240,
                    margin=dict(l=10, r=10, t=36, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11.5)),
                    xaxis=dict(gridcolor="#E2E8F0", color="#64748B"),
                    yaxis=dict(title="Pressure (mbar)", gridcolor="#E2E8F0", color="#64748B", range=[55, 78]),
                    font=dict(family="Inter", color="#192B45")
                )
                st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})

    else:
        # Clean, Intentional Pre-Scan State (Details load ONLY after clicking Run Predictive Scan)
        st.markdown(f"""
        <div class="m3-readiness-card">
            <div class="m3-readiness-badge">
                <span class="m3-icon" style="font-size:16px;">radar</span> Telemetry Stream Standby • {region}
            </div>
            <div class="m3-readiness-title">Ready to Run Predictive Pipeline Integrity Scan</div>
            <div class="m3-readiness-desc">
                Configure your target <strong>Distribution Operating Zone</strong> and <strong>Minimum Night Flow (MNF) Lookback Window</strong> in the toolbar above, 
                then click <strong>Run Predictive Scan</strong> to evaluate pipe metallurgy against live SCADA pressure decay and generate preventive dispatch orders.
            </div>
            <div class="m3-mini-stat-grid">
                <div class="m3-mini-stat">
                    <div class="m3-mini-stat-label">Selected Scope</div>
                    <div class="m3-mini-stat-val">{len(telemetry_df)} Priority Districts</div>
                </div>
                <div class="m3-mini-stat">
                    <div class="m3-mini-stat-label">Lookback Window</div>
                    <div class="m3-mini-stat-val">{scada_window} Hours SCADA</div>
                </div>
                <div class="m3-mini-stat">
                    <div class="m3-mini-stat-label">Inference Engine</div>
                    <div class="m3-mini-stat-val">GPT-4o-mini + LangSmith</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    with st.container(border=True):
        st.markdown('<div class="m3-section-title">Raw SCADA Pressure &amp; Metallurgy Telemetry</div>', unsafe_allow_html=True)
        st.markdown('<div class="m3-section-sub">Live sensor feed across Cadent Gas distribution districts</div>', unsafe_allow_html=True)
        st.dataframe(telemetry_df, use_container_width=True, hide_index=True)

with tab3:
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="m3-section-card" style="border-top: 4px solid #B3261E;">
            <div class="m3-section-title" style="color: #B3261E; display: flex; align-items: center; gap: 8px;">
                <span class="m3-icon">report_problem</span> Legacy Reactive Dispatch (Complaint-Driven)
            </div>
            <div class="m3-section-sub">High public safety risk &amp; emergency SLA penalties</div>
            <ul style="font-size:14px; line-height:1.85; color:#192B45; padding-left:20px; margin-bottom:0;">
                <li>Circumferential fracture or lead-yarn joint dries out in aged Cast Iron main.</li>
                <li>Gas migrates underground into basements, creating explosion/asphyxiation risk.</li>
                <li>Public smells mercaptan odorant and places emergency hotline call.</li>
                <li>Unplanned emergency excavation under severe regulatory penalty.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="m3-section-card" style="border-top: 4px solid #137333;">
            <div class="m3-section-title" style="color: #137333; display: flex; align-items: center; gap: 8px;">
                <span class="m3-icon">task_alt</span> Predictive Asset Integrity (Telemetry-Driven)
            </div>
            <div class="m3-section-sub">Proactive detection prior to surface odor thresholds</div>
            <ul style="font-size:14px; line-height:1.85; color:#192B45; padding-left:20px; margin-bottom:0;">
                <li><strong>Minimum Night Flow (MNF)</strong> isolates 02:00–04:00 AM pressure drops when domestic demand is near zero.</li>
                <li>AI correlates Δ-pressure against 50+ yr Cast Iron &amp; acidic soil corrosion maps.</li>
                <li>High-risk segments flagged 24–48 hours before gas reaches hazardous levels.</li>
                <li>Scheduled PE (Polyethylene) pipe relining eliminates public safety risk.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)