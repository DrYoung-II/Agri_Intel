"""
Module 4: Plant Breeding Intelligence
Trait Prioritisation, GxE Stability, and Breeding Population Design for African Agro-ecologies
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core.crop_taxonomy import PAN_AFRICAN_CROPS, PAN_AFRICAN_ENVIRONMENTS, get_crop_breeding_profile
from core.broadcast_dispatcher import render_dispatch_trigger_card


def render_plant_breeding():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 🌽 Sélection Végétale & Création Variétale Quantitative")
        st.caption("Sélection génomique, priorisation quantitative des caractères, stabilité G×E et conception de populations de sélection adaptées aux agro-écologies africaines.")
    else:
        st.markdown("### 🌽 Plant Breeding & Cultivar Design Intelligence")
        st.caption("Genomic selection, quantitative trait prioritisation, G×E stability, and pan-African breeding population design.")

    c1, c2 = st.columns(2)
    with c1:
        crop_target_raw = st.selectbox(
            "Culture Panafricaine Cible :" if is_fr else "Target African Crop / Commodity:",
            PAN_AFRICAN_CROPS,
            index=0,
            help="Select any major African cereal, tuber, pulse, vegetable, or cash crop, or enter a custom African crop."
        )
        if "Custom Input" in crop_target_raw:
            custom_crop = st.text_input("Enter African Crop / Species Name:", "Enset (Ensete ventricosum)")
            crop_target = custom_crop.strip() if custom_crop.strip() else "Custom African Crop"
        else:
            custom_crop = ""
            crop_target = crop_target_raw

    with c2:
        agro_target_raw = st.selectbox(
            "Zone Agro-Écologique Cible :" if is_fr else "Target Agro-Ecological Environment:",
            PAN_AFRICAN_ENVIRONMENTS,
            index=1,
            help="Select any major pan-African agro-ecological zone or enter a custom ecological region."
        )
        if "Custom" in agro_target_raw:
            custom_agro = st.text_input("Enter Custom Agro-Ecological Environment:", "Sudano-Sahelian Riverine Transition Belt")
            agro_target = custom_agro.strip() if custom_agro.strip() else "Custom Agro-Ecological Environment"
        else:
            custom_agro = ""
            agro_target = agro_target_raw

    # Fetch dynamic crop breeding profile
    breeding_prof = get_crop_breeding_profile(crop_target_raw, custom_crop)
    trait_defs = breeding_prof["traits"]  # List of 4 tuples: (Trait Name, Default Weight)

    st.markdown("#### 🎯 Interactive Breeding Trait Prioritisation Engine")
    st.caption(f"Adjust relative economic, physiological, and environmental trait weights tailored for **{breeding_prof['category']}**:")

    # Stable sanitized keys based on crop name
    k_prefix = "".join(ch for ch in crop_target[:10] if ch.isalnum()).lower()
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        w_t1 = st.slider(f"{trait_defs[0][0]}:", 0, 100, int(trait_defs[0][1]), key=f"w_t1_{k_prefix}")
    with col_t2:
        w_t2 = st.slider(f"{trait_defs[1][0]}:", 0, 100, int(trait_defs[1][1]), key=f"w_t2_{k_prefix}")
    with col_t3:
        w_t3 = st.slider(f"{trait_defs[2][0]}:", 0, 100, int(trait_defs[2][1]), key=f"w_t3_{k_prefix}")
    with col_t4:
        w_t4 = st.slider(f"{trait_defs[3][0]}:", 0, 100, int(trait_defs[3][1]), key=f"w_t4_{k_prefix}")

    # Calculate selection index weights safely
    weights = [w_t1, w_t2, w_t3, w_t4]
    trait_names = [t[0] for t in trait_defs]
    total_w = sum(weights)
    
    if total_w == 0:
        norm_weights = {name: 0.25 for name in trait_names}
    else:
        norm_weights = {name: w / total_w for name, w in zip(trait_names, weights)}

    # Radar Chart of Breeding Weights
    max_val = max(norm_weights.values()) if norm_weights else 0.25
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=list(norm_weights.values()),
        theta=list(norm_weights.keys()),
        fill='toself',
        fillcolor='rgba(46, 125, 50, 0.35)',
        line=dict(color='#2E7D32', width=2.5)
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(max_val * 1.25, 0.35)])),
        showlegend=False,
        title=f"<b>Optimal Breeding Trait Weight Profile for {crop_target}</b>",
        height=380,
        margin=dict(t=40, b=20, l=50, r=50)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("#### 📑 Synthesized Breeding Strategy & Cultivar Deployment")
    st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🌱 Targeted Strategy for {crop_target} in {agro_target}</div>
1. <b>Primary Germplasm Base</b>: {breeding_prof['germplasm']}<br>
2. <b>Genomic & Molecular Targets</b>:<br>
   {breeding_prof['genomics']}<br>
3. <b>G×E Multi-Environment Trial (MET) Design</b>: {breeding_prof['trials']}<br>
4. <b>End-User Adoption Criteria</b>: {breeding_prof['adoption']}
</div>
""", unsafe_allow_html=True)

    # 1-Click Extension Radio Dispatch
    render_dispatch_trigger_card(
        source_module="Module 2 & 4: Plant Breeding & Cultivar Design",
        commodity=crop_target,
        region=agro_target,
        headline=f"New Resilient {crop_target} Seed Trait Profile & Planting Guidance",
        trigger_summary=f"Optimized breeding index confirmed for {crop_target} in {agro_target}. Trait priorities: {trait_names[0]} and {trait_names[1]}.",
        recommendation_summary=f"Farmers are advised to source certified seeds matching this profile ({breeding_prof['adoption'][:75]}...). Align planting dates with the first sustained rains."
    )
