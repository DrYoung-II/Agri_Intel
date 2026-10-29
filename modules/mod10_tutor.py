"""
Module 10: AI Thesis & Student Research Assistant
Comprehensive Socratic Agricultural Research Tutor for BSc, MSc, and PhD Students
Supporting all major departments and sub-specializations of Animal Science, Plant/Crop Science,
Soil Science, Economics, and Aquaculture.
"""

import streamlit as st
from core.orchestrator import (
    rule_based_agent_synthesis,
    get_gemini_api_key,
    set_gemini_api_key,
    validate_gemini_key,
    call_live_llm_orchestration
)


# Comprehensive list of agricultural departments and specializations
DEPARTMENTS = [
    # --- ANIMAL SCIENCE DISCIPLINES ---
    "Animal Science (General)",
    "Animal Nutrition & Feed Technology",
    "Animal Breeding & Genetics",
    "Animal Physiology & Bioclimatology",
    "Pasture & Range Management",
    "Animal Production & Livestock Management",

    # --- PLANT & CROP SCIENCE DISCIPLINES ---
    "Crop & Plant Science (General)",
    "Agronomy & Farming Systems",
    "Plant Breeding & Seed Technology",
    "Crop Protection (Entomology & Pathology)",
    "Horticulture & Post-Harvest Science",
    "Plant Physiology & Weed Science",

    # --- SOIL, APPLIED & RESOURCE DISCIPLINES ---
    "Soil Science & Land Resource Management",
    "Agricultural Economics & Agribusiness",
    "Agricultural Extension & Rural Development",
    "Aquaculture & Fisheries Management",
]

# Specialized Departmental Benchmarks & Tailored Guidance
DISCIPLINE_METADATA = {
    "Animal Nutrition & Feed Technology": {
        "focus": "Dietary formulation, proximate analysis (AOAC), voluntary intake, feed conversion ratio (FCR), rumen fermentation, volatile fatty acids, anti-nutritional factor detoxification.",
        "journals": "Nigerian Journal of Animal Production (NJAP), Animal Nutrition, British Journal of Nutrition, Livestock Science, Journal of Animal Physiology and Animal Nutrition.",
        "sample_topics": [
            "Effect of graded inclusion of fermented cassava peel meal on growth performance, nutrient digestibility, and blood profile of weaner rabbits.",
            "Evaluation of exogenous enzyme supplementation on phosphorus utilization and ileal amino acid digestibility in broilers fed sorghum-soybean diets.",
            "Rumen fermentation kinetics and methane mitigation in West African Dwarf goats fed browse legume (Gliricidia sepium) silage."
        ],
        "design_advice": "For feeding trials, use Completely Randomized Design (CRD) with single-caged animals, or Randomized Complete Block Design (RCBD) balancing initial body weight as a blocking factor. In digestibility trials, use metabolic crates with a 14-day dietary adaptation period followed by a 7-day total fecal/urinary collection period.",
        "dmrt_advice": "When dietary treatments involve incremental quantitative levels (e.g. 0%, 5%, 10%, 15% inclusion), external examiners will ask: <i>'Why did you use DMRT instead of Orthogonal Polynomial Contrasts to test for linear or quadratic trends?'</i><br><br><b>Your Defense</b>: <i>'Sir/Madam, orthogonal polynomial contrasts test the underlying mathematical dose-response trajectory, but Duncan's Multiple Range Test (DMRT) was essential to identify the exact discrete threshold level at which biological performance significantly separated from the control without incurring Type II error.'</i>"
    },
    "Animal Physiology & Bioclimatology": {
        "focus": "Thermoregulatory mechanisms, rectal temperature, respiration rate, cutaneous evaporation, heat shock proteins (HSP70/90), hormonal assays (cortisol, thyroid, progesterone), semen cryopreservation, estrus synchronization.",
        "journals": "International Journal of Biometeorology, Domestic Animal Endocrinology, Theriogenology, Tropical Animal Health and Production.",
        "sample_topics": [
            "Diurnal physiological responses, serum electrolytes, and HSP70 gene expression in indigenous and exotic dairy cattle under sub-humid tropical heat stress.",
            "Evaluating conductive cooling (frozen water containers) on semen quality, testosterone kinetics, and testicular thermoregulation in heat-stressed bucks.",
            "Estrus synchronization efficiency and conception rates in West African Dwarf sheep using progesterone intravaginal sponges and PMSG."
        ],
        "design_advice": "Repeated measurements across diurnal timepoints (07:00, 13:00, 18:00 hrs) require Repeated Measures ANOVA or a Linear Mixed Model (LMM) with individual animal fitted as a random factor to account for within-subject covariance.",
        "dmrt_advice": "Defend the use of repeated-measures post-hoc separation: <i>'Because physiological variables change continuously across circadian cycles, DMRT was applied within designated peak thermal windows (13:00–15:00 UTC) to identify distinct heat stress severity thresholds across breeds.'</i>"
    },
    "Pasture & Range Management": {
        "focus": "Forage agronomy, pasture establishment, dry matter yield, botanical composition, nutritive value of tropical grasses and browse legumes, grazing capacity, carrying capacity (AUE), rangeland degradation.",
        "journals": "African Journal of Range & Forage Science, Grass and Forage Science, Rangeland Ecology & Management, Pastoralism.",
        "sample_topics": [
            "Herbage yield, nutritive value, and persistence of Panicum maximum intercropped with Stylosanthes guianensis under varied cutting frequencies.",
            "Botanical composition and rangeland carrying capacity of communal grazing lands in the Sudan Savanna of Nigeria across seasonal transitions.",
            "Silage quality and aerobic stability of tropical forage grasses ensiled with varied levels of sugarcane molasses and urea."
        ],
        "design_advice": "Deploy Split-Plot Designs where pasture species or fertilization levels form the main plots, and cutting intervals or seasonal harvesting stages form the sub-plots. Use quadrat sampling (1m × 1m, minimum 5 throws per paddock).",
        "dmrt_advice": "For multi-harvest pasture studies: <i>'DMRT enabled clear pairwise separation of cumulative biomass across distinct phenological cutting stages, highlighting the optimal harvest date that maximizes crude protein yield before lignification.'</i>"
    },
    "Animal Production & Livestock Management": {
        "focus": "Broiler, layer, swine, small ruminant, and cuniculture production systems; housing microclimate, stocking density, growth kinetics, carcass dressing percentage, retail cut yield, farm biosecurity.",
        "journals": "Poultry Science, Tropical Animal Health and Production, Journal of Applied Poultry Research, Livestock Science.",
        "sample_topics": [
            "Comparative growth kinetics, carcass yield, and economic return of commercial broilers reared under open-sided vs tunnel-ventilated tropical housing.",
            "Evaluating stocking density and dietary betaine supplementation on welfare biomarkers and meat quality of pigs during the humid dry season.",
            "Effect of raised hutch wire mesh flooring vs deep litter on kit survivability, coccidiosis incidence, and gross margin in rabbit production."
        ],
        "design_advice": "Factorial RCBD (e.g., 2 Housing Systems × 3 Stocking Densities) with pens/cages as experimental units. Always measure both biological metrics (FCR, ADG, dressing %) and economic margins (benefit-cost ratio, gross margin per animal).",
        "dmrt_advice": "Defend carcass and performance mean separations: <i>'DMRT allowed stepwise identification of the optimal stocking density threshold where bird density was maximized without significantly depressing carcass dressing percentage.'</i>"
    },
    "Animal Breeding & Genetics": {
        "focus": "Quantitative genetics, heritability (h²), genetic correlations, breeding values (EBVs/GEBVs), selection indices, crossbreeding heterosis, molecular markers, candidate genes, QTL mapping, GWAS.",
        "journals": "Journal of Animal Breeding and Genetics, Genetics Selection Evolution, Animal Genetics, South African Journal of Animal Science.",
        "sample_topics": [
            "Genomic characterization of heat tolerance and disease resistance loci in Nigerian indigenous cattle (Muturu and Bunaji) using high-density SNP arrays.",
            "Estimation of genetic parameters and breeding values for growth and reproductive traits in a synthetic rabbit population using Animal Model BLUP.",
            "Crossbreeding heterosis and maternal effects for body weight and carcass traits in crosses between New Zealand White and Chinchilla rabbits."
        ],
        "design_advice": "Use animal pedigree records with Henderson's Mixed Model Equations (LMM/BLUP). Ensure pedigree depth of at least 3 generations. For molecular GWAS trials, ensure genomic quality control (call rate > 0.95, MAF > 0.05, Hardy-Weinberg equilibrium $P > 10^{-6}$).",
        "dmrt_advice": "Defend genotype separation: <i>'While BLUP generates continuous genetic breeding values, DMRT was utilized on phenotypic trait means to empirically demonstrate phenotypic superiority across distinct breed crosses and genetic groups.'</i>"
    },
    "Agronomy & Farming Systems": {
        "focus": "Crop physiology, plant population geometry, intercropping land equivalent ratio (LER), planting dates, soil-tillage systems, weed-crop interference, drought stress mitigation.",
        "journals": "Field Crops Research, European Journal of Agronomy, Agronomy Journal, African Crop Science Journal.",
        "sample_topics": [
            "Tillage systems and spatial planting geometry effects on soil moisture conservation and grain yield of drought-tolerant maize in the Northern Guinea Savanna.",
            "Productivity and Land Equivalent Ratio (LER) of cassava-cowpea intercropping systems under varied nitrogen fertilization regimes.",
            "Weed interference duration and critical period of weed control in dry-season irrigated tomato production in Western Nigeria."
        ],
        "design_advice": "Randomized Complete Block Design (RCBD) with minimum 4 replications. Ensure plot border rows (minimum 2 outer rows per plot) are discarded during harvest to eliminate edge/border effects.",
        "dmrt_advice": "Defend agronomic mean separation: <i>'DMRT provided the stepwise discriminating sensitivity to pinpoint the exact plant spacing that optimized canopy radiation interception and yield without statistical over-conservatism.'</i>"
    },
    "Plant Breeding & Seed Technology": {
        "focus": "Genetic variation, combining ability (GCA/SCA), diallel analysis, heterosis, G×E interaction, AMMI and GGE biplots, speed breeding, seed vigor and germination viability.",
        "journals": "Theoretical and Applied Genetics (TAG), Crop Science, Euphytica, Plant Breeding, African Crop Science Journal.",
        "sample_topics": [
            "Genotype × Environment interaction and grain yield stability of early-maturing provitamin-A maize hybrids across savanna agro-ecologies using GGE biplots.",
            "Combining ability and heterotic grouping of drought-tolerant white maize inbred lines under low-nitrogen and drought stress environments.",
            "Seed physiological quality, longevity, and seedling emergence of primed soybean (Glycine max) seeds stored under tropical ambient conditions."
        ],
        "design_advice": "Multi-Environment Trials (MET) across at least 2 distinct agro-ecological zones or seasons using Alpha Lattice or RCBD with 3 replications. Test homogeneity of variance (Bartlett's test) before combining ANOVA across locations.",
        "dmrt_advice": "Defend stability vs mean separation: <i>'While AMMI and GGE biplots evaluate multidimensional genotype stability, DMRT was essential for rank-ordering mean performance within individual high-stress test environments.'</i>"
    },
    "Crop Protection (Entomology & Pathology)": {
        "focus": "Plant pathology, economic entomology, pest and pathogen dynamics, disease incidence & severity, AUDPC, integrated pest management (IPM), bio-pesticide efficacy, vector genetics.",
        "journals": "Crop Protection, Phytopathology, Journal of Economic Entomology, Plant Disease, International Journal of Pest Management.",
        "sample_topics": [
            "Epidemiology, vector dynamics of Bemisia tabaci, and field screening of tomato lines for resistance to Tomato Yellow Leaf Curl Virus (TYLCV).",
            "Efficacy of botanical extracts (Azadirachta indica) and synthetic insecticides on Maruca vitrata damage and yield of cowpea (Vigna unguiculata).",
            "Pathogenic variability and virulence profiling of Ralstonia solanacearum isolates causing bacterial wilt of solanaceous crops in southwestern Nigeria."
        ],
        "design_advice": "Disease scoring on 1–5 or 1–9 ordinal scales. Compute Area Under the Disease Progress Curve (AUDPC). Percentage data must be subjected to Arcsine Square Root transformation ($\arcsin(\sqrt{p})$) or Log transformation prior to ANOVA.",
        "dmrt_advice": "Defend transformed disease mean separation: <i>'DMRT was performed on arcsine-transformed severity indices to separate treatment efficacy against viral/bacterial progression while satisfying ANOVA normality assumptions.'</i>"
    },
    "Horticulture & Post-Harvest Science": {
        "focus": "Olericulture, pomology, floriculture, seedling nursery media, blossom end rot calcium nutrition, shade netting, post-harvest shelf life, physiological weight loss, total soluble solids (Brix).",
        "journals": "Scientia Horticulturae, Postharvest Biology and Technology, HortScience, Journal of Horticultural Science and Biotechnology.",
        "sample_topics": [
            "Evaluating calcium-boron foliar supplementation on Blossom End Rot incidence, fruit firmness, and yield of determinate tomatoes in Western Nigeria.",
            "Effect of color shade nets and drip irrigation scheduling on microclimate, yield, and lycopene content of sweet pepper under tropical heat.",
            "Extending post-harvest storage longevity and sensory attributes of tomato fruits using chitosan edible coatings and modified atmosphere packaging."
        ],
        "design_advice": "Factorial RCBD with 3 to 4 replications. Measure physiological weight loss (PWL %) at 2-day intervals post-harvest, fruit firmness using a penetrometer, and titratable acidity/Brix.",
        "dmrt_advice": "Defend shelf-life separation: <i>'DMRT accurately identified the specific post-harvest treatment combinations that delayed fruit decay by over 7 days while preserving total soluble solids.'</i>"
    },
    "Soil Science & Land Resource Management": {
        "focus": "Pedology, soil chemistry, nutrient dynamics, fertilizer micro-dosing, soil organic carbon, cation exchange capacity (CEC), biological nitrogen fixation, spatial fertility mapping.",
        "journals": "Geoderma, Soil and Tillage Research, Communications in Soil Science and Plant Analysis, African Journal of Soil Science.",
        "sample_topics": [
            "Interactive effects of biochar amendment and inorganic fertilizer micro-dosing on nutrient leaching, soil microbial biomass, and maize yield in acidic ultisols.",
            "Phosphorus sorption isotherms and mycorrhizal inoculation efficiency in phosphorus-deficient savanna alfisols of Nigeria.",
            "Spatial variability of soil macronutrients and digital soil fertility mapping across varied toposequences using geostatistical kriging."
        ],
        "design_advice": "RCBD with core soil sampling (0–15 cm and 15–30 cm). Measure baseline physical and chemical properties prior to trial establishment. Run post-harvest soil nutrient balance calculations.",
        "dmrt_advice": "Defend soil chemical separation: <i>'DMRT provided the discriminating power needed to separate soil available phosphorus and exchangeable acidity levels across fertilizer application treatments.'</i>"
    },
    "Agricultural Economics & Agribusiness": {
        "focus": "Production economics, stochastic frontier production functions, technical efficiency, gross margin analysis, market integration, value chain governance, price transmission.",
        "journals": "Food Policy, Agricultural Economics, Journal of Agricultural Economics, African Journal of Agricultural and Resource Economics (AfJARE).",
        "sample_topics": [
            "Technical, allocative, and economic efficiency of smallholder rabbit producers in urban and peri-urban centers of Nigeria: A Stochastic Frontier approach.",
            "Price transmission, spatial market integration, and transaction costs across wholesale tomato markets in Southwestern Nigeria.",
            "Welfare impacts of agricultural input credit and adoption of climate-smart agronomic practices among savanna cereal farmers."
        ],
        "design_advice": "Multi-stage stratified random sampling ($N \ge 300$ households). Instrument pre-testing (Cronbach's alpha $\ge 0.70$). Test for multicollinearity (VIF < 10) and heteroskedasticity (Breusch-Pagan test).",
        "dmrt_advice": "Defend categorical group comparison: <i>'DMRT was employed across farm size quartiles and adoption categories to separate mean gross margins and return-on-investment across distinct producer clusters.'</i>"
    },
    "Agricultural Extension & Rural Development": {
        "focus": "Extension methodologies, technology adoption, innovation diffusion, farmer field schools, indigenous knowledge systems, gender empowerment, participatory rural appraisal.",
        "journals": "Journal of Agricultural Extension, Journal of Rural Studies, The Journal of Agricultural Education and Extension.",
        "sample_topics": [
            "Effectiveness of bilingual community radio extension advisories on the adoption of micro-dosing and climate-resilient practices among smallholder farmers.",
            "Determinants of youth participation in commercial cuniculture and poultry value chains in Southwestern Nigeria.",
            "Assessing farmer perceptions and barriers to adoption of biofortified provitamin-A maize varieties in the Guinea Savanna."
        ],
        "design_advice": "Survey research design with structured interview schedules. Use 5-point Likert scales, Focus Group Discussions (FGDs), and Key Informant Interviews (KIIs). Deploy probit/logit regression models for adoption analysis.",
        "dmrt_advice": "Defend Likert and group separation: <i>'DMRT was applied to mean perception scores across socio-economic strata to identify specific institutional barriers that significantly impaired technology adoption.'</i>"
    },
    "Aquaculture & Fisheries Management": {
        "focus": "Fish nutrition, water quality parameters, dissolved oxygen, fingerling nursing, stocking density, feed formulation, cold-season feeding management in Clarias and Tilapia.",
        "journals": "Aquaculture, Journal of the World Aquaculture Society, Aquaculture Research, African Journal of Aquatic Science.",
        "sample_topics": [
            "Growth performance, nutrient utilization, and carcass composition of African Catfish (Clarias gariepinus) fed black soldier fly (Hermetia illucens) meal.",
            "Evaluating water quality, ammonia toxicity, and gut histology of Tilapia (Oreochromis niloticus) under varied biofloc carbon-to-nitrogen ratios.",
            "Cold Harmattan water temperature management and lipid-enhanced diets for mitigating winter growth depression in catfish fingerlings."
        ],
        "design_advice": "CRD with triplicate or quadruplicate tanks/hapas per dietary treatment. Daily water quality monitoring (pH, DO, temperature, total ammonia nitrogen). Equalized initial stocking weights.",
        "dmrt_advice": "Defend specific growth rate (SGR) separation: <i>'DMRT clearly separated specific growth rates (SGR) and feed conversion ratios across dietary replacement tiers, establishing the maximum safe insect meal inclusion rate.'</i>"
    },
    "Animal Science (General)": {
        "focus": "General livestock production, integrated animal husbandry, breed characterization, reproductive efficiency, welfare, and sustainable mixed crop-livestock farming systems.",
        "journals": "Tropical Animal Health and Production, Livestock Science, South African Journal of Animal Science, Nigerian Journal of Animal Production.",
        "sample_topics": [
            "Evaluation of peri-urban livestock production systems and farmer adaptation strategies to seasonal feed scarcity.",
            "Phenotypic characterization, reproductive performance, and mortality risk factors in indigenous smallholder sheep and goat flocks.",
            "Economic feasibility and carcass evaluation of semi-intensive poultry and rabbit production for smallholder income diversification."
        ],
        "design_advice": "Randomized Complete Block Design (RCBD) using age, sex, or initial body weight as blocking factors. For multi-village survey studies, use stratified multi-stage random sampling.",
        "dmrt_advice": "Defend general livestock mean separation: <i>'Duncan's Multiple Range Test (DMRT) was used to separate production parameters across diverse housing and management groups, pinpointing the intervention tier with optimal biological and economic returns.'</i>"
    },
    "Crop & Plant Science (General)": {
        "focus": "Crop ecology, general agronomy, plant growth dynamics, yield components, seed germination, canopy light interception, and crop-weed competition in tropical agro-ecosystems.",
        "journals": "African Crop Science Journal, Field Crops Research, Experimental Agriculture, Journal of Agricultural Science.",
        "sample_topics": [
            "Comparative vegetative growth, phenological development, and harvest index of tropical cereals under variable planting dates and densities.",
            "Integrated crop and soil management options for improving smallholder productivity and resource-use efficiency in Guinea Savanna.",
            "Evaluation of intercropping spatial configurations and population densities on canopy architecture and aggregate grain yields."
        ],
        "design_advice": "Randomized Complete Block Design (RCBD) with at least 4 replications. Ensure adequate border rows are discarded to prevent border effects from inflating treatment means.",
        "dmrt_advice": "Defend agronomic mean separation: <i>'DMRT was selected to provide sensitive stepwise post-hoc ranking of crop performance across treatments, identifying the specific spacing or planting date that delivered maximum yield without incurring Type II error.'</i>"
    },
    "Plant Physiology & Weed Science": {
        "focus": "Photosynthetic gas exchange, stomatal conductance, water potential, stay-green physiology, weed-crop interference, critical period of weed control (CPWC), and herbicide mode-of-action.",
        "journals": "Weed Science, Weed Research, Plant Physiology and Biochemistry, Crop Protection.",
        "sample_topics": [
            "Determination of the critical period of weed interference and yield loss thresholds in dry-season furrow-irrigated tomato.",
            "Photosynthetic efficiency, chlorophyll fluorescence (Fv/Fm), and membrane stability in drought-tolerant maize inbred lines under terminal water stress.",
            "Efficacy and residual activity of pre-emergence herbicide mixtures on weed suppression, crop tolerance, and nodulation in grain legumes."
        ],
        "design_advice": "Factorial RCBD or Split-Plot Design. Measure weed dry biomass using quadrat sampling (0.5m × 0.5m) and determine physiological indices (SPAD chlorophyll index, relative water content, leaf area index) at fixed phenological growth stages.",
        "dmrt_advice": "Defend physiological and weed biomass separation: <i>'DMRT enabled clear pairwise separation of weed suppression efficacy and physiological stay-green indices across timing treatments, revealing the exact duration threshold where weed interference triggered significant crop yield loss.'</i>"
    }
}


def render_student_tutor():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 🎓 Tuteur de Recherche Agronomique & Mentor de Thèse")
        st.caption("Superviseur de recherche socratique guidant les étudiants dans la rigueur scientifique, la conception biométrique et la préparation aux soutenances de mémoire et de thèse.")
    else:
        st.markdown("### 🎓 Agricultural Research Tutor & Thesis Mentor")
        st.caption("A Socratic research supervisor that guides students through scientific rigor, statistical design, and thesis defense across all agricultural disciplines.")

    c1, c2 = st.columns([1, 1.3])
    with c1:
        degree_level = st.selectbox(
            "Niveau Académique :" if is_fr else "Academic Level:",
            [
                "Undergraduate (B.Sc / B.Agric)",
                "Master of Science (M.Sc)",
                "Doctor of Philosophy (Ph.D)"
            ],
            index=1
        )
    with c2:
        field_of_study = st.selectbox(
            "Département / Spécialisation :" if is_fr else "Department / Specialization:",
            DEPARTMENTS,
            index=1  # Default to Animal Nutrition
        )

    # Fetch discipline metadata with intelligent fallback
    if field_of_study in DISCIPLINE_METADATA:
        meta = DISCIPLINE_METADATA[field_of_study]
    elif "Animal" in field_of_study or "Pasture" in field_of_study or "Livestock" in field_of_study:
        meta = DISCIPLINE_METADATA["Animal Science (General)"]
    elif "Crop" in field_of_study or "Plant" in field_of_study or "Weed" in field_of_study or "Agronomy" in field_of_study:
        meta = DISCIPLINE_METADATA["Crop & Plant Science (General)"]
    else:
        meta = DISCIPLINE_METADATA["Animal Nutrition & Feed Technology"]

    # Department Banner Callout
    st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #1B5E20; background: #F1F8E9; padding: 0.6rem 1rem; margin: 0.5rem 0 1rem 0;">
    <div style="font-size: 0.85rem; font-weight: 700; color: #1B5E20;">
        🔬 Academic Focus: {field_of_study} ({degree_level})
    </div>
    <div style="font-size: 0.75rem; color: #33691E; line-height: 1.4;">
        <b>Disciplinary Core:</b> {meta['focus']}
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("#### 🗺️ 10-Stage Research Roadmap")
    current_stage = st.select_slider(
        "Étape Actuelle du Mémoire / Thèse :" if is_fr else "Current Thesis Stage:",
        options=[
            "1. Topic Ideation",
            "2. Research Questions",
            "3. Specific Objectives",
            "4. Hypotheses (H0/H1)",
            "5. Literature Synthesis",
            "6. Experimental Design",
            "7. Data Collection",
            "8. Statistical Analysis (DMRT/ANOVA)",
            "9. Results Interpretation",
            "10. Thesis Defense & Viva"
        ],
        value="8. Statistical Analysis (DMRT/ANOVA)"
    )

    st.markdown(f"#### 💡 Guidance for: **{current_stage}** — *{field_of_study}* ({degree_level})")

    # Render specific guidance for selected stage
    if "8. Statistical Analysis" in current_stage:
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🎓 Thesis Supervisor Advisory: Post-Hoc Test Selection in {field_of_study}</div>
<b>Dear {degree_level} Researcher in {field_of_study}</b>:<br>
When defending your thesis before an external examiner, you will likely face the quintessential defense challenge: 
<i>"Why did you use Duncan's Multiple Range Test (DMRT) rather than Tukey or LSD for your {field_of_study} data?"</i><br><br>
<b>Your Model Viva Defense Answer</b>:<br>
{meta['dmrt_advice']}<br><br>
<b>Statistical Rigor Checklist for {degree_level}</b>:
• <b>Test for Normality & Homogeneity of Variance</b>: Ensure Shapiro-Wilk ($P > 0.05$) and Levene's test ($P > 0.05$) pass prior to running ANOVA.<br>
• <b>Avoid Misinterpreting Non-Significance</b>: If treatments are non-significant ($P > 0.05$), do NOT apply DMRT mean lettering.<br>
• <b>Report Standard Error of Mean (SEM)</b>: External examiners require Pooled SEM alongside treatment means rather than individual standard deviations.
</div>
""", unsafe_allow_html=True)

    elif "1. Topic Ideation" in current_stage:
        topics_html = "".join([f"<li><i>{t}</i></li>" for t in meta["sample_topics"]])
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🌱 Formulating a High-Impact, Fundable Research Gap in {field_of_study}</div>
Avoid generic, superficial titles like <i>'Effect of feed on animals'</i> or <i>'Yield of crops'</i>.<br>
In <b>{field_of_study}</b>, competitive {degree_level} research must address a clear biological, edaphic, or economic mechanism.<br><br>
<b>Recommended Research Topic Blueprints for {field_of_study}</b>:
<ul>
{topics_html}
</ul>
<b>Supervisor Tip for {degree_level}</b>: Ensure your research addresses climate adaptation, input cost reduction, or genetic food security within African agro-ecologies.
</div>
""", unsafe_allow_html=True)

    elif "6. Experimental Design" in current_stage:
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📐 Gold-Standard Experimental Design Protocol for {field_of_study}</div>
<b>Design Strategy</b>:<br>
{meta['design_advice']}<br><br>
<b>Core Guardrails for {degree_level}</b>:
• <b>Randomization</b>: Use computer-generated random numbers or Latin square tables. Never place treatments sequentially.<br>
• <b>Replication & Power</b>: Ensure adequate degrees of freedom for error ($DF_{{error}} \ge 12$) to achieve statistical power $\ge 0.80$.<br>
• <b>Guard against Confounding</b>: Account for litter effects, pen location microclimates, or soil toposequence gradients by blocking.
</div>
""", unsafe_allow_html=True)

    elif "5. Literature Synthesis" in current_stage:
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📚 Literature Synthesis & Citation Standards in {field_of_study}</div>
To build academic authority in <b>{field_of_study}</b>, at least 70% of your citations must come from high-impact peer-reviewed journals within the last 5 to 7 years.<br><br>
<b>Top Tier Disciplinary Journals Recommended</b>:
• <i>{meta['journals']}</i><br>
• CGIAR Research Repositories (ILRI, IITA, AfricaRice, CIMMYT, CIAT).<br><br>
<b>Supervisor Rule</b>: Zero unverified Wikipedia citations. Cite original methodological authors (e.g., AOAC 2019 for proximal analysis, SAS/R packages for biometrics).
</div>
""", unsafe_allow_html=True)

    elif "10. Thesis Defense & Viva" in current_stage:
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">🎓 Top Viva Questions Asked by External Examiners in {field_of_study}</div>
<b>Prepare for these 3 rigorous viva questions</b>:
1. <i>"What was the specific biological or economic rationale for the treatment levels you selected in your {field_of_study} trial?"</i><br>
2. <i>"How did you confirm that your statistical model accounted for confounding variables (e.g., pen microclimate, animal baseline weight, soil gradient)?"</i><br>
3. <i>"If an agricultural extension officer or smallholder farmer adopts your findings today, what is the exact economic return-on-investment and practical risk?"</i><br><br>
<b>Viva Strategy</b>: Answer directly, ground your statements in your ANOVA tables, and present confidence without being defensive.
</div>
""", unsafe_allow_html=True)

    else:
        # Stages 2, 3, 4, 7, 9
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📋 Supervisor Checklist for {current_stage} ({field_of_study})</div>
• <b>Alignment with Research Questions</b>: Ensure every specific objective maps directly to a measurable biological trait and statistical model.<br>
• <b>Methodological Fidelity</b>: Adhere to standard laboratory and field sampling protocols calibrated for {field_of_study}.<br>
• <b>Data Integrity</b>: Maintain raw field data logs with double-entry validation prior to statistical analysis.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Interactive Socratic Supervisor Chat Assistant
    st.markdown("#### 💬 Ask Your Socratic Thesis Supervisor")
    st.caption("Ask specific questions regarding research proposals, experimental design defense, or external examiner viva preparation:")

    # Live Gemini Key Connection Status & Settings
    gemini_key = get_gemini_api_key()
    c_eng1, c_eng2 = st.columns([2, 1])
    with c_eng1:
        if gemini_key:
            st.markdown("🟢 **Live Google Gemini Supervisor Connected** *(Secured via Cloud Secrets)*")
        else:
            st.markdown("⚡ **Built-in Socratic Thesis Engine Active** *(Offline Mode • Free)*")
    with c_eng2:
        if not gemini_key:
            with st.expander("🔑 Connect Gemini Key", expanded=False):
                tutor_key_input = st.text_input(
                    "Google Gemini Key:",
                    value="",
                    type="password",
                    placeholder="AIzaSy...",
                    key="tutor_gemini_key_input",
                    help="Enter free Gemini key from aistudio.google.com"
                )
                cleaned_tk = (tutor_key_input or "").strip().strip("'\"")
                if cleaned_tk:
                    set_gemini_api_key(cleaned_tk)
                    gemini_key = cleaned_tk
                    val = validate_gemini_key(cleaned_tk)
                    if val.get("valid"):
                        st.success(f"🟢 {val.get('message')}")
                    else:
                        st.error(f"🔴 {val.get('message')}")

    c_q1, c_q2 = st.columns([3, 1])
    with c_q1:
        student_query = st.text_input(
            "Your Research or Defense Question:",
            placeholder=f"e.g. How do I defend using CRD instead of RCBD in my {field_of_study} thesis?"
        )
    with c_q2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        ask_btn = st.button("🧑‍🏫 Ask Supervisor", use_container_width=True)

    # Preset Quick Defense Questions
    st.caption("Quick Viva Inquiries:")
    pq1, pq2, pq3 = st.columns(3)
    preset_chosen = ""
    if pq1.button("⚖️ Defend CRD vs RCBD"):
        preset_chosen = f"How do I defend using Completely Randomized Design (CRD) versus RCBD in {field_of_study}?"
    if pq2.button("📊 Defend DMRT vs LSD"):
        preset_chosen = f"Why did I choose Duncan's Multiple Range Test (DMRT) over LSD or Tukey in {field_of_study}?"
    if pq3.button("🧪 Sample Size Justification"):
        preset_chosen = f"How do I justify my experimental sample size and replication number in {field_of_study} to my external examiner?"

    final_query = preset_chosen if preset_chosen else student_query

    if (ask_btn and student_query) or preset_chosen:
        with st.spinner("Formulating personalized Socratic thesis supervisor guidance..."):
            active_reg = st.session_state.get("active_region")
            active_key = get_gemini_api_key()

            live_response = ""
            if active_key:
                supervisor_prompt = f"""You are a distinguished Senior University Professor and External Examiner in Agricultural Sciences, serving as a Socratic Thesis Supervisor for a {degree_level} student in {field_of_study}.
The student is at the stage of '{current_stage}' and is preparing to defend their research methodology before an external viva panel.
Student Inquiry: "{final_query}"

Provide an authoritative, Socratic, and intellectually rigorous advisory structured as:
### 1. 🎯 Socratic Viva Defense Strategy
Explain exactly how the student should articulate their answer calmly and authoritatively before the external examination panel, stating the biological rationale first before the mathematical model.

### 2. 🔬 Theoretical & Disciplinary Justification
Detail the specific biological, physiological, edaphic, or biometric principles in {field_of_study} that justify this protocol.

### 3. ⚠️ 3 Tricky Viva Counter-Questions from External Examiners
List 3 realistic traps external examiners love to pose on this topic, with the exact bulletproof counter-responses.

### 4. 📚 Gold-Standard African & International Citations
Provide 3–4 classic and recent peer-reviewed methodology citations to quote during the viva (e.g., Cochran, Steel & Torrie, Gomez & Gomez, AOAC, or NARS/CGIAR protocols)."""

                try:
                    orch_res = call_live_llm_orchestration(supervisor_prompt, api_key=active_key, provider="gemini", active_region=active_reg)
                    live_response = orch_res.get("final_synthesis", "")
                except Exception:
                    live_response = ""

            if live_response:
                st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #2E7D32; background: #F1F8F2; margin-top: 1rem; padding: 1.2rem; border-radius: 6px;">
    <div style="font-weight: 700; color: #1B5E20; font-size: 1.05rem; margin-bottom: 0.4rem;">
        🧑‍🏫 Socratic Thesis Supervisor Guidance (Live Gemini Cloud Intelligence)
    </div>
    <div style="font-size: 0.82rem; color: #37474F; margin-bottom: 0.8rem;">
        <b>Inquiry</b>: <i>"{final_query}"</i> &bull; <b>Discipline</b>: {field_of_study} ({degree_level}) &bull; <b>Stage</b>: {current_stage}
    </div>
</div>
""", unsafe_allow_html=True)
                st.markdown(live_response)
            else:
                st.markdown(f"""
<div class="agri-card" style="border-left: 4px solid #2E7D32; background: #FFFFFF; margin-top: 1rem; padding: 1.2rem;">
    <div style="font-weight: 700; color: #1B5E20; margin-bottom: 0.5rem;">
        🎓 Supervisor Guidance for: <i>"{final_query}"</i>
    </div>
    <div style="font-size: 0.85rem; line-height: 1.6; color: #212121;">
        <b>Socratic Defense Strategy</b>:<br>
        When answering this inquiry before your {degree_level} defense panel:
        <ol>
            <li><b>Acknowledge the Underlying Statistical Principle</b>: Demonstrate that you understand the trade-off between Type I and Type II error, and the assumptions of experimental homogeneity.</li>
            <li><b>Ground your Choice in {field_of_study} Realities</b>: For instance, in laboratory feeding crates or controlled metabolic cages, environmental homogeneity justifies CRD; whereas in open fields or pasture paddocks, soil and topography variations necessitate blocking (RCBD).</li>
            <li><b>Quote Published African & Global Standards</b>: Cite established institutional guidelines (such as CSIR, KALRO, ARC, IER, NAPRI, IITA, NIHORT, AOAC depending on your agro-ecological jurisdiction) to confirm that your protocol mirrors published peer-reviewed methodology.</li>
        </ol>
        <i>Summary: "Always state the biological reason first, then reinforce it with the mathematical model."</i>
    </div>
</div>
""", unsafe_allow_html=True)
