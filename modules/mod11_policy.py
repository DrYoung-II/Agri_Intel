"""
Modules 11 & 12: Government Agricultural Intelligence & Policy Simulator
Macro-economic What-If policy simulations, fiscal cost-benefit, and national intervention optimization.
Designed for Federal/State Ministries of Agriculture, Finance, Budget & Planning, Labour & Productivity,
Humanitarian Affairs & Poverty Alleviation, Central Banks, and Multilateral Development Partners.
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core.exporter import render_download_buttons
from core.orchestrator import get_gemini_api_key, call_live_llm_orchestration, set_gemini_api_key, validate_gemini_key


def render_policy_simulator():
    st.markdown("### 🏛️ Government Agricultural Intelligence & Policy Simulator")
    st.caption("Institutional macro-economic decision platform for national food security, inter-ministerial budget allocation, employment creation, poverty reduction, and counter-cyclical market stabilization.")

    # Retrieve active Pan-African region
    active_reg = st.session_state.get("active_region", {
        "country": "Nigeria",
        "currency_symbol": "₦",
        "currency_code": "NGN",
        "budget_unit": "₦1.0 Billion",
        "commercial_bag_price": 38_000,
        "total_smallholders": 18_000_000,
        "agro_zones": ["Sudan Savanna", "Guinea Savanna", "Rainforest", "Derived Savanna"]
    })
    curr_sym = active_reg.get("currency_symbol", "₦")
    curr_code = active_reg.get("currency_code", "NGN")
    country_name = active_reg.get("country", "Nigeria")

    st.markdown(f"""
<div style="background: linear-gradient(90deg, #F1F8F2 0%, #FFFFFF 100%); border-left: 5px solid #1B5E20; padding: 10px 16px; border-radius: 6px; margin-bottom: 15px;">
    <div style="font-size: 0.82rem; font-weight: 700; color: #2E7D32; text-transform: uppercase; letter-spacing: 0.5px;">
        🏛️ Sovereign Policy Architecture • {country_name} National Agricultural Framework (2026–2030)
    </div>
    <div style="font-size: 0.90rem; color: #1B3B1D; margin-top: 3px;">
        • <b>Lead Coordinating Authority</b>: Federal Ministry of Agriculture and Food Security (FMAFS)<br>
        • <b>Inter-Ministerial Partners</b>: Budget & National Planning • Labour & Productivity • Poverty Alleviation • Central Bank<br>
        • <b>Currency Sovereignty</b>: <b>{curr_code} ({curr_sym})</b> &bull; Global Parity: <b>USD ($)</b>
    </div>
</div>
""", unsafe_allow_html=True)

    tab_budget, tab_commodity, tab_shock, tab_cabinet = st.tabs([
        "🏛️ Fiscal Budget & Inter-Ministerial Impact",
        "🌾 Strategic Commodity Portfolio & Import Substitution",
        "🛡️ Food Inflation & Macro Shock Resilience",
        "📑 Cabinet Memorandum & Policy Brief Generator"
    ])

    # =========================================================================
    # TAB 1: FISCAL BUDGET & INTER-MINISTERIAL IMPACT ENGINE
    # =========================================================================
    with tab_budget:
        st.markdown("#### 🏛️ Multi-Ministerial Capital Expenditure & Return Engine")
        st.caption("Simulate public agricultural investment allocations across ministries to evaluate fiscal returns, employment generation, poverty alleviation, and foreign exchange preservation.")

        col_b_cfg, col_b_res = st.columns([1.0, 1.65], gap="large")

        with col_b_cfg:
            st.markdown("##### 🎛️ 1. Public Capital Envelope & Pillar Allocations")
            
            # Default envelope based on currency
            default_env = 50.0 if curr_code == "NGN" else (500.0 if curr_code in ["KES", "XOF", "XAF"] else 50.0)
            budget_billions = st.slider(
                f"Total Intervention Capital Envelope ({curr_sym} Billions):",
                min_value=5.0,
                max_value=250.0,
                value=float(default_env),
                step=5.0,
                key="policy_budget_env",
                help="Total budgetary appropriation under consideration by the Cabinet / Treasury."
            )
            total_budget_amount = budget_billions * 1_000_000_000

            st.markdown("###### Strategic Public Investment Pillars (% Share):")
            w_inputs = st.slider("1. Smart E-Vouchers & Stoichiometric Inputs (%):", 0, 100, 25, 5, key="w_inp", help="Certified drought-tolerant seeds, balanced NPK, bio-fertilizers via biometric e-wallet.")
            w_irrig = st.slider("2. Solar Irrigation & Basin Water Infrastructure (%):", 0, 100, 25, 5, key="w_irr", help="Smallholder solar drip kits, river basin retention dams, dry-season double-cropping.")
            w_phl = st.slider("3. Post-Harvest Loss (PHL) & Hermetic Storage (%):", 0, 100, 20, 5, key="w_phl", help="Community hermetic storage silos, solar-powered aggregation cold rooms, rural feeder logistics.")
            w_live = st.slider("4. Livestock Genetics & NVRI Vaccine Hubs (%):", 0, 100, 15, 5, key="w_liv", help="National veterinary vaccine distribution (PPR/CBPP), artificial insemination, tsetse suppression.")
            w_credit = st.slider("5. Agricultural Credit De-risking & Guarantee (%):", 0, 100, 15, 5, key="w_crd", help="Credit guarantee facilities, interest drawdown concessions, blended private finance leverage.")

            # Normalize weights to 100%
            sum_w = w_inputs + w_irrig + w_phl + w_live + w_credit
            if sum_w == 0:
                sum_w = 1
            norm_w_inp = w_inputs / sum_w
            norm_w_irr = w_irrig / sum_w
            norm_w_phl = w_phl / sum_w
            norm_w_liv = w_live / sum_w
            norm_w_crd = w_credit / sum_w

            admin_leakage = st.slider("Estimated Administrative & Leakage Risk (%):", 2.0, 30.0, 10.0, 1.0, key="policy_leakage", help="Fiduciary risk, transport friction, and non-target diversion. E-vouchers reduce leakage below 8%.")

        # Econometric Calculations
        # 1. Treasury BCR
        bcr_inp = max(1.1, 2.6 - (0.02 * admin_leakage))
        bcr_irr = 4.3
        bcr_phl = 3.7
        bcr_liv = 3.2
        bcr_crd = 4.1 # High leverage from commercial bank matching

        agg_bcr = (
            (norm_w_inp * bcr_inp) +
            (norm_w_irr * bcr_irr) +
            (norm_w_phl * bcr_phl) +
            (norm_w_liv * bcr_liv) +
            (norm_w_crd * bcr_crd)
        )
        gross_economic_value = total_budget_amount * agg_bcr
        net_economic_addition = gross_economic_value - total_budget_amount

        # 2. Employment Multipliers (Jobs per Billion)
        # Irrigation: 18,500 jobs/B; Inputs: 13,000 jobs/B; PHL: 14,000 jobs/B; Livestock: 11,500 jobs/B; Credit: 16,500 jobs/B
        weighted_job_multiplier = (
            (norm_w_inp * 13000) +
            (norm_w_irr * 18500) +
            (norm_w_phl * 14000) +
            (norm_w_liv * 11500) +
            (norm_w_crd * 16500)
        )
        total_jobs_created = int(budget_billions * weighted_job_multiplier * (1.0 - (admin_leakage / 100.0) * 0.5))
        youth_jobs = int(total_jobs_created * 0.42)
        women_jobs = int(total_jobs_created * 0.46)

        # 3. Poverty Alleviation & Caloric Headcount
        # Households lifted above extreme poverty ($2.15/day line) ~ 11,200 households per Billion
        households_out_of_poverty = int(budget_billions * 11200 * (agg_bcr / 3.0))
        stunted_children_averted = int(households_out_of_poverty * 1.8)

        # 4. Central Bank FX & Food Inflation
        # FX Saved: ~ $6.2M USD per N1.0 Billion allocated to irrigation/inputs/credit
        fx_savings_usd = budget_billions * 6.25 * 1_000_000
        # Food CPI reduction: ~ 16 basis points per N1.0B invested in grain/PHL
        food_cpi_cooling_bps = int(budget_billions * 15.5)

        with col_b_res:
            st.markdown("##### 📊 2. Inter-Ministerial Policy Scorecard")

            # Ministry of Finance Card
            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #1B5E20; background: #ffffff; padding: 14px 18px; margin-bottom: 14px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
    <div style="font-size: 0.78rem; font-weight: 700; color: #1B5E20; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
        🏛️ Ministry of Finance, Budget & National Planning
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F8FAF8; padding: 10px 14px; border-radius: 6px; border: 1px solid #E8F0E8; margin-bottom: 8px;">
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Aggregate Benefit-Cost Ratio (BCR)</div>
            <div style="color: #1B5E20; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{agg_bcr:.2f} : 1</div>
        </div>
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Gross Economic Return</div>
            <div style="color: #2E7D32; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{curr_sym}{gross_economic_value / 1e9:,.1f}B</div>
        </div>
    </div>
    <div style="font-size: 0.81rem; color: #555; line-height: 1.4;">
        Every {curr_sym}1.00 committed returns <b>{curr_sym}{agg_bcr:.2f}</b> into real agricultural GDP. Net economic gain: <b style="color: #1B5E20;">{curr_sym}{net_economic_addition / 1e9:,.1f}B</b>.
    </div>
</div>
""", unsafe_allow_html=True)

            # Ministry of Labour & Productivity Card
            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #00897B; background: #ffffff; padding: 14px 18px; margin-bottom: 14px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
    <div style="font-size: 0.78rem; font-weight: 700; color: #00897B; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
        💼 Ministry of Labour, Employment & Productivity
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F4FBF9; padding: 10px 14px; border-radius: 6px; border: 1px solid #E0F2F1; margin-bottom: 8px;">
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Total Rural Jobs Created</div>
            <div style="color: #00897B; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{total_jobs_created:,}</div>
        </div>
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Youth Employment (&lt;35 yrs)</div>
            <div style="color: #00695C; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{youth_jobs:,} <span style="font-size: 0.82rem; font-weight: 600; color: #555;">(42%)</span></div>
        </div>
    </div>
    <div style="font-size: 0.81rem; color: #555; line-height: 1.4;">
        Includes on-farm dry-season double-cropping, aggregation logistics, and agro-dealer jobs. Women participation: <b style="color: #00897B;">{women_jobs:,} (46%)</b>.
    </div>
</div>
""", unsafe_allow_html=True)

            # Ministry of Humanitarian Affairs & Poverty Alleviation Card
            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #E65100; background: #ffffff; padding: 14px 18px; margin-bottom: 14px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
    <div style="font-size: 0.78rem; font-weight: 700; color: #E65100; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
        🤝 Ministry of Humanitarian Affairs & Poverty Alleviation
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #FFF8F3; padding: 10px 14px; border-radius: 6px; border: 1px solid #FFE0B2; margin-bottom: 8px;">
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Households Lifted Out of Poverty</div>
            <div style="color: #E65100; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{households_out_of_poverty:,}</div>
        </div>
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Child Stunting Cases Averted</div>
            <div style="color: #D84315; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">{stunted_children_averted:,}</div>
        </div>
    </div>
    <div style="font-size: 0.81rem; color: #555; line-height: 1.4;">
        Direct caloric stability and household farm-gate income gains moving smallholders above the $2.15/day extreme poverty threshold.
    </div>
</div>
""", unsafe_allow_html=True)

            # Central Bank & Ministry of Trade Card
            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #1565C0; background: #ffffff; padding: 14px 18px; margin-bottom: 14px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
    <div style="font-size: 0.78rem; font-weight: 700; color: #1565C0; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
        💱 Central Bank of {country_name} & Ministry of Trade / Industry
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F4F8FD; padding: 10px 14px; border-radius: 6px; border: 1px solid #BBDEFB; margin-bottom: 8px;">
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Foreign Exchange (FX) Preserved</div>
            <div style="color: #1565C0; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">${fx_savings_usd / 1e6:,.1f}M USD</div>
        </div>
        <div>
            <div style="font-size: 0.74rem; color: #666; text-transform: uppercase; font-weight: 600;">Food Inflation CPI Relief</div>
            <div style="color: #2E7D32; font-size: 1.35rem; font-weight: 800; line-height: 1.2; margin-top: 2px;">-{food_cpi_cooling_bps} bps</div>
        </div>
    </div>
    <div style="font-size: 0.81rem; color: #555; line-height: 1.4;">
        Direct import substitution across wheat, rice, and maize reduces external reserves pressure and dampens urban consumer food inflation.
    </div>
</div>
""", unsafe_allow_html=True)


        # Plotly Inter-Pillar Comparison Chart
        st.markdown("---")
        st.markdown("##### 📈 Public Expenditure Allocation vs Socio-Economic Output by Pillar")

        pillar_names = ["1. Smart Inputs", "2. Solar Irrigation", "3. Storage & PHL", "4. Livestock & Vaccines", "5. Credit Guarantee"]
        pillar_costs = [
            (total_budget_amount * norm_w_inp) / 1e9,
            (total_budget_amount * norm_w_irr) / 1e9,
            (total_budget_amount * norm_w_phl) / 1e9,
            (total_budget_amount * norm_w_liv) / 1e9,
            (total_budget_amount * norm_w_crd) / 1e9,
        ]
        pillar_returns = [
            pillar_costs[0] * bcr_inp,
            pillar_costs[1] * bcr_irr,
            pillar_costs[2] * bcr_phl,
            pillar_costs[3] * bcr_liv,
            pillar_costs[4] * bcr_crd,
        ]

        df_pillars = pd.DataFrame({
            "Pillar": pillar_names,
            f"Budget Committed ({curr_sym}B)": pillar_costs,
            f"Gross Economic Return ({curr_sym}B)": pillar_returns,
            "BCR (x)": [bcr_inp, bcr_irr, bcr_phl, bcr_liv, bcr_crd]
        })

        fig_p = go.Figure()
        fig_p.add_trace(go.Bar(
            x=df_pillars["Pillar"],
            y=df_pillars[f"Budget Committed ({curr_sym}B)"],
            name=f"Fiscal Commitment ({curr_sym}B)",
            marker_color="#81C784"
        ))
        fig_p.add_trace(go.Bar(
            x=df_pillars["Pillar"],
            y=df_pillars[f"Gross Economic Return ({curr_sym}B)"],
            name=f"Gross Economic Return ({curr_sym}B)",
            marker_color="#1B5E20"
        ))
        fig_p.update_layout(
            barmode="group",
            plot_bgcolor="#F8FAF8",
            paper_bgcolor="#FFFFFF",
            title=f"Public Capital Committed vs Real Economic Value Added ({country_name})",
            margin=dict(l=10, r=10, t=35, b=10),
            height=300
        )
        st.plotly_chart(fig_p, use_container_width=True)

    # =========================================================================
    # TAB 2: STRATEGIC COMMODITY PORTFOLIO & IMPORT SUBSTITUTION MATRIX
    # =========================================================================
    with tab_commodity:
        st.markdown("#### 🌾 Strategic Commodity Portfolio & Import Substitution Matrix")
        st.caption("Expand beyond single commodities to model national self-sufficiency, land demand, irrigation water requirements, and foreign exchange import savings across 12 strategic value chains.")

        commodity_database = {
            "Bread Wheat (Triticum aestivum) - Major FX Drain": {
                "base_prod_mt": 120_000,
                "consumption_mt": 5_400_000,
                "import_price_usd_ton": 340,
                "yield_t_ha": 3.0,
                "water_m3_ha": 6500,
                "category": "Cereals & Grains"
            },
            "Milled Rice (Oryza sativa) - National Staple": {
                "base_prod_mt": 5_200_000,
                "consumption_mt": 7_400_000,
                "import_price_usd_ton": 560,
                "yield_t_ha": 3.2,
                "water_m3_ha": 9200,
                "category": "Cereals & Grains"
            },
            "White Maize (Zea mays) - Food Security Anchor": {
                "base_prod_mt": 12_800_000,
                "consumption_mt": 13_500_000,
                "import_price_usd_ton": 270,
                "yield_t_ha": 2.5,
                "water_m3_ha": 4800,
                "category": "Cereals & Grains"
            },
            "Yellow Maize (Zea mays) - Poultry & Feed Industry": {
                "base_prod_mt": 3_500_000,
                "consumption_mt": 5_200_000,
                "import_price_usd_ton": 285,
                "yield_t_ha": 3.5,
                "water_m3_ha": 5000,
                "category": "Cereals & Grains"
            },
            "Cassava Starch & HQCF (Manihot esculenta) - Industrial Substitution": {
                "base_prod_mt": 60_000_000,
                "consumption_mt": 62_000_000,
                "import_price_usd_ton": 450,
                "yield_t_ha": 15.0,
                "water_m3_ha": 3200,
                "category": "Roots & Tubers"
            },
            "Soybean (Glycine max) - Protein & Vegetable Oil": {
                "base_prod_mt": 950_000,
                "consumption_mt": 1_850_000,
                "import_price_usd_ton": 520,
                "yield_t_ha": 1.6,
                "water_m3_ha": 3900,
                "category": "Legumes & Oilseeds"
            },
            "Cowpea / Black-Eyed Beans (Vigna unguiculata)": {
                "base_prod_mt": 3_800_000,
                "consumption_mt": 4_100_000,
                "import_price_usd_ton": 680,
                "yield_t_ha": 1.1,
                "water_m3_ha": 2800,
                "category": "Legumes & Oilseeds"
            },
            "Commercial Broiler Meat - Poultry Protein": {
                "base_prod_mt": 450_000,
                "consumption_mt": 950_000,
                "import_price_usd_ton": 1850,
                "yield_t_ha": 0.0,
                "water_m3_ha": 0,
                "category": "Livestock & Protein"
            },
            "Fresh Cattle Milk (Dairy) - Import Replacement": {
                "base_prod_mt": 680_000,
                "consumption_mt": 1_800_000,
                "import_price_usd_ton": 3200,
                "yield_t_ha": 0.0,
                "water_m3_ha": 0,
                "category": "Livestock & Protein"
            },
            "Farmed Catfish & Tilapia - Aquaculture Security": {
                "base_prod_mt": 380_000,
                "consumption_mt": 1_200_000,
                "import_price_usd_ton": 2200,
                "yield_t_ha": 0.0,
                "water_m3_ha": 0,
                "category": "Livestock & Protein"
            },
            "Export Cocoa Beans - Foreign Exchange Earner": {
                "base_prod_mt": 340_000,
                "consumption_mt": 40_000,
                "import_price_usd_ton": 4200,
                "yield_t_ha": 0.55,
                "water_m3_ha": 4000,
                "category": "Export Cash Crops"
            }
        }

        col_c_sel, col_c_kpi = st.columns([1.0, 1.35], gap="large")

        with col_c_sel:
            st.markdown("##### 🎛️ 1. Commodity Target & Policy Instruments")
            selected_commodity = st.selectbox(
                "Select Strategic Commodity Value Chain:",
                options=list(commodity_database.keys()),
                index=1,
                key="comm_select"
            )
            c_meta = commodity_database[selected_commodity]

            target_growth_pct = st.slider(
                "Target National Production Expansion (%):",
                min_value=10,
                max_value=100,
                value=35,
                step=5,
                key="comm_growth_pct"
            )

            policy_instrument = st.selectbox(
                "Strategic Government Policy Lever:",
                [
                    "Biometric Input E-Vouchers + Solar Irrigation Scheme",
                    "Anchor Outgrower Contract + Processing Tax Credit",
                    "Import Tariff Enhancement (+35% Customs Duty)",
                    "Guaranteed Minimum Price (GMP) & Strategic Buffer Procurement"
                ],
                key="comm_lever"
            )

            st.markdown(f"""
<div style="font-size: 0.81rem; color: #1B5E20; background: #E8F5E9; padding: 6px 10px; border-radius: 5px; margin-top: 4px; border-left: 3px solid #2E7D32;">
    • <b>Current Baseline Production</b>: {c_meta['base_prod_mt']:,} MT<br>
    • <b>National Domestic Demand</b>: {c_meta['consumption_mt']:,} MT<br>
    • <b>Baseline Self-Sufficiency Index</b>: <b>{(c_meta['base_prod_mt'] / c_meta['consumption_mt']) * 100:.1f}%</b><br>
    • <b>World Parity Import Price</b>: ${c_meta['import_price_usd_ton']:,} / Metric Ton
</div>
""", unsafe_allow_html=True)

        # Mathematical calculations for Commodity
        base_prod = c_meta["base_prod_mt"]
        national_demand = c_meta["consumption_mt"]
        added_production_mt = base_prod * (target_growth_pct / 100.0)
        new_total_prod_mt = base_prod + added_production_mt
        new_self_sufficiency = min(100.0, (new_total_prod_mt / national_demand) * 100.0)

        # Land & water calculations if crop
        if c_meta["yield_t_ha"] > 0:
            additional_ha = added_production_mt / c_meta["yield_t_ha"]
            water_demand_m3 = additional_ha * c_meta["water_m3_ha"]
        else:
            additional_ha = 0
            water_demand_m3 = 0

        # Import bill saved
        import_bill_saved_usd = added_production_mt * c_meta["import_price_usd_ton"]
        # Convert to local currency equivalent (~1550 NGN/USD as benchmark)
        fx_rate = 1550 if curr_code == "NGN" else (130 if curr_code == "KES" else (15 if curr_code == "GHS" else 610))
        local_curr_saved = import_bill_saved_usd * fx_rate

        with col_c_kpi:
            st.markdown("##### 📊 2. Macro-Economic & Self-Sufficiency Projections")

            ck1, ck2 = st.columns(2)
            ck1.metric("New Domestic Harvest", f"{new_total_prod_mt / 1e6:.2f}M MT", f"+{added_production_mt / 1e6:.2f}M MT")
            ck2.metric("National Self-Sufficiency", f"{new_self_sufficiency:.1f}%", f"+{(new_total_prod_mt - base_prod)/national_demand * 100:.1f}%")

            ck3, ck4 = st.columns(2)
            ck3.metric("Foreign Exchange Saved", f"${import_bill_saved_usd / 1e6:,.1f}M USD")
            ck4.metric(f"Local Currency Value", f"{curr_sym}{local_curr_saved / 1e9:,.1f}B")

            if additional_ha > 0:
                st.caption(f"🌱 **Resource Requirements**: **{additional_ha:,.0f} Hectares** of cultivated arable land and **{water_demand_m3 / 1e9:.2f} Billion m³** of irrigation water.")

            # Gauge Chart for Self Sufficiency
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=new_self_sufficiency,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"National {selected_commodity.split(' (')[0]} Self-Sufficiency Index (%)", 'font': {'size': 14}},
                delta={'reference': (base_prod / national_demand) * 100.0, 'increasing': {'color': "#1B5E20"}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2E7D32"},
                    'bar': {'color': "#1B5E20"},
                    'bgcolor': "white",
                    'borderwidth': 1,
                    'bordercolor': "#CCCCCC",
                    'steps': [
                        {'range': [0, 50], 'color': '#FFCDD2'},
                        {'range': [50, 80], 'color': '#FFF9C4'},
                        {'range': [80, 100], 'color': '#C8E6C9'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 3},
                        'thickness': 0.75,
                        'value': 100.0
                    }
                }
            ))
            fig_gauge.update_layout(height=230, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor="#FFFFFF")
            st.plotly_chart(fig_gauge, use_container_width=True)

    # =========================================================================
    # TAB 3: FOOD INFLATION & MACRO SHOCK RESILIENCE
    # =========================================================================
    with tab_shock:
        st.markdown("#### 🛡️ Food Inflation, Strategic Reserves & Macro Shock Simulator")
        st.caption("Stress-test national food security, urban consumer prices, and household purchasing power against global supply chain shocks, droughts, and currency devaluations.")

        col_sh_cfg, col_sh_res = st.columns([1.0, 1.45], gap="large")

        with col_sh_cfg:
            st.markdown("##### 🎛️ 1. External Geopolitical & Climate Stress Scenarios")
            
            shock_type = st.selectbox(
                "Select External Shock Scenario:",
                [
                    "Geopolitical Global Fertilizer Spike (+60% Import Price Surge)",
                    "Severe Climate Drought & Rainfall Deficit (-28% National Harvest)",
                    "Macroeconomic Currency Devaluation (+45% Foreign Exchange Depreciation)",
                    "Regional Insecurity & Internal Trade Route Blockade"
                ],
                key="shock_type"
            )

            st.markdown("###### Counter-Cyclical Government Mitigations:")
            sgr_release_mt = st.slider(
                "Strategic Grain Reserve (SGR) Release (Metric Tons):",
                min_value=0,
                max_value=600_000,
                value=250_000,
                step=25_000,
                key="sgr_release",
                help="Releasing government-held buffer grain stocks into wholesale open markets dampens consumer price spikes."
            )

            emergency_safety_net = st.slider(
                "Targeted Vulnerable Household Food Vouchers (Households):",
                min_value=0,
                max_value=2_000_000,
                value=650_000,
                step=50_000,
                key="safety_net_hh",
                help="Emergency digital food e-vouchers protecting vulnerable urban and rural poor."
            )

            tariff_waiver = st.checkbox("Enforce Emergency 0% Import Tariff on Essential Food & Inputs", value=True, key="shock_tariff")

        # Shock Computations
        if "Fertilizer Spike" in shock_type:
            unmitigated_inflation = 38.5
            shock_driver = "Escalating farm-gate production costs across commercial grain belts."
        elif "Drought" in shock_type:
            unmitigated_inflation = 44.0
            shock_driver = "Acute domestic grain deficit triggering speculative hoarding."
        elif "Currency Devaluation" in shock_type:
            unmitigated_inflation = 41.2
            shock_driver = "Import parity spike across wheat, edible oils, and packaged foods."
        else:
            unmitigated_inflation = 36.0
            shock_driver = "Localized supply starvation and transport risk premiums."

        # Mitigation impacts
        sgr_relief_pts = (sgr_release_mt / 100_000.0) * 2.8
        safety_net_relief_pts = (emergency_safety_net / 500_000.0) * 2.1
        tariff_relief_pts = 3.5 if tariff_waiver else 0.0

        total_mitigation = sgr_relief_pts + safety_net_relief_pts + tariff_relief_pts
        mitigated_inflation = max(12.0, unmitigated_inflation - total_mitigation)
        total_cooling_bps = int(total_mitigation * 100)

        with col_sh_res:
            st.markdown("##### 📊 2. Food Inflation & Household Impact")

            sk1, sk2 = st.columns(2)
            sk1.metric("Unmitigated Food Inflation", f"{unmitigated_inflation:.1f}%", "Peak Shock", delta_color="inverse")
            sk2.metric("Stabilized Food Inflation", f"{mitigated_inflation:.1f}%", f"-{total_cooling_bps} bps Relief")

            st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #1B5E20; padding: 12px 14px; margin-top: 10px;">
    <div style="font-size: 0.76rem; font-weight: 700; color: #2E7D32; text-transform: uppercase;">
        🏛️ Government Stabilization Evaluation
    </div>
    <div style="font-size: 0.85rem; color: #333; margin-top: 4px; line-height: 1.5;">
    • <b>Primary Driver</b>: {shock_driver}<br>
    • <b>SGR Buffer Release ({sgr_release_mt:,} MT)</b>: Injected directly into wholesale deficit grain hubs, shaving <b>{sgr_relief_pts:.1f}%</b> off speculative food inflation.<br>
    • <b>Targeted Food Vouchers</b>: Shielded <b>{emergency_safety_net:,} vulnerable households</b> from acute calorie deprivation.<br>
    • <b>Net Macro Result</b>: Food inflation successfully contained from a catastrophic <b>{unmitigated_inflation:.1f}% down to {mitigated_inflation:.1f}%</b>.
    </div>
</div>
""", unsafe_allow_html=True)

        # 12-Month Simulated Food CPI Curve
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        baseline_cpi = [21.5, 22.0, 22.8, 23.5, 24.2, 25.0, 25.5, 24.8, 23.5, 22.2, 21.8, 21.4]
        unmitigated_cpi = [21.5, 24.0, 28.5, 33.2, 38.5, unmitigated_inflation, unmitigated_inflation - 1.2, unmitigated_inflation - 2.5, 35.0, 32.0, 29.5, 28.0]
        mitigated_cpi = [21.5, 23.2, 26.0, 28.5, mitigated_inflation, mitigated_inflation - 1.5, mitigated_inflation - 3.0, 25.0, 23.5, 22.8, 22.0, 21.8]

        df_cpi = pd.DataFrame({
            "Month": months,
            "Baseline Inflation (%)": baseline_cpi,
            "Unmitigated Shock (%)": unmitigated_cpi,
            "Government Stabilized Policy Response (%)": mitigated_cpi
        })

        fig_cpi = px.line(
            df_cpi,
            x="Month",
            y=["Baseline Inflation (%)", "Unmitigated Shock (%)", "Government Stabilized Policy Response (%)"],
            title=f"12-Month Food Price Inflation (CPI) Trajectory Under Shock vs Intervention ({country_name})",
            color_discrete_map={
                "Baseline Inflation (%)": "#78909C",
                "Unmitigated Shock (%)": "#D32F2F",
                "Government Stabilized Policy Response (%)": "#1B5E20"
            }
        )
        fig_cpi.update_layout(plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF", height=280, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_cpi, use_container_width=True)

    # =========================================================================
    # TAB 4: CABINET MEMORANDUM & POLICY BRIEF GENERATOR
    # =========================================================================
    with tab_cabinet:
        st.markdown("#### 📑 Federal Executive Council (FEC) Cabinet Memorandum Generator")
        st.caption("Automatically synthesize an institutional, publication-grade Cabinet Policy Memorandum ready for submission to the Federal Executive Council, Ministry of Finance, Parliamentary Committees, and Multilateral Donors.")

        memo_title = st.text_input(
            "Memorandum Title:",
            value=f"COMPREHENSIVE NATIONAL AGRICULTURAL EMPOWERMENT & FOOD INFLATION CONTAINMENT PROGRAMME (2026–2030)",
            key="policy_memo_title"
        )

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            sponsoring_min = st.text_input(
                "Sponsoring Ministry / Department:",
                value=f"Federal Ministry of Agriculture and Food Security (in Conjunction with Ministry of Budget & National Planning)",
                key="policy_sponsoring_min"
            )
        with col_m2:
            target_cabinet = st.text_input(
                "Cabinet / Committee Jurisdiction:",
                value=f"Federal Executive Council (FEC) & National Economic Council (NEC) of {country_name}",
                key="policy_jurisdiction"
            )

        # Synthesize Full Institutional Policy Brief
        cabinet_memorandum = f"""# EXECUTIVE CABINET MEMORANDUM: FEDERAL AGRICULTURAL POLICY

**MEMORANDUM TITLE**: {memo_title}  
**SUBMITTED BY**: {sponsoring_min}  
**TARGET JURISDICTION**: {target_cabinet}  
**DATE OF SUBMISSION**: 2026 FISCAL HORIZON  
**TOTAL FISCAL APPROPRIATION REQUEST**: **{curr_sym}{total_budget_amount / 1e9:,.1f} BILLION** ({curr_code})  

---

## 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
The national agriculture sector in **{country_name}** currently operates below its agro-ecological potential due to acute vulnerabilities: escalating chemical input prices, severe post-harvest storage deficits (averaging 30%–40% grain loss), reliance on erratic rainfed production regimes, and seasonal food inflation shocks. 

To overcome these structural bottlenecks, this Memorandum presents an integrated, cross-ministerial capital investment framework. Rather than sustaining inefficient open-market commodity subsidies, this policy allocates **{curr_sym}{budget_billions:.1f} Billion** across five Pareto-optimal public goods: biometric smart e-vouchers, smallholder solar irrigation, hermetic grain storage hubs, livestock disease biosecurity, and agricultural credit de-risking.

---

## 2. CROSS-MINISTERIAL BUDGET ALLOCATION MATRIX
| Strategic Pillar | Budget Share (%) | Capital Appropriation ({curr_sym}) | Primary Executing Agency | Primary Strategic Objective |
| :--- | :--- | :--- | :--- | :--- |
| **1. Smart E-Vouchers & Stoichiometric Nutrients** | {norm_w_inp * 100:.1f}% | {curr_sym}{(total_budget_amount * norm_w_inp) / 1e9:,.2f}B | FMAFS & National Seed Council | Biometric delivery of certified seed and balanced NPK to verified farmers. |
| **2. Solar Irrigation & Basin Water Infrastructure** | {norm_w_irr * 100:.1f}% | {curr_sym}{(total_budget_amount * norm_w_irr) / 1e9:,.2f}B | River Basin Development Authorities | Dry-season double-cropping expansion across lowland basins. |
| **3. Post-Harvest Loss (PHL) & Hermetic Storage Hubs** | {norm_w_phl * 100:.1f}% | {curr_sym}{(total_budget_amount * norm_w_phl) / 1e9:,.2f}B | Strategic Grain Reserve Dept | Community hermetic silos, solar cold rooms, and rural aggregation centers. |
| **4. Livestock Genetics & NVRI Vaccine Hubs** | {norm_w_liv * 100:.1f}% | {curr_sym}{(total_budget_amount * norm_w_liv) / 1e9:,.2f}B | NVRI Vom, NAPRI & Vet Services | Mass annual vaccination against PPR, CBPP, and tick-borne epizootics. |
| **5. Agricultural Credit De-risking & Blended Guarantee** | {norm_w_crd * 100:.1f}% | {curr_sym}{(total_budget_amount * norm_w_crd) / 1e9:,.2f}B | Central Bank / Dev Finance Dept | Concessionary single-digit credit matching and commercial bank de-risking. |
| **TOTAL PUBLIC INVESTMENT** | **100.0%** | **{curr_sym}{budget_billions:.1f} BILLION** | **Inter-Ministerial Project Steering Committee** | **Comprehensive National Food Security Transformation** |

---

## 3. INTER-MINISTERIAL SOCIO-ECONOMIC IMPACT ASSESSMENT

### A. Ministry of Finance, Budget & National Planning (Fiscal Returns)
- **Aggregate Benefit-Cost Ratio (BCR)**: **{agg_bcr:.2f} to 1.00**
- **Gross Economic Value Added**: **{curr_sym}{gross_economic_value / 1e9:,.2f} Billion**
- **Net Fiscal Expansion**: Every **{curr_sym}1.00** appropriated by Treasury generates **{curr_sym}{agg_bcr:.2f}** in real national GDP.
- **Fiduciary Safeguards**: Biometric identification and geospatial GPS farm-mapping restrict administrative leakage below {admin_leakage:.1f}%.

### B. Ministry of Labour, Employment & Productivity (Rural Jobs)
- **Total Employment Creation**: **{total_jobs_created:,} Direct & Indirect Rural Jobs**
- **Youth Empowerment (Ages 18–35)**: **{youth_jobs:,} positions** in mechanization hiring hubs, solar pump maintenance, and digital aggregation.
- **Women Integration**: **{women_jobs:,} positions (46.0%)** in seed sorting, post-harvest processing, and urban retail distribution.

### C. Ministry of Humanitarian Affairs & Poverty Alleviation (Human Capital)
- **Poverty Headcount Reduction**: **{households_out_of_poverty:,} Rural Households** permanently lifted above the national extreme poverty line ($2.15/day).
- **Childhood Stunting & Malnutrition**: Averting acute protein-energy malnutrition across **{stunted_children_averted:,} children** through bio-fortified maize/cassava and dairy access.

### D. Central Bank & Ministry of Trade / Industry (Macroeconomic Stability)
- **Foreign Exchange (FX) Import Substitution**: **${fx_savings_usd / 1e6:,.1f} Million USD** saved annually.
- **Headline Food Inflation (CPI) Relief**: Shaving **{food_cpi_cooling_bps} basis points** off national urban consumer food inflation.

---

## 4. STRATEGIC RISK MATRIX & FIDUCIARY SAFEGUARDS
| Strategic Risk Factor | Severity | Fiduciary Mitigation Framework |
| :--- | :--- | :--- |
| **Input Diversion / Black-Market Resale** | Moderate | Mandate 100% digital e-voucher redemption tied to National Identity Number (NIN) and biometric fingerprint verification at accredited agro-dealer POS terminals. |
| **Severe Drought / Rainfall Variability** | High | Pillar 2 allocates {norm_w_irr * 100:.1f}% exclusively to solar drip irrigation and water retention basins, decoupling production from erratic rainfall. |
| **Macroeconomic FX Devaluation** | High | Prioritize domestic bio-fertilizer blending, local seed multiplying cooperatives, and solar infrastructure over imported chemical inputs. |

---

## 5. MINISTERIAL PRAYERS & RESOLUTIONS FOR CABINET APPROVAL
The Federal Executive Council (FEC) is respectfully requested to:
1. **APPROVE** the allocation of **{curr_sym}{budget_billions:.1f} Billion** for the National Agricultural Empowerment & Food Inflation Containment Programme over the 2026–2030 fiscal cycle.
2. **AUTHORIZE** the Federal Ministry of Finance and Central Bank to release the capital envelope to the designated Inter-Ministerial Project Account in four phased quarterly tranches.
3. **MANDATE** the National Agricultural Technology Steering Committee to enforce strict biometric e-voucher validation to maintain fiduciary leakage below {admin_leakage:.1f}%.
4. **DIRECT** the National Bureau of Statistics (NBS) and Federal Ministry of Labour to audit semi-annual progress on job creation ({total_jobs_created:,} target) and household poverty headcount reduction.
"""

        st.markdown("---")
        st.markdown("##### 📄 Executive Cabinet Memorandum Preview")

        # Gemini AI Policy Enhancement Option
        gemini_key = get_gemini_api_key()
        c_pm1, c_pm2 = st.columns([2, 1])
        with c_pm1:
            if gemini_key:
                st.markdown("🟢 **Live Google Gemini Engine Active** *(Secured via Cloud Secrets)*")
            else:
                st.markdown("⚡ **Built-in Institutional Policy Engine Active** *(Offline Mode)*")
        with c_pm2:
            if not gemini_key:
                with st.expander("🔑 Connect Gemini Key", expanded=False):
                    pol_key_input = st.text_input(
                        "Google Gemini Key:",
                        value="",
                        type="password",
                        placeholder="AIzaSy...",
                        key="pol_gemini_key_input",
                        help="Enter free Gemini key from aistudio.google.com"
                    )
                    cleaned_pk = (pol_key_input or "").strip().strip("'\"")
                    if cleaned_pk:
                        set_gemini_api_key(cleaned_pk)
                        gemini_key = cleaned_pk
                        val = validate_gemini_key(cleaned_pk)
                        if val.get("valid"):
                            st.success(f"🟢 {val.get('message')}")
                        else:
                            st.error(f"🔴 {val.get('message')}")

        col_enh_btn, col_enh_info = st.columns([1, 2])
        with col_enh_btn:
            enhance_clicked = st.button("✨ Enhance Memo with Live Gemini AI", key="btn_enhance_memo", type="secondary")
        with col_enh_info:
            st.caption("Drafts bespoke executive cabinet prose incorporating macroeconomic debt sustainability, FX reserves, and civil service resolutions.")

        if enhance_clicked:
            if not gemini_key:
                st.warning("⚠️ No Gemini API key detected. Please configure your free key above or in the API Hub.")
            else:
                with st.spinner("Synthesizing high-level ministerial prose, macro-economic justifications, and inter-ministerial resolutions with Gemini AI..."):
                    policy_prompt = f"""You are the Principal Economic Advisor to the Minister of Agriculture and the Federal Cabinet of {country_name}.
Transform and expand the following draft policy brief into a bespoke, ministerial-grade Executive Cabinet Memorandum for the Federal Executive Council / National Cabinet:

{cabinet_memorandum}

Specific Instructions:
1. Retain the exact figures, tables, and budgetary allocations ({curr_sym}{total_budget_amount / 1e9:,.1f} Billion).
2. Elevate the prose to executive civil-service grade, incorporating macroeconomic rationale (fiscal return on investment, sovereign debt sustainability, foreign exchange reserve protection, and headline CPI food inflation cooling).
3. Elaborate on inter-ministerial coordination across Ministries of Finance, Budget & National Planning, Labour & Productivity, Water Resources, Central Bank, and Humanitarian Affairs.
4. Provide structured Cabinet Prayers, Implementation Phasing, and Risk Mitigation Guardrails in publication-grade markdown."""

                    try:
                        orch_res = call_live_llm_orchestration(policy_prompt, api_key=gemini_key, provider="gemini", active_region=active_reg)
                        enhanced_text = orch_res.get("final_synthesis", "")
                        if enhanced_text:
                            st.session_state["enhanced_cabinet_memo"] = enhanced_text
                            st.success("✅ Executive Cabinet Memorandum successfully enhanced via Live Gemini Intelligence!")
                        else:
                            st.warning("Could not retrieve live enhanced memo; displaying baseline institutional memo.")
                    except Exception as e:
                        st.error(f"Error during AI enhancement: {str(e)}")

        # Memo View Selector if Enhanced Memo exists
        memo_to_display = cabinet_memorandum
        if "enhanced_cabinet_memo" in st.session_state:
            view_choice = st.radio(
                "Select Memorandum Version to Inspect & Export:",
                ["✨ Gemini AI Enhanced Executive Cabinet Memorandum", "📄 Standard Institutional Memorandum"],
                horizontal=True
            )
            if "Gemini AI Enhanced" in view_choice:
                memo_to_display = st.session_state["enhanced_cabinet_memo"]

        st.markdown(memo_to_display)

        # Download Buttons Bar
        render_download_buttons(
            content_text=memo_to_display,
            filename_prefix=f"Cabinet_Memorandum_AgriPolicy_{country_name}",
            title=f"Cabinet Memorandum - Agricultural Policy ({country_name})",
            key_prefix="btn_dl_policy_memo"
        )
