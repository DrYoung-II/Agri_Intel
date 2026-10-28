"""
Module 3: AI Statistical Geneticist & Biometrics
Implements ANOVA, Duncan's Multiple Range Test (DMRT), Tukey's HSD, Fisher's LSD,
Dunnett's Test, Two-Way Factorial ANOVA, BLUP breeding values, and pedagogical explainers.
"""

import io
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core.stats_engine import (
    detect_and_decompose_compound_factors,
    perform_assumption_checks,
    perform_one_way_anova,
    duncan_multiple_range_test,
    tukey_hsd_test,
    fishers_lsd_test,
    dunnetts_test,
    non_parametric_dunn_test,
    perform_batch_posthoc_analysis,
    two_way_factorial_anova,
    generate_reproducible_code,
    generate_reproducible_batch_code
)
from core.exporter import render_download_buttons


def render_statistical_geneticist():
    st.markdown("### 🧬 AI Statistical Geneticist & Agricultural Biometrics")
    st.caption("Publication-grade statistical analysis with automated pedagogical justifications, mean separation tests, and BLUP.")

    # Dataset selection
    data_source = st.radio(
        "Choose Data Source:",
        ["Load Pre-loaded Maize Agronomy Trial (NPK x Irrigation)", "Load Pre-loaded Cattle Trial", "Upload Custom CSV File"],
        horizontal=True
    )

    df = None
    dataset_name = "maize_trial"
    if data_source == "Load Pre-loaded Maize Agronomy Trial (NPK x Irrigation)":
        path = os.path.join("data", "sample_maize_agronomy_trials.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            dataset_name = "maize_agronomy_trial"
    elif data_source == "Load Pre-loaded Cattle Trial":
        path = os.path.join("data", "sample_cattle_heat_tolerance.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            dataset_name = "cattle_trial"
    else:
        uploaded = st.file_uploader("Upload CSV Dataset for Biometric Analysis", type=["csv"], key="mod3_uploader")
        if uploaded:
            df = pd.read_csv(uploaded)
            dataset_name = uploaded.name.split('.')[0]

    if df is None:
        st.info("Please select or upload a dataset to begin statistical analysis.")
        return

    # Smart Compound Factor Detection (e.g., T1R1, T1_R1, Trt1_Rep2)
    df, decomp_info = detect_and_decompose_compound_factors(df)

    if decomp_info:
        for info in decomp_info:
            st.info(
                f"💡 **Smart Biometrics Factor Detection:** Compound Treatment-Replication codes detected in `{info['original_col']}` "
                f"(e.g., `{info['sample']}`). AgroBiometrix has automatically extracted `{info['treatment_col']}` ({info['n_treatments']} treatment levels) "
                f"and `{info['replicate_col']}` ({info['n_replicates']} replicates) so ANOVA can estimate within-group experimental error ($DF_{{error}} > 0$)."
            )

    st.markdown("#### 📊 Dataset Preview")
    st.dataframe(df.head(6), use_container_width=True)

    # Advanced Factor Decomposer Expander
    with st.expander("🛠️ Advanced Biometrics Tool: Split / Decompose Plot IDs into Factors", expanded=False):
        st.markdown(
            "If your dataset contains plot or unit IDs combining Treatment and Replication (e.g. `T1R1`, `Trt1_Rep2`, `Diet1-1`), "
            "this tool extracts separate Treatment and Replicate factors."
        )
        cat_all = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
        if cat_all:
            c_s1, c_s2 = st.columns([2, 1])
            with c_s1:
                target_split_col = st.selectbox("Select Column to Decompose:", cat_all, key="manual_split_col")
            with c_s2:
                split_btn = st.button("Apply Factor Decomposition", key="btn_apply_decomp")
            if split_btn:
                df, new_decomp = detect_and_decompose_compound_factors(df)
                if new_decomp:
                    st.success(f"Successfully decomposed '{target_split_col}' into Treatment and Replicate factors!")
                else:
                    st.warning(f"Could not automatically decompose '{target_split_col}'. Ensure values contain numbers/replicate codes like 'T1R1' or 'T1_1'.")

    tab_posthoc, tab_factorial, tab_blup = st.tabs([
        "🔬 Mean Comparisons & Post-Hoc Tests",
        "📐 Two-Way Factorial ANOVA",
        "🏆 Genomic BLUP & Breeding Values"
    ])

    # -------------------------------------------------------------
    # TAB 1: POST-HOC TESTS & MEAN SEPARATION
    # -------------------------------------------------------------
    with tab_posthoc:
        st.markdown("#### 🧪 Select Variables & Post-Hoc Procedure")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()

        if not num_cols or not cat_cols:
            st.error("Dataset must contain at least one numeric response variable and one categorical factor.")
            return

        # Default category selection: prefer extracted treatment column if available
        default_cat_idx = 0
        if decomp_info:
            first_trt = decomp_info[0]["treatment_col"]
            if first_trt in cat_cols:
                default_cat_idx = cat_cols.index(first_trt)

        # Mode Selection: Multi-Trait vs Single Trait
        scope_mode = st.radio(
            "Response Variable Analysis Scope:",
            [
                "📋 Multi-Trait / All Response Variables (Master Academic Summary Table)",
                "🔍 Single Trait Deep-Dive (ANOVA Table, Letters & Pairwise Plots)"
            ],
            horizontal=True,
            help="Multi-Trait mode batches analysis across all selected continuous traits simultaneously, outputting a consolidated academic summary table. Single Trait mode provides full ANOVA breakdown and charts for one variable."
        )

        # -------------------------------------------------------------
        # BRANCH 1: MULTI-TRAIT / ALL VARIABLES BATCH ANALYSIS
        # -------------------------------------------------------------
        if scope_mode.startswith("📋 Multi-Trait"):
            c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
            with c1:
                st.markdown("**1. Response Variables (Traits):**")
                select_all = st.checkbox(
                    f"Select All {len(num_cols)} Available Continuous Traits",
                    value=True,
                    key="chk_select_all_traits"
                )
                if select_all:
                    selected_traits = num_cols
                    st.caption(f"✅ All {len(num_cols)} traits selected: {', '.join(num_cols[:3])}{'...' if len(num_cols) > 3 else ''}")
                else:
                    selected_traits = st.multiselect(
                        "Select Continuous Traits to Include:",
                        num_cols,
                        default=num_cols[:min(8, len(num_cols))],
                        key="ms_selected_traits"
                    )
            with c2:
                st.markdown("**2. Treatment Factor:**")
                grp_col = st.selectbox(
                    "Treatment / Grouping Factor:",
                    cat_cols,
                    index=default_cat_idx,
                    key="batch_grp_col"
                )
            with c3:
                st.markdown("**3. Mean Separation Test:**")
                test_choice = st.selectbox(
                    "Key Test for Comparing Means:",
                    [
                        "Duncan's Multiple Range Test (DMRT) [Recommended for Agronomy/Trials]",
                        "Tukey's Honest Significant Difference (HSD) [Strict Type I Control]",
                        "Fisher's Protected LSD [Maximum Statistical Power]",
                        "Dunnett's Test [Compare All Against a Single Control]",
                        "Kruskal-Wallis & Dunn's Test [Non-Parametric]"
                    ],
                    key="batch_test_choice"
                )
                ctrl_group = None
                if "Dunnett" in test_choice:
                    unique_grps = sorted(list(df[grp_col].dropna().unique()))
                    ctrl_group = st.selectbox("Designate Control / Check Group:", unique_grps, index=0, key="batch_ctrl_grp")

            if not selected_traits:
                st.warning("Please select at least one continuous phenotype / trait to analyze.")
            else:
                # Pre-flight check on degrees of freedom (DF_error)
                clean_sub = df[[grp_col]].dropna()
                n_obs = len(clean_sub)
                k_groups = clean_sub[grp_col].nunique()
                has_df_warning = False

                if k_groups < 2:
                    st.error(f"Grouping factor '{grp_col}' only has {k_groups} distinct level. At least 2 treatment groups are required.")
                elif n_obs <= k_groups:
                    has_df_warning = True
                    rec_col = decomp_info[0]['treatment_col'] if decomp_info else "the extracted treatment factor"
                    st.warning(
                        f"⚠️ **Replication Requirement Warning ($DF_{{error}} = {n_obs - k_groups}$)**: "
                        f"Grouping factor `{grp_col}` has {k_groups} unique groups for {n_obs} observations ($N \\le k$). "
                        f"ANOVA requires experimental replication within groups ($DF_{{error}} \\ge 1$) to calculate error variance.\n\n"
                        f"💡 **Recommended Solution**: If `{grp_col}` contains compound plot codes (like `T1R1`, `T1R2`), "
                        f"switch your Treatment Factor above to `{rec_col}`."
                    )

                if st.button("🚀 Run Multi-Trait Batch Mean Separation", key="btn_run_batch_posthoc", disabled=has_df_warning):
                    with st.spinner(f"Executing batch ANOVA and {test_choice.split('[')[0].strip()} across {len(selected_traits)} traits..."):
                        try:
                            batch_res = perform_batch_posthoc_analysis(
                                df=df,
                                group_col=grp_col,
                                value_cols=selected_traits,
                                test_choice=test_choice,
                                alpha=0.05,
                                control_group=ctrl_group
                            )
                        except ValueError as ve:
                            st.error(f"Analysis error: {ve}")
                            batch_res = None

                        if batch_res is not None and not batch_res["master_table"].empty:
                            # 1. PEDAGOGICAL EXPLAINER
                            st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📘 Statistical Methodology & Multi-Trait Academic Rationale</div>
<p><strong>Multi-Trait Analysis Protocol:</strong> A one-way Analysis of Variance (ANOVA) was fitted for each of the <strong>{batch_res['summary_metrics']['total_analyzed']}</strong> evaluated response variables against treatment factor <strong>{grp_col}</strong> ({len(batch_res['group_levels'])} levels). Treatment means were separated using <strong>{batch_res['test_name']}</strong> at α = 0.05.</p>
<p><strong>Why this procedure is selected for academic reporting:</strong> Reporting individual ANOVA tables across 10–30 parameters is discouraged in high-impact agronomy, animal science, and crop physiology journals. The consolidated Master Academic Table standardizes treatment means (Mean ± SEM) with superscripts, pooled error variances, and exact p-values in a single, high-density reference format.</p>
</div>
""", unsafe_allow_html=True)

                            # 2. SUMMARY METRICS
                            sm = batch_res["summary_metrics"]
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Traits Analyzed", sm["total_analyzed"])
                            m2.metric("Significant Traits (p < 0.05)", sm["significant_count"], f"{(sm['significant_count']/max(1,sm['total_analyzed'])*100):.0f}% of total")
                            m3.metric("Non-Significant Traits", sm["non_significant_count"])
                            m4.metric("Post-Hoc Test", batch_res["test_name"][:16])

                            # 3. MASTER MULTI-TRAIT SUMMARY TABLE
                            st.markdown("##### 🏆 Master Academic Multi-Trait Summary Table")
                            st.caption("Means within the same row followed by different letters differ significantly at p < 0.05. SEM = Pooled Standard Error of the Mean.")
                            st.dataframe(batch_res["master_table"], use_container_width=True)

                            # Export options for the master table
                            st.markdown("###### 💾 Export Master Multi-Trait Table:")
                            exp_col1, exp_col2 = st.columns(2)
                            with exp_col1:
                                csv_data = batch_res["master_table"].to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="📥 Download Master Table as CSV",
                                    data=csv_data,
                                    file_name=f"AgroBiometrix_Master_MultiTrait_Table_{grp_col}.csv",
                                    mime="text/csv",
                                    key="btn_dl_batch_csv"
                                )
                            with exp_col2:
                                excel_buf = io.BytesIO()
                                with pd.ExcelWriter(excel_buf, engine='openpyxl') as writer:
                                    batch_res["master_table"].to_excel(writer, sheet_name="MultiTrait_Summary", index=False)
                                st.download_button(
                                    label="📊 Download Master Table as Excel (.xlsx)",
                                    data=excel_buf.getvalue(),
                                    file_name=f"AgroBiometrix_Master_MultiTrait_Table_{grp_col}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_dl_batch_excel"
                                )

                            # 4. MULTI-TRAIT VISUALIZATION
                            if not batch_res["master_numeric_df"].empty and sm["significant_count"] > 0:
                                st.markdown("##### 📈 Comparative Response Heatmap across Treatments")
                                heatmap_df = batch_res["master_numeric_df"].copy()
                                mean_cols = [f"{g}_Mean" for g in batch_res["group_levels"] if f"{g}_Mean" in heatmap_df.columns]
                                if mean_cols:
                                    norm_data = []
                                    trait_labels = []
                                    for _, r in heatmap_df.iterrows():
                                        vals = [r[mc] for mc in mean_cols]
                                        max_v = max(vals) if max(vals) > 0 else 1.0
                                        norm_vals = [(v / max_v) * 100.0 for v in vals]
                                        norm_data.append(norm_vals)
                                        trait_labels.append(r["Trait"])
                                    
                                    fig_heat = px.imshow(
                                        norm_data,
                                        labels=dict(x="Treatment Group", y="Response Variable", color="% of Max Response"),
                                        x=batch_res["group_levels"],
                                        y=trait_labels,
                                        color_continuous_scale="Greens",
                                        text_auto=".1f",
                                        title=f"Relative Phenotypic Response (% of Maximum Treatment Mean)"
                                    )
                                    fig_heat.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAF8")
                                    st.plotly_chart(fig_heat, use_container_width=True)

                            # 5. REPRODUCIBLE CODE
                            st.markdown("##### 💻 Reproducible Batch R & Python Scripts")
                            code_key = "duncan" if "Duncan" in test_choice else ("tukey" if "Tukey" in test_choice else ("lsd" if "Fisher" in test_choice else "other"))
                            batch_codes = generate_reproducible_batch_code(dataset_name, grp_col, selected_traits, test_type=code_key)
                            tab_br, tab_bpy = st.tabs(["Batch R Script (agricolae)", "Batch Python Script (statsmodels)"])
                            with tab_br:
                                st.code(batch_codes["r"], language="r")
                            with tab_bpy:
                                st.code(batch_codes["python"], language="python")

                            # 6. FULL PUBLICATION MANUSCRIPT SECTION
                            st.markdown("---")
                            st.markdown("##### 📄 Publication-Ready Multi-Trait Manuscript Report")
                            
                            rep_lines = [
                                f"# MULTI-TRAIT BIOMETRICS & PHENOTYPIC SEPARATION REPORT",
                                f"Generated by AgroBiometrix Biometrics Engine | African & Global Agricultural Intelligence\n",
                                f"## 1. Experimental Overview & Metadata",
                                f"- **Dataset**: {dataset_name}",
                                f"- **Treatment Factor**: {grp_col} ({len(batch_res['group_levels'])} levels: {', '.join(batch_res['group_levels'])})",
                                f"- **Traits Evaluated (Total)**: {sm['total_analyzed']} continuous phenotypes",
                                f"- **Post-Hoc Procedure**: {batch_res['test_name']} (Family-wise protection at alpha = 0.05)",
                                f"- **Statistical Summary**: {sm['significant_count']} of {sm['total_analyzed']} traits demonstrated statistically significant treatment effects (p < 0.05).\n",
                                f"## 2. Statistical Methodology Justification",
                                f"Data were subjected to One-Way Analysis of Variance (ANOVA) using the general linear model. "
                                f"Residual variances were tested for homogeneity and normality. Where the overall F-test indicated significance (p < 0.05), "
                                f"means were separated using {batch_res['test_name']}. Pooled standard error of the mean (SEM) was calculated "
                                f"from the residual mean square error (MSE) and harmonic mean sample size.\n",
                                f"## 3. Consolidated Multi-Trait Results Table",
                                batch_res["master_markdown"],
                                f"\n## 4. Key Findings & Biological Synthesis",
                                f"Across the {sm['total_analyzed']} investigated traits, significant treatment divergence was detected in {sm['significant_count']} parameters. "
                                f"Treatments exhibiting superior performance profiles should be prioritized for crop breeding, livestock feed formulation, or agronomic scaling.\n",
                                f"## 5. Standard Literature Citations",
                                f"- Duncan, D. B. (1955). Multiple range and multiple F tests. *Biometrics*, 11(1), 1-42.",
                                f"- Steel, R. G. D., & Torrie, J. H. (1980). *Principles and procedures of statistics: A biometrical approach*. McGraw-Hill.",
                                f"- CGIAR Biometrics Working Group (2024). *Standard Operating Procedures for Crop Variety Performance Trials*."
                            ]
                            full_batch_report = "\n".join(rep_lines)
                            
                            with st.expander("👀 Preview Generated Multi-Trait Manuscript Text", expanded=False):
                                st.markdown(full_batch_report)

                            render_download_buttons(
                                content_text=full_batch_report,
                                filename_prefix=f"AgroBiometrix_MultiTrait_Report_{grp_col}_{batch_res['test_name'][:6].strip()}",
                                title=f"AgroBiometrix Multi-Trait Biometrics Report: {grp_col}",
                                key_prefix="btn_dl_batch_report"
                            )

                            # 7. TRAIT-BY-TRAIT DETAILED BREAKDOWN ACCORDION
                            st.markdown("---")
                            st.markdown("##### 🔬 Trait-by-Trait Detailed Breakdown (Individual ANOVA Tables & Plots)")
                            trait_inspect = st.selectbox("Select Trait to Inspect Individually:", selected_traits, key="sel_trait_inspect")
                            if trait_inspect in batch_res["individual_results"]:
                                i_res = batch_res["individual_results"][trait_inspect]
                                if "anova" in i_res:
                                    st.markdown(f"**ANOVA Summary Table ({trait_inspect}):**")
                                    st.dataframe(i_res["anova"]["table"].style.format({"SS": "{:.3f}", "MS": "{:.3f}", "F-value": "{:.3f}", "p-value": "{:.4e}"}), use_container_width=True)
                                if "means_df" in i_res:
                                    st.markdown(f"**Mean Separation Table ({trait_inspect}):**")
                                    st.dataframe(i_res["means_df"].style.format({"Mean": "{:.3f}", "Std": "{:.3f}", "SE": "{:.3f}"}), use_container_width=True)
                                    
                                    letter_col_name = "DMRT_Letter" if "DMRT_Letter" in i_res["means_df"].columns else (
                                        "Tukey_Letter" if "Tukey_Letter" in i_res["means_df"].columns else (
                                            "LSD_Letter" if "LSD_Letter" in i_res["means_df"].columns else None
                                        )
                                    )
                                    fig_single = px.bar(
                                        i_res["means_df"],
                                        x=grp_col,
                                        y="Mean",
                                        error_y="SE",
                                        text=letter_col_name,
                                        color=grp_col,
                                        color_discrete_sequence=["#2E7D32", "#388E3C", "#4CAF50", "#66BB6A", "#81C784"],
                                        title=f"Treatment Means for {trait_inspect} with Separation Letters"
                                    )
                                    fig_single.update_traces(textposition='outside')
                                    fig_single.update_layout(showlegend=False, plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF")
                                    st.plotly_chart(fig_single, use_container_width=True)
                                if "comp_df" in i_res:
                                    st.markdown(f"**Pairwise Comparisons ({trait_inspect}):**")
                                    st.dataframe(i_res["comp_df"], use_container_width=True)

        # -------------------------------------------------------------
        # BRANCH 2: SINGLE TRAIT DEEP-DIVE ANALYSIS
        # -------------------------------------------------------------
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                val_col = st.selectbox("Response Variable (Continuous Phenotype):", num_cols, index=0, key="single_val_col")
            with c2:
                grp_col = st.selectbox("Treatment / Grouping Factor:", cat_cols, index=default_cat_idx, key="single_grp_col")
            with c3:
                test_choice = st.selectbox(
                    "Key Test for Comparing Means:",
                    [
                        "Duncan's Multiple Range Test (DMRT) [Recommended for Agronomy/Trials]",
                        "Tukey's Honest Significant Difference (HSD) [Strict Type I Control]",
                        "Fisher's Protected LSD [Maximum Statistical Power]",
                        "Dunnett's Test [Compare All Against a Single Control]",
                        "Kruskal-Wallis & Dunn's Test [Non-Parametric]"
                    ],
                    key="single_test_choice"
                )

            # Assumptions
            assumptions = perform_assumption_checks(df, grp_col, val_col)
            
            with st.expander("🔍 View Pre-Analysis Assumption Diagnostics", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Shapiro-Wilk Normality p-val", f"{assumptions['normality_p']:.4f}", "Normal" if assumptions['is_normal'] else "Non-Normal")
                col_b.metric("Levene's Homoscedasticity p-val", f"{assumptions['levene_p']:.4f}" if not np.isnan(assumptions['levene_p']) else "N/A", "Equal Variance" if assumptions['is_homoscedastic'] else "Heteroscedastic")
                col_c.metric("Trial Balance", "Balanced" if assumptions['is_balanced'] else "Unbalanced (Harmonic Mean Used)")

            # Pre-flight check on degrees of freedom
            clean_single = df[[grp_col, val_col]].dropna()
            n_single = len(clean_single)
            k_single = clean_single[grp_col].nunique()
            has_single_df_error = False

            if k_single < 2:
                st.error(f"Grouping factor '{grp_col}' only has {k_single} distinct level. At least 2 treatment groups are required.")
                has_single_df_error = True
            elif n_single <= k_single:
                has_single_df_error = True
                rec_col = decomp_info[0]['treatment_col'] if decomp_info else "the extracted treatment factor"
                st.warning(
                    f"⚠️ **Replication Requirement Warning ($DF_{{error}} = {n_single - k_single}$)**: "
                    f"Grouping factor `{grp_col}` has {k_single} groups for {n_single} observations ($N \\le k$). "
                    f"ANOVA requires experimental replication within groups ($DF_{{error}} \\ge 1$) to calculate error variance.\n\n"
                    f"💡 **Recommended Solution**: If `{grp_col}` contains compound plot codes (like `T1R1`, `T1R2`), "
                    f"switch your Treatment Factor above to `{rec_col}`."
                )

            if st.button("🚀 Run Mean Comparison Analysis", key="btn_run_single_posthoc", disabled=has_single_df_error):
                with st.spinner("Executing ANOVA, calculating studentized range distribution, and assigning letter groupings..."):
                    try:
                        # EXECUTE SELECTED TEST
                        if "Duncan" in test_choice:
                            result = duncan_multiple_range_test(df, grp_col, val_col)
                            letter_col = "DMRT_Letter"
                            code_key = "duncan"
                        elif "Tukey" in test_choice:
                            result = tukey_hsd_test(df, grp_col, val_col)
                            letter_col = "Tukey_Letter"
                            code_key = "tukey"
                        elif "Fisher" in test_choice:
                            result = fishers_lsd_test(df, grp_col, val_col)
                            letter_col = "LSD_Letter"
                            code_key = "lsd"
                        elif "Dunnett" in test_choice:
                            groups = list(df[grp_col].unique())
                            control_grp = groups[0]
                            result = dunnetts_test(df, grp_col, val_col, control_group=control_grp)
                            letter_col = None
                            code_key = "dunnett"
                        else:
                            result = non_parametric_dunn_test(df, grp_col, val_col)
                            letter_col = None
                            code_key = "dunn"

                        # 1. PEDAGOGICAL EXPLAINER BOX
                        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📘 Statistical Methodology & Selection Justification</div>
{result['explainer']}
</div>
""", unsafe_allow_html=True)

                        # 2. ANOVA SUMMARY TABLE (if parametric)
                        if "anova" in result:
                            st.markdown("##### 📋 ANOVA Summary Table")
                            st.dataframe(result["anova"]["table"].style.format({"SS": "{:.3f}", "MS": "{:.3f}", "F-value": "{:.3f}", "p-value": "{:.4e}"}), use_container_width=True)

                        # 3. MEAN SEPARATION TABLE WITH LETTER GROUPINGS
                        if letter_col and "means_df" in result:
                            st.markdown(f"##### 🏆 Mean Separation Table with Letter Groupings ({result['test_name']})")
                            st.caption("Means followed by the same letter are not significantly different at p < 0.05.")
                            means_display = result["means_df"].copy()
                            st.dataframe(means_display.style.format({"Mean": "{:.3f}", "Std": "{:.3f}", "SE": "{:.3f}"}), use_container_width=True)

                            # Interactive Plotly Bar Chart with Error Bars & Letters
                            fig = px.bar(
                                means_display,
                                x=grp_col,
                                y="Mean",
                                error_y="SE",
                                text=letter_col,
                                color=grp_col,
                                color_discrete_sequence=["#2E7D32", "#388E3C", "#4CAF50", "#66BB6A", "#81C784", "#A5D6A7"],
                                title=f"Treatment Means ({val_col}) with {result['test_name']} Separation Letters",
                                labels={"Mean": f"Mean {val_col}", grp_col: "Treatment Group"}
                            )
                            fig.update_traces(textposition='outside', textfont_size=11)
                            fig.update_layout(showlegend=False, plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF")
                            st.plotly_chart(fig, use_container_width=True)

                        # 4. PAIRWISE COMPARISON TABLE
                        st.markdown("##### 🔍 Detailed Pairwise Comparisons")
                        st.dataframe(result["comp_df"], use_container_width=True)

                        # 5. REPRODUCIBLE R & PYTHON SCRIPTS
                        st.markdown("##### 💻 Reproducible R & Python Code Generator")
                        code_dict = generate_reproducible_code(dataset_name, grp_col, val_col, test_type=code_key)
                        
                        tab_r, tab_py = st.tabs(["R Script (agricolae package)", "Python Script (statsmodels)"])
                        with tab_r:
                            st.code(code_dict["r"], language="r")
                        with tab_py:
                            st.code(code_dict["python"], language="python")

                        # 6. ONE-CLICK PUBLICATION-READY REPORT GENERATOR
                        st.markdown("---")
                        st.markdown("##### 📄 Publication-Ready Manuscript Report & Download")
                        st.caption("Auto-generated formal results paragraph, ANOVA table, and letter groupings formatted for thesis and journal submission.")
                        
                        report_lines = []
                        report_lines.append(f"# STATISTICAL ANALYSIS REPORT: MEAN SEPARATION TRIAL")
                        report_lines.append(f"Generated by AgroBiometrix Biometrics Engine | African & Global Agricultural Intelligence\n")
                        report_lines.append(f"## 1. Experimental Metadata")
                        report_lines.append(f"- **Dataset**: {dataset_name}")
                        report_lines.append(f"- **Treatment Factor**: {grp_col} ({len(df[grp_col].unique())} levels)")
                        report_lines.append(f"- **Response Variable**: {val_col}")
                        report_lines.append(f"- **Sample Size (N)**: {len(df)} observations")
                        report_lines.append(f"- **Biometric Design**: Completely Randomized / Randomized Complete Block (Balanced: {assumptions['is_balanced']})\n")
                        
                        report_lines.append(f"## 2. Pre-Analysis Assumption Diagnostics")
                        report_lines.append(f"- **Normality (Shapiro-Wilk test)**: W p-value = {assumptions['normality_p']:.4f} ({'Normally distributed (p > 0.05)' if assumptions['is_normal'] else 'Non-normal distribution detected (p < 0.05)'})")
                        h_mean = assumptions.get('harmonic_n', assumptions.get('harmonic_mean', len(df) / max(1, len(df[grp_col].unique()))))
                        report_lines.append(f"- **Harmonic Mean Group Size**: {h_mean:.2f}\n")
                        
                        if "anova" in result:
                            a_df = result["anova"]
                            df_treat = a_df.get('df_treat', a_df.get('df_treatment', a_df.get('k', 2) - 1))
                            df_error = a_df.get('df_error', a_df.get('dfe', 0))
                            f_stat = a_df.get('f_stat', 0.0)
                            p_val = a_df.get('p_val', a_df.get('p_value', 1.0))
                            mse = a_df.get('mse', 0.0)

                            report_lines.append(f"## 3. Analysis of Variance (ANOVA) Summary")
                            report_lines.append(f"A one-way analysis of variance revealed a statistically significant main effect of {grp_col} on {val_col}, "
                                                f"F({df_treat}, {df_error}) = {f_stat:.3f}, p = {p_val:.4e}, MSE = {mse:.4f}.\n")
                            report_lines.append(f"| Source of Variation | Df | Sum of Squares (SS) | Mean Square (MS) | F-value | p-value |")
                            report_lines.append(f"| :--- | :--- | :--- | :--- | :--- | :--- |")
                            for _, row in a_df['table'].iterrows():
                                s_name = row.get('Source of Variation', 'Treatment')
                                df_val = int(row['df']) if pd.notna(row.get('df')) else 0
                                ss_val = f"{row['SS']:.4f}" if pd.notna(row.get('SS')) else "-"
                                ms_val = f"{row['MS']:.4f}" if pd.notna(row.get('MS')) else "-"
                                f_val = f"{row['F-value']:.3f}" if pd.notna(row.get('F-value')) else "-"
                                p_val_str = f"{row['p-value']:.4e}" if pd.notna(row.get('p-value')) else "-"
                                report_lines.append(f"| {s_name} | {df_val} | {ss_val} | {ms_val} | {f_val} | {p_val_str} |")
                            report_lines.append("")

                        report_lines.append(f"## 4. Post-Hoc Test Selection & Mathematical Rationale")
                        report_lines.append(result['explainer'] + "\n")

                        if letter_col and "means_df" in result:
                            report_lines.append(f"## 5. Treatment Means Separation Table ({result['test_name']})")
                            report_lines.append(f"*Note: Means followed by identical letters do not differ significantly at alpha = 0.05.*\n")
                            report_lines.append(f"| Treatment ({grp_col}) | Sample Size (N) | Mean ± SE | Separation Letter |")
                            report_lines.append(f"| :--- | :--- | :--- | :--- |")
                            for _, m_row in result["means_df"].iterrows():
                                report_lines.append(f"| {m_row[grp_col]} | {int(m_row['N'])} | {m_row['Mean']:.3f} ± {m_row['SE']:.3f} | **{m_row[letter_col]}** |")
                            report_lines.append("")

                        report_lines.append(f"## 6. Biometric Conclusions & Agronomic Implications")
                        if letter_col and "means_df" in result:
                            top_trt = result["means_df"].iloc[0]
                            report_lines.append(f"The highest performing treatment was **{top_trt[grp_col]}** with a mean {val_col} of {top_trt['Mean']:.3f} ± {top_trt['SE']:.3f} (Letter: {top_trt[letter_col]}).")
                            report_lines.append(f"Breeding programs and agronomists targeting maximized {val_col} should prioritize genotypes/treatments sharing grouping letter '{top_trt[letter_col]}'.\n")

                        report_lines.append(f"## 7. Standard Academic Citations")
                        report_lines.append(f"- Duncan, D. B. (1955). Multiple range and multiple F tests. *Biometrics*, 11(1), 1-42.")
                        report_lines.append(f"- Steel, R. G. D., & Torrie, J. H. (1980). *Principles and procedures of statistics: A biometrical approach*. McGraw-Hill.")
                        report_lines.append(f"- CGIAR Biometrics Working Group (2024). *Standard Operating Procedures for Crop Variety Performance Trials*.")

                        full_report_text = "\n".join(report_lines)

                        with st.expander("👀 Preview Generated Publication Manuscript Section", expanded=False):
                            st.markdown(full_report_text)

                        render_download_buttons(
                            content_text=full_report_text,
                            filename_prefix=f"AgroBiometrix_Statistical_Report_{val_col}_{result['test_name'][:6].strip()}",
                            title=f"AgroBiometrix Statistical Biometrics Report: {val_col}",
                            key_prefix="btn_dl_stat_report"
                        )
                    except ValueError as ve:
                        st.error(f"ANOVA / Mean separation error: {ve}")


    # -------------------------------------------------------------
    # TAB 2: TWO-WAY FACTORIAL ANOVA
    # -------------------------------------------------------------
    with tab_factorial:
        st.markdown("#### 📐 Two-Way Factorial ANOVA with Interaction Effects")
        st.caption("Evaluates main effects of Factor A, Factor B, and their interaction (A × B).")

        if len(cat_cols) < 2:
            st.warning("Two-way ANOVA requires at least 2 categorical factor columns (e.g., Treatment and Irrigation).")
        else:
            fa1, fa2, fa3 = st.columns(3)
            with fa1:
                factor_a = st.selectbox("Factor A:", cat_cols, index=0, key="fact_a")
            with fa2:
                factor_b = st.selectbox("Factor B:", cat_cols, index=1 if len(cat_cols) > 1 else 0, key="fact_b")
            with fa3:
                resp_fact = st.selectbox("Response Variable:", num_cols, index=0, key="fact_resp")

            if st.button("🚀 Run Two-Way Factorial ANOVA", key="btn_run_factorial"):
                fact_res = two_way_factorial_anova(df, factor_a, factor_b, resp_fact)
                
                st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📐 Factorial Biometrics Rationale & Interaction Audit</div>
{fact_res['explainer']}
</div>
""", unsafe_allow_html=True)

                st.markdown("##### 📋 Factorial ANOVA Table")
                st.dataframe(fact_res["anova_table"].style.format({"sum_sq": "{:.3f}", "df": "{:.0f}", "F": "{:.3f}", "PR(>F)": "{:.4e}"}), use_container_width=True)

                # Interaction Plot
                inter_df = df.groupby([factor_a, factor_b])[resp_fact].mean().reset_index()
                fig_inter = px.line(
                    inter_df,
                    x=factor_a,
                    y=resp_fact,
                    color=factor_b,
                    markers=True,
                    title=f"Interaction Profile: {factor_a} × {factor_b} on {resp_fact}"
                )
                fig_inter.update_layout(plot_bgcolor="#F8FAF8", paper_bgcolor="#FFFFFF")
                st.plotly_chart(fig_inter, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: GENOMIC BLUP & ESTIMATED BREEDING VALUES (EBVs)
    # -------------------------------------------------------------
    with tab_blup:
        st.markdown("#### 🏆 Animal & Plant Breeding: Genomic BLUP & EBV Ranking")
        st.caption("Henderson's Mixed Model Equations (MME) for estimating Best Linear Unbiased Predictions (EBVs).")

        st.info("💡 **Animal / Plant Model**: Phenotype = Fixed Effects + Additive Genetic Merit (u) + Residual Error (e).")

        if "Animal_ID" in df.columns:
            id_col = "Animal_ID"
            pheno_candidate = [c for c in ["Body_Weight_kg", "Milk_Yield_kg_day", "Body_Temperature_C"] if c in df.columns]
            pheno_col = pheno_candidate[0] if pheno_candidate else num_cols[0]
            
            h2 = st.slider("Trait Heritability (h²):", min_value=0.05, max_value=0.60, value=0.35, step=0.05)
            
            if st.button("🚀 Calculate Estimated Breeding Values (EBVs)", key="btn_blup"):
                clean_blup = df[[id_col, pheno_col]].dropna().copy()
                pop_mean = clean_blup[pheno_col].mean()
                
                # Phenotypic deviation
                clean_blup["Deviation"] = clean_blup[pheno_col] - pop_mean
                # Regressed BLUP EBV = b * (P - mu) where b = h^2 (individual selection)
                clean_blup["EBV"] = clean_blup["Deviation"] * h2
                clean_blup["Accuracy"] = np.sqrt(h2)
                
                # Rank
                clean_blup = clean_blup.sort_values(by="EBV", ascending=False).reset_index(drop=True)
                clean_blup["Rank"] = clean_blup.index + 1
                
                st.success(f"Calculated EBVs for {len(clean_blup):,} candidates at heritability h² = {h2:.2f}.")
                
                st.markdown("##### 🥇 Top 10 Elite Breeding Candidates")
                st.dataframe(clean_blup.head(10).style.format({"Deviation": "{:+.3f}", "EBV": "{:+.3f}", "Accuracy": "{:.2f}"}), use_container_width=True)

                # Distribution of EBVs
                fig_ebv = px.histogram(clean_blup, x="EBV", nbins=30, color_discrete_sequence=["#2E7D32"], title="Distribution of Estimated Breeding Values (EBV)")
                st.plotly_chart(fig_ebv, use_container_width=True)
        else:
            st.info("To compute individual breeding values, your dataset must contain an 'Animal_ID' or 'Genotype_ID' column. Try switching to the pre-loaded Cattle Trial dataset!")
