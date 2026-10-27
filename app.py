"""
AgriIntel: The Generative Intelligence Platform for Agriculture
Africa-First, Globally Relevant Agricultural Intelligence Infrastructure
"""

import os
import re
import base64
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np

# Load brand icons and base64 helper
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

LOGO_B64 = get_base64_image(os.path.join("assets", "agriintel_logo.png"))
ICON_B64 = get_base64_image(os.path.join("assets", "agriintel_icon.png"))
icon_path = os.path.join("assets", "agriintel_icon.png")
page_icon_obj = Image.open(icon_path) if os.path.exists(icon_path) else "🌱"

# Page configuration
st.set_page_config(
    page_title="AgriIntel | Generative Intelligence Platform for Agriculture",
    page_icon=page_icon_obj,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import assets, config, and modules
from config import APP_NAME, APP_SUBTITLE, APP_TAGLINE, APP_MOTTO, FOUNDER_STORY, THEME, PAN_AFRICAN_REGIONS
from assets.styles import LEAF_GREEN_CSS
from assets.silhouettes import CATTLE_SVG, MAIZE_SVG, POULTRY_SVG, LEAF_SVG
from core.orchestrator import rule_based_agent_synthesis, call_live_llm_orchestration, AGENT_DESCRIPTIONS, validate_gemini_key, get_gemini_api_key, set_gemini_api_key
from core.exporter import render_download_buttons

from modules.suites import (
    render_suite_biometrics,
    render_suite_research_studio,
    render_suite_agro_ecosystems,
    render_suite_livestock,
    render_suite_policy,
    render_suite_tools
)

# -------------------------------------------------------------
# Google Gemini API Client Configuration
# -------------------------------------------------------------
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    genai = None

# Fetch the key securely from Streamlit secrets (or environment fallback)
gemini_key = ""
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    gemini_key = st.secrets["GEMINI_API_KEY"]
elif not gemini_key:
    gemini_key = os.getenv("GEMINI_API_KEY", "")

# Configure the Gemini API client & model
gemini_model = None
if gemini_key:
    set_gemini_api_key(gemini_key)
    if HAS_GENAI and genai is not None:
        try:
            genai.configure(api_key=gemini_key)
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            st.session_state["gemini_model"] = gemini_model
        except Exception:
            pass

# Inject Leaf Green CSS styling
st.markdown(LEAF_GREEN_CSS, unsafe_allow_html=True)


def main():
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # UNIFIED INSTITUTIONAL HERO BANNER
    # -------------------------------------------------------------
    st.markdown(f"""
<div class="agri-hero-banner">
    <div class="agri-hero-main">
        <div class="agri-hero-identity">
            <div class="agri-hero-logo">
                <img src="data:image/png;base64,{ICON_B64}" alt="AgriIntel Emblem" />
            </div>
            <div class="agri-hero-text">
                <div class="agri-hero-title-row">
                    <span class="agri-hero-title">{APP_NAME}</span>
                    <span class="agri-hero-pill">v1.0 Institutional</span>
                </div>
                <div class="agri-hero-subtitle">{APP_SUBTITLE}</div>
                <div class="agri-hero-framework">
                    <span>🏛️ Aligned with <b>CGIAR AI Hub &bull; IITA &bull; ILRI &bull; FAO &bull; IFPRI</b> &bull; Sub-Saharan NARS</span>
                </div>
            </div>
        </div>
        <div class="agri-hero-cert">
            <div class="agri-cert-tag">Africa-First Biometrics</div>
            <div class="agri-cert-status">100% Offline &bull; Live Multi-Agent AI</div>
        </div>
    </div>
    <div class="agri-hero-scope">
        <div class="agri-scope-label">Calibrated Systems:</div>
        <div class="agri-scope-chips">
            <div class="agri-chip"><span class="agri-chip-icon">{CATTLE_SVG}</span><span>Indigenous Cattle</span></div>
            <div class="agri-chip"><span class="agri-chip-icon">{MAIZE_SVG}</span><span>Drought Maize</span></div>
            <div class="agri-chip"><span class="agri-chip-icon">{POULTRY_SVG}</span><span>Poultry & Ruminants</span></div>
            <div class="agri-chip"><span class="agri-chip-icon">{LEAF_SVG}</span><span>Cassava & Soils</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # SIDEBAR NAVIGATION & OFFICIAL LOGO BRAND CARD
    # -------------------------------------------------------------
    with st.sidebar:
        # Official Brand Logo Card
        if LOGO_B64:
            st.markdown(f"""
<div class="sidebar-brand-card">
    <img src="data:image/png;base64,{LOGO_B64}" alt="AgriIntel Official Logo" />
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"### 🌿 **{APP_NAME} Engine**")
            st.caption("Intelligence infrastructure behind African agriculture")
        
        # Pan-African Regional & Currency Selector
        selected_region_label = st.selectbox(
            "🌍 Regional Context & Currency:",
            options=list(PAN_AFRICAN_REGIONS.keys()),
            index=0,
            help="Dynamically adapts currency symbols, commodity prices, and policy metrics across modules."
        )
        st.session_state["active_region"] = PAN_AFRICAN_REGIONS[selected_region_label]
        st.session_state["active_region_label"] = selected_region_label

        menu = st.radio(
            "Select Intelligence Suite:",
            [
                "🌟 Multi-Agent Orchestrator",
                "🧬 Agricultural Biometrics & Breeding Suite",
                "🔬 AI Research Scientist & Proposal Studio",
                "🌍 Agro-Ecosystems: Soil & Climate Intelligence",
                "🐄 Livestock & Veterinary Intelligence",
                "🏛️ Agricultural Policy & Economic Simulator",
                "⚙️ Knowledge Graph & Developer API Hub"
            ],
            index=0
        )

        st.markdown("---")
        active_sb_key = get_gemini_api_key()
        if active_sb_key:
            st.markdown(
                '<div style="background: rgba(46,125,50,0.18); border: 1px solid #81C784; '
                'border-radius: 6px; padding: 10px 14px; margin-bottom: 12px;">'
                '<div style="font-size: 0.80rem; font-weight: 700; color: #A5D6A7;">'
                '🟢 Live Google Gemini Engine Active'
                '</div>'
                '<div style="font-size: 0.72rem; color: #E8F5E9; margin-top: 2px;">'
                'Cloud Verified &bull; Secrets Secured'
                '</div></div>',
                unsafe_allow_html=True
            )
        else:
            with st.expander("🔑 Connect Google Gemini (Optional Free Key)", expanded=False):
                sb_gemini_key = st.text_input(
                    "Google Gemini Key:",
                    value="",
                    type="password",
                    placeholder="AIzaSy...",
                    key="sidebar_gemini_key_input",
                    help="Enter free Gemini key from aistudio.google.com"
                )
                cleaned_sb_key = (sb_gemini_key or "").strip().strip("'\"")
                if cleaned_sb_key:
                    set_gemini_api_key(cleaned_sb_key)
                    if HAS_GENAI and genai is not None:
                        try:
                            genai.configure(api_key=cleaned_sb_key)
                            st.session_state["gemini_model"] = genai.GenerativeModel("gemini-1.5-flash")
                        except Exception:
                            pass
                    val = validate_gemini_key(cleaned_sb_key)
                    if val.get("valid"):
                        st.success(f"🟢 {val.get('message')}")
                    else:
                        st.error(f"🔴 {val.get('message')}")
                else:
                    st.caption("Optional: Free key from [Google AI Studio](https://aistudio.google.com/) unlocks live AI everywhere.")

        with st.expander("📖 Founder Story & Vision", expanded=False):
            st.markdown(f"*{FOUNDER_STORY}*")

        st.markdown(f"""
<div style="text-align: center; padding: 6px 0; opacity: 0.88;">
    <div style="font-size: 0.72rem; letter-spacing: 0.6px; color: #C8E6C9; font-weight: 700; text-transform: uppercase;">
        {APP_MOTTO}
    </div>
    <div style="font-size: 0.70rem; color: #A5D6A7; margin-top: 2px;">
        AgriIntel v1.0 &bull; Africa-First Institutional Edition
    </div>
</div>
""", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ROUTE TO SELECTED INTELLIGENCE SUITE
    # -------------------------------------------------------------
    if menu == "🌟 Multi-Agent Orchestrator":
        render_orchestrator_home()
    elif menu == "🧬 Agricultural Biometrics & Breeding Suite":
        render_suite_biometrics()
    elif menu == "🔬 AI Research Scientist & Proposal Studio":
        render_suite_research_studio()
    elif menu == "🌍 Agro-Ecosystems: Soil & Climate Intelligence":
        render_suite_agro_ecosystems()
    elif menu == "🐄 Livestock & Veterinary Intelligence":
        render_suite_livestock()
    elif menu == "🏛️ Agricultural Policy & Economic Simulator":
        render_suite_policy()
    elif menu == "⚙️ Knowledge Graph & Developer API Hub":
        render_suite_tools()


def render_orchestrator_home():
    """
    Multi-Agent Orchestrator Home Panel
    """
    st.markdown("### 🤖 Multi-Agent Orchestration Layer")
    st.markdown(
        "A normal agricultural AI says: *'Upload a picture of your tomato leaf, and I will tell you what disease it has.'*<br>"
        "**AgriIntel says**: *'Give me a crop, animal, location, genotype, soil condition, climate scenario, production objective, "
        "research question or policy problem—and I will assemble the relevant evidence, analyze the available data, run appropriate models, "
        "explain the results, and recommend what should be done.'*",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("#### 💬 Ask AgriIntel Anything (Cross-Agent Query)")
    
    # Preset query chips
    sample_queries = [
        "🐇 The best breed of rabbit for the Nigerian climate",
        "🐔 How favourable is the climatic condition to poultry production at this period?",
        "🍅 Best tomato varieties and management for Western Nigeria at this period?",
        "🌽 Which maize varieties should Northern Nigerian farmers plant under increasing heat stress?",
        "🐟 Water quality and feeding management for catfish during the cold Harmattan period?",
        "🐐 Best management and PPR prevention for goats and sheep under dry season forage scarcity?",
        "🐄 What are the major genomic regions associated with heat tolerance and trypanosomiasis in West African cattle?",
        "📉 What happens if fertilizer prices increase by 40% and rainfall declines by 15% in Kaduna?",
        "💰 What agricultural interventions could create the largest food-security impact per ₦1 billion?"
    ]
    
    preset_choice = st.selectbox(
        "💡 Quick-Select Strategic Inquiry (or choose Custom to write your own):",
        options=["-- Type Your Own Custom Query Below --"] + sample_queries,
        index=1,
        help="Select any strategic preset inquiry to instantly populate the query box, or choose Custom to write your own."
    )
    
    if preset_choice == "-- Type Your Own Custom Query Below --":
        default_val = st.session_state.get("custom_typed_query", "")
    else:
        cleaned = preset_choice
        for prefix in ["🐇 ", "🐔 ", "🍅 ", "🌽 ", "🐟 ", "🐐 ", "🐄 ", "📉 ", "💰 "]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                break
        default_val = cleaned

    user_query = st.text_area(
        "Enter Agricultural Inquiry:",
        value=default_val,
        placeholder="Type any crop, livestock, poultry, fish, soil, or climate question here (e.g. The best breed of rabbit for the Nigerian climate)...",
        height=95
    )
    if preset_choice == "-- Type Your Own Custom Query Below --":
        st.session_state["custom_typed_query"] = user_query

    st.markdown("##### ⚙️ Intelligence Engine Mode")
    engine_choices = [
        "🟢 Live Google Gemini API (Cloud Multi-Agent Reasoning)",
        "⚡ Built-in African Agronomic Science Engine (Offline • Local Biometrics)"
    ]
    selected_engine = st.selectbox(
        "Select Engine:",
        options=engine_choices,
        index=0,
        help="Select whether AgriIntel runs with live Google Gemini cloud reasoning or local offline African scientific models."
    )

    api_key_to_use = ""
    provider_to_use = "gemini"

    if selected_engine == engine_choices[0]:
        active_key = get_gemini_api_key()
        if active_key:
            st.success("🟢 **Google Gemini Live Intelligence Active**: Cloud multi-agent reasoning is connected and secured via server secrets. Zero client-side key entry required.")
            api_key_to_use = active_key
            provider_to_use = "gemini"
        else:
            c_k1, c_k2 = st.columns([2, 1])
            with c_k1:
                input_gemini_key = st.text_input(
                    "Paste Google Gemini API Key:",
                    value="",
                    type="password",
                    placeholder="AIzaSy...",
                    help="Get a free API key at https://aistudio.google.com/"
                )
                cleaned_key = (input_gemini_key or "").strip().strip("'\"")
                if cleaned_key:
                    set_gemini_api_key(cleaned_key)
                    if HAS_GENAI and genai is not None:
                        try:
                            genai.configure(api_key=cleaned_key)
                            st.session_state["gemini_model"] = genai.GenerativeModel("gemini-1.5-flash")
                        except Exception:
                            pass
                    val = validate_gemini_key(cleaned_key)
                    if val.get("valid"):
                        st.success(f"🟢 **API Key Verified & Active**: {val.get('message')}")
                    else:
                        st.error(f"🔴 **Google AI Studio Key Notice**: `{val.get('message')}`")
                        st.caption("💡 *Tip: Ensure the key is active in [Google AI Studio](https://aistudio.google.com/), has no IP restrictions, and 'Generative Language API' is enabled.*")
                    api_key_to_use = cleaned_key
                else:
                    api_key_to_use = ""
                provider_to_use = "gemini"
            with c_k2:
                st.caption("🔑 **Free Tier Available**: Generate a free API key at [Google AI Studio](https://aistudio.google.com/). Live Gemini enables real-time reasoning across all 48+ African countries.")
    else:
        st.info("🌿 **Built-in African Agronomic Science Engine Active**: Operates 100% offline with zero external API calls. Powered by calibrated agronomic, edaphic, and genomic models for Western Nigeria (NIHORT, IITA), Northern Savanna, and East Africa.")
        api_key_to_use = ""
        provider_to_use = "offline"

    col_btn, col_mode = st.columns([1, 2])
    with col_btn:
        run_query = st.button("🚀 Invoke Agent Ensemble", key="btn_invoke_agents")
    with col_mode:
        if api_key_to_use:
            mode_label = f"🟢 Live Cloud LLM ({provider_to_use.title()})"
        else:
            mode_label = "⚡ Offline Deterministic Expert Mode (100% Free)"
        st.caption(f"Current Engine Status: **{mode_label}**")

    if run_query:
        if not user_query.strip():
            st.warning("⚠️ Please enter a question or select one of the strategic presets above.")
        else:
            with st.spinner("Decomposing question and dispatching specialized agents..."):
                active_reg = st.session_state.get("active_region")
                if api_key_to_use:
                    result = call_live_llm_orchestration(user_query, api_key_to_use, provider=provider_to_use, active_region=active_reg)
                else:
                    result = rule_based_agent_synthesis(user_query, active_region=active_reg)

            if result.get("unsupported"):
                st.warning(result["message"])
                st.info(result.get("suggestion", ""))
            else:
                st.success("✅ Multi-Agent Consultation Complete!")

                if result.get("is_live_cloud"):
                    st.info(f"🟢 **Live Cloud AI Consultation**: Generated via **{result.get('provider')} ({result.get('model')})** with your Google AI Studio API key.")
                elif result.get("live_api_error"):
                    st.warning(f"⚠️ **Live Cloud AI Notice**: Google Gemini API returned: `{result['live_api_error']}`. AgriIntel automatically served this consultation using its built-in **Offline African Agronomic Science Engine**.")
                elif not api_key_to_use and selected_engine == engine_choices[0]:
                    st.info(
                        "💡 **Offline Mode Notice**: No Gemini API key detected. "
                        "AgriIntel synthesized this consultation using its built-in **Offline African Agronomic Science Engine**. "
                        "To activate live unconstrained generative reasoning on any question, configure a free key from Google AI Studio above."
                    )

                # Dispatch Banner with Badges
                st.markdown(f"""
<div style="background: #E8F5E9; border-left: 5px solid #2E7D32; border-radius: 6px; padding: 12px 16px; margin: 12px 0 18px 0;">
    <div style="font-size: 0.82rem; font-weight: 700; color: #1B5E20; text-transform: uppercase; letter-spacing: 0.5px;">
        🏛️ Multi-Agent Dispatch Roster &bull; {len(result['selected_agents'])} Specialized Disciplines
    </div>
    <div style="margin-top: 6px; display: flex; flex-wrap: wrap; gap: 8px;">
        {' '.join([f'<span style="background: #FFFFFF; border: 1px solid #A5D6A7; color: #1B5E20; font-size: 0.78rem; font-weight: 600; padding: 3px 8px; border-radius: 4px;">🤖 {a}</span>' for a in result['selected_agents']])}
    </div>
</div>
""", unsafe_allow_html=True)

                tab_advisory, tab_agents = st.tabs([
                    "📑 Consolidated Scientific Advisory & Action Plan",
                    "👥 Individual Specialist Agent Deliberations"
                ])

                with tab_advisory:
                    st.markdown(result["final_synthesis"])
                    
                    st.markdown("---")
                    clean_title = re.sub(r'[^a-zA-Z0-9_]', '_', user_query[:30]).strip('_')
                    render_download_buttons(
                        content_text=result["final_synthesis"],
                        filename_prefix=f"AgriIntel_Advisory_{clean_title}",
                        title=f"AgriIntel Scientific Advisory: {user_query[:60]}",
                        key_prefix="orch_advisory"
                    )

                with tab_agents:
                    st.markdown("##### 👥 Disciplinary Consultations from Dispatched Agents")
                    st.caption("Inspect the granular domain-specific reasoning contributed by each specialized agent:")

                    for agent_name in result["selected_agents"]:
                        out_text = result["agent_outputs"].get(agent_name, "Consulted and contributed to synthesis.")
                        st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #2E7D32; margin-bottom: 1rem; background: #FAFCFA;">
    <div style="font-size: 0.95rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">
        🤖 {agent_name}
    </div>
    <div style="font-size: 0.88rem; color: #1B381E; line-height: 1.5;">
""", unsafe_allow_html=True)
                        st.markdown(out_text)
                        st.markdown("</div></div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
