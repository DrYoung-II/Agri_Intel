"""
Module 5: Soil Intelligence & Economic What-If Simulator
Edaphic Health Diagnosis, Nutrient Deficiency Analysis, and Scenario Simulation
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core.crop_taxonomy import PAN_AFRICAN_CROPS, get_crop_climate_profile


def render_soil_intelligence():
    st.markdown("### 🌍 Soil Intelligence & Scenario Simulation Engine")
    st.caption("Precision edaphic diagnostics, balanced nutrient strategy, and what-if economic/climate shock simulations.")

    tab_diag, tab_scenario = st.tabs(["🧪 Soil Health Diagnosis & Fertilizer Strategy", "📈 What-If Scenario Simulator"])

    # Load soil database
    soil_path = os.path.join("data", "sample_soil_profiles_africa.csv")
    df_soil_samples = pd.read_csv(soil_path) if os.path.exists(soil_path) else None

    with tab_diag:
        st.markdown("#### 🌾 Input Soil Test Parameters")
        
        mode = st.radio("Choose Input Mode:", ["Select Pre-loaded African Soil Profile", "Enter Manual Soil Sample"], horizontal=True)
        
        if mode == "Select Pre-loaded African Soil Profile" and df_soil_samples is not None and not df_soil_samples.empty:
            chosen_loc = st.selectbox("Select Soil Sample Location:", df_soil_samples["Location"].tolist())
            row = df_soil_samples[df_soil_samples["Location"] == chosen_loc].iloc[0]
            ph_val = float(row["Soil_pH"])
            n_val = float(row["Nitrogen_pct"])
            p_val = float(row["Phosphorus_ppm"])
            k_val = float(row["Potassium_cmol_kg"])
            oc_val = float(row["Organic_Carbon_pct"])
            texture_val = str(row["Texture"])
            cec_val = float(row["CEC_cmol_kg"])
            rainfall_val = float(row["Annual_Rainfall_mm"])
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                ph_val = st.number_input("Soil pH (1:1 H2O):", 3.5, 9.0, 5.8, 0.1)
                n_val = st.number_input("Total Nitrogen (%):", 0.01, 0.80, 0.08, 0.01)
                texture_val = st.selectbox("Texture Class:", ["Sandy Loam", "Loamy Sand", "Sand", "Clay Loam", "Sandy Clay"])
            with c2:
                p_val = st.number_input("Available Phosphorus (Bray-1 ppm):", 1.0, 50.0, 7.5, 0.5)
                k_val = st.number_input("Exchangeable K (cmol/kg):", 0.05, 2.0, 0.22, 0.02)
                cec_val = st.number_input("Cation Exchange Capacity (CEC):", 1.0, 40.0, 6.5, 0.5)
            with c3:
                oc_val = st.number_input("Organic Carbon (%):", 0.1, 5.0, 0.65, 0.05)
                rainfall_val = st.number_input("Annual Rainfall (mm):", 300, 3000, 1050, 50)

        st.markdown("---")
        st.markdown("#### 🩺 Comprehensive Soil Health Assessment")

        col1, col2, col3, col4 = st.columns(4)
        ph_status = "Optimal" if 6.0 <= ph_val <= 7.0 else ("Acidic (P-Fix)" if ph_val < 6.0 else "Alkaline")
        col1.metric("Soil pH", f"{ph_val:.1f}", ph_status)
        n_status = "Adequate" if n_val >= 0.15 else "Deficient"
        col2.metric("Total Nitrogen", f"{n_val:.2f}%", n_status)
        p_status = "Adequate" if p_val >= 15 else "Critically Low"
        col3.metric("Available P", f"{p_val:.1f} ppm", p_status)
        oc_status = "Adequate" if oc_val >= 1.5 else "Low (<1.5%)"
        col4.metric("Organic Carbon", f"{oc_val:.2f}%", oc_status)

        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🌱 Precision Fertilizer & Edaphic Strategy</div>
• <b>Acidity & Liming</b>: {f'Soil pH is {ph_val:.1f} (acidic). Aluminium and iron toxicity induce severe phosphorus fixation. Apply 1.0 - 1.5 tons/ha of agricultural lime (CaCO3) or dolomitic limestone 3 weeks prior to planting.' if ph_val < 5.5 else f'Soil pH is {ph_val:.1f}, within an acceptable range for cereal and legume growth.'}<br>
• <b>Phosphorus Priming</b>: Available P is {p_val:.1f} ppm ({p_status}). Recommend basal band-placement of Single Super Phosphate (SSP) or Di-ammonium Phosphate (DAP) at 40 kg P2O5/ha to stimulate early root proliferation.<br>
• <b>Soil Organic Matter & CEC</b>: CEC is {cec_val:.1f} cmol/kg with low organic carbon ({oc_val:.2f}%). Sandy texture promotes rapid leaching of soluble nutrients. Incorporate 3.0 tons/ha of crop residue compost or biochar to expand cation exchange sites.<br>
• <b>Nitrogen Split Application</b>: Apply 1/3 Nitrogen at planting and 2/3 at 4-5 weeks after emergence (knee-high stage) to prevent volatilisation and leaching losses.
</div>
""", unsafe_allow_html=True)

    with tab_scenario:
        st.markdown("#### 🔮 Agricultural Scenario Simulation")
        st.caption("Evaluate what happens to yield, input economics, and profit under climate shocks and price volatility across diverse African crops.")

        sc_c1, sc_c2, sc_c3 = st.columns(3)
        with sc_c1:
            crop_choice_raw = st.selectbox(
                "Target African Crop / Enterprise:",
                PAN_AFRICAN_CROPS,
                index=0,
                help="Select any African cereal, tuber, legume, vegetable, or cash crop, or enter a custom crop."
            )
            if "Custom Input" in crop_choice_raw:
                custom_sim_crop = st.text_input("Enter African Crop / Commodity:", "Cassava (Manihot esculenta)")
                sim_crop_name = custom_sim_crop.strip() if custom_sim_crop.strip() else "Custom African Crop"
            else:
                custom_sim_crop = ""
                sim_crop_name = crop_choice_raw.split("(")[0].strip()

        with sc_c2:
            fert_price_change = st.slider("Fertilizer Price Volatility (% change):", -50, 100, 40, 5, help="e.g. +40% increase in market fertilizer price")
        with sc_c3:
            rainfall_change = st.slider("Rainfall Anomaly (% change):", -50, 50, -15, 5, help="e.g. -15% rainfall reduction (drought stress)")

        # Regional baseline parameters
        active_reg = st.session_state.get("active_region", {
            "currency_symbol": "₦",
            "currency_code": "NGN",
            "base_maize_price": 450_000,
            "base_fert_cost": 240_000,
            "base_other_cost": 180_000,
            "country": "Nigeria"
        })
        curr_sym = active_reg.get("currency_symbol", "₦")
        curr_code = active_reg.get("currency_code", "NGN")
        country_name = active_reg.get("country", "Nigeria")

        # Dynamic Crop Baseline parameters from taxonomy
        crop_prof = get_crop_climate_profile(crop_choice_raw, custom_sim_crop)
        base_yield = crop_prof["base_yield"]
        unit = crop_prof["unit"]
        crop_base_price = crop_prof["price_per_unit"]
        water_sensitivity = crop_prof["water_sens"]

        base_fert_cost = active_reg.get("base_fert_cost", 240_000)
        base_other_cost = active_reg.get("base_other_cost", 180_000)

        # Yield response model
        fert_price_adoption_drop = max(0, fert_price_change * 0.35)  # price hike reduces fertilizer rate
        
        sim_yield = base_yield * (1.0 + (rainfall_change / 100.0) * water_sensitivity) * (1.0 - fert_price_adoption_drop / 100.0)
        sim_yield = max(round(base_yield * 0.15, 2), sim_yield)
        
        sim_fert_cost = base_fert_cost * (1.0 + fert_price_change / 100.0) * (1.0 - fert_price_adoption_drop / 100.0)
        sim_revenue = sim_yield * crop_base_price
        base_revenue = base_yield * crop_base_price
        
        base_gross_margin = base_revenue - (base_fert_cost + base_other_cost)
        sim_gross_margin = sim_revenue - (sim_fert_cost + base_other_cost)

        st.caption(f"📍 Active Economic Baseline: **{country_name}** ({curr_code}) | Crop Profile: **{sim_crop_name}**")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Simulated Yield", f"{sim_yield:.2f} {unit}", f"{sim_yield - base_yield:+.2f} {unit}")
        m2.metric("Harvest Revenue", f"{curr_sym}{sim_revenue:,.0f}", f"{curr_sym}{sim_revenue - base_revenue:+,.0f}")
        m3.metric("Fertilizer Outlay", f"{curr_sym}{sim_fert_cost:,.0f}", f"{curr_sym}{sim_fert_cost - base_fert_cost:+,.0f}")
        m4.metric("Farmer Gross Margin", f"{curr_sym}{sim_gross_margin:,.0f}", f"{curr_sym}{sim_gross_margin - base_gross_margin:+,.0f}")

        # Comparison Bar Chart
        comp_df = pd.DataFrame([
            {"Metric": "Harvest Revenue", "Scenario": "Baseline", "Value": base_revenue},
            {"Metric": "Harvest Revenue", "Scenario": "Simulated Shock", "Value": sim_revenue},
            {"Metric": "Fertilizer Cost", "Scenario": "Baseline", "Value": base_fert_cost},
            {"Metric": "Fertilizer Cost", "Scenario": "Simulated Shock", "Value": sim_fert_cost},
            {"Metric": "Gross Margin (Profit)", "Scenario": "Baseline", "Value": base_gross_margin},
            {"Metric": "Gross Margin (Profit)", "Scenario": "Simulated Shock", "Value": sim_gross_margin},
        ])
        fig_sim = px.bar(
            comp_df, x="Metric", y="Value", color="Scenario", barmode="group",
            color_discrete_map={"Baseline": "#81C784", "Simulated Shock": "#2E7D32"},
            title=f"Baseline vs Shock Financial Impact for {sim_crop_name} (per Hectare in {curr_code})"
        )
        fig_sim.update_layout(plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig_sim, use_container_width=True)

        pct_margin_change = ((sim_gross_margin - base_gross_margin) / base_gross_margin * 100) if base_gross_margin != 0 else 0.0

        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">💡 AgriIntel Decision Support & Hedging Strategy ({country_name}) for {sim_crop_name}</div>
Under a <b>{fert_price_change:+d}% fertilizer price shift</b> and <b>{rainfall_change:+d}% rainfall shock</b>:<br>
• Gross margin changes by <b>{curr_sym}{sim_gross_margin - base_gross_margin:+,.0f}</b> per hectare ({pct_margin_change:+.1f}%).<br>
• <b>Mitigation Action</b>: Combine <i>micro-dosing</i> with organo-mineral compost or indigenous rhizobium/mycorrhizal bio-inoculants, maintaining target crop yield while hedging against chemical fertilizer inflation.
</div>
""", unsafe_allow_html=True)

