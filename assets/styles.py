"""
Leaf Green Theme CSS for AgriIntel
Includes refined, compact font sizing for all module outputs, metrics, and cards
"""

LEAF_GREEN_CSS = """
<style>
/* ============================================================
   AgriIntel - Leaf Green Theme & Compact Typography
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


/* Background watermark styling */
.main {
    background-color: #F8FAF8;
    background-image: 
        radial-gradient(circle at 92% 8%, rgba(0, 191, 165, 0.035) 0%, transparent 45%),
        radial-gradient(circle at 8% 92%, rgba(46, 125, 50, 0.040) 0%, transparent 45%);
}

/* ============================================================
   AgriIntel Unified Institutional Hero Banner
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

/* Integrated Bottom Scope Bar */
.agri-hero-scope {
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(0, 0, 0, 0.16);
    padding: 8px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.agri-scope-label {
    font-size: 0.70rem;
    font-weight: 700;
    color: #A5D6A7;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    white-space: nowrap;
}

.agri-scope-chips {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.agri-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #E8F5E9;
    transition: background 0.2s ease;
}

.agri-chip:hover {
    background: rgba(255, 255, 255, 0.14);
    color: #FFFFFF;
}

.agri-chip-icon {
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: #81C784;
}

/* Sidebar Brand Card */
.sidebar-brand-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 12px 14px 10px 14px;
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.35);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.14);
    text-align: center;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.sidebar-brand-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.20);
}

.sidebar-brand-card img {
    max-width: 180px;
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    border-radius: 6px;
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

/* Main Sidebar Container */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #134E1B 0%, #1B5E20 35%, #18521C 70%, #123F16 100%) !important;
    border-right: 1px solid #2E7D32 !important;
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.12) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Sidebar Title and Text Headers */
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-size: 1.15rem !important;
    letter-spacing: -0.2px !important;
    margin-bottom: 2px !important;
}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] label {
    color: #E8F5E9 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #C8E6C9 !important;
    font-size: 0.86rem !important;
    opacity: 0.95 !important;
}

/* Radio Group Container */
section[data-testid="stSidebar"] div[data-testid="stRadio"] {
    margin-top: 4px !important;
}

/* Radio Group Label ("Select Intelligence Module:") */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    color: #C8E6C9 !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 6px !important;
    display: block !important;
}

/* Spacing and Card Styling for each Module item in the Sidebar - Tighter, refined gap */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 4px !important;
    display: flex !important;
    flex-direction: column !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    margin-bottom: 1px !important;
    margin-top: 1px !important;
    padding: 7px 11px !important;
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 8px !important;
    transition: all 0.20s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
}

/* Hover state on module capsules */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
    transform: translateX(3px) !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12) !important;
}

/* Active / Selected Module Capsule */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(255, 255, 255, 0.24) !important;
    border: 1px solid #A5D6A7 !important;
    border-left: 4px solid #81C784 !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.16) !important;
    transform: translateX(2px) !important;
}

/* Text inside module capsules */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
    color: #FFFFFF !important;
    font-size: 0.93rem !important;
    font-weight: 500 !important;
    line-height: 1.3 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {
    font-weight: 700 !important;
    color: #FFFFFF !important;
}

/* Sidebar Divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.20) !important;
    margin: 14px 0 !important;
}

/* Sidebar Expander (Founder Story) */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 9px !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    color: #E8F5E9 !important;
    font-size: 0.82rem !important;
    line-height: 1.45 !important;
}

/* ============================================================
   MOBILE & TABLET RESPONSIVE SYSTEM (< 768px & < 480px)
   Engineered for clean Android / iOS browser viewing
   ============================================================ */

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

    /* Integrated scope chips on mobile */
    .agri-hero-scope {
        padding: 7px 12px !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px !important;
    }

    .agri-scope-label {
        font-size: 0.65rem !important;
    }

    .agri-scope-chips {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 5px !important;
        width: 100% !important;
    }

    .agri-chip {
        padding: 4px 6px !important;
        font-size: 0.72rem !important;
        border-radius: 6px !important;
    }

    .agri-chip-icon {
        width: 15px !important;
        height: 15px !important;
    }

    /* Sidebar Mobile Optimization */
    section[data-testid="stSidebar"] {
        max-width: 86vw !important;
    }

    .sidebar-brand-card {
        padding: 8px 10px !important;
        margin-bottom: 8px !important;
    }

    .sidebar-brand-card img {
        max-width: 125px !important;
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

    .agri-chip {
        font-size: 0.68rem !important;
        padding: 3px 5px !important;
    }
}
</style>
"""
