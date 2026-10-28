"""
Generates benchmark agricultural datasets for AgroBiometrix
"""

import json
import numpy as np
import pandas as pd

np.random.seed(42)

# 1. Maize Agronomy Trials (NPK x Irrigation x Cultivar)
treatments = [
    "T0_Local_Check",
    "T1_NPK_Standard",
    "T2_NPK_Plus_Biochar",
    "T3_Nano_NPK_Precision",
    "T4_Integrated_Organic_Manure"
]
irrigations = ["Rainfed", "Supplemental_Drip"]
reps = ["Rep_1", "Rep_2", "Rep_3", "Rep_4"]

base_yields = {
    "T0_Local_Check": 2.8,
    "T1_NPK_Standard": 4.6,
    "T2_NPK_Plus_Biochar": 5.9,
    "T3_Nano_NPK_Precision": 6.4,
    "T4_Integrated_Organic_Manure": 5.1
}

maize_rows = []
for trt in treatments:
    for irr in irrigations:
        irr_boost = 1.2 if irr == "Supplemental_Drip" else 0.0
        for rep in reps:
            yield_val = base_yields[trt] + irr_boost + np.random.normal(0, 0.28)
            height = 140 + base_yields[trt] * 12 + (15 if irr == "Supplemental_Drip" else 0) + np.random.normal(0, 4.5)
            cob = 12 + base_yields[trt] * 1.1 + np.random.normal(0, 0.6)
            days = 60 - base_yields[trt] * 1.5 + np.random.normal(0, 1.2)
            maize_rows.append({
                "Treatment": trt,
                "Irrigation": irr,
                "Replication": rep,
                "Grain_Yield_tons_ha": round(max(0.5, yield_val), 2),
                "Plant_Height_cm": round(height, 1),
                "Cob_Length_cm": round(cob, 1),
                "Days_to_Anthesis": round(days, 1)
            })

df_maize = pd.DataFrame(maize_rows)
df_maize.to_csv("data/sample_maize_agronomy_trials.csv", index=False)
print("Saved data/sample_maize_agronomy_trials.csv")

# 2. Cattle Heat Tolerance and Genomic Data
breeds = {
    "N'Dama": {"temp": 38.4, "resp": 28, "milk": 4.5, "weight": 290, "thi_sens": 0.12},
    "White Fulani": {"temp": 38.7, "resp": 36, "milk": 7.2, "weight": 380, "thi_sens": 0.22},
    "Muturu": {"temp": 38.3, "resp": 26, "milk": 3.8, "weight": 220, "thi_sens": 0.10},
    "Sokoto Gudali": {"temp": 38.9, "resp": 38, "milk": 6.8, "weight": 410, "thi_sens": 0.25}
}

cattle_rows = []
animal_id = 1001
for breed, params in breeds.items():
    # 250 animals per breed = 1000 animals
    for i in range(250):
        sex = np.random.choice(["Female", "Male"], p=[0.75, 0.25])
        age = np.random.uniform(2.0, 7.5)
        thi = np.random.uniform(72, 88)
        thi_stress = max(0, thi - 76) * params["thi_sens"]
        
        body_temp = params["temp"] + thi_stress + np.random.normal(0, 0.25)
        resp_rate = params["resp"] + thi_stress * 15 + np.random.normal(0, 3.5)
        milk = (params["milk"] - thi_stress * 1.1 + np.random.normal(0, 0.6)) if sex == "Female" else np.nan
        weight = params["weight"] + (age * 12) + (50 if sex == "Male" else 0) + np.random.normal(0, 15)
        hsp_allele = np.random.choice(["HSP70_A1_Resistant", "HSP70_A2_Intermediate", "HSP70_B1_Susceptible"], p=[0.5, 0.35, 0.15] if "N'Dama" in breed or "Muturu" in breed else [0.2, 0.45, 0.35])
        tryp_status = "Tolerant" if breed in ["N'Dama", "Muturu"] else np.random.choice(["Tolerant", "Susceptible"], p=[0.15, 0.85])
        
        cattle_rows.append({
            "Animal_ID": f"AG-{animal_id}",
            "Breed": breed,
            "Sex": sex,
            "Age_Years": round(age, 1),
            "THI_Index": round(thi, 1),
            "Body_Temperature_C": round(body_temp, 2),
            "Respiration_Rate_bpm": round(resp_rate, 1),
            "Milk_Yield_kg_day": round(max(0, milk), 2) if not np.isnan(milk) else np.nan,
            "Body_Weight_kg": round(weight, 1),
            "HSP_Genotype": hsp_allele,
            "Trypanotolerance": tryp_status
        })
        animal_id += 1

df_cattle = pd.DataFrame(cattle_rows)
df_cattle.to_csv("data/sample_cattle_heat_tolerance.csv", index=False)
print("Saved data/sample_cattle_heat_tolerance.csv")

# 3. Soil Profiles
soil_data = [
    {"Location": "Kaduna (Zaria)", "Zone": "Northern Guinea Savanna", "Soil_pH": 5.8, "Nitrogen_pct": 0.08, "Phosphorus_ppm": 7.4, "Potassium_cmol_kg": 0.22, "Organic_Carbon_pct": 0.65, "Texture": "Sandy Loam", "CEC_cmol_kg": 6.5, "Annual_Rainfall_mm": 1050},
    {"Location": "Kano (Bichi)", "Zone": "Sudan Savanna", "Soil_pH": 6.3, "Nitrogen_pct": 0.05, "Phosphorus_ppm": 5.1, "Potassium_cmol_kg": 0.18, "Organic_Carbon_pct": 0.42, "Texture": "Loamy Sand", "CEC_cmol_kg": 4.8, "Annual_Rainfall_mm": 780},
    {"Location": "Ibadan (IITA)", "Zone": "Derived Savanna / Forest", "Soil_pH": 6.2, "Nitrogen_pct": 0.14, "Phosphorus_ppm": 12.8, "Potassium_cmol_kg": 0.38, "Organic_Carbon_pct": 1.15, "Texture": "Sandy Clay Loam", "CEC_cmol_kg": 11.2, "Annual_Rainfall_mm": 1320},
    {"Location": "Sokoto (Wamakko)", "Zone": "Sahelian Zone", "Soil_pH": 6.7, "Nitrogen_pct": 0.03, "Phosphorus_ppm": 3.8, "Potassium_cmol_kg": 0.15, "Organic_Carbon_pct": 0.28, "Texture": "Sand", "CEC_cmol_kg": 3.5, "Annual_Rainfall_mm": 550},
    {"Location": "Enugu (Nsukka)", "Zone": "Humid Forest Margin", "Soil_pH": 4.9, "Nitrogen_pct": 0.12, "Phosphorus_ppm": 6.2, "Potassium_cmol_kg": 0.25, "Organic_Carbon_pct": 1.05, "Texture": "Sandy Clay", "CEC_cmol_kg": 9.8, "Annual_Rainfall_mm": 1680},
    {"Location": "Nairobi (Kabete)", "Zone": "East African Highland", "Soil_pH": 5.6, "Nitrogen_pct": 0.18, "Phosphorus_ppm": 14.5, "Potassium_cmol_kg": 0.55, "Organic_Carbon_pct": 2.10, "Texture": "Clay (Nitisol)", "CEC_cmol_kg": 18.4, "Annual_Rainfall_mm": 1020}
]
df_soil = pd.DataFrame(soil_data)
df_soil.to_csv("data/sample_soil_profiles_africa.csv", index=False)
print("Saved data/sample_soil_profiles_africa.csv")

# 4. African Evidence Base JSON
evidence_db = {
    "trypanosomiasis_resistance": [
        {"Study": "Hanotte et al. (2003)", "Population": "N'Dama x Boran Cross", "Trait": "Parasitaemia & PCV Control", "Sample_Size": 176, "Method": "QTL Linkage Mapping", "Major_Finding": "Identified 18 chromosome regions (BTA2, BTA7, BTA14) controlling anaemia and parasitaemia control.", "Evidence_Strength": "Strong (Replicated)"},
        {"Study": "Kim et al. (2020)", "Population": "N'Dama, Muturu, Baoulé", "Trait": "Trypanotolerance Signature", "Sample_Size": 420, "Method": "Whole-Genome Sequencing & XP-EHH", "Major_Finding": "Selective sweep at TICAM1 and TLR signaling loci; indigenous West African taurines possess unique ancestral haplotypes.", "Evidence_Strength": "Strong"},
        {"Study": "Obeidat et al. (2022)", "Population": "Muturu (Nigeria)", "Trait": "Disease Response & Haematology", "Sample_Size": 180, "Method": "Targeted Candidate Gene Panel", "Major_Finding": "Hemoglobin polymorphisms and cytokine expression profile contribute to mild parasitaemia without severe wasting.", "Evidence_Strength": "Moderate"}
    ],
    "heat_tolerance_cattle": [
        {"Study": "Dikmen et al. (2014)", "Population": "SLICK Zebu x Dairy Cross", "Trait": "Thermoregulation & Rectal Temp", "Sample_Size": 350, "Method": "Candidate Gene & Phenotyping", "Major_Finding": "PRLR (Prolactin Receptor) slick hair gene mutation lowers core body temperature by 0.5-0.8°C under severe heat stress.", "Evidence_Strength": "Strong (Replicated)"},
        {"Study": "Taye et al. (2017)", "Population": "African Indigenous Zebu (Fulani, Boran)", "Trait": "Heat Shock Response", "Sample_Size": 284, "Method": "RNA-Seq & SNP Chip", "Major_Finding": "HSP70 and HSP90 upregulation enhances cellular cytoprotection during peak solar radiation periods.", "Evidence_Strength": "Strong"},
        {"Study": "Gautier et al. (2019)", "Population": "West African Zebu vs Taurine", "Trait": "Arid Adaptation Signatures", "Sample_Size": 512, "Method": "Population Genomics (Fst scan)", "Major_Finding": "Adaptive introgressions linked to water conservation (aquaporins) and cutaneous evaporation in Sahelian cattle.", "Evidence_Strength": "Moderate"}
    ],
    "maize_drought_tolerance": [
        {"Study": "Badu-Apraku et al. (2016)", "Population": "Early-Maturity Maize (IITA)", "Trait": "Drought & Heat Tolerance", "Sample_Size": 140, "Method": "GxE Biplot & Multi-Environment Trials", "Major_Finding": "TZE-W Pop x TZE-Y Pop showed shortest anthesis-silking interval (ASI < 2.5 days) and 35% higher yield under moisture stress.", "Evidence_Strength": "Strong (Replicated)"},
        {"Study": "Menkir et al. (2020)", "Population": "Sub-Saharan Intermediate Maize", "Trait": "Stay-Green & Canopy Temperature", "Sample_Size": 210, "Method": "Spectral Phenotyping & GWAS", "Major_Finding": "Significant QTL on chromosome 1 and 8 correlated with functional stay-green and prolonged photosynthesis during grain filling.", "Evidence_Strength": "Strong"}
    ]
}

with open("data/african_evidence_base.json", "w") as f:
    json.dump(evidence_db, f, indent=2)
print("Saved data/african_evidence_base.json")
