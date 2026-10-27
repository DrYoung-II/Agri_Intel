"""
Module 15: API Subscription Hub & Accessible Domains Directory
Complete guide on where to subscribe to paid/free APIs, direct links, and API key management.
"""

import pandas as pd
import streamlit as st
from config import API_DIRECTORY
from core.orchestrator import get_gemini_api_key, set_gemini_api_key, validate_gemini_key


def render_api_hub():
    st.markdown("### 🔌 API Subscriptions, Accessible Domains & Integration Hub")
    st.caption("Complete transparency on where to obtain API keys, direct links to subscribe, pricing models, and key configuration.")

    st.markdown("""
<div class="agri-explainer-box">
<div class="agri-explainer-title">💡 Zero-Cost Test Running Guarantee</div>
<b>AgriIntel is designed to run 100% free out of the box!</b><br>
All core statistical models (ANOVA, Duncan's Multiple Range Test, BLUP), soil diagnostic algorithms, climate scenario engines, 
and knowledge graphs execute locally using deterministic scientific pipelines and preloaded African agricultural databases.<br>
Connecting Google Gemini is strictly <b>optional</b> (free tier available at Google AI Studio) and is only required if you want live real-time LLM agent synthesis.
</div>
""", unsafe_allow_html=True)

    # API Configuration Section
    st.markdown("#### 🔑 Live AI Engine (Google Gemini)")
    current_k = get_gemini_api_key()
    if current_k:
        val = validate_gemini_key(current_k)
        if val.get("valid"):
            st.success("🟢 **Google Gemini Live API Connected & Active**: Secured via Streamlit Cloud Secrets. All multi-agent reasoning is authenticated server-side with zero client-side key exposure.")
        else:
            st.warning(f"🟡 **Google Gemini Status**: {val.get('message')}")
    else:
        gemini_key = st.text_input(
            "Google Gemini API Key (Recommended - Free Tier Available):",
            value="",
            type="password",
            help="Get your free key at https://aistudio.google.com/"
        )
        cleaned_gk = (gemini_key or "").strip().strip("'\"")
        if cleaned_gk:
            set_gemini_api_key(cleaned_gk)
            current_k = cleaned_gk
            val = validate_gemini_key(current_k)
            if val.get("valid"):
                st.success(f"🟢 **Key Active & Synchronized**: {val.get('message')}")
            else:
                st.error(f"🔴 **Key Notice**: {val.get('message')}")

    st.markdown("---")
    st.markdown("#### 📚 Comprehensive Directory of Agricultural & AI APIs")

    # Filter by Paid vs Free
    api_filter = st.radio("Filter API Directory:", ["All APIs", "Paid / Freemium APIs", "100% Free / Open Access APIs"], horizontal=True)

    for api in API_DIRECTORY:
        if api_filter == "Paid / Freemium APIs" and not api["is_paid"]:
            continue
        if api_filter == "100% Free / Open Access APIs" and api["is_paid"]:
            continue

        cost_badge = "💰 Paid / Freemium" if api["is_paid"] else "🆓 100% Free & Open"
        with st.expander(f"{api['name']} ({cost_badge}) — {api['category']}", expanded=True):
            st.markdown(f"**Provider**: {api['provider']}")
            st.markdown(f"**Direct Subscription Link**: [{api['link']}]({api['link']})")
            st.markdown(f"**Accessible Domains**: `{api['accessible_domain']}`")
            st.markdown(f"**Pricing Details**: {api['pricing']}")
            st.markdown(f"**Usage in AgriIntel**: {api['usage_in_app']}")
            st.markdown(f"**How to Subscribe / Setup**:\n```\n{api['how_to_subscribe']}\n```")
