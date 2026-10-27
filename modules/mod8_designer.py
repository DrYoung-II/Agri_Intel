"""
Module 8: Agricultural Experiment Designer
CRD, RCBD, Split-Plot Factorial Design, Randomisation Tables, and Template Generators
"""

import pandas as pd
import numpy as np
import streamlit as st
from core.crop_taxonomy import PAN_AFRICAN_CROPS


def render_experiment_designer():
    st.markdown("### 📐 Agricultural Experiment Designer")
    st.caption("Automated experimental layouts, treatment randomisation, field book CSV templates, and R/Python analysis pipelines.")

    c1, c2, c3 = st.columns(3)
    with c1:
        exp_design = st.selectbox("Experimental Design:", ["Randomized Complete Block Design (RCBD)", "Completely Randomized Design (CRD)", "Split-Plot Design"])
    with c2:
        num_reps = st.slider("Number of Replications / Blocks:", 2, 8, 4)
    with c3:
        crop_choice_raw = st.selectbox(
            "Trial Crop / Organism:",
            PAN_AFRICAN_CROPS,
            index=0,
            help="Select any African crop or enter a custom organism/commodity."
        )
        if "Custom Input" in crop_choice_raw:
            custom_crop = st.text_input("Enter Specific Trial Crop / Species:", "White Yam (Dioscorea rotundata)")
            target_crop = custom_crop.strip() if custom_crop.strip() else "Custom Organism"
        else:
            target_crop = crop_choice_raw

    st.markdown("#### 🧪 Define Treatments")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        factor_a_name = st.text_input("Factor A Name:", "Fertilizer_Treatment")
        factor_a_levels = st.text_area("Factor A Levels (comma separated):", "Control_Zero, NPK_Standard, NPK_Biochar, Integrated_Manure")
    with col_t2:
        factor_b_name = st.text_input("Factor B Name (Optional / Factorial):", "Irrigation_Regime")
        factor_b_levels = st.text_area("Factor B Levels (comma separated):", "Rainfed, Drip_Irrigation")

    if st.button("🎲 Generate Randomised Field Layout & Data Collection Template", key="btn_gen_layout"):
        levels_a = [x.strip() for x in factor_a_levels.split(",") if x.strip()]
        levels_b = [x.strip() for x in factor_b_levels.split(",") if x.strip()]
        if not levels_a:
            st.error("⚠️ Please specify at least one level for Factor A.")
            return

        if not levels_b:
            levels_b = ["None"]

        clean_crop = target_crop.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")[:20]
        clean_fa = factor_a_name.strip().replace(" ", "_")
        clean_fb = factor_b_name.strip().replace(" ", "_")

        # Determine dynamic phenotypic response variables tailored to the crop/organism
        c_low = target_crop.lower()
        if any(k in c_low for k in ["cassava", "yam", "potato", "tuber", "cocoyam"]):
            primary_metric = "Storage_Root_Yield_t_ha"
            pheno_cols = {primary_metric: np.nan, "Tuber_Count_per_Plant": np.nan, "Dry_Matter_Content_pct": np.nan}
        elif any(k in c_low for k in ["cowpea", "soybean", "groundnut", "bean", "legume"]):
            primary_metric = "Grain_Yield_kg_plot"
            pheno_cols = {primary_metric: np.nan, "Pod_Count_per_Plant": np.nan, "Nodule_Score": np.nan}
        elif any(k in c_low for k in ["tomato", "pepper", "onion", "okra", "vegetable"]):
            primary_metric = "Marketable_Fruit_Yield_kg_plot"
            pheno_cols = {primary_metric: np.nan, "Fruit_Firmness_N": np.nan, "BRIX_Soluble_Solids_pct": np.nan}
        elif any(k in c_low for k in ["cattle", "sheep", "goat", "poultry", "livestock"]):
            primary_metric = "Live_Body_Weight_kg"
            pheno_cols = {primary_metric: np.nan, "Average_Daily_Gain_g": np.nan, "Feed_Conversion_Ratio": np.nan}
        elif any(k in c_low for k in ["cocoa", "coffee", "oil palm", "cashew"]):
            primary_metric = "Export_Yield_kg_tree"
            pheno_cols = {primary_metric: np.nan, "Pod_Index": np.nan, "Grade_A_Bean_pct": np.nan}
        else:
            primary_metric = "Grain_Yield_kg_plot"
            pheno_cols = {primary_metric: np.nan, "Plant_Height_cm": np.nan, "Days_to_50_Flowering": np.nan}

        # Generate plots
        rows = []
        plot_id = 101
        for rep in range(1, num_reps + 1):
            block_plots = []
            for la in levels_a:
                for lb in levels_b:
                    block_plots.append((la, lb))
            
            # Randomize within block if RCBD
            np.random.seed(42 + rep)
            np.random.shuffle(block_plots)
            
            for la, lb in block_plots:
                row_dict = {
                    "Plot_ID": plot_id,
                    "Replication_Block": f"Block_{rep}",
                    clean_fa: la,
                }
                if levels_b != ["None"]:
                    row_dict[clean_fb] = lb
                row_dict.update(pheno_cols)
                row_dict["Notes"] = ""
                rows.append(row_dict)
                plot_id += 1

        df_fieldbook = pd.DataFrame(rows)
        st.success(f"Generated {len(df_fieldbook)} experimental plots randomized across {num_reps} blocks for {target_crop}!")
        
        st.markdown(f"##### 📋 Randomised Field Book Preview ({target_crop})")
        st.dataframe(df_fieldbook.head(12), use_container_width=True)

        csv_fieldbook = df_fieldbook.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Field Data Collection Template (CSV)",
            data=csv_fieldbook,
            file_name=f"{clean_crop}_experimental_fieldbook.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.markdown(f"##### 💻 Auto-Generated R Analysis Script for {target_crop}")

        is_rcbd = "Block" in exp_design
        is_split = "Split" in exp_design
        if levels_b != ["None"]:
            if is_rcbd:
                formula = f"{primary_metric} ~ Replication_Block + {clean_fa} + {clean_fb} + {clean_fa}:{clean_fb}"
            elif is_split:
                formula = f"{primary_metric} ~ Replication_Block + {clean_fa} + Error(Replication_Block/{clean_fa}) + {clean_fb} + {clean_fa}:{clean_fb}"
            else:
                formula = f"{primary_metric} ~ {clean_fa} + {clean_fb} + {clean_fa}:{clean_fb}"
        else:
            if is_rcbd:
                formula = f"{primary_metric} ~ Replication_Block + {clean_fa}"
            else:
                formula = f"{primary_metric} ~ {clean_fa}"

        r_script = f"""# Auto-generated R script by AgriIntel for {exp_design} ({target_crop})
library(agricolae)

# 1. Load your populated field data
data <- read.csv("{clean_crop}_experimental_fieldbook.csv")

# 2. ANOVA Model
model <- aov({formula}, data = data)
summary(model)

# 3. Post-Hoc Duncan's Multiple Range Test
duncan_out <- duncan.test(model, "{clean_fa}", alpha = 0.05, console = TRUE)
plot(duncan_out, main = "Duncan Multiple Range Test Mean Separation")
"""
        st.code(r_script, language="r")
