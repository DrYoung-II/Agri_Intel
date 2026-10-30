"""
Leaf Green Theme CSS for AgroBiometrix
Includes refined, compact font sizing for all module outputs, metrics, and cards
"""

LEAF_GREEN_CSS = """
<style>
/* ============================================================
   AgroBiometrix - Leaf Green Theme & Compact Typography
   ============================================================ */

:root {
    --primary-green: #2E7D32;
    --dark-green: #1B5E20;
    --light-green: #4CAF50;
    --sprout-green: #81C784;
    --pale-leaf: #E8F5E9;
    --forest-bg: #F9FBF9;
    --text-primary: #1B3B1D;
    --circuit-teal: #00BFA5;
    --circuit-glow: #64FFDA;
    --circuit-gold: #FFD54F;
    --card-shadow: 0 4px 18px rgba(46, 125, 50, 0.07);
}

/* Base App Sizing */
html, body, [class*="css"] {
    font-size: 15.5px;
}

/* Headings Proportions */
h1 {
    font-size: 1.95rem !important;
    font-weight: 700 !important;
    color: #1B5E20 !important;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-size: 1.50rem !important;
    font-weight: 700 !important;
    color: #1B5E20 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.4rem !important;
}

h3 {
    font-size: 1.30rem !important;
    font-weight: 700 !important;
    color: #2E7D32 !important;
    margin-top: 0.8rem !important;
    margin-bottom: 0.35rem !important;
}

h4 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #2E7D32 !important;
    margin-top: 0.6rem !important;
    margin-bottom: 0.3rem !important;
}

h5 {
    font-size: 1.02rem !important;
    font-weight: 600 !important;
    color: #1B5E20 !important;
}

p, span, label, li {
    font-size: 0.98rem;
}

.stMarkdown p, .stMarkdown span, .stMarkdown li {
    font-size: 0.98rem;
    line-height: 1.55;
}



/* KaTeX math error safety styling - prevents jarring red text blocks */
.katex-error {
    color: #1B3B1D !important;
    background: #F1F8F2 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    border-left: 3px solid #2E7D32 !important;
    font-family: inherit !important;
    white-space: pre-wrap !important;
}

/* Background watermark styling */
.main {
    background-color: #F8FAF8;
    background-image: 
        radial-gradient(circle at 92% 8%, rgba(0, 191, 165, 0.035) 0%, transparent 45%),
        radial-gradient(circle at 8% 92%, rgba(46, 125, 50, 0.040) 0%, transparent 45%);
}

/* ============================================================
   AgroBiometrix Unified Institutional Hero Banner
   ============================================================ */
.agri-hero-banner {
    background: linear-gradient(135deg, #0A2F10 0%, #134B1B 45%, #1B5E20 85%, #103B14 100%);
    border: 1px solid rgba(129, 199, 132, 0.32);
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(10, 38, 14, 0.16), 0 2px 6px rgba(0, 0, 0, 0.08);
    color: #FFFFFF;
    margin-bottom: 1.15rem;
    overflow: hidden;
    position: relative;
}

.agri-hero-banner::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 240px;
    height: 240px;
    background: radial-gradient(circle, rgba(100, 255, 218, 0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.agri-hero-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.20rem 1.45rem 1.0rem 1.45rem;
    gap: 18px;
}

.agri-hero-identity {
    display: flex;
    align-items: center;
    gap: 16px;
    min-width: 0;
}

.agri-hero-logo {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 6px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18), 0 0 0 2px rgba(100, 255, 218, 0.40);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.agri-hero-logo img {
    width: 52px;
    height: 52px;
    aspect-ratio: 1 / 1;
    object-fit: contain;
    display: block;
}

.agri-hero-text {
    min-width: 0;
}

.agri-hero-title-row {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.agri-hero-title {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.4px !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    hyphens: none !important;
    margin: 0 !important;
}

.agri-hero-pill {
    background: rgba(0, 229, 255, 0.14) !important;
    border: 1px solid rgba(100, 255, 218, 0.40) !important;
    color: #64FFDA !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    padding: 3px 8px !important;
    border-radius: 12px !important;
    white-space: nowrap !important;
    display: inline-block !important;
}

.agri-hero-subtitle {
    font-size: 0.95rem !important;
    color: #E8F5E9 !important;
    font-weight: 400 !important;
    margin-top: 4px !important;
    margin-bottom: 3px !important;
    line-height: 1.35 !important;
}

.agri-hero-framework {
    font-size: 0.78rem !important;
    color: #A5D6A7 !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
    line-height: 1.3 !important;
}

.agri-hero-cert {
    background: rgba(0, 0, 0, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 10px;
    padding: 9px 14px;
    text-align: right;
    flex-shrink: 0;
}

.agri-cert-tag {
    font-size: 0.70rem;
    font-weight: 700;
    color: #81C784;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
}

.agri-cert-status {
    font-size: 0.76rem;
    color: #FFFFFF;
    font-weight: 600;
    opacity: 0.92;
}

/* Sidebar Brand Card - Dark Green Border to Differentiate */
.sidebar-brand-card {
    background: #FFFFFF !important;
    border: 2.5px solid #1B5E20 !important;
    border-radius: 12px !important;
    padding: 12px 14px 10px 14px !important;
    margin: 2px 0 16px 0 !important;
    box-shadow: 0 3px 10px rgba(27, 94, 32, 0.10) !important;
    text-align: center !important;
    box-sizing: border-box !important;
}

.sidebar-brand-card img {
    max-width: 225px !important;
    width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
}

/* ============================================================
   STREAMLIT METRICS COMPACT STYLING (REDUCED FONT SIZE)
   Universal overrides targeting all container, Emotion, and child elements
   ============================================================ */

div[data-testid="stMetric"],
div.stMetric {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(46, 125, 50, 0.25) !important;
    border-radius: 9px !important;
    padding: 8px 11px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stMetric"]:hover {
    border-color: #81C784 !important;
    box-shadow: 0 4px 10px rgba(46, 125, 50, 0.10) !important;
}

/* Metric value font size (crisp, readable, preventing truncation) */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] *,
div[data-testid="stMetricValue"] > div,
div[data-testid="stMetricValue"] div,
div[data-testid="stMetricValue"] p,
div[data-testid="stMetricValue"] span,
.eozy2n84,
.eozy2n84 * {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* Metric label font size */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricLabel"] > div,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] span {
    font-size: 0.80rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.35px !important;
    margin-bottom: 2px !important;
    white-space: normal !important;
}

/* Delta badge font size */
div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] *,
div[data-testid="stMetricDelta"] > div,
div[data-testid="stMetricDelta"] span {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding-top: 2px !important;
    white-space: normal !important;
}

/* Custom Card Container */
.agri-card {
    background: #FFFFFF;
    border: 1px solid #E0EBE1;
    border-radius: 10px;
    padding: 1.1rem;
    margin-bottom: 1.0rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    font-size: 0.95rem;
}

.agri-card:hover {
    box-shadow: 0 6px 18px rgba(46, 125, 50, 0.10);
}

.agri-card-highlight {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5FBF6 100%);
    border-left: 4px solid #2E7D32;
}

/* Method Justification & Explainer Box */
.agri-explainer-box {
    background: #F1F8F2;
    border-left: 5px solid #2E7D32;
    border-radius: 0 10px 10px 0;
    padding: 1.05rem 1.25rem;
    margin: 1.0rem 0;
    color: #1B3B1D;
    line-height: 1.55;
    font-size: 0.96rem;
}

.agri-explainer-title {
    font-size: 1.10rem;
    font-weight: 700;
    color: #1B5E20;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Stat Box Component */
.agri-stat-box {
    background: #FFFFFF;
    border: 1px solid #E8F5E9;
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.agri-stat-number {
    font-size: 1.25rem;
    font-weight: 800;
    color: #2E7D32;
}

.agri-stat-label {
    font-size: 0.76rem;
    font-weight: 600;
    color: #557A58;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* Button & interactive styling adjustments */
div.stButton > button:first-child {
    background-color: #2E7D32 !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    padding: 0.4rem 1.0rem !important;
    transition: all 0.2s ease-in-out !important;
}

div.stButton > button:first-child:hover {
    background-color: #1B5E20 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(27, 94, 32, 0.20) !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #F1F8F2;
    border-radius: 6px 6px 0px 0px;
    padding: 8px 14px;
    color: #2E7D32;
    font-weight: 600;
    font-size: 0.86rem;
}

.stTabs [aria-selected="true"] {
    background-color: #2E7D32 !important;
    color: #FFFFFF !important;
}

/* Dataframe & Table styling */
.dataframe {
    border-radius: 8px;
    font-size: 0.82rem !important;
}

[data-testid="stDataFrame"] {
    font-size: 0.82rem !important;
}

/* Text inputs and select boxes */
.stTextInput input, .stSelectbox div {
    font-size: 0.88rem !important;
}

/* ============================================================
   SIDEBAR GREEN THEME & SPACING BETWEEN MODULES
   ============================================================ */

/* Main Sidebar Container - Clean White Plane Surface (AgriIntel Style) */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E9E5 !important;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.04) !important;
}

section[data-testid="stSidebar"] > div {
    background: #FFFFFF !important;
}

/* Sidebar Title and Text Headers */
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #1B5E20 !important;
    font-size: 1.15rem !important;
    letter-spacing: -0.2px !important;
    margin-bottom: 2px !important;
}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] label {
    color: #374151 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #6B7280 !important;
    font-size: 0.82rem !important;
}

/* Sidebar Section Headers (Language, Region, Suites) - Clean, Unboxed Web Headers */
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > label {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-top: 14px !important;
    margin-bottom: 6px !important;
    display: flex !important;
    align-items: center !important;
    transform: none !important;
    cursor: default !important;
}

section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label p,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > label p {
    color: #2E7D32 !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    line-height: 1.2 !important;
    margin: 0 !important;
}

/* Horizontal Radio Group (Language Toggle: Side-by-side on Same Line) */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[data-testid="stRadioGroup"][aria-orientation="horizontal"] {
    display: flex !important;
    flex-direction: row !important;
    gap: 6px !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    background: #F3F4F6 !important;
    padding: 3px !important;
    border-radius: 8px !important;
    border: 1px solid #E5E7EB !important;
}

/* Hide radio circle in language switcher for sleek tab look */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label,
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[data-testid="stRadioGroup"][aria-orientation="horizontal"] > label {
    flex: 1 1 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 6px 10px !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    box-shadow: none !important;
    white-space: nowrap !important;
    transition: all 0.18s ease !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label p {
    color: #4B5563 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    text-align: center !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label:hover {
    background: rgba(255, 255, 255, 0.65) !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label:has(input:checked) {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"][aria-orientation="horizontal"] > label:has(input:checked) p {
    color: #1B5E20 !important;
    font-weight: 700 !important;
}

/* Vertical Radio Group (Suite Navigation: Standalone Flat Web Links like AgriIntel) */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) {
    display: flex !important;
    flex-direction: column !important;
    gap: 1px !important;
    width: 100% !important;
}

/* Hide radio circle in suite navigation for clean web appearance */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label {
    margin: 0 !important;
    padding: 9px 12px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label p {
    color: #374151 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    margin: 0 !important;
    white-space: nowrap !important;
}

/* Subtle chevron on the right like AgriIntel */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label::after {
    content: '›' !important;
    font-size: 1.20rem !important;
    color: #9CA3AF !important;
    margin-left: auto !important;
    padding-left: 8px !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    transition: transform 0.15s ease, color 0.15s ease !important;
}

/* Hover state: subtle tint like modern web navbar */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover {
    background: #F0FDF4 !important;
    border: none !important;
    transform: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover p {
    color: #15803D !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover::after {
    color: #15803D !important;
    transform: translateX(2px) !important;
}

/* Active / Selected Suite Item */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked) {
    background: #E8F5E9 !important;
    border: none !important;
    border-left: 3px solid #2E7D32 !important;
    border-radius: 0 6px 6px 0 !important;
    box-shadow: none !important;
    transform: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked) p {
    font-weight: 700 !important;
    color: #1B5E20 !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked)::after {
    color: #2E7D32 !important;
    font-weight: 700 !important;
}

/* Selectbox styling in sidebar (Region selector) - Clean Web Form Input */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #FAFCFA !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 6px !important;
    color: #1F2937 !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #1F2937 !important;
    font-size: 0.86rem !important;
}

/* Sidebar Divider */
section[data-testid="stSidebar"] hr {
    border-color: #E5E7EB !important;
    margin: 14px 0 !important;
}

/* Sidebar Expander (Founder Story & Gemini Key) */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #1B5E20 !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    color: #374151 !important;
    font-size: 0.82rem !important;
    line-height: 1.45 !important;
}

/* ============================================================
   MOBILE & TABLET RESPONSIVE SYSTEM (< 768px & < 480px)
   Engineered for clean Android / iOS browser viewing
   ============================================================ */


/* ============================================================
   AgroBiometrix Footer & Powered by Naysa-84 Labs
   ============================================================ */
.agri-footer-card {
    background: linear-gradient(135deg, #0A2F10 0%, #134B1B 45%, #1B5E20 85%, #0D3310 100%);
    border-radius: 14px;
    border: 1px solid rgba(129, 199, 132, 0.35);
    box-shadow: 0 8px 24px rgba(10, 38, 14, 0.16), 0 2px 6px rgba(0, 0, 0, 0.08);
    color: #FFFFFF;
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
}

.agri-footer-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 1.8rem 1.3rem 1.8rem;
    gap: 24px;
    flex-wrap: wrap;
}

.agri-footer-brand {
    flex: 1 1 360px;
    min-width: 0;
}

.agri-footer-badge {
    display: inline-block;
    background: rgba(129, 199, 132, 0.18);
    border: 1px solid rgba(129, 199, 132, 0.45);
    color: #C8E6C9;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.agri-footer-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.2px;
    line-height: 1.25;
}

.agri-footer-subtitle {
    font-size: 0.88rem;
    color: #E8F5E9;
    margin-top: 4px;
    line-height: 1.45;
}

.agri-footer-legal {
    font-size: 0.76rem;
    color: #A5D6A7;
    margin-top: 6px;
    line-height: 1.4;
}

.agri-footer-attribution {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(129, 199, 132, 0.35);
    border-radius: 12px;
    padding: 12px 18px 10px 18px;
    min-width: 220px;
    text-align: center;
    backdrop-filter: blur(4px);
}

.agri-footer-powered-label {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #81C784;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.agri-footer-naysa-card {
    background: #646768;
    border-radius: 8px;
    padding: 6px 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.22);
    margin-bottom: 0px !important;
}

.agri-footer-naysa-card img {
    max-height: 48px;
    width: auto;
    max-width: 170px;
    object-fit: contain;
    display: block;
}

.agri-footer-naysa-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.4px;
}

.agri-footer-naysa-tagline {
    font-size: 0.72rem;
    color: #80DEEA;
    font-style: italic;
    margin-top: 1px;
}

.agri-footer-bottom {
    background: rgba(0, 0, 0, 0.28);
    border-top: 1px solid rgba(129, 199, 132, 0.22);
    padding: 10px 1.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
    color: #A5D6A7;
    flex-wrap: wrap;
    gap: 8px;
}

.agri-footer-links {
    color: #C8E6C9;
    font-weight: 500;
}

/* Sidebar Naysa Attribution Card */
.sidebar-naysa-card {
    background: rgba(0, 0, 0, 0.28);
    border: 1px solid rgba(129, 199, 132, 0.32);
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 12px;
    margin-bottom: 8px;
    text-align: center;
}

.sidebar-naysa-card img {
    max-width: 145px;
    width: 90%;
    height: auto;
    border-radius: 6px;
    margin: 4px auto;
    display: block;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.20);
}

@media (max-width: 768px) {
    /* Optimize Streamlit viewport margins on mobile phones */
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.65rem !important;
        padding-right: 0.65rem !important;
        max-width: 100% !important;
    }

    /* Hero Banner Mobile Styling: One single unified card */
    .agri-hero-banner {
        border-radius: 12px !important;
        margin-bottom: 0.80rem !important;
    }

    .agri-hero-main {
        padding: 12px 12px 10px 12px !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
    }

    .agri-hero-identity {
        gap: 12px !important;
        width: 100% !important;
    }

    .agri-hero-logo {
        padding: 4px !important;
        border-radius: 10px !important;
    }

    .agri-hero-logo img {
        width: 42px !important;
        height: 42px !important;
    }

    .agri-hero-title {
        font-size: 1.45rem !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        hyphens: none !important;
    }

    .agri-hero-pill {
        font-size: 0.60rem !important;
        padding: 2px 6px !important;
    }

    .agri-hero-subtitle {
        font-size: 0.82rem !important;
        line-height: 1.30 !important;
        margin-top: 2px !important;
        margin-bottom: 2px !important;
    }

    .agri-hero-framework {
        font-size: 0.70rem !important;
        line-height: 1.30 !important;
    }

    /* Hide redundant desktop right card on small screens */
    .agri-hero-cert {
        display: none !important;
    }

    /* Sidebar Mobile Optimization */
    section[data-testid="stSidebar"] {
        max-width: 86vw !important;
    }

    .sidebar-brand-card {
        padding: 10px 12px !important;
        margin-bottom: 12px !important;
        border: 2.5px solid #1B5E20 !important;
        border-radius: 12px !important;
    }

    .sidebar-brand-card img {
        max-width: 220px !important;
        width: 100% !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        padding: 6px 9px !important;
        margin-bottom: 2px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
        font-size: 0.83rem !important;
    }

    /* Streamlit Columns Mobile Stacking */
    div[data-testid="column"] {
        min-width: 100% !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="column"] button {
        width: 100% !important;
    }

    /* Streamlit Metrics on Mobile */
    div[data-testid="stMetric"], div.stMetric {
        padding: 6px 9px !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stMetricValue"] * {
        font-size: 1.10rem !important;
    }

    div[data-testid="stMetricLabel"] * {
        font-size: 0.70rem !important;
    }

    /* Primary and Secondary Buttons: Touch-friendly 44px min-height */
    div.stButton > button:first-child {
        width: 100% !important;
        padding: 0.55rem 1.0rem !important;
        font-size: 0.90rem !important;
        min-height: 44px !important;
    }

    /* Responsive Tabs */
    .stTabs [data-baseweb="tab"] {
        padding: 6px 10px !important;
        font-size: 0.78rem !important;
    }

    /* Touch-friendly scrolling for dataframes, tables, and preformatted blocks */
    [data-testid="stDataFrame"], .stTable, pre {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        max-width: 100% !important;
    }

    /* Footer Mobile Responsiveness */
    .agri-footer-inner {
        padding: 1.2rem 1.1rem 1.0rem 1.1rem !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 16px !important;
    }

    .agri-footer-attribution {
        width: 100% !important;
    }

    .agri-footer-bottom {
        padding: 8px 1.1rem !important;
        flex-direction: column !important;
        text-align: center !important;
        gap: 4px !important;
    }
}

/* Extra small devices (< 420px) like compact Android phones */
@media (max-width: 420px) {
    .agri-hero-title {
        font-size: 1.30rem !important;
    }

    .agri-hero-logo img {
        width: 36px !important;
        height: 36px !important;
    }
}
</style>
"""
