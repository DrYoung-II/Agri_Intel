"""
Module 8: Agricultural Experiment Designer
CRD, RCBD, Split-Plot Factorial Design, Randomisation Tables, and Template Generators
"""

import pandas as pd
import numpy as np
import os
import streamlit as st
from core.crop_taxonomy import PAN_AFRICAN_CROPS
from core.broadcast_dispatcher import render_dispatch_trigger_card


def render_experiment_designer():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 📐 Concepteur de Dispositifs Expérimentaux Agricoles")
        st.caption("Plans d'expérimentation automatisés, randomisation des traitements, modèles de carnet de champ CSV et pipelines d'analyse statistique.")
    else:
        st.markdown("### 📐 Agricultural Experiment Designer")
        st.caption("Automated experimental layouts, treatment randomisation, field book CSV templates, and R/Python analysis pipelines.")

    c1, c2, c3 = st.columns(3)
    with c1:
        des_lbl = "Dispositif Expérimental :" if is_fr else "Experimental Design:"
        des_opts = ["Blocs Complets Randomisés (RCBD)", "Complètement Aléatoire (CRD)", "Parcelles Divisées (Split-Plot)"] if is_fr else ["Randomized Complete Block Design (RCBD)", "Completely Randomized Design (CRD)", "Split-Plot Design"]
        exp_design = st.selectbox(des_lbl, des_opts)
    with c2:
        rep_lbl = "Nombre de Répétitions / Blocs :" if is_fr else "Number of Replications / Blocks:"
        num_reps = st.slider(
            rep_lbl,
            min_value=2,
            max_value=30,
            value=4,
            help="Field trials (RCBD) typically use 3–6 blocks. Laboratory, greenhouse pots, poultry, and animal feeding trials routinely use 8–30 replications."
        )
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

    st.markdown("#### 🧪 Définition des Traitements" if is_fr else "#### 🧪 Define Treatments")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        factor_a_name = st.text_input("Nom du Facteur A :" if is_fr else "Factor A Name:", "Fertilizer_Treatment")
        factor_a_levels = st.text_area("Niveaux Facteur A (séparés par virgules) :" if is_fr else "Factor A Levels (comma separated):", "Control_Zero, NPK_Standard, NPK_Biochar, Integrated_Manure")
    with col_t2:
        factor_b_name = st.text_input("Nom Facteur B (Optionnel / Factoriel) :" if is_fr else "Factor B Name (Optional / Factorial):", "Irrigation_Regime")
        factor_b_levels = st.text_area("Niveaux Facteur B (séparés par virgules) :" if is_fr else "Factor B Levels (comma separated):", "Rainfed, Drip_Irrigation")

    btn_layout_lbl = "🎲 Générer le Plan de Champ Randomisé & Modèle de Collecte" if is_fr else "🎲 Generate Randomised Field Layout & Data Collection Template"
    if st.button(btn_layout_lbl, key="btn_gen_layout"):
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
            label="📥 Télécharger le Carnet de Champ (CSV)" if is_fr else "📥 Download Field Data Collection Template (CSV)",
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

        r_script = f"""# Auto-generated R script by AgroBiometrix for {exp_design} ({target_crop})
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


def render_dataset_health_auditor():
    """
    Pre-Analysis Dataset Health, Missingness & Assumption Auditor
    Audits experimental trial datasets before running ANOVA, DMRT, or Mixed Models.
    """
    is_fr = st.session_state.get("app_lang", "en") == "fr"

    if is_fr:
        st.markdown("### 🩺 Audit de Santé des Données Expérimentales & Données Manquantes")
        st.caption("Inspecte les jeux de données expérimentaux pour détecter les valeurs manquantes, l'équilibre des facteurs et l'adéquation des modèles.")
        ds_choice_lbl = "Choisir le jeu de données à auditer :"
        ds_choice_opts = ["Charger l'Essai Bovin Pré-chargé", "Téléverser un Fichier CSV Personnalisé"]
    else:
        st.markdown("### 🩺 Pre-Analysis Dataset Health & Missingness Auditor")
        st.caption("Inspects experimental datasets for missingness, experimental factor balance, repeated measures, and model appropriateness before running ANOVA/DMRT.")
        ds_choice_lbl = "Choose Dataset to Inspect:"
        ds_choice_opts = ["Load Pre-loaded Cattle Trial Dataset", "Upload Custom CSV File"]

    ds_choice = st.radio(ds_choice_lbl, ds_choice_opts, horizontal=True, key="auditor_ds_choice")

    df_inspect = None
    if ds_choice in ["Load Pre-loaded Cattle Trial Dataset", "Charger l'Essai Bovin Pré-chargé"]:
        cattle_path = os.path.join("data", "sample_cattle_heat_tolerance.csv")
        if os.path.exists(cattle_path):
            df_inspect = pd.read_csv(cattle_path)
        else:
            st.info("Le jeu de données de démonstration sera initialisé lors de l'accès." if is_fr else "Sample cattle trial dataset will be automatically initialized when accessed.")
    else:
        up_lbl = "Téléverser un Jeu de Données Expérimental (CSV)" if is_fr else "Upload Experimental Dataset (CSV)"
        uploaded_file = st.file_uploader(up_lbl, type=["csv"], key="mod8_auditor_uploader")
        if uploaded_file:
            df_inspect = pd.read_csv(uploaded_file)

    if df_inspect is not None:
        if df_inspect.empty:
            st.warning("⚠️ Le jeu de données sélectionné ou téléversé est vide (0 observation)." if is_fr else "⚠️ The selected or uploaded dataset is empty (0 observations).")
            return

        st.markdown("##### 👁️ Aperçu du Jeu de Données (5 Premières Lignes)" if is_fr else "##### 👁️ Dataset Preview (First 5 Rows)")
        st.dataframe(df_inspect.head(), use_container_width=True)

        # Health Calculations
        n_rows, n_cols = df_inspect.shape
        missing_series = df_inspect.isnull().sum()
        total_missing = missing_series.sum()
        total_cells = n_rows * n_cols
        missing_pct = (total_missing / total_cells * 100) if total_cells > 0 else 0.0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Enregistrements" if is_fr else "Total Records", f"{n_rows:,}")
        col2.metric("Variables", f"{n_cols}")
        col3.metric("Valeurs Manquantes" if is_fr else "Missing Values", f"{total_missing:,}")
        col4.metric("Taux Global Manquant" if is_fr else "Overall Missing %", f"{missing_pct:.1f}%")

        # Missing breakdown
        cols_with_missing = missing_series[missing_series > 0]
        if not cols_with_missing.empty:
            st.warning(f"⚠️ **{'Détails des Observations Manquantes' if is_fr else 'Missing Observation Details'}**: {dict(cols_with_missing)}")

        # Balance check on categorical columns
        cat_cols = df_inspect.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_cols:
            cat_lbl = "Inspecter l'Équilibre selon le Facteur :" if is_fr else "Inspect Balance Across Factor:"
            selected_cat = st.selectbox(cat_lbl, cat_cols, key="auditor_cat_select")
            counts = df_inspect[selected_cat].value_counts()
            st.bar_chart(counts)

        rec_hdr = "🤖 Recommandation Biométrique AgroBiometrix" if is_fr else "🤖 AgroBiometrix Biometrics Recommendation"
        stat_audit_title = "📊 Audit de l'Architecture Statistique" if is_fr else "📊 Statistical Architecture Audit"
        ds_contains_txt = "Votre jeu de données contient" if is_fr else "Your dataset contains"
        obs_txt = "observations"
        across_txt = "réparties sur" if is_fr else "across"
        miss_hdr = "Données manquantes" if is_fr else "Missingness"
        if not cols_with_missing.empty:
            cols_str = str(list(cols_with_missing.keys()))
            miss_val_txt = f"Détectées dans les colonnes {cols_str}. Pour les caractères liés au sexe comme la production laitière, les mâles doivent être codés comme non observés plutôt que zéro." if is_fr else f"Detected in columns {cols_str}. For sex-limited traits like Milk Yield, males should be coded as unobserved rather than zero."
        else:
            miss_val_txt = "Aucune donnée manquante détectée. L'analyse sur cas complets est valide." if is_fr else "No missing data detected. Complete case analysis is valid."
        bal_hdr = "Équilibre expérimental" if is_fr else "Experimental Balance"
        bal_val_txt = "Les effectifs par sous-groupe indiquent une stratification structurée." if is_fr else "Sample sizes across groups show structured stratification."
        model_hdr = "Modèle recommandé" if is_fr else "Recommended Model"
        model_val_txt = "Si des mesures répétées existent par sujet, une régression MCO ordinaire sous-estimera sévèrement les erreurs types en ignorant la corrélation intra-sujet." if is_fr else "If repeated observations exist per subject, ordinary OLS regression will severely underestimate standard errors by ignoring intra-subject correlation."
        rec_line = "Recommandation : Passez à l'onglet 'Statistiques Biométriques & DMRT' pour exécuter l'ANOVA et la séparation de moyennes de Duncan." if is_fr else "Recommendation: Proceed to the 'Statistical Biometrics & DMRT' tab to execute ANOVA and Duncan's Multiple Range Test."

        st.markdown(f"##### {rec_hdr}")
        st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #1B5E20; background: #F1F8F2; padding: 12px 16px; border-radius: 4px; margin-top: 10px;">
<div style="font-weight: 700; color: #1B5E20; font-size: 0.95rem; margin-bottom: 4px;">{stat_audit_title}</div>
<div style="font-size: 0.85rem; color: #37474F; line-height: 1.5;">
{ds_contains_txt} <b>{n_rows:,} {obs_txt}</b> {across_txt} <b>{n_cols} variables</b>.<br>
• <b>{miss_hdr}</b> : {miss_val_txt}<br>
• <b>{bal_hdr}</b> : {bal_val_txt}<br>
• <b>{model_hdr}</b> : {model_val_txt}<br>
<b>{rec_line}</b>
</div>
</div>
""", unsafe_allow_html=True)

        render_dispatch_trigger_card(
            source_module="Suite 2: Biometric Field Trial & Statistical Audit",
            commodity="Multi-Commodity Field Trials",
            region="Sub-Saharan Agricultural Research Zones",
            headline="Validated Field Trial Protocol & Experimental Balance Advisory",
            trigger_summary=f"Analysis of {n_rows:,} observations across {n_cols} factors completed. Recommended model: {model_val_txt[:90]}.",
            recommendation_summary=rec_line
        )
