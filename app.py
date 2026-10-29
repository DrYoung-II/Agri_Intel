"""
AgroBiometrix: The Quantitative Biometrics & Generative Intelligence Platform for Agriculture
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

LOGO_B64 = get_base64_image(os.path.join("assets", "agrobiometrix_logo.png"))
ICON_B64 = get_base64_image(os.path.join("assets", "agrobiometrix_icon.png"))
NAYSA_B64 = get_base64_image(os.path.join("assets", "naysa84_labs_logo.png"))
icon_path = os.path.join("assets", "agrobiometrix_icon.png")
page_icon_obj = Image.open(icon_path) if os.path.exists(icon_path) else "🌱"

# Page configuration
st.set_page_config(
    page_title="AgroBiometrix | Quantitative Biometrics & Generative Intelligence for Agriculture",
    page_icon=page_icon_obj,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import assets, config, and modules
import importlib
import config
import assets.styles
import core.i18n
try:
    importlib.reload(config)
    importlib.reload(assets.styles)
    importlib.reload(core.i18n)
except Exception:
    pass
from config import APP_NAME, APP_SUBTITLE, APP_TAGLINE, APP_MOTTO, FOUNDER_STORY, THEME, PAN_AFRICAN_REGIONS
from assets.styles import LEAF_GREEN_CSS
from core.orchestrator import rule_based_agent_synthesis, call_live_llm_orchestration, AGENT_DESCRIPTIONS, validate_gemini_key, get_gemini_api_key, set_gemini_api_key
from core.exporter import render_download_buttons
from core.i18n import t, get_current_lang
try:
    from core.i18n import translate_agent_name
except Exception:
    def translate_agent_name(name, lang=None):
        return name

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

# Synchronize interface language from radio state if already toggled by user
if "app_language_toggle" in st.session_state:
    st.session_state["app_lang"] = "fr" if "Français" in st.session_state["app_language_toggle"] else "en"
elif "app_lang" not in st.session_state:
    st.session_state["app_lang"] = "en"

# Inject Leaf Green CSS styling
st.markdown(LEAF_GREEN_CSS, unsafe_allow_html=True)


def main():
    cur_lang = st.session_state.get("app_lang", "en")
    pill_text = "v1.0 Institutionnel" if cur_lang == "fr" else "v1.0 Institutional"
    cert_badge = t("hero_cert_badge", cur_lang)
    cert_sub = t("hero_cert_sub", cur_lang)
    hero_sub = t("hero_sub", cur_lang)
    hero_framework = t("hero_framework", cur_lang)

    # -------------------------------------------------------------
    # UNIFIED INSTITUTIONAL HERO BANNER
    # -------------------------------------------------------------
    st.markdown(f"""
<div class="agri-hero-banner" style="background: linear-gradient(135deg, #0A2F10 0%, #134B1B 45%, #1B5E20 85%, #103B14 100%); border-radius: 14px; color: #FFFFFF; overflow: hidden; margin-bottom: 1.15rem; border: 1px solid rgba(129, 199, 132, 0.32);">
    <div class="agri-hero-main" style="display: flex; justify-content: space-between; align-items: center; padding: 1.15rem 1.40rem 1.0rem 1.40rem; gap: 18px;">
        <div class="agri-hero-identity" style="display: flex; align-items: center; gap: 16px; min-width: 0;">
            <div class="agri-hero-logo" style="background: #FFFFFF; border-radius: 12px; padding: 6px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 64px; height: 64px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);">
                <img src="data:image/png;base64,{ICON_B64}" alt="AgroBiometrix Emblem" style="width: 52px; height: 52px; max-width: 52px; max-height: 52px; object-fit: contain; display: block;" />
            </div>
            <div class="agri-hero-text">
                <div class="agri-hero-title-row">
                    <span class="agri-hero-title"><span style="color: #81C784; font-weight: 800;">Agro</span><span style="color: #FFFFFF; font-weight: 800;">Biometrix</span></span>
                    <span class="agri-hero-pill">{pill_text}</span>
                </div>
                <div class="agri-hero-subtitle">{hero_sub}</div>
                <div class="agri-hero-framework">
                    <span>🏛️ {hero_framework}</span>
                </div>
            </div>
        </div>
        <div class="agri-hero-cert" style="text-align: right; flex-shrink: 0;">
            <div class="agri-cert-tag">{cert_badge}</div>
            <div class="agri-cert-status">{cert_sub}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # SIDEBAR NAVIGATION & OFFICIAL LOGO BRAND CARD
    # -------------------------------------------------------------
    with st.sidebar:
        # Official Brand Logo Card
        curr_logo = get_base64_image(os.path.join("assets", "agrobiometrix_logo.png")) or LOGO_B64
        if curr_logo:
            st.markdown(f"""
<div class="sidebar-brand-card">
    <img src="data:image/png;base64,{curr_logo}" alt="AgroBiometrix Official Logo" />
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("### 🌿 **<span style='color: #4CAF50;'>Agro</span><span style='color: #1B5E20;'>Biometrix</span> Engine**", unsafe_allow_html=True)
            st.caption("Intelligence infrastructure behind African agriculture")
        
        # Bilingual Language Switcher (English / Français)
        lang_choice = st.radio(
            t("lang_selector_label", cur_lang),
            options=["English 🇬🇧", "Français 🇫🇷"],
            index=0 if cur_lang == "en" else 1,
            horizontal=True,
            key="app_language_toggle"
        )
        new_lang = "fr" if "Français" in lang_choice else "en"
        if new_lang != cur_lang:
            st.session_state["app_lang"] = new_lang
            cur_lang = new_lang
            st.rerun()
        
        # Pan-African Regional & Currency Selector
        selected_region_label = st.selectbox(
            t("region_selector_label", cur_lang),
            options=list(PAN_AFRICAN_REGIONS.keys()),
            index=0,
            help=t("region_selector_help", cur_lang)
        )
        st.session_state["active_region"] = PAN_AFRICAN_REGIONS[selected_region_label]
        st.session_state["active_region_label"] = selected_region_label

        suite_options = [
            t("suite_orchestrator", cur_lang),
            t("suite_biometrics", cur_lang),
            t("suite_scientist", cur_lang),
            t("suite_agro", cur_lang),
            t("suite_livestock", cur_lang),
            t("suite_policy", cur_lang),
            t("suite_api", cur_lang)
        ]
        menu = st.radio(
            t("suite_selector_label", cur_lang),
            suite_options,
            index=0
        )

        st.markdown("---")
        active_sb_key = get_gemini_api_key()
        if active_sb_key:
            st.markdown(f"""
<div style="background: rgba(46,125,50,0.22); border: 1px solid #81C784; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
    <div style="font-size: 0.80rem; font-weight: 700; color: #A5D6A7;">
        {t("gemini_active", cur_lang)}
    </div>
    <div style="font-size: 0.72rem; color: #E8F5E9; margin-top: 2px;">
        {t("gemini_secured", cur_lang)}
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            with st.expander(t("connect_gemini_label", cur_lang), expanded=False):
                sb_gemini_key = st.text_input(
                    t("gemini_key_prompt", cur_lang),
                    value="",
                    type="password",
                    placeholder="AIzaSy...",
                    key="sidebar_gemini_key_input",
                    help="Entrez une clé gratuite sur aistudio.google.com" if cur_lang == "fr" else "Enter free Gemini key from aistudio.google.com"
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
                    caption_hint = "Optionnel : Clé gratuite sur [Google AI Studio](https://aistudio.google.com/) pour activer l'IA partout." if cur_lang == "fr" else "Optional: Free key from [Google AI Studio](https://aistudio.google.com/) unlocks live AI everywhere."
                    st.caption(caption_hint)

        with st.expander(t("founder_story_label", cur_lang), expanded=False):
            st.markdown(f"*{FOUNDER_STORY}*")

        st.markdown(f"""
<div style="text-align: center; padding: 6px 0; opacity: 0.88;">
    <div style="font-size: 0.72rem; letter-spacing: 0.6px; color: #C8E6C9; font-weight: 700; text-transform: uppercase;">
        {t("app_motto", cur_lang)}
    </div>
    <div style="font-size: 0.70rem; color: #A5D6A7; margin-top: 2px;">
        {t("edition_label", cur_lang)}
    </div>
</div>
""", unsafe_allow_html=True)

        # Naysa-84 Labs Sidebar Attribution Card
        curr_naysa = get_base64_image(os.path.join("assets", "naysa84_labs_logo.png")) or NAYSA_B64
        if curr_naysa:
            st.markdown(f"""
<div class="sidebar-naysa-card">
    <div style="font-size: 0.65rem; font-weight: 800; color: #81C784; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">{t("powered_by", cur_lang)}</div>
    <img src="data:image/png;base64,{curr_naysa}" alt="Naysa-84 Labs" />
    <div style="font-size: 0.76rem; color: #FFFFFF; font-weight: 700; margin-top: 5px; letter-spacing: 0.2px;">Naysa-84 Labs</div>
    <div style="font-size: 0.68rem; color: #80DEEA; font-style: italic;">{t("unlocking_data", cur_lang)}</div>
</div>
""", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ROUTE TO SELECTED INTELLIGENCE SUITE
    # -------------------------------------------------------------
    if "Orchestrator" in menu or "Orchestrateur" in menu:
        render_orchestrator_home()
    elif "Biometrics" in menu or "Biométrie" in menu:
        render_suite_biometrics()
    elif "Scientist" in menu or "Chercheur" in menu:
        render_suite_research_studio()
    elif "Agro-Ecosystems" in menu or "Agro-Écosystèmes" in menu:
        render_suite_agro_ecosystems()
    elif "Livestock" in menu or "Élevage" in menu or "Zootechnique" in menu or "Vétérinaire" in menu:
        render_suite_livestock()
    elif "Policy" in menu or "Politique" in menu or "Politiques" in menu:
        render_suite_policy()
    elif "Knowledge" in menu or "Connaissances" in menu or "API" in menu:
        render_suite_tools()

    # -------------------------------------------------------------
    # INSTITUTIONAL FOOTER (POWERED BY NAYSA-84 LABS)
    # -------------------------------------------------------------
    render_page_footer()


def render_page_footer():
    """Renders the unified institutional footer at the base of every page."""
    naysa_b64 = get_base64_image(os.path.join("assets", "naysa84_labs_logo.png")) or NAYSA_B64
    st.markdown("---")
    cur_lang = st.session_state.get("app_lang", "en")
    st.markdown(f"""
<div class="agri-footer-card">
    <div class="agri-footer-inner">
        <div class="agri-footer-brand">
            <span class="agri-footer-badge">{t("footer_badge", cur_lang)}</span>
            <div class="agri-footer-title">{t("footer_title", cur_lang)}</div>
            <div class="agri-footer-subtitle">{t("footer_subtitle", cur_lang)}</div>
            <div class="agri-footer-legal">{t("footer_legal", cur_lang)}</div>
        </div>
        <div class="agri-footer-attribution">
            <div class="agri-footer-powered-label">{t("powered_by", cur_lang)}</div>
            <div class="agri-footer-naysa-card">
                <img src="data:image/png;base64,{naysa_b64}" alt="Naysa-84 Labs Logo" />
            </div>
            <div class="agri-footer-naysa-name">Naysa-84 Labs</div>
            <div class="agri-footer-naysa-tagline"><i>{t("unlocking_data", cur_lang)}</i></div>
        </div>
    </div>
    <div class="agri-footer-bottom">
        <div>{t("footer_rights", cur_lang)}</div>
        <div class="agri-footer-links">{t("footer_meta", cur_lang)}</div>
    </div>
</div>
""", unsafe_allow_html=True)


def render_orchestrator_home():
    """
    Multi-Agent Orchestrator Home Panel
    """
    cur_lang = st.session_state.get("app_lang", "en")

    st.markdown(f"### 🤖 {t('orch_header', cur_lang)}")
    st.markdown(t("orch_quote", cur_lang), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"#### 💬 {t('orch_ask_label', cur_lang)}")
    st.caption(t("orch_ask_sub", cur_lang))
    
    # Preset query chips
    if cur_lang == "fr":
        sample_queries = [
            "🐇 Meilleure race de lapin pour le climat ouest-africain et sahélien",
            "🐔 Conditions climatiques et conduite d'élevage avicole en période actuelle",
            "🍅 Variétés de tomates performantes et gestion sanitaire en zone tropicale humide",
            "🌽 Quelles variétés de maïs cultiver face au stress thermique et hydrique croissant au Sahel ?",
            "🐟 Qualité de l'eau et alimentation du silure (poisson-chat) en période d'harmattan",
            "🐐 Conduite d'élevage et prévention de la PPR chez les caprins et ovins en saison sèche",
            "🐄 Régions génomiques associées à la thermotolérance et à la trypanosomiase chez les bovins africains",
            "📉 Impact d'une hausse de 40% des engrais et baisse pluviométrique de 15% sur les rendements céréaliers",
            "💰 Quelles interventions agricoles offrent le plus fort impact sur la sécurité alimentaire ?"
        ]
        custom_opt = t("orch_custom_choice", "fr")
    else:
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
        custom_opt = t("orch_custom_choice", "en")
    
    preset_choice = st.selectbox(
        t("orch_preset_label", cur_lang),
        options=[custom_opt] + sample_queries,
        index=1,
        help="Sélectionnez une requête prédéfinie pour remplir le champ ou choisissez Personnalisée pour rédiger la vôtre." if cur_lang == "fr" else "Select any strategic preset inquiry to instantly populate the query box, or choose Custom to write your own."
    )
    
    if preset_choice == custom_opt:
        default_val = st.session_state.get("custom_typed_query", "")
    else:
        cleaned = preset_choice
        for prefix in ["🐇 ", "🐔 ", "🍅 ", "🌽 ", "🐟 ", "🐐 ", "🐄 ", "📉 ", "💰 "]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                break
        default_val = cleaned

    user_query = st.text_area(
        t("orch_query_label", cur_lang),
        value=default_val,
        placeholder=t("orch_query_placeholder", cur_lang),
        height=95
    )
    if preset_choice == custom_opt:
        st.session_state["custom_typed_query"] = user_query

    st.markdown(f"##### ⚙️ {t('orch_engine_mode', cur_lang)}")
    engine_gemini = t("orch_engine_gemini", cur_lang)
    engine_offline = t("orch_engine_offline", cur_lang)
    engine_choices = [engine_gemini, engine_offline]

    selected_engine = st.selectbox(
        t("orch_engine_select", cur_lang),
        options=engine_choices,
        index=0,
        help=t("orch_engine_help", cur_lang)
    )

    api_key_to_use = ""
    provider_to_use = "gemini"

    if selected_engine == engine_choices[0]:
        active_key = get_gemini_api_key()
        if active_key:
            st.success(t("orch_gemini_active_msg", cur_lang))
            api_key_to_use = active_key
            provider_to_use = "gemini"
        else:
            c_k1, c_k2 = st.columns([2, 1])
            with c_k1:
                key_prompt = "Coller la Clé API Google Gemini :" if cur_lang == "fr" else "Paste Google Gemini API Key:"
                input_gemini_key = st.text_input(
                    key_prompt,
                    value="",
                    type="password",
                    placeholder="AIzaSy...",
                    help="Obtenez une clé API gratuite sur https://aistudio.google.com/" if cur_lang == "fr" else "Get a free API key at https://aistudio.google.com/"
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
                        msg_ok = "Clé API Vérifiée & Active" if cur_lang == "fr" else "API Key Verified & Active"
                        st.success(f"🟢 **{msg_ok}**: {val.get('message')}")
                    else:
                        msg_err = "Notification Clé Google AI Studio" if cur_lang == "fr" else "Google AI Studio Key Notice"
                        st.error(f"🔴 **{msg_err}**: `{val.get('message')}`")
                        tip_msg = "💡 *Conseil : Vérifiez que la clé est active dans Google AI Studio et que l'API Generative Language est activée.*" if cur_lang == "fr" else "💡 *Tip: Ensure the key is active in [Google AI Studio](https://aistudio.google.com/), has no IP restrictions, and 'Generative Language API' is enabled.*"
                        st.caption(tip_msg)
                    api_key_to_use = cleaned_key
                else:
                    api_key_to_use = ""
                provider_to_use = "gemini"
            with c_k2:
                tier_msg = "🔑 **Niveau Gratuit Disponible** : Obtenez une clé gratuite sur [Google AI Studio](https://aistudio.google.com/). Gemini en direct permet un raisonnement instantané sur l'ensemble des 48+ pays africains." if cur_lang == "fr" else "🔑 **Free Tier Available**: Generate a free API key at [Google AI Studio](https://aistudio.google.com/). Live Gemini enables real-time reasoning across all 48+ African countries."
                st.caption(tier_msg)
    else:
        st.info(t("orch_offline_active_msg", cur_lang))
        api_key_to_use = ""
        provider_to_use = "offline"

    col_btn, col_mode = st.columns([1, 2])
    with col_btn:
        run_query = st.button(t("orch_btn_run", cur_lang), key="btn_invoke_agents")
    with col_mode:
        if api_key_to_use:
            mode_label = f"🟢 IA Cloud en Direct ({provider_to_use.title()})" if cur_lang == "fr" else f"🟢 Live Cloud LLM ({provider_to_use.title()})"
        else:
            mode_label = t("orch_status_offline", cur_lang)
        st.caption(f"{t('orch_status_label', cur_lang)} **{mode_label}**")

    if run_query:
        if not user_query.strip():
            st.warning(t("orch_query_warning", cur_lang))
        else:
            with st.spinner(t("orch_spinner", cur_lang)):
                active_reg = st.session_state.get("active_region")
                if api_key_to_use:
                    result = call_live_llm_orchestration(user_query, api_key_to_use, provider=provider_to_use, active_region=active_reg, lang=cur_lang)
                else:
                    result = rule_based_agent_synthesis(user_query, active_region=active_reg, lang=cur_lang)

            if result.get("unsupported"):
                st.warning(result["message"])
                st.info(result.get("suggestion", ""))
            else:
                st.success(t("orch_complete", cur_lang))

                if result.get("is_live_cloud"):
                    cloud_notice = f"🟢 **Consultation IA Cloud en Direct** : Générée via **{result.get('provider')} ({result.get('model')})**." if cur_lang == "fr" else f"🟢 **Live Cloud AI Consultation**: Generated via **{result.get('provider')} ({result.get('model')})** with your Google AI Studio API key."
                    st.info(cloud_notice)
                elif result.get("live_api_error"):
                    warn_notice = f"⚠️ **Notification IA Cloud** : L'API Google Gemini a retourné : `{result['live_api_error']}`. AgroBiometrix a automatiquement basculé sur son **Moteur Scientifique Agronomique Africain Hors-ligne**." if cur_lang == "fr" else f"⚠️ **Live Cloud AI Notice**: Google Gemini API returned: `{result['live_api_error']}`. AgroBiometrix automatically served this consultation using its built-in **Offline African Agronomic Science Engine**."
                    st.warning(warn_notice)
                elif not api_key_to_use and selected_engine == engine_choices[0]:
                    off_notice = "💡 **Mode Hors-ligne Actif** : Aucune clé Gemini détectée. AgroBiometrix a synthétisé cette consultation via son **Moteur Scientifique Agronomique Africain Intégré**." if cur_lang == "fr" else "💡 **Offline Mode Notice**: No Gemini API key detected. AgroBiometrix synthesized this consultation using its built-in **Offline African Agronomic Science Engine**."
                    st.info(off_notice)

                # Dispatch Banner with Badges
                roster_hdr = f"🏛️ {t('orch_roster_title', cur_lang)} &bull; {len(result['selected_agents'])} {t('orch_roster_sub', cur_lang)}"
                agent_tags = ' '.join([
                    f'<span style="background: #FFFFFF; border: 1px solid #A5D6A7; color: #1B5E20; font-size: 0.78rem; font-weight: 600; padding: 3px 8px; border-radius: 4px;">🤖 {translate_agent_name(a, cur_lang)}</span>'
                    for a in result['selected_agents']
                ])
                st.markdown(f"""
<div style="background: #E8F5E9; border-left: 5px solid #2E7D32; border-radius: 6px; padding: 12px 16px; margin: 12px 0 18px 0;">
    <div style="font-size: 0.82rem; font-weight: 700; color: #1B5E20; text-transform: uppercase; letter-spacing: 0.5px;">
        {roster_hdr}
    </div>
    <div style="margin-top: 6px; display: flex; flex-wrap: wrap; gap: 8px;">
        {agent_tags}
    </div>
</div>
""", unsafe_allow_html=True)

                tab_advisory, tab_agents = st.tabs([
                    t("orch_advisory_tab", cur_lang),
                    t("orch_agents_tab", cur_lang)
                ])

                with tab_advisory:
                    st.markdown(result["final_synthesis"])
                    
                    st.markdown("---")
                    clean_title = re.sub(r'[^a-zA-Z0-9_]', '_', user_query[:30]).strip('_')
                    file_prefix = f"AgroBiometrix_{'Avis' if cur_lang == 'fr' else 'Advisory'}_{clean_title}"
                    report_title = f"{'Avis Scientifique AgroBiometrix' if cur_lang == 'fr' else 'AgroBiometrix Scientific Advisory'}: {user_query[:60]}"
                    render_download_buttons(
                        content_text=result["final_synthesis"],
                        filename_prefix=file_prefix,
                        title=report_title,
                        key_prefix="orch_advisory"
                    )

                with tab_agents:
                    st.markdown(f"##### {t('orch_consultations_title', cur_lang)}")
                    st.caption(t("orch_consultations_sub", cur_lang))

                    for agent_name in result["selected_agents"]:
                        out_text = result["agent_outputs"].get(agent_name, "Consulté et intégré à la synthèse." if cur_lang == "fr" else "Consulted and contributed to synthesis.")
                        fr_agent = translate_agent_name(agent_name, cur_lang)
                        st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #2E7D32; margin-bottom: 1rem; background: #FAFCFA;">
    <div style="font-size: 0.95rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">
        🤖 {fr_agent}
    </div>
    <div style="font-size: 0.88rem; color: #1B381E; line-height: 1.5;">
""", unsafe_allow_html=True)
                        st.markdown(out_text)
                        st.markdown("</div></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
