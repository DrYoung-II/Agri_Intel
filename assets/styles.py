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

/* Header & Banner - Harmonized with Official Logo */
.agri-header {
    background: linear-gradient(135deg, #103B16 0%, #1B5E20 40%, #2E7D32 80%, #1E6B35 100%);
    color: #FFFFFF;
    padding: 1.25rem 1.50rem;
    border-radius: 16px;
    margin-bottom: 1.1rem;
    border: 1px solid rgba(100, 255, 218, 0.22);
    box-shadow: 0 10px 28px rgba(16, 59, 22, 0.18), 0 2px 6px rgba(0, 0, 0, 0.08);
    position: relative;
    overflow: hidden;
}

.agri-header::before {
    content: '';
    position: absolute;
    top: -50px;
    right: -50px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(100, 255, 218, 0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.agri-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.agri-header-brand {
    display: flex;
    align-items: center;
    gap: 16px;
    min-width: 0;
}

.agri-header-text {
    min-width: 0;
}

.agri-title-pill-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    min-width: 0;
}

.hero-logo-badge {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 7px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.16), 0 0 0 2px rgba(100, 255, 218, 0.40);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.hero-logo-badge img {
    width: clamp(42px, 36px + 2vw, 56px);
    height: clamp(42px, 36px + 2vw, 56px);
    aspect-ratio: 1 / 1;
    object-fit: contain;
    display: block;
}

.hero-logo-badge:hover {
    transform: scale(1.05) rotate(1deg);
    box-shadow: 0 8px 24px rgba(0, 229, 255, 0.35), 0 0 0 3px rgba(100, 255, 218, 0.65);
}

.agri-title {
    font-size: clamp(1.40rem, 1.1rem + 2.5vw, 2.15rem) !important;
    font-weight: 800;
    letter-spacing: -0.4px;
    margin: 0;
    color: #FFFFFF !important;
    line-height: 1.15;
    white-space: nowrap !important;
    word-break: keep-all !important;
    hyphens: none !important;
}

.agri-version-pill {
    background: rgba(0, 229, 255, 0.16);
    color: #64FFDA;
    font-size: clamp(0.62rem, 0.55rem + 0.35vw, 0.72rem);
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
    border: 1px solid rgba(100, 255, 218, 0.40);
    display: inline-block;
    white-space: nowrap;
}

.agri-subtitle {
    font-size: clamp(0.85rem, 0.75rem + 0.35vw, 1.05rem);
    font-weight: 400;
    color: #E8F5E9;
    margin-top: 0.2rem;
    margin-bottom: 0.35rem;
    line-height: 1.35;
}

.agri-tagline {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px;
    background: rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(8px);
    padding: 0.28rem 0.80rem;
    border-radius: 16px;
    font-size: clamp(0.70rem, 0.65rem + 0.25vw, 0.86rem);
    font-weight: 600;
    color: #C8E6C9;
    border: 1px solid rgba(255, 255, 255, 0.20);
    line-height: 1.4;
}

.agri-tagline-divider {
    opacity: 0.8;
}

.header-partner-badge {
    background: rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 12px;
    padding: 9px 15px;
    text-align: right;
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.10);
    flex-shrink: 0;
}

.header-partner-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #C8E6C9;
    font-weight: 700;
    margin-bottom: 3px;
}

.header-partner-sub {
    font-size: 0.78rem;
    opacity: 0.9;
    margin-top: 2px;
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
    max-width: 185px;
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    border-radius: 6px;
}

/* Silhouette Banner Decor */
.silhouette-strip {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 0.65rem 0.95rem;
    background: linear-gradient(90deg, #F1F8F2 0%, #FFFFFF 50%, #F1F8F2 100%);
    border-radius: 12px;
    margin-bottom: 1.2rem;
    color: #2E7D32;
    border: 1px solid #DCEADE;
    box-shadow: 0 2px 6px rgba(46, 125, 50, 0.04);
}

.silhouette-item {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 0.92rem;
    font-weight: 600;
    color: #1B5E20;
    opacity: 0.95;
    transition: transform 0.2s ease, color 0.2s ease;
}

.silhouette-item:hover {
    transform: translateY(-1px);
    color: #00897B;
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
        padding-left: 0.70rem !important;
        padding-right: 0.70rem !important;
        max-width: 100% !important;
    }

    /* Hero Header: Stack brand and institutional badge gracefully */
    .agri-header {
        padding: 0.95rem 0.90rem !important;
        border-radius: 14px !important;
        margin-bottom: 0.85rem !important;
    }

    .agri-header-row {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 12px !important;
    }

    .agri-header-brand {
        gap: 12px !important;
        width: 100% !important;
    }

    .hero-logo-badge {
        padding: 5px !important;
        border-radius: 12px !important;
    }

    .hero-logo-badge img {
        width: 44px !important;
        height: 44px !important;
    }

    .agri-title-pill-wrap {
        gap: 6px !important;
    }

    .agri-title {
        font-size: 1.45rem !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        hyphens: none !important;
    }

    .agri-version-pill {
        font-size: 0.62rem !important;
        padding: 2px 7px !important;
    }

    .agri-subtitle {
        font-size: 0.82rem !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.30rem !important;
        line-height: 1.30 !important;
    }

    .agri-tagline {
        padding: 0.25rem 0.60rem !important;
        font-size: 0.70rem !important;
        width: 100% !important;
        justify-content: flex-start !important;
    }

    /* Institutional Badge: Full-width balanced banner on mobile */
    .header-partner-badge {
        width: 100% !important;
        text-align: center !important;
        padding: 7px 10px !important;
        border-radius: 10px !important;
        box-sizing: border-box !important;
    }

    .header-partner-title {
        font-size: 0.68rem !important;
    }

    .header-partner-badge b {
        font-size: 0.76rem !important;
        line-height: 1.3 !important;
    }

    .header-partner-sub {
        font-size: 0.70rem !important;
    }

    /* Enterprise Silhouettes: Balanced 2x2 grid prevents cramped text */
    .silhouette-strip {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 6px !important;
        padding: 8px 8px !important;
        margin-bottom: 0.90rem !important;
    }

    .silhouette-item {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 7px !important;
        font-size: 0.75rem !important;
        background: rgba(46, 125, 50, 0.04) !important;
        padding: 6px 8px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(46, 125, 50, 0.10) !important;
    }

    .silhouette-item span {
        white-space: normal !important;
        line-height: 1.20 !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
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
        max-width: 130px !important;
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
    .agri-header {
        padding: 0.80rem 0.70rem !important;
    }

    .agri-title {
        font-size: 1.30rem !important;
    }

    .hero-logo-badge img {
        width: 38px !important;
        height: 38px !important;
    }

    .silhouette-strip {
        grid-template-columns: 1fr 1fr !important;
        gap: 5px !important;
    }

    .silhouette-item {
        font-size: 0.70rem !important;
        padding: 5px 6px !important;
    }

    .silhouette-item span {
        font-size: 0.70rem !important;
    }
}
</style>
"""
