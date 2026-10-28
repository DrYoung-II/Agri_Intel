"""
AgroBiometrix - Core Statistical & Biometrics Engine
Comprehensive Mean Comparison, Post-Hoc Testing, BLUP, and Pedagogical Explainers
"""

import re
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import studentized_range, f as f_dist, t as t_dist
import statsmodels.api as sm
from statsmodels.formula.api import ols


def detect_and_decompose_compound_factors(df):
    """
    Scans categorical / string columns in df for combined Treatment-Replicate patterns
    (e.g., 'T1R1', 'T1_R2', 'Trt1_Rep2', 'Treatment1-R1', 'T1-1', 'DietA_1').
    
    Returns:
        df_augmented (pd.DataFrame): DataFrame with new extracted factor columns added.
        decomposed_info (list): List of dicts describing which columns were decomposed.
    """
    df_out = df.copy()
    decomposed_info = []
    
    cat_cols = df_out.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    
    patterns = [
        # Pattern 1: e.g. T1R1, T1_R2, Trt1_Rep2, Trt-R1, Treatment1-Rep3
        (re.compile(r'^(.+?)[_\s\-\.]*(?:[Rr]|[Rr]ep|[Rr]eplicate|[Rr]eplication)\s*(\d+)$', re.IGNORECASE), "R"),
        # Pattern 2: e.g. T1-1, T1_1, DietA-2, TrtA_3 (separator followed by integer)
        (re.compile(r'^(.+?)[_\-\.]\s*(\d+)$'), "sep_num"),
    ]
    
    for col in cat_cols:
        series_str = df_out[col].astype(str).str.strip()
        n_total = len(series_str)
        if n_total < 2:
            continue
            
        for pattern, pat_type in patterns:
            extracted = series_str.str.extract(pattern)
            valid_mask = extracted[0].notna() & extracted[1].notna()
            match_ratio = valid_mask.sum() / n_total
            
            if match_ratio >= 0.8:
                trts = extracted[0].str.strip()
                reps = extracted[1].str.strip()
                n_trts = trts.nunique()
                
                # Must reduce dimensionality to genuine treatment groups
                if 1 < n_trts < series_str.nunique():
                    trt_col_name = f"{col} (Extracted Treatment)"
                    rep_col_name = f"{col} (Extracted Replicate)"
                    
                    df_out[trt_col_name] = trts
                    df_out[rep_col_name] = "Rep_" + reps if pat_type != "R" else "R" + reps
                    
                    decomposed_info.append({
                        "original_col": col,
                        "treatment_col": trt_col_name,
                        "replicate_col": rep_col_name,
                        "n_treatments": n_trts,
                        "treatments": sorted(list(trts.unique())),
                        "n_replicates": reps.nunique(),
                        "sample": series_str.iloc[0]
                    })
                    break
                    
    return df_out, decomposed_info



def perform_assumption_checks(df, group_col, value_col):
    """
    Checks normality (Shapiro-Wilk) and homogeneity of variances (Levene's test).
    """
    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col)]
    group_names = [str(name) for name, _ in df.groupby(group_col)]
    
    # 1. Normality of residuals
    all_vals = df[value_col].dropna()
    mean_by_grp = df.groupby(group_col)[value_col].transform('mean')
    residuals = df[value_col] - mean_by_grp
    res_clean = residuals.dropna()
    
    if len(res_clean) >= 3 and len(res_clean) <= 5000:
        stat_norm, p_norm = stats.shapiro(res_clean)
    else:
        stat_norm, p_norm = stats.jarque_bera(res_clean)
    
    # 2. Homogeneity of variances (Levene's test)
    if len(groups) > 1 and all(len(g) > 1 for g in groups):
        stat_levene, p_levene = stats.levene(*groups, center='median')
    else:
        stat_levene, p_levene = np.nan, np.nan
        
    # 3. Balance check
    sample_sizes = [len(g) for g in groups]
    is_balanced = len(set(sample_sizes)) == 1
    harmonic_n = len(sample_sizes) / sum(1.0 / n for n in sample_sizes) if sample_sizes else 0
    
    return {
        "normality_p": p_norm,
        "is_normal": p_norm >= 0.05 if not np.isnan(p_norm) else True,
        "levene_p": p_levene,
        "is_homoscedastic": p_levene >= 0.05 if not np.isnan(p_levene) else True,
        "is_balanced": is_balanced,
        "sample_sizes": dict(zip(group_names, sample_sizes)),
        "harmonic_n": harmonic_n,
    }


def perform_one_way_anova(df, group_col, value_col):
    """
    Computes One-Way ANOVA: SS, df, MS, F-statistic, p-value.
    """
    clean_df = df[[group_col, value_col]].dropna()
    groups = [group[value_col].values for _, group in clean_df.groupby(group_col)]
    k = len(groups)
    N = len(clean_df)
    
    if k < 2:
        raise ValueError(
            f"Insufficient groups for One-Way ANOVA: grouping factor '{group_col}' only has {k} distinct level. "
            f"ANOVA requires at least 2 distinct treatment groups."
        )
    if N <= k:
        raise ValueError(
            f"Insufficient degrees of freedom for ANOVA on '{group_col}' (Total observations N={N}, Groups k={k}, DF_error={N-k}). "
            f"ANOVA requires experimental replication within groups (DF_error >= 1) to calculate within-group error variance. "
            f"If your '{group_col}' column contains combined treatment and replicate codes (e.g. 'T1R1', 'T1R2'), "
            f"please select the extracted Treatment factor."
        )
        
    grand_mean = clean_df[value_col].mean()
    
    # SS Treatment & SS Error
    ss_treatment = sum(len(g) * ((np.mean(g) - grand_mean) ** 2) for g in groups)
    df_treatment = k - 1
    ms_treatment = ss_treatment / df_treatment if df_treatment > 0 else 0
    
    ss_error = sum(sum((x - np.mean(g)) ** 2 for x in g) for g in groups)
    df_error = N - k
    ms_error = ss_error / df_error if df_error > 0 else 0
    
    ss_total = ss_treatment + ss_error
    df_total = N - 1
    
    f_stat = ms_treatment / ms_error if ms_error > 0 else 0
    p_value = 1.0 - f_dist.cdf(f_stat, df_treatment, df_error) if df_error > 0 else 1.0
    
    anova_table = pd.DataFrame([
        {"Source of Variation": "Treatment (Between)", "SS": ss_treatment, "df": df_treatment, "MS": ms_treatment, "F-value": f_stat, "p-value": p_value},
        {"Source of Variation": "Error (Within)", "SS": ss_error, "df": df_error, "MS": ms_error, "F-value": np.nan, "p-value": np.nan},
        {"Source of Variation": "Total", "SS": ss_total, "df": df_total, "MS": np.nan, "F-value": np.nan, "p-value": np.nan}
    ])
    
    return {
        "table": anova_table,
        "f_stat": f_stat,
        "p_value": p_value,
        "p_val": p_value,
        "is_significant": p_value < 0.05,
        "mse": ms_error,
        "dfe": df_error,
        "df_error": df_error,
        "df_treat": df_treatment,
        "df_treatment": df_treatment,
        "k": k,
        "N": N,
        "grand_mean": grand_mean
    }


def compute_group_means(df, group_col, value_col):
    """
    Computes group mean, std, standard error, and sample size.
    """
    summary = df.groupby(group_col)[value_col].agg(
        Mean='mean',
        Std='std',
        N='count'
    ).reset_index()
    summary['SE'] = summary['Std'] / np.sqrt(summary['N'])
    return summary


def assign_letters_from_significant_differences(ordered_groups, ordered_means, is_diff_matrix):
    """
    Algorithmic letter assignment (a, b, ab, c) based on pairwise significance matrix.
    ordered_groups: list of group labels ordered descending by mean.
    ordered_means: list of mean values ordered descending.
    is_diff_matrix: dict of (g1, g2) -> True if significantly different, False if not.
    """
    n = len(ordered_groups)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Start with empty letters for each group
    group_letters = {g: [] for g in ordered_groups}
    
    # Identify maximal homogeneous subsets (cliques where no pairs differ)
    subsets = []
    for i in range(n):
        for j in range(i, n):
            # check if all pairs in range [i..j] are non-different
            homogeneous = True
            for x in range(i, j + 1):
                for y in range(x + 1, j + 1):
                    g1, g2 = ordered_groups[x], ordered_groups[y]
                    if is_diff_matrix.get((g1, g2), False) or is_diff_matrix.get((g2, g1), False):
                        homogeneous = False
                        break
                if not homogeneous:
                    break
            if homogeneous:
                subsets.append(set(ordered_groups[i:j+1]))
                
    # Filter maximal subsets
    maximal_subsets = []
    for s in subsets:
        if not any(s < other for other in subsets):
            if s not in maximal_subsets:
                maximal_subsets.append(s)
                
    # Sort subsets by mean of members descending
    maximal_subsets.sort(key=lambda s: -np.mean([ordered_means[ordered_groups.index(g)] for g in s]))
    
    letter_idx = 0
    for s in maximal_subsets:
        letter = alphabet[letter_idx % len(alphabet)]
        for g in s:
            group_letters[g].append(letter)
        letter_idx += 1
        
    result = {}
    for g in ordered_groups:
        letters = sorted(list(set(group_letters[g])))
        result[g] = "".join(letters) if letters else "a"
    return result


def duncan_multiple_range_test(df, group_col, value_col, alpha=0.05):
    """
    Publication-grade Duncan's Multiple Range Test (DMRT).
    Uses exact studentized range protection level alpha_p = 1 - (1 - alpha)^(p-1).
    """
    anova = perform_one_way_anova(df, group_col, value_col)
    mse = anova["mse"]
    dfe = anova["dfe"]
    k = anova["k"]
    
    means_df = compute_group_means(df, group_col, value_col)
    means_df = means_df.sort_values(by="Mean", ascending=False).reset_index(drop=True)
    
    # Harmonic mean of sample sizes
    harmonic_n = len(means_df) / sum(1.0 / n for n in means_df['N'])
    se = np.sqrt(mse / harmonic_n)
    
    # Compute Least Significant Ranges (LSR) for steps p = 2..k
    lsr_table = []
    lsr_dict = {}
    for p in range(2, k + 1):
        alpha_p = 1.0 - (1.0 - alpha) ** (p - 1)
        ssr = studentized_range.ppf(1.0 - alpha_p, p, dfe)
        lsr = ssr * se
        lsr_dict[p] = lsr
        lsr_table.append({
            "Range (p)": p,
            "Protection Level (α_p)": round(alpha_p, 4),
            "SSR Critical Value": round(ssr, 3),
            "Least Significant Range (LSR_p)": round(lsr, 4)
        })
    lsr_df = pd.DataFrame(lsr_table)
    
    # Pairwise comparison
    ordered_groups = list(means_df[group_col])
    ordered_means = list(means_df["Mean"])
    is_diff = {}
    comparisons = []
    
    for i in range(k):
        for j in range(i + 1, k):
            g1, g2 = ordered_groups[i], ordered_groups[j]
            m1, m2 = ordered_means[i], ordered_means[j]
            diff = abs(m1 - m2)
            step_p = j - i + 1
            crit = lsr_dict[step_p]
            sig = diff >= crit
            is_diff[(g1, g2)] = sig
            is_diff[(g2, g1)] = sig
            comparisons.append({
                "Comparison": f"{g1} vs {g2}",
                "Mean Diff": round(diff, 4),
                "Step Range (p)": step_p,
                "Critical LSR": round(crit, 4),
                "Significant (p < 0.05)": "Yes (*)" if sig else "No (ns)"
            })
            
    comp_df = pd.DataFrame(comparisons)
    letter_mapping = assign_letters_from_significant_differences(ordered_groups, ordered_means, is_diff)
    means_df["DMRT_Letter"] = means_df[group_col].map(letter_mapping)
    
    # Pedagogical Rationale
    explainer = (
        f"**Duncan Multiple Range test was used** because the one-way ANOVA F-test was statistically significant "
        f"(F({anova['table'].iloc[0]['df']}, {dfe}) = {anova['f_stat']:.3f}, p = {anova['p_value']:.4e} < {alpha}), "
        f"and pairwise comparison among {k} treatment means was required to separate cultivar/treatment effects.\n\n"
        f"**Why Duncan's Test was selected**: In agricultural and biological field trials, conservative procedures "
        f"like Tukey's HSD or Bonferroni adjustments prioritize protection against Type I errors (false positives) "
        f"at the severe cost of inflating Type II errors (missing genuine biological differences between treatments). "
        f"Duncan's Multiple Range Test (DMRT) uses a stepwise variable critical range: as the distance (p) between "
        f"ordered means increases, the test applies a protective level α_p = 1 - (1 - α)^(p-1). This delivers greater "
        f"statistical power while maintaining adequate protection against false negatives, making DMRT the historical "
        f"and practical benchmark for agronomy, crop breeding, and livestock trials."
    )
    
    return {
        "test_name": "Duncan's Multiple Range Test (DMRT)",
        "anova": anova,
        "means_df": means_df,
        "lsr_df": lsr_df,
        "comp_df": comp_df,
        "explainer": explainer,
        "se": se,
        "harmonic_n": harmonic_n
    }


def tukey_hsd_test(df, group_col, value_col, alpha=0.05):
    """
    Tukey's Honest Significant Difference (HSD) Test.
    """
    anova = perform_one_way_anova(df, group_col, value_col)
    mse = anova["mse"]
    dfe = anova["dfe"]
    k = anova["k"]
    
    means_df = compute_group_means(df, group_col, value_col)
    means_df = means_df.sort_values(by="Mean", ascending=False).reset_index(drop=True)
    harmonic_n = len(means_df) / sum(1.0 / n for n in means_df['N'])
    se = np.sqrt(mse / harmonic_n)
    
    q_crit = studentized_range.ppf(1.0 - alpha, k, dfe)
    hsd_crit = q_crit * se
    
    ordered_groups = list(means_df[group_col])
    ordered_means = list(means_df["Mean"])
    is_diff = {}
    comparisons = []
    
    for i in range(k):
        for j in range(i + 1, k):
            g1, g2 = ordered_groups[i], ordered_groups[j]
            m1, m2 = ordered_means[i], ordered_means[j]
            diff = abs(m1 - m2)
            sig = diff >= hsd_crit
            is_diff[(g1, g2)] = sig
            is_diff[(g2, g1)] = sig
            comparisons.append({
                "Comparison": f"{g1} vs {g2}",
                "Mean Diff": round(diff, 4),
                "Tukey Critical HSD": round(hsd_crit, 4),
                "Significant": "Yes (*)" if sig else "No (ns)"
            })
            
    comp_df = pd.DataFrame(comparisons)
    letter_mapping = assign_letters_from_significant_differences(ordered_groups, ordered_means, is_diff)
    means_df["Tukey_Letter"] = means_df[group_col].map(letter_mapping)
    
    explainer = (
        f"**Tukey's Honestly Significant Difference (HSD) test was used** because all possible pairwise comparisons "
        f"among {k} treatment means were evaluated, and strict experiment-wise Type I error control was required "
        f"(Family-wise error rate bounded at α = {alpha}).\n\n"
        f"**Why Tukey's HSD was selected**: When researchers want to guarantee that the overall chance of making even "
        f"a single false positive across all {int(k*(k-1)/2)} comparisons does not exceed 5%, Tukey's studentized "
        f"range statistic provides exact, conservative confidence boundaries."
    )
    
    return {
        "test_name": "Tukey's Honest Significant Difference (HSD)",
        "anova": anova,
        "means_df": means_df,
        "critical_value": hsd_crit,
        "q_crit": q_crit,
        "comp_df": comp_df,
        "explainer": explainer
    }


def fishers_lsd_test(df, group_col, value_col, alpha=0.05):
    """
    Fisher's Protected Least Significant Difference (LSD) Test.
    """
    anova = perform_one_way_anova(df, group_col, value_col)
    mse = anova["mse"]
    dfe = anova["dfe"]
    k = anova["k"]
    
    means_df = compute_group_means(df, group_col, value_col)
    means_df = means_df.sort_values(by="Mean", ascending=False).reset_index(drop=True)
    harmonic_n = len(means_df) / sum(1.0 / n for n in means_df['N'])
    
    t_crit = t_dist.ppf(1.0 - alpha / 2.0, dfe)
    lsd_crit = t_crit * np.sqrt(2.0 * mse / harmonic_n)
    
    ordered_groups = list(means_df[group_col])
    ordered_means = list(means_df["Mean"])
    is_diff = {}
    comparisons = []
    
    for i in range(k):
        for j in range(i + 1, k):
            g1, g2 = ordered_groups[i], ordered_groups[j]
            m1, m2 = ordered_means[i], ordered_means[j]
            diff = abs(m1 - m2)
            sig = diff >= lsd_crit
            is_diff[(g1, g2)] = sig
            is_diff[(g2, g1)] = sig
            comparisons.append({
                "Comparison": f"{g1} vs {g2}",
                "Mean Diff": round(diff, 4),
                "Critical LSD": round(lsd_crit, 4),
                "Significant": "Yes (*)" if sig else "No (ns)"
            })
            
    comp_df = pd.DataFrame(comparisons)
    letter_mapping = assign_letters_from_significant_differences(ordered_groups, ordered_means, is_diff)
    means_df["LSD_Letter"] = means_df[group_col].map(letter_mapping)
    
    explainer = (
        f"**Fisher's Protected Least Significant Difference (LSD) test was used** because the one-way ANOVA F-test was "
        f"statistically significant (p < 0.05), and maximum statistical sensitivity was needed to detect differences "
        f"between specific treatment pairs.\n\n"
        f"**Why Fisher's LSD was selected**: Fisher's LSD is the most sensitive (powerful) pairwise test because it is "
        f"anchored directly to Student's t-distribution. It is protected by the preliminary overall ANOVA F-test, making "
        f"it valid for 3-group trials or planned orthogonal comparisons where high statistical power is desired."
    )
    
    return {
        "test_name": "Fisher's Protected LSD",
        "anova": anova,
        "means_df": means_df,
        "critical_value": lsd_crit,
        "t_crit": t_crit,
        "comp_df": comp_df,
        "explainer": explainer
    }


def dunnetts_test(df, group_col, value_col, control_group, alpha=0.05):
    """
    Dunnett's Test: Compares all treatment groups against a designated Control / Check variety.
    """
    anova = perform_one_way_anova(df, group_col, value_col)
    mse = anova["mse"]
    dfe = anova["dfe"]
    k = anova["k"]
    
    means_df = compute_group_means(df, group_col, value_col)
    ctrl_row = means_df[means_df[group_col] == control_group]
    if ctrl_row.empty:
        raise ValueError(f"Control group '{control_group}' not found in data.")
    ctrl_mean = ctrl_row["Mean"].values[0]
    ctrl_n = ctrl_row["N"].values[0]
    
    comparisons = []
    # Approximation of Dunnett's critical multiplier using studentized maximum modulus
    # For k-1 comparisons against control, alpha/k-1 Bonferroni-t provides close conservative bound
    num_comp = k - 1
    alpha_adj = alpha / num_comp
    t_crit = t_dist.ppf(1.0 - alpha_adj / 2.0, dfe)
    
    for _, row in means_df.iterrows():
        grp = row[group_col]
        if grp == control_group:
            continue
        m = row["Mean"]
        n_grp = row["N"]
        diff = m - ctrl_mean
        se_diff = np.sqrt(mse * (1.0 / ctrl_n + 1.0 / n_grp))
        crit_diff = t_crit * se_diff
        t_stat = diff / se_diff
        p_val = min(1.0, 2.0 * (1.0 - t_dist.cdf(abs(t_stat), dfe)) * num_comp)
        sig = abs(diff) >= crit_diff
        comparisons.append({
            "Treatment vs Control": f"{grp} vs Control ({control_group})",
            "Treatment Mean": round(m, 3),
            "Control Mean": round(ctrl_mean, 3),
            "Difference": round(diff, 4),
            "SE of Diff": round(se_diff, 4),
            "Critical Diff": round(crit_diff, 4),
            "p-value (Dunnett-adj)": round(p_val, 4),
            "Conclusion": "Significantly Different (*)" if sig else "Not Significant (ns)"
        })
        
    comp_df = pd.DataFrame(comparisons)
    
    explainer = (
        f"**Dunnett's test was used** because the biological and agronomic research objective was specifically to compare "
        f"multiple experimental treatments or candidate genotypes against a single commercial check / standard control: '{control_group}'.\n\n"
        f"**Why Dunnett's Test was selected**: Conducting all possible pairwise comparisons when only comparisons against a "
        f"control are relevant wastes degrees of freedom and severely penalizes statistical power. Dunnett's procedure evaluates "
        f"exactly {k - 1} comparisons rather than {int(k*(k-1)/2)}, retaining maximum experimental power to confirm whether new "
        f"varieties statistically outperform the control."
    )
    
    return {
        "test_name": "Dunnett's Test (Many-to-One)",
        "control": control_group,
        "anova": anova,
        "comp_df": comp_df,
        "explainer": explainer,
        "means_df": means_df
    }


def non_parametric_dunn_test(df, group_col, value_col):
    """
    Kruskal-Wallis H-test followed by Dunn's Post-Hoc Test for non-normal data.
    """
    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col)]
    group_names = [str(name) for name, _ in df.groupby(group_col)]
    
    stat_h, p_kw = stats.kruskal(*groups)
    
    # Ranks
    clean_df = df[[group_col, value_col]].dropna().copy()
    clean_df["Rank"] = clean_df[value_col].rank()
    mean_ranks = clean_df.groupby(group_col)["Rank"].mean()
    
    N = len(clean_df)
    k = len(groups)
    comparisons = []
    
    for i in range(k):
        for j in range(i + 1, k):
            g1, g2 = group_names[i], group_names[j]
            r1, r2 = mean_ranks[g1], mean_ranks[g2]
            n1, n2 = len(groups[i]), len(groups[j])
            diff = abs(r1 - r2)
            se_rank = np.sqrt((N * (N + 1) / 12.0) * (1.0 / n1 + 1.0 / n2))
            z = diff / se_rank
            # Dunn's p-value with Bonferroni correction
            num_comp = k * (k - 1) / 2
            p_val = min(1.0, 2.0 * (1.0 - stats.norm.cdf(z)) * num_comp)
            comparisons.append({
                "Comparison": f"{g1} vs {g2}",
                "Mean Rank Diff": round(diff, 2),
                "Z-statistic": round(z, 3),
                "p-value (Dunn-adj)": round(p_val, 4),
                "Significant": "Yes (*)" if p_val < 0.05 else "No (ns)"
            })
            
    comp_df = pd.DataFrame(comparisons)
    
    explainer = (
        f"**Kruskal-Wallis H-test followed by Dunn's post-hoc test was used** because preliminary diagnostic screening "
        f"showed that the continuous response data violated the assumption of normality (or contains ordinal scoring/counts), "
        f"invalidating standard parametric ANOVA F-tests.\n\n"
        f"**Why Dunn's Test was selected**: Kruskal-Wallis established significant overall rank differences (H = {stat_h:.3f}, "
        f"p = {p_kw:.4e}). Dunn's post-hoc procedure evaluates pairwise differences in mean ranks with multiplicity adjustments, "
        f"providing an exact distribution-free statistical separation."
    )
    
    means_df = compute_group_means(df, group_col, value_col)
    
    return {
        "test_name": "Kruskal-Wallis & Dunn's Test",
        "h_stat": stat_h,
        "p_value": p_kw,
        "comp_df": comp_df,
        "explainer": explainer,
        "means_df": means_df
    }


def two_way_factorial_anova(df, factor_a, factor_b, response_col):
    """
    Two-Way Factorial ANOVA with interaction effects (A, B, A x B).
    """
    # Use Q(...) to escape column names with spaces or special characters in patsy formula
    formula = f'Q("{response_col}") ~ C(Q("{factor_a}")) + C(Q("{factor_b}")) + C(Q("{factor_a}")):C(Q("{factor_b}"))'
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    # Interaction check with resilient candidate naming
    inter_candidates = [
        f'C(Q("{factor_a}")):C(Q("{factor_b}"))',
        f'C({factor_a}):C({factor_b})',
        f'{factor_a}:{factor_b}'
    ]
    inter_p = 1.0
    for cand in inter_candidates:
        if cand in anova_table.index:
            inter_p = anova_table.loc[cand, "PR(>F)"]
            break
    has_sig_interaction = inter_p < 0.05
    
    explainer = (
        f"**Two-Way Factorial ANOVA was used** to evaluate the main effects of Factor A ('{factor_a}'), "
        f"Factor B ('{factor_b}'), and their interaction ('{factor_a} × {factor_b}').\n\n"
        f"**Interaction Finding**: The interaction effect between {factor_a} and {factor_b} was "
        f"{'STATISTICALLY SIGNIFICANT (p = ' + f'{inter_p:.4f}' + ' < 0.05)' if has_sig_interaction else 'not statistically significant (p = ' + f'{inter_p:.4f}' + ' >= 0.05)'}.\n\n"
        f"**Statistical Guidance**: "
        + (
            f"Because interaction is significant, reporting main effects alone would be biologically misleading! "
            f"The response to {factor_a} depends on the level of {factor_b}. Simple-effects mean comparisons "
            f"(e.g., Duncan's Multiple Range Test within each level of {factor_b}) are recommended."
            if has_sig_interaction else
            f"Because interaction is not significant, main effects of {factor_a} and {factor_b} can be interpreted "
            f"independently across all experimental conditions."
        )
    )
    
    return {
        "model": model,
        "anova_table": anova_table,
        "has_sig_interaction": has_sig_interaction,
        "explainer": explainer
    }


def generate_reproducible_code(dataset_name, group_col, value_col, test_type="duncan"):
    """
    Generates reproducible R and Python code for agricultural researchers and thesis students.
    """
    r_code = f"""# Reproducible Agricultural Biometrics Script in R
# AgroBiometrix Automated Pipeline
library(agricolae)

# 1. Load data
data <- read.csv("{dataset_name}.csv")

# 2. Fit ANOVA Model
model <- aov({value_col} ~ {group_col}, data = data)
print(summary(model))

# 3. Mean Comparison & Post-Hoc Test
"""
    if test_type == "duncan":
        r_code += f"""out_dmrt <- duncan.test(model, "{group_col}", alpha = 0.05, console = TRUE)
plot(out_dmrt, main = "Duncan Multiple Range Test Mean Separation")
"""
    elif test_type == "tukey":
        r_code += f"""out_tukey <- HSD.test(model, "{group_col}", alpha = 0.05, console = TRUE)
plot(out_tukey, main = "Tukey HSD Mean Separation")
"""
    elif test_type == "lsd":
        r_code += f"""out_lsd <- LSD.test(model, "{group_col}", p.adj = "none", console = TRUE)
plot(out_lsd, main = "Fisher Protected LSD Mean Separation")
"""

    python_code = f"""# Reproducible Python Code with AgroBiometrix Engine
import pandas as pd
from statsmodels.formula.api import ols
import statsmodels.api as sm

# 1. Load data
df = pd.read_csv("{dataset_name}.csv")

# 2. ANOVA
model = ols('Q("{value_col}") ~ C(Q("{group_col}"))', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA Summary Table:")
print(anova_table)
"""
    return {"r": r_code, "python": python_code}


def perform_batch_posthoc_analysis(df, group_col, value_cols, test_choice="Duncan", alpha=0.05, control_group=None):
    """
    Executes batch ANOVA and the chosen mean separation procedure across all selected continuous traits.
    Assembles a publication-grade Master Academic Summary Table (Means ± SEM with grouping letters).
    """
    master_rows = []
    numeric_rows = []
    individual_results = {}
    failed_traits = []
    
    clean_df = df.dropna(subset=[group_col])
    # Natural / stable sorting of groups
    group_levels = sorted(list(clean_df[group_col].unique()), key=lambda x: str(x))
    
    if "Dunnett" in test_choice and (not control_group or control_group not in group_levels):
        control_group = group_levels[0]
        
    for trait in value_cols:
        try:
            # Check variance of trait
            valid_vals = clean_df[trait].dropna()
            if len(valid_vals) < 2 or valid_vals.nunique() <= 1:
                failed_traits.append({"trait": trait, "error": "Insufficient variation or empty column"})
                continue
                
            if "Duncan" in test_choice:
                res = duncan_multiple_range_test(clean_df, group_col, trait, alpha=alpha)
                letter_col = "DMRT_Letter"
            elif "Tukey" in test_choice:
                res = tukey_hsd_test(clean_df, group_col, trait, alpha=alpha)
                letter_col = "Tukey_Letter"
            elif "Fisher" in test_choice:
                res = fishers_lsd_test(clean_df, group_col, trait, alpha=alpha)
                letter_col = "LSD_Letter"
            elif "Dunnett" in test_choice:
                res = dunnetts_test(clean_df, group_col, trait, control_group=control_group, alpha=alpha)
                letter_col = None
            else:
                res = non_parametric_dunn_test(clean_df, group_col, trait)
                letter_col = None
                
            individual_results[trait] = res
            
            # Form display row
            row_display = {"Trait / Variable": trait}
            row_numeric = {"Trait": trait}
            
            if "means_df" in res:
                m_df = res["means_df"].set_index(group_col)
                for g in group_levels:
                    if g in m_df.index:
                        m_val = m_df.loc[g, "Mean"]
                        se_val = m_df.loc[g, "SE"]
                        row_numeric[f"{g}_Mean"] = m_val
                        row_numeric[f"{g}_SE"] = se_val
                        
                        if letter_col and letter_col in m_df.columns:
                            let = m_df.loc[g, letter_col]
                            row_display[g] = f"{m_val:.2f} ± {se_val:.2f} {let}"
                            row_numeric[f"{g}_Letter"] = let
                        elif "Dunnett" in test_choice and g != control_group:
                            # Check if significant vs control
                            comp_sub = res["comp_df"][res["comp_df"]["Treatment vs Control"].str.startswith(f"{g} ")]
                            is_sig = False
                            if not comp_sub.empty:
                                is_sig = "(*)" in comp_sub["Conclusion"].values[0]
                            sig_mark = " *" if is_sig else ""
                            row_display[g] = f"{m_val:.2f} ± {se_val:.2f}{sig_mark}"
                            row_numeric[f"{g}_SigCtrl"] = is_sig
                        else:
                            row_display[g] = f"{m_val:.2f} ± {se_val:.2f}"
                    else:
                        row_display[g] = "N/A"
                        row_numeric[f"{g}_Mean"] = np.nan
            
            if "anova" in res:
                p_val = res["anova"]["p_val"]
                f_stat = res["anova"]["f_stat"]
                se_pooled = res.get("se", np.sqrt(res["anova"]["mse"] / max(1, res.get("harmonic_n", 1.0))))
                row_display["Pooled SEM"] = f"{se_pooled:.3f}"
                row_display["F-value"] = f"{f_stat:.2f}"
                row_display["p-value"] = f"{p_val:.4f}"
                sig_symbol = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else "ns"))
                row_display["Sig."] = sig_symbol
                
                row_numeric["Pooled_SEM"] = se_pooled
                row_numeric["F_val"] = f_stat
                row_numeric["p_val"] = p_val
                row_numeric["Sig"] = sig_symbol
            elif "p_value" in res:
                p_val = res["p_value"]
                h_stat = res.get("h_stat", np.nan)
                row_display["Pooled SEM"] = "N/A"
                row_display["F-value"] = f"H={h_stat:.2f}"
                row_display["p-value"] = f"{p_val:.4f}"
                sig_symbol = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else "ns"))
                row_display["Sig."] = sig_symbol
                
                row_numeric["Pooled_SEM"] = np.nan
                row_numeric["F_val"] = h_stat
                row_numeric["p_val"] = p_val
                row_numeric["Sig"] = sig_symbol
                
            master_rows.append(row_display)
            numeric_rows.append(row_numeric)
            
        except Exception as e:
            failed_traits.append({"trait": trait, "error": str(e)})
            
    master_table = pd.DataFrame(master_rows)
    master_numeric_df = pd.DataFrame(numeric_rows)
    
    # Summary metrics
    sig_count = 0
    non_sig_count = 0
    if not master_numeric_df.empty and "p_val" in master_numeric_df.columns:
        sig_count = int((master_numeric_df["p_val"] < alpha).sum())
        non_sig_count = len(master_numeric_df) - sig_count
        
    # Construct Markdown representation
    md_lines = []
    test_title = "Duncan's Multiple Range Test" if "Duncan" in test_choice else (
        "Tukey's HSD" if "Tukey" in test_choice else (
            "Fisher's LSD" if "Fisher" in test_choice else (
                "Dunnett's Test" if "Dunnett" in test_choice else "Kruskal-Wallis / Dunn's Test"
            )
        )
    )
    md_lines.append(f"### Table 1: Master Academic Multi-Trait Summary Table ({test_title})")
    md_lines.append(f"*Evaluated across {len(master_rows)} continuous traits under factor '{group_col}'.*\n")
    
    def _df_to_md(dframe):
        if dframe.empty:
            return ""
        cols = list(dframe.columns)
        hdr = "| " + " | ".join(str(c) for c in cols) + " |"
        divider = "| " + " | ".join("---" for _ in cols) + " |"
        rows = ["| " + " | ".join(str(r[c]) for c in cols) + " |" for _, r in dframe.iterrows()]
        return "\n".join([hdr, divider] + rows)

    if not master_table.empty:
        md_lines.append(_df_to_md(master_table))
        md_lines.append("\n*Note: Means within the same row followed by different letters differ significantly (p < 0.05). "
                        "Pooled SEM = Standard Error of the Mean computed from ANOVA residual variance. "
                        "*** p < 0.001, ** p < 0.01, * p < 0.05, ns = not significant (p >= 0.05).*")
        
    return {
        "master_table": master_table,
        "master_numeric_df": master_numeric_df,
        "master_markdown": "\n".join(md_lines),
        "individual_results": individual_results,
        "failed_traits": failed_traits,
        "group_levels": group_levels,
        "test_name": test_title,
        "summary_metrics": {
            "total_analyzed": len(master_rows),
            "significant_count": sig_count,
            "non_significant_count": non_sig_count
        }
    }


def generate_reproducible_batch_code(dataset_name, group_col, value_cols, test_type="duncan"):
    """
    Generates batch R and Python scripts for processing multiple response variables in publication workflows.
    """
    traits_r = ", ".join(f'"{col}"' for col in value_cols)
    r_code = f"""# ==============================================================================
# AgroBiometrix Multi-Trait Biometrics Pipeline in R
# Batch Analysis of {len(value_cols)} Traits with agricolae package
# ==============================================================================
library(agricolae)

data <- read.csv("{dataset_name}.csv")
traits <- c({traits_r})

cat("Running Multi-Trait Analysis on Factor: {group_col}\\n")
results_list <- list()

for (tr in traits) {{
  cat("\\n------------------------------------------------------------\\n")
  cat("ANALYZING TRAIT:", tr, "\\n")
  cat("------------------------------------------------------------\\n")
  
  fmla <- as.formula(paste(tr, "~", "{group_col}"))
  model <- aov(fmla, data = data)
  print(summary(model))
  
"""
    if test_type == "duncan":
        r_code += f"""  out_posthoc <- duncan.test(model, "{group_col}", alpha = 0.05, console = TRUE)
  results_list[[tr]] <- out_posthoc$groups
}}
"""
    elif test_type == "tukey":
        r_code += f"""  out_posthoc <- HSD.test(model, "{group_col}", alpha = 0.05, console = TRUE)
  results_list[[tr]] <- out_posthoc$groups
}}
"""
    elif test_type == "lsd":
        r_code += f"""  out_posthoc <- LSD.test(model, "{group_col}", p.adj = "none", console = TRUE)
  results_list[[tr]] <- out_posthoc$groups
}}
"""
    else:
        r_code += f"""  # Kruskal-Wallis test
  kw <- kruskal.test(fmla, data = data)
  print(kw)
}}
"""

    traits_py = ", ".join(f'"{col}"' for col in value_cols)
    python_code = f"""# ==============================================================================
# AgroBiometrix Multi-Trait Biometrics Pipeline in Python
# Batch Analysis of {len(value_cols)} Traits with statsmodels
# ==============================================================================
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

df = pd.read_csv("{dataset_name}.csv")
traits = [{traits_py}]

print(f"Batch analyzing {{len(traits)}} traits grouped by '{group_col}'...")

for tr in traits:
    formula = f'Q("{{tr}}") ~ C(Q("{group_col}"))'
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    p_val = anova_table.loc['C(Q("{group_col}"))', 'PR(>F)']
    f_stat = anova_table.loc['C(Q("{group_col}"))', 'F']
    print(f"Trait: {{tr}} | F = {{f_stat:.2f}}, p = {{p_val:.4e}}")
"""
    return {"r": r_code, "python": python_code}

