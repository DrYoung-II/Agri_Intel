"""
Module 7: Livestock & Poultry Intelligence Engine
Multi-Species Analytics:
Tab 1: 🐄 Bovine & Pastoral Genetics (Thermotolerance, EBVs & Multi-Trait Indexing)
Tab 2: 🐔 Poultry Bioclimatic Housing, Avian THI & Festive Production Simulator
Tab 3: 🐐 Small Ruminants & Swine Management
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core.exporter import render_download_buttons


def render_livestock_intelligence():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 🐾 Infrastructure d'Intelligence Animale & Vétérinaire")
        st.caption("Sciences animales multi-espèces : génétique bovine quantitative, bioclimatologie avicole et nutrition des petits ruminants.")
        tab_names = [
            "🐄 Génétique Bovine & Pastorale",
            "🐔 Simulateur Bioclimatique & Aviculture",
            "🐐 Petits Ruminants & Porciculture"
        ]
    else:
        st.markdown("### 🐾 Livestock & Poultry Intelligence Infrastructure")
        st.caption("Cross-species animal science: bovine quantitative genetics, poultry bioclimatics, and small ruminant nutrition.")
        tab_names = [
            "🐄 Bovine & Pastoral Genetics",
            "🐔 Poultry Bioclimatic & Festive Simulator",
            "🐐 Small Ruminants & Swine"
        ]

    tab_cattle, tab_poultry, tab_ruminants = st.tabs(tab_names)

    # =========================================================================
    # TAB 1: BOVINE & PASTORAL GENETICS
    # =========================================================================
    with tab_cattle:
        render_cattle_section()

    # =========================================================================
    # TAB 2: POULTRY BIOCLIMATIC & FESTIVE SIMULATOR
    # =========================================================================
    with tab_poultry:
        render_poultry_section()

    # =========================================================================
    # TAB 3: SMALL RUMINANTS & SWINE
    # =========================================================================
    with tab_ruminants:
        render_small_ruminants_section()


def render_cattle_section():
    st.markdown("#### 🐄 Cattle Multi-Criteria Breeding Index Configuration")
    st.caption("Weight traits according to your herd objective (e.g., Pastoral Resilience vs Commercial Dairy):")

    path = os.path.join("data", "sample_cattle_heat_tolerance.csv")
    if not os.path.exists(path):
        st.error("Cattle trial dataset not found.")
        return

    df_cattle = pd.read_csv(path)
    if df_cattle.empty:
        st.warning("⚠️ Cattle trial dataset is empty.")
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        w_prod = st.slider("Weight / Milk Production:", 0, 100, 70, key="cat_prod")
    with c2:
        w_heat = st.slider("Heat Tolerance (Lower Temp):", 0, 100, 85, key="cat_heat")
    with c3:
        w_resp = st.slider("Low Respiration Rate:", 0, 100, 60, key="cat_resp")
    with c4:
        w_tryp = st.slider("Trypanotolerance Bonus:", 0, 100, 90, key="cat_tryp")

    # Standardize weights
    w_sum = w_prod + w_heat + w_resp + w_tryp
    if w_sum == 0:
        w_sum = 1

    norm_w_prod = w_prod / w_sum
    norm_w_heat = w_heat / w_sum
    norm_w_resp = w_resp / w_sum
    norm_w_tryp = w_tryp / w_sum

    df = df_cattle.copy()
    std_wt = df["Body_Weight_kg"].std()
    z_prod = (df["Body_Weight_kg"] - df["Body_Weight_kg"].mean()) / (std_wt if std_wt and std_wt > 0 else 1.0)
    std_temp = df["Body_Temperature_C"].std()
    z_heat = -(df["Body_Temperature_C"] - df["Body_Temperature_C"].mean()) / (std_temp if std_temp and std_temp > 0 else 1.0)
    std_resp = df["Respiration_Rate_bpm"].std()
    z_resp = -(df["Respiration_Rate_bpm"] - df["Respiration_Rate_bpm"].mean()) / (std_resp if std_resp and std_resp > 0 else 1.0)
    tryp_score = df["Trypanotolerance"].apply(lambda x: 1.5 if x == "Tolerant" else -0.5)

    df["Composite_Index"] = (
        (z_prod * norm_w_prod * 10) +
        (z_heat * norm_w_heat * 10) +
        (z_resp * norm_w_resp * 10) +
        (tryp_score * norm_w_tryp * 10)
    )

    df_ranked = df.sort_values(by="Composite_Index", ascending=False).reset_index(drop=True)
    df_ranked["Selection_Rank"] = df_ranked.index + 1

    if df_ranked.empty:
        st.warning("No animal records available after ranking.")
        return

    col1, col2, col3, col4 = st.columns(4)
    top_candidate = df_ranked.iloc[0]
    col1.metric("Top Candidate", str(top_candidate["Animal_ID"]))
    col2.metric("Breed", str(top_candidate["Breed"]))
    col3.metric("Composite Score", f"{top_candidate['Composite_Index']:.2f}")
    col4.metric("Body Weight", f"{top_candidate['Body_Weight_kg']:.1f} kg")

    st.markdown("##### 🥇 Top 15 Recommended Breeding Candidates")
    display_cols = ["Selection_Rank", "Animal_ID", "Breed", "Sex", "Body_Weight_kg", "Body_Temperature_C", "Respiration_Rate_bpm", "HSP_Genotype", "Trypanotolerance", "Composite_Index"]
    st.dataframe(df_ranked[display_cols].head(15).style.format({"Composite_Index": "{:.2f}", "Body_Temperature_C": "{:.2f}°C", "Body_Weight_kg": "{:.1f} kg"}), use_container_width=True)

    fig_scatter = px.scatter(
        df_ranked.head(100),
        x="Body_Temperature_C",
        y="Body_Weight_kg",
        color="Breed",
        size="Composite_Index",
        hover_data=["Animal_ID", "Selection_Rank", "HSP_Genotype"],
        title="Top 100 Bovine Candidates: Body Temperature (°C) vs Body Weight (kg)",
        color_discrete_sequence=["#1B5E20", "#2E7D32", "#4CAF50", "#81C784"]
    )
    fig_scatter.update_layout(plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🧬 Animal Geneticist Selection Strategy</div>
• <b>Top Rank Identification</b>: Animal <b>{top_candidate['Animal_ID']}</b> ({top_candidate['Breed']}) combines superior weight merit with low thermal load (rectal temp {top_candidate['Body_Temperature_C']}°C) and carrier status for <i>{top_candidate['HSP_Genotype']}</i>.<br>
• <b>Breeding Recommendation</b>: Use this sire/dam in structured AI (Artificial Insemination) or nucleus breeding schemes to fix thermotolerance alleles without compromising beef/milk conformation.
</div>
""", unsafe_allow_html=True)


def render_poultry_section():
    st.markdown("#### 🐔 Poultry Bioclimatic Housing, Avian THI & Festive Production Simulator")
    st.caption("Models avian thermoregulation, diurnal Harmattan stress, respiratory risks, and festive Christmas/New Year broiler economics.")

    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        bird_type = st.selectbox(
            "Flock Enterprise:",
            ["Commercial Broilers (Ross 308 / Cobb 500)", "Commercial Layers (Isa Brown)", "Dual-Purpose (Noiler / ShikaBrown)"]
        )
    with c_p2:
        period_choice = st.selectbox(
            "Agro-Climatic Period:",
            [
                "October/November Transition (Late Rains → Harmattan Onset)",
                "Peak Dry Harmattan (December / January)",
                "Hot Dry Summer Peak (February / March)",
                "Rainy Season (June / July)"
            ]
        )
    with c_p3:
        housing_type = st.selectbox(
            "Housing Design:",
            ["Open-Sided Deep Litter (Natural Ventilation)", "Evaporative Tunnel-Ventilated (Closed)", "Battery Cage (High Density)"]
        )

    # Sliders for ambient telemetry
    if "October/November" in period_choice:
        def_temp, def_rh = 33.5, 48.0
    elif "Peak Dry Harmattan" in period_choice:
        def_temp, def_rh = 31.0, 25.0
    elif "Hot Dry" in period_choice:
        def_temp, def_rh = 38.0, 32.0
    else:
        def_temp, def_rh = 28.0, 82.0

    st.markdown("##### 🌡️ Ambient Micro-Climate Configuration")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        temp = st.slider("Afternoon Peak Pen Temperature (°C):", 20.0, 44.0, def_temp, 0.5)
    with col_t2:
        rh = st.slider("Relative Humidity (%):", 10.0, 95.0, def_rh, 1.0)

    # Compute Avian THI
    # Avian THI Formula: THI = 0.8 * T + (RH / 100) * (T - 14.4) + 46.4
    thi = 0.8 * temp + (rh / 100.0) * (temp - 14.4) + 46.4

    # Determine stress status
    if thi < 72.0:
        stress_cat = "🟢 Comfort Zone"
        stress_desc = "Optimal thermoregulatory comfort. Normal feed intake and zero heat-induced mortality."
        feed_drop_pct = 0.0
        water_surge_pct = 0.0
        mortality_risk = 0.1
    elif thi < 78.0:
        stress_cat = "🟡 Mild Heat Alert"
        stress_desc = "Mild heat load. Birds begin wing-spreading. Feed intake drops slightly; water demand increases."
        feed_drop_pct = 6.5
        water_surge_pct = 20.0
        mortality_risk = 0.5
    elif thi < 84.0:
        stress_cat = "🟠 Severe Panting & Alkalosis"
        stress_desc = "Acute heat stress! Intense evaporative panting causes respiratory alkalosis. Severe feed anorexia and eggshell thinning."
        feed_drop_pct = 18.0
        water_surge_pct = 65.0
        mortality_risk = 2.8
    else:
        stress_cat = "🔴 Critical Danger / Emergency"
        stress_desc = "Critical thermal overload! Core temperature exceeds 43°C. Risk of Sudden Death Syndrome and massive flock mortality."
        feed_drop_pct = 35.0
        water_surge_pct = 120.0
        mortality_risk = 8.5

    # Metrics Display
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avian THI Index", f"{thi:.1f}")
    m2.metric("Stress Category", stress_cat.split(" ", 1)[1])
    m3.metric("Predicted Feed Intake Drop", f"-{feed_drop_pct:.1f}%")
    m4.metric("Water Consumption Surge", f"+{water_surge_pct:.1f}%")

    # Alert Box
    if thi >= 78.0:
        st.warning(f"⚠️ **{stress_cat}**: {stress_desc}")
    else:
        st.success(f"✅ **{stress_cat}**: {stress_desc}")

    st.markdown("---")
    st.markdown("##### 💰 Festive December Broiler Commercial Economics Calculator")
    st.caption("Calculate flock budgets when stocking Day-Old Chicks (DOC) in late October / early November for the peak Christmas & New Year market:")

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        flock_size = st.number_input("Flock Size (Birds):", min_value=100, max_value=50000, value=1000, step=100)
    with b_col2:
        doc_price = st.number_input("Day-Old Chick Price (₦):", min_value=500, max_value=2500, value=1100, step=50)
    with b_col3:
        bag_price = st.number_input("Feed Cost (₦/25kg bag):", min_value=10000, max_value=40000, value=22500, step=500)
    with b_col4:
        sale_price = st.number_input("Festive Sale Price (₦/bird):", min_value=5000, max_value=25000, value=12500, step=500)

    # Budget Calculation
    # Average broiler consumes 4.5 kg feed to reach 2.4 kg in 48 days (FCR = 1.87)
    feed_per_bird_kg = 4.5
    feed_cost_per_kg = bag_price / 25.0
    feed_cost_per_bird = feed_per_bird_kg * feed_cost_per_kg
    medication_per_bird = 450.0  # Vaccines, vitamins, electrolytes, antibiotics
    brooding_fuel_litter_per_bird = 350.0
    total_cost_per_bird = doc_price + feed_cost_per_bird + medication_per_bird + brooding_fuel_litter_per_bird

    est_mortality_pct = max(2.5, mortality_risk)
    surviving_birds = int(flock_size * (1.0 - (est_mortality_pct / 100.0)))
    total_investment = total_cost_per_bird * flock_size
    gross_revenue = surviving_birds * sale_price
    net_profit = gross_revenue - total_investment
    roi_pct = (net_profit / total_investment) * 100.0 if total_investment > 0 else 0.0

    ec1, ec2, ec3, ec4 = st.columns(4)
    ec1.metric("Production Cost / Bird", f"₦{total_cost_per_bird:,.0f}")
    ec2.metric("Total Flock Investment", f"₦{total_investment:,.0f}")
    ec3.metric("Projected Gross Revenue", f"₦{gross_revenue:,.0f}")
    ec4.metric("Net Festive Profit", f"₦{net_profit:,.0f}", f"{roi_pct:.1f}% ROI")

    # Actionable Protocol
    st.markdown(f"""
<div class="agri-card agri-card-highlight">
    <div style="font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">📋 Actionable Bioclimatic Housing & Management Protocol (October/November Transition)</div>
    <div style="font-size: 0.88rem; color: #2E7D32; line-height: 1.5;">
    • <b>Chilling vs Overheating Curfew</b>: The incoming Harmattan wind creates 33°C afternoons but 19°C chilly mornings. Use double brooder curtains from 11:00 PM to 6:00 AM, but <b>lower curtains by 9:00 AM</b> to prevent lethal ammonia accumulation.<br>
    • <b>Combating Alkalosis (Panting)</b>: When panting commences, add <b>Vitamin C (1g per liter)</b> and <b>Sodium Bicarbonate (0.2%)</b> to cool drinking water between 10:30 AM and 4:00 PM.<br>
    • <b>Feed Withdrawal Window</b>: Remove feed from hoppers between 11:30 AM and 3:30 PM. Feed birds heavily during the cool evening and early morning to eliminate metabolic heat death.<br>
    • <b>Airborne Dust Vaccination</b>: Vaccinate with <b>Newcastle Disease (ND Lasota / Clone 30)</b> at Day 14 and Day 28, and Gumboro (IBD) at Day 10 and 18. Administer prophylactic tylosin at the onset of dust haze to prevent Chronic Respiratory Disease (CRD).
    </div>
</div>
""", unsafe_allow_html=True)


def render_small_ruminants_section():
    st.markdown("#### 🐐 Small Ruminants (Goats & Sheep) & Swine Intelligence Engine")
    st.caption("Nutritional energy partitioning, festive ram fattening arbitrage, porcine bioclimatic respiration modeling, and heat abatement economics.")

    cur_sym = st.session_state.get("active_region", {}).get("currency_symbol", "₦")

    sub_tab_rum, sub_tab_swine = st.tabs([
        "🐐 Small Ruminants: Ram Fattening & Forage Arbitrage",
        "🐖 Swine: Bioclimatics, Respiration & Heat Abatement"
    ])

    # =========================================================================
    # SUB-TAB 1: SMALL RUMINANTS FATTENING & FORAGE ARBITRAGE
    # =========================================================================
    with sub_tab_rum:
        st.markdown("##### 🐏 Ram & Goat Festive Fattening Optimizer")
        st.caption("Simulates daily liveweight gain (ADG), dry matter intake (DMI), feed conversion efficiency (FCR), and festive market arbitrage across African small ruminant ecotypes.")

        breed_info = {
            "Sahelian / Uda Sheep": {
                "base_adg": 195.0,
                "dressing_pct": 52.0,
                "dmi_factor": 3.2,
                "feed_efficiency": 1.15,
                "default_feeder": 55000,
                "desc": "Desert meat breed • Long-legged tall frame • High ADG potential (up to 230g/day) • Heat & trekking hardy"
            },
            "Yankasa Sheep": {
                "base_adg": 155.0,
                "dressing_pct": 50.0,
                "dmi_factor": 3.0,
                "feed_efficiency": 1.05,
                "default_feeder": 45000,
                "desc": "Savanna dual-purpose white sheep • Moderate-high ADG • Superior flock prolificacy and maternal ability"
            },
            "Red Sokoto (Maradi) Goat": {
                "base_adg": 120.0,
                "dressing_pct": 49.0,
                "dmi_factor": 3.3,
                "feed_efficiency": 1.00,
                "default_feeder": 32000,
                "desc": "Sahelian prolific chevon breed • High dressing yield (49%) • World-renowned premium Maradi leather"
            },
            "West African Dwarf Goat": {
                "base_adg": 75.0,
                "dressing_pct": 48.0,
                "dmi_factor": 3.5,
                "feed_efficiency": 0.85,
                "default_feeder": 25000,
                "desc": "Humid forest dwarf ecotype • Natural genetic trypanotolerance to T. vivax • Compact frame & prolific kidding"
            },
            "West African Dwarf Sheep": {
                "base_adg": 85.0,
                "dressing_pct": 49.0,
                "dmi_factor": 3.4,
                "feed_efficiency": 0.90,
                "default_feeder": 28000,
                "desc": "Djallonke forest mutton breed • Trypanotolerant • Suited for humid forest & tree-crop plantations"
            }
        }

        ration_info = {
            "Cottonseed Cake + Wheat Offal + Cowpea Husk": {
                "tdn": 74.0,
                "desc": "⚡ High Energy & Crude Protein • TDN ~74% • CP ~18% • Fast muscle accretion for rapid finish"
            },
            "Groundnut Haulms + Maize Bran + Soya Residue": {
                "tdn": 70.0,
                "desc": "🌾 Balanced Savanna Ruminant Ration • TDN ~70% • CP ~16% • High palatability & intake"
            },
            "Stylosanthes Hay + Sorghum Bran + Urea Salt": {
                "tdn": 63.0,
                "desc": "🌿 Silvopastoral Forage Blend • TDN ~63% • CP ~13% • Cost-effective dry season maintenance"
            },
            "Cassava Peel + Palm Kernel Cake + Spent Grain": {
                "tdn": 65.0,
                "desc": "🍠 Humid Zone Low-Cost Byproduct • TDN ~65% • CP ~14% • Abundant agro-industrial source"
            }
        }

        market_info = {
            "Peak Festive Market (Eid / Christmas / Tabaski)": {
                "premium": 1.50,
                "desc": "🌟 Premium Festive Valuation (+50% margin) • Strict live conformation and horn aesthetics"
            },
            "Urban Abattoir Contract (Wholesale Meat)": {
                "premium": 1.15,
                "desc": "🏢 Wholesale carcass valuation (+15% premium) • Regular monthly off-take agreement"
            },
            "Standard Weekly Livestock Auction": {
                "premium": 1.00,
                "desc": "🏷️ Baseline farm-gate price • Variable weekly live bidding"
            }
        }

        # 2-COLUMN SPACIOUS LAYOUT
        col_cfg, col_kpi = st.columns([1, 1], gap="large")

        with col_cfg:
            st.markdown("##### 🎛️ 1. Animal & Ration Configuration")
            
            breed_choice = st.selectbox(
                "Animal Ecotype / Breed:",
                options=list(breed_info.keys()),
                index=0,
                key="rum_breed"
            )
            b_meta = breed_info[breed_choice]
            st.markdown(f'<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 5px 10px; border-radius: 5px; margin-top: -8px; margin-bottom: 12px; border-left: 3px solid #2E7D32;">{b_meta["desc"]}</div>', unsafe_allow_html=True)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                duration_days = st.slider("Fattening Days:", 30, 120, 90, 5, key="rum_days", help="Typical intensive festive ram fattening runs 60 to 90 days.")
            with col_s2:
                init_wt = st.slider("Initial Feeder Weight (kg):", 15.0, 45.0, 28.0, 0.5, key="rum_init_wt")

            ration_choice = st.selectbox(
                "Dietary Formulation & Forage Base:",
                options=list(ration_info.keys()),
                index=0,
                key="rum_diet"
            )
            r_meta = ration_info[ration_choice]
            st.markdown(f'<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 5px 10px; border-radius: 5px; margin-top: -8px; margin-bottom: 12px; border-left: 3px solid #2E7D32;">{r_meta["desc"]}</div>', unsafe_allow_html=True)

            col_s3, col_s4 = st.columns(2)
            with col_s3:
                ration_tdn = st.slider("Diet Energy (TDN %):", 55.0, 80.0, float(r_meta["tdn"]), 0.5, key="rum_tdn")
            with col_s4:
                market_channel = st.selectbox(
                    "Target Market Channel:",
                    options=list(market_info.keys()),
                    index=0,
                    key="rum_market"
                )
            m_meta = market_info[market_channel]
            st.markdown(f'<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 5px 10px; border-radius: 5px; margin-top: -8px; margin-bottom: 14px; border-left: 3px solid #2E7D32;">{m_meta["desc"]}</div>', unsafe_allow_html=True)

        # Biological Computations
        base_adg = b_meta["base_adg"]
        dressing_pct = b_meta["dressing_pct"]
        dmi_factor = b_meta["dmi_factor"]
        feed_efficiency = b_meta["feed_efficiency"]

        diet_energy_mult = (ration_tdn / 70.0) ** 1.15
        effective_adg = base_adg * diet_energy_mult * feed_efficiency
        effective_adg = max(40.0, min(240.0, effective_adg))

        total_gain_kg = (effective_adg * duration_days) / 1000.0
        final_wt = init_wt + total_gain_kg
        avg_body_wt = (init_wt + final_wt) / 2.0
        daily_dmi_kg = avg_body_wt * (dmi_factor / 100.0)
        total_feed_consumed_kg = daily_dmi_kg * duration_days
        fcr = total_feed_consumed_kg / total_gain_kg if total_gain_kg > 0 else 7.0
        carcass_wt = final_wt * (dressing_pct / 100.0)

        with col_kpi:
            st.markdown("##### 📊 2. Live Performance & Carcass Yield")
            
            kp1, kp2 = st.columns(2)
            kp1.metric("Predicted Daily Gain (ADG)", f"{effective_adg:.1f} g/day")
            kp2.metric("Final Finish Weight", f"{final_wt:.1f} kg", f"+{total_gain_kg:.1f} kg gain")

            kp3, kp4 = st.columns(2)
            kp3.metric("Feed Conversion (FCR)", f"{fcr:.2f}")
            kp4.metric("Dressed Carcass Yield", f"{carcass_wt:.1f} kg", f"{dressing_pct:.0f}% Dressing")

            # Trajectory Chart fitting in column
            weeks = list(range(0, int(duration_days // 7) + 1))
            days_series = [w * 7 for w in weeks]
            if days_series[-1] != duration_days:
                days_series.append(duration_days)
            wt_series = [init_wt + (effective_adg * d / 1000.0) for d in days_series]

            df_traj = pd.DataFrame({"Day": days_series, "Liveweight_kg": wt_series})
            fig_rum = px.line(
                df_traj,
                x="Day",
                y="Liveweight_kg",
                title=f"📈 {breed_choice} Gain Trajectory ({duration_days} Days)",
                labels={"Day": "Day in Pen", "Liveweight_kg": "Weight (kg)"},
                color_discrete_sequence=["#1B5E20"]
            )
            fig_rum.update_layout(
                plot_bgcolor="#F8FAF8",
                paper_bgcolor="#FFFFFF",
                margin=dict(l=10, r=10, t=35, b=10),
                height=230
            )
            st.plotly_chart(fig_rum, use_container_width=True)

        st.markdown("---")

        # Commercial Budget Section
        st.markdown(f"##### 💰 3. Enterprise Fattening Commercial Budget ({cur_sym})")
        
        b_r1, b_r2, b_r3, b_r4 = st.columns(4)
        with b_r1:
            batch_size = st.number_input("Batch Size (Heads):", min_value=5, max_value=2000, value=50, step=5, key="rum_batch")
        with b_r2:
            def_feeder_cost = b_meta["default_feeder"]
            feeder_cost = st.number_input(f"Feeder Purchase Price ({cur_sym}):", min_value=10000, max_value=150000, value=def_feeder_cost, step=2500, key="rum_feeder_cost")
        with b_r3:
            feed_kg_cost = st.number_input(f"Feed Ration Cost ({cur_sym}/kg DM):", min_value=50, max_value=800, value=280, step=10, key="rum_feed_cost")
        with b_r4:
            vet_med_cost = st.number_input(f"Vet & Prophylaxis ({cur_sym}/head):", min_value=500, max_value=15000, value=3500, step=250, key="rum_vet_cost")

        total_feed_cost_head = total_feed_consumed_kg * feed_kg_cost
        total_cost_head = feeder_cost + total_feed_cost_head + vet_med_cost

        base_price_per_kg = 2800.0
        premium_mult = m_meta["premium"]

        sale_price_head = final_wt * base_price_per_kg * premium_mult
        net_profit_head = sale_price_head - total_cost_head
        total_batch_investment = total_cost_head * batch_size
        total_batch_profit = net_profit_head * batch_size
        batch_roi_pct = (total_batch_profit / total_batch_investment) * 100.0 if total_batch_investment > 0 else 0.0

        eb1, eb2, eb3, eb4 = st.columns(4)
        eb1.metric("Production Cost / Head", f"{cur_sym}{total_cost_head:,.0f}")
        eb2.metric("Terminal Sale Value", f"{cur_sym}{sale_price_head:,.0f}")
        eb3.metric("Net Margin / Head", f"{cur_sym}{net_profit_head:,.0f}")
        eb4.metric(f"Batch Net Profit ({batch_size} heads)", f"{cur_sym}{total_batch_profit:,.0f}", f"{batch_roi_pct:.1f}% ROI")

        st.markdown(f"""
<div class="agri-card agri-card-highlight">
    <div style="font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">📋 Actionable Ruminant Veterinary & Prophylaxis Protocol</div>
    <div style="font-size: 0.88rem; color: #2E7D32; line-height: 1.5;">
    • <b>Day 1–3 Intake Quarantine & Deworming</b>: Administer broad-spectrum anthelmintic (Albendazole 10% @ 7.5 mg/kg or Ivermectin 1% s/c @ 0.2 mg/kg) to eliminate <i>Haemonchus contortus</i> and nasal bot flies (<i>Oestrus ovis</i>).<br>
    • <b>PPR Homologous Vaccination</b>: Administer <b>NVRI Vom Live Attenuated PPR Vaccine</b> (Nigerian 75/1 clone) subcutaneous injection to confer lifelong immunity against viral morbillivirus stomatitis.<br>
    • <b>Urinary Calculi (Water Belly) Prevention</b>: High-concentrate fattening diets (>60% offal/grain) alter Ca:P stoichiometry, triggering obstructive magnesium ammonium phosphate calculi in wethers/rams. Add <b>0.5% Ammonium Chloride</b> and <b>1.0% Limestone (Calcium carbonate)</b> to maintain Ca:P at $\ge 2:1$ with unlimited cool drinking water.
    </div>
</div>
""", unsafe_allow_html=True)

        # Export report for Small Ruminants
        rum_report = f"""# AgroBiometrix Small Ruminant Fattening & Nutritional Advisory Report

## 1. Enterprise Profile & Simulation Parameters
- **Target Breed / Ecotype**: {breed_choice}
- **Fattening Cycle Duration**: {duration_days} Days
- **Initial Feeder Liveweight**: {init_wt:.1f} kg
- **Dietary Formulation**: {ration_choice}
- **Diet Energy Density (TDN)**: {ration_tdn:.1f}%
- **Target Market Channel**: {market_channel}

## 2. Predicted Biological Performance Metrics
| Metric | Value |
| :--- | :--- |
| **Predicted Average Daily Gain (ADG)** | {effective_adg:.1f} g/day |
| **Total Liveweight Gain** | {total_gain_kg:.1f} kg |
| **Final Finish Liveweight** | {final_wt:.1f} kg |
| **Feed Conversion Ratio (FCR)** | {fcr:.2f} |
| **Dressed Carcass Yield ({dressing_pct:.0f}%)** | {carcass_wt:.1f} kg |
| **Total Feed Consumed per Head** | {total_feed_consumed_kg:.1f} kg DM |

## 3. Enterprise Financial Budget ({cur_sym})
| Financial Item | Cost / Return per Head | Batch Total ({batch_size} Heads) |
| :--- | :--- | :--- |
| **Feeder Animal Purchase Cost** | {cur_sym}{feeder_cost:,.2f} | {cur_sym}{feeder_cost * batch_size:,.2f} |
| **Total Feed Cost ({cur_sym}{feed_kg_cost}/kg DM)** | {cur_sym}{total_feed_cost_head:,.2f} | {cur_sym}{total_feed_cost_head * batch_size:,.2f} |
| **Veterinary & PPR Vaccination** | {cur_sym}{vet_med_cost:,.2f} | {cur_sym}{vet_med_cost * batch_size:,.2f} |
| **Total Investment Cost** | **{cur_sym}{total_cost_head:,.2f}** | **{cur_sym}{total_batch_investment:,.2f}** |
| **Projected Gross Revenue** | **{cur_sym}{sale_price_head:,.2f}** | **{cur_sym}{sale_price_head * batch_size:,.2f}** |
| **Net Enterprise Margin** | **{cur_sym}{net_profit_head:,.2f}** | **{cur_sym}{total_batch_profit:,.2f}** |
| **Return on Investment (ROI)** | **{batch_roi_pct:.1f}%** | **{batch_roi_pct:.1f}%** |

## 4. Actionable Veterinary Prophylaxis Protocol
- **Intake Deworming**: Broad-spectrum Albendazole 10% (@ 7.5 mg/kg) or Ivermectin 1% s/c (@ 0.2 mg/kg).
- **Vaccination**: NVRI Vom Live Attenuated PPR Vaccine (Nigerian 75/1 clone) at intake.
- **Urinary Calculi Prevention**: 0.5% Ammonium Chloride + 1.0% Limestone with ad-libitum water.
"""
        render_download_buttons(
            content_text=rum_report,
            filename_prefix="AgroBiometrix_Small_Ruminant_Advisory",
            title="AgroBiometrix Small Ruminant Fattening Advisory",
            key_prefix="btn_dl_rum"
        )

    # =========================================================================
    # SUB-TAB 2: SWINE BIOCLIMATICS & HEAT ABATEMENT
    # =========================================================================
    with sub_tab_swine:
        st.markdown("##### 🐖 Porcine Bioclimatics, Respiration & Heat Abatement Simulator")
        st.caption("Pigs lack functional sweat glands and rely on respiratory evaporative cooling and conductive wallowing. Simulates heat stress impact on feed intake, respiration rates, and cooling abatement ROI.")

        swine_classes = {
            "Grower-Finisher (50–90 kg)": {
                "uct": 24.0,
                "base_feed": 2.80,
                "base_adg": 680.0,
                "base_fcr": 2.85,
                "base_rr": 30.0,
                "desc": "⚠️ High heat susceptibility: thick subcutaneous fat layer. Upper Critical Temp = 24°C."
            },
            "Lactating Sow (with Litter)": {
                "uct": 20.0,
                "base_feed": 6.20,
                "base_adg": 0.0,
                "base_fcr": 2.20,
                "base_rr": 28.0,
                "desc": "🚨 Extreme heat risk: massive milk heat production. UCT = 20°C. Risk of acute agalactia."
            },
            "Gestating Sow (Dry / Pregnant)": {
                "uct": 22.0,
                "base_feed": 2.20,
                "base_adg": 350.0,
                "base_fcr": 3.20,
                "base_rr": 25.0,
                "desc": "⚠️ Reproductive vulnerability: thermal distress induces embryonic resorption and delayed estrus."
            },
            "Weaner Piglets (12–25 kg)": {
                "uct": 27.0,
                "base_feed": 1.10,
                "base_adg": 420.0,
                "base_fcr": 1.95,
                "base_rr": 35.0,
                "desc": "ℹ️ Higher thermal comfort range (27°C). Vulnerable to chilling and cold drafts rather than heat."
            }
        }

        abatement_systems = {
            "Unshaded Open Pen (No Cooling)": {
                "temp_drop": 0.0,
                "desc": "🔴 Maximum thermal stress • 0°C cooling relief • Severe voluntary feed reduction"
            },
            "Insulated / Thatch Shaded Roof": {
                "temp_drop": 2.5,
                "desc": "🟡 -2.5°C effective cooling • Blocks direct solar heat gain • Natural cross ventilation"
            },
            "Concrete Clean Water Wallow": {
                "temp_drop": 4.5,
                "desc": "🟢 -4.5°C effective conductive cooling • Significant respiratory relief & cooling"
            },
            "Cycle Drip Sprinklers / Foggers": {
                "temp_drop": 6.0,
                "desc": "🟢 -6.0°C effective evaporative skin cooling • Prevents severe feed anorexia"
            },
            "Tunnel Ventilation & Cooling Pads": {
                "temp_drop": 8.0,
                "desc": "🟢 -8.0°C fully controlled commercial cooling • High air velocity & heat evacuation"
            }
        }

        # 2-COLUMN SPACIOUS LAYOUT
        col_sw_cfg, col_sw_kpi = st.columns([1, 1], gap="large")

        with col_sw_cfg:
            st.markdown("##### 🎛️ 1. Swine Category & Pen Micro-Climate")
            
            swine_class = st.selectbox(
                "Swine Physiological Category:",
                options=list(swine_classes.keys()),
                index=0,
                key="swine_class"
            )
            sw_meta = swine_classes[swine_class]
            st.markdown(f'<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 5px 10px; border-radius: 5px; margin-top: -8px; margin-bottom: 12px; border-left: 3px solid #2E7D32;">{sw_meta["desc"]}</div>', unsafe_allow_html=True)

            abatement_sys = st.selectbox(
                "Cooling & Housing Abatement System:",
                options=list(abatement_systems.keys()),
                index=0,
                key="swine_abatement"
            )
            ab_meta = abatement_systems[abatement_sys]
            st.markdown(f'<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 5px 10px; border-radius: 5px; margin-top: -8px; margin-bottom: 14px; border-left: 3px solid #2E7D32;">{ab_meta["desc"]}</div>', unsafe_allow_html=True)

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                pen_temp = st.slider("Afternoon Peak Temp (°C):", 22.0, 44.0, 33.5, 0.5, key="swine_temp")
            with col_t2:
                pen_rh = st.slider("Relative Humidity (%):", 15.0, 95.0, 60.0, 1.0, key="swine_rh")

        # Calculations
        uct_temp = sw_meta["uct"]
        base_adg_g = sw_meta["base_adg"]
        base_fcr = sw_meta["base_fcr"]
        base_rr = sw_meta["base_rr"]
        temp_abatement = ab_meta["temp_drop"]

        effective_temp = max(20.0, pen_temp - temp_abatement)
        swine_thi = (0.8 * effective_temp) + ((pen_rh / 100.0) * (effective_temp - 14.4)) + 46.4

        degrees_above_uct = max(0.0, effective_temp - uct_temp)
        feed_drop_pct = min(45.0, degrees_above_uct * 2.2)
        respiration_rate = min(170.0, base_rr + (degrees_above_uct * 8.5))

        adg_penalty_pct = min(45.0, degrees_above_uct * 2.8)
        sim_adg = base_adg_g * (1.0 - (adg_penalty_pct / 100.0))
        fcr_penalty = degrees_above_uct * 0.09
        sim_fcr = base_fcr + fcr_penalty

        if swine_thi < 74.0:
            sw_stress_cat = "🟢 Comfort Zone"
            sw_desc = "Optimal thermal comfort. Normal respiratory rhythm and uninhibited feed intake."
        elif swine_thi < 79.0:
            sw_stress_cat = "🟡 Mild Heat Stress"
            sw_desc = "Mild heat load. Pigs seek moist flooring; slight drop in voluntary intake."
        elif swine_thi < 84.0:
            sw_stress_cat = "🟠 Severe Thermal Distress"
            sw_desc = "Acute distress! Rapid open-mouth panting, severe voluntary feed reduction, reduced milk output."
        else:
            sw_stress_cat = "🔴 Critical Emergency / Heat Stroke"
            sw_desc = "Core body temperature >41°C. Severe cyanosis, risk of sudden mortality and collapse."

        with col_sw_kpi:
            st.markdown("##### 📊 2. Physiological Thermal Markers")
            
            sm1, sm2 = st.columns(2)
            sm1.metric("Effective Pen Temp", f"{effective_temp:.1f}°C", f"-{temp_abatement:.1f}°C Cooling" if temp_abatement > 0 else "No Abatement")
            sm2.metric("Swine THI Index", f"{swine_thi:.1f}")

            sm3, sm4 = st.columns(2)
            sm3.metric("Respiration Rate", f"{respiration_rate:.0f} bpm", f"+{respiration_rate - base_rr:.0f} bpm" if respiration_rate > base_rr else "Normal")
            sm4.metric("Feed Intake Drop", f"-{feed_drop_pct:.1f}%")

            if swine_thi >= 79.0:
                st.warning(f"⚠️ **{sw_stress_cat}**: {sw_desc}")
            else:
                st.success(f"✅ **{sw_stress_cat}**: {sw_desc}")

        st.markdown("---")

        # Economic Impact Section
        st.markdown(f"##### 💰 3. Finisher Batch Economic Impact & Cooling ROI ({cur_sym})")

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            herd_pigs = st.number_input("Grower Batch Size (Pigs):", min_value=10, max_value=2000, value=100, step=10, key="sw_herd")
        with sc2:
            sw_feed_price_kg = st.number_input(f"Commercial Feed Price ({cur_sym}/kg):", min_value=100, max_value=1000, value=420, step=20, key="sw_feed_price")
        with sc3:
            sprinkler_cost = st.number_input(f"Sprinkler / Cooling Capex ({cur_sym}):", min_value=10000, max_value=1000000, value=125000, step=10000, key="sw_sprinkler_cost")

        required_gain = 40.0
        normal_days = (required_gain / (base_adg_g / 1000.0)) if base_adg_g > 0 else 60.0
        actual_days = (required_gain / (sim_adg / 1000.0)) if sim_adg > 0 else normal_days
        days_delayed = max(0.0, actual_days - normal_days)

        feed_normal_kg = required_gain * base_fcr
        feed_actual_kg = required_gain * sim_fcr
        extra_feed_per_pig = max(0.0, feed_actual_kg - feed_normal_kg)
        extra_feed_cost_batch = extra_feed_per_pig * sw_feed_price_kg * herd_pigs

        payback_batches = sprinkler_cost / extra_feed_cost_batch if extra_feed_cost_batch > 0 else 1.0

        sec1, sec2, sec3, sec4 = st.columns(4)
        sec1.metric("Days to 90kg Market Weight", f"{actual_days:.0f} days", f"+{days_delayed:.0f} days delay" if days_delayed > 0 else "On Schedule")
        sec2.metric("Feed Conversion (FCR)", f"{sim_fcr:.2f}", f"+{fcr_penalty:.2f} penalty" if fcr_penalty > 0 else "Optimal")
        sec3.metric("Heat Loss in Wasted Feed", f"{cur_sym}{extra_feed_cost_batch:,.0f}")
        sec4.metric("Sprinkler Payback Period", f"{payback_batches:.1f} Batches" if payback_batches < 5 else "< 1 Year")

        st.markdown(f"""
<div class="agri-card agri-card-highlight">
    <div style="font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">🛡️ Actionable Swine Biosecurity & Heat Stress Abatement Protocol</div>
    <div style="font-size: 0.88rem; color: #2E7D32; line-height: 1.5;">
    • <b>Nocturnal Feeding Shift</b>: During high ambient heat (>32°C), feed intake drops by up to 30%. Deliver <b>70% of the daily ration between 6:30 PM and 5:30 AM</b> when pen temperatures are cool.<br>
    • <b>Dietary Energy Density Adjustment</b>: Fiber digestion generates high internal heat increment of feeding (HIF). Reduce fiber and supplement ration with <b>2.5% to 3.5% vegetable oil / fat</b> to maintain metabolizable energy intake without heat overload.<br>
    • <b>Water Flow Rates & Electrolytes</b>: Finisher pigs consume >12 liters/day under heat stress. Ensure nipple drinkers deliver $\ge 1.5$ liters/min flow rate; supplement drinking water with <b>0.2% Sodium Bicarbonate</b> and <b>Vitamin C (150 mg/kg feed)</b>.<br>
    • <b>African Swine Fever (ASF) Zero-Tolerance Biosecurity</b>: Never feed hotel scraps, swill, or untreated kitchen waste. Maintain a 3-meter perimeter double fence, enforce 3-minute wheel and boot dips (2% Virkon or Caustic Soda), and restrict all external visitors.
    </div>
</div>
""", unsafe_allow_html=True)

        swine_report = f"""# AgroBiometrix Swine Bioclimatics & Heat Stress Abatement Report

## 1. Herd & Thermal Configuration
- **Swine Physiological Class**: {swine_class}
- **Housing Abatement Strategy**: {abatement_sys}
- **Peak Afternoon Pen Temperature**: {pen_temp:.1f}°C
- **Relative Humidity**: {pen_rh:.1f}%
- **Effective Pen Temperature (Post-Abatement)**: {effective_temp:.1f}°C (-{temp_abatement:.1f}°C cooling effect)

## 2. Predicted Physiological & Performance Markers
| Physiological Indicator | Simulated Value | Baseline Status |
| :--- | :--- | :--- |
| **Swine THI Index** | {swine_thi:.1f} | {sw_stress_cat} |
| **Respiration Rate** | {respiration_rate:.0f} breaths/min | Baseline: {base_rr:.0f} bpm |
| **Voluntary Feed Intake Drop** | -{feed_drop_pct:.1f}% | Due to heat increment avoidance |
| **Predicted Average Daily Gain (ADG)** | {sim_adg:.1f} g/day | Baseline: {base_adg_g:.1f} g/day |
| **Feed Conversion Ratio (FCR)** | {sim_fcr:.2f} | Baseline: {base_fcr:.2f} |
| **Days to 90 kg Slaughter Weight** | {actual_days:.0f} days | Delayed by +{days_delayed:.0f} days |

## 3. Commercial Batch Financial Analysis ({cur_sym})
- **Grower Herd Size**: {herd_pigs} pigs
- **Commercial Feed Price**: {cur_sym}{sw_feed_price_kg:,.2f} / kg
- **Wasted Feed Cost due to Thermal Inefficiency**: **{cur_sym}{extra_feed_cost_batch:,.2f}** per batch
- **Capital Cost of Drip Cooling Sprinklers**: {cur_sym}{sprinkler_cost:,.2f}
- **Estimated Payback Period**: **{payback_batches:.1f} batches** of finishers

## 4. Operational Veterinary & Management Directives
- **Nocturnal Feeding**: Deliver 70% of feed during cool hours (6:30 PM – 5:30 AM).
- **Dietary Fat**: Add 2.5%–3.5% fat/oil to lower metabolic heat increment.
- **Electrolytes**: 0.2% Sodium Bicarbonate + Vitamin C (150 mg/kg feed).
- **ASF Biosecurity**: Absolute ban on swill/hotel scraps; maintain double perimeter fence.
"""
        render_download_buttons(
            content_text=swine_report,
            filename_prefix="AgroBiometrix_Swine_Bioclimatic_Advisory",
            title="AgroBiometrix Swine Bioclimatics Advisory",
            key_prefix="btn_dl_swine"
        )

        from core.broadcast_dispatcher import render_dispatch_trigger_card
        render_dispatch_trigger_card(
            source_module="Module 7: Livestock Biometrics & Swine THI",
            commodity=f"Swine / Piggery ({herd_pigs} head)",
            region="Sub-Saharan Commercial Piggery Belts",
            headline=f"Swine THI {swine_thi:.1f} Heat Stress Alert",
            trigger_summary=f"Swine THI reached {swine_thi:.1f} ({sw_stress_cat}). Respiration {respiration_rate:.0f} bpm, feed intake dropped -{feed_drop_pct:.1f}%.",
            recommendation_summary="Shift 70% of feed delivery to cool hours (6:30 PM - 5:30 AM). Supplement drinking water with 0.2% sodium bicarbonate and Vitamin C."
        )


