"""
AGROBIOMETRIX -- CORE CROP & AGRO-ECOLOGICAL TAXONOMY ENGINE
Exhaustive Pan-African Crop Species, Agro-Ecological Environments,
and Biometrical Trait Profiles
"""

# Categorized Pan-African Crops List
PAN_AFRICAN_CROPS = [
    # Cereals & Grains
    "Maize (Zea mays)",
    "Sorghum (Sorghum bicolor)",
    "Pearl Millet (Pennisetum glaucum)",
    "Finger Millet (Eleusine coracana)",
    "Upland & Lowland Rice (Oryza sativa / O. glaberrima)",
    "Teff (Eragrostis tef)",
    "Fonio (Digitaria exilis)",
    "Wheat (Triticum aestivum)",
    
    # Roots, Tubers & Bananas
    "Cassava (Manihot esculenta)",
    "White Yam (Dioscorea rotundata)",
    "Water Yam (Dioscorea alata)",
    "Sweet Potato (Ipomoea batatas)",
    "Irish Potato (Solanum tuberosum)",
    "Plantain & Cooking Banana (Musa spp.)",
    "Cocoyam & Taro (Colocasia esculenta)",
    "Enset (Ensete ventricosum)",
    
    # Grain Legumes & Pulses
    "Cowpea (Vigna unguiculata)",
    "Soybean (Glycine max)",
    "Groundnut / Peanut (Arachis hypogaea)",
    "Pigeonpea (Cajanus cajan)",
    "Chickpea (Cicer arietinum)",
    "Bambara Groundnut (Vigna subterranea)",
    "Common Bean (Phaseolus vulgaris)",
    
    # Horticulture & Vegetables
    "Tomato (Solanum lycopersicum)",
    "Hot Pepper / Chili (Capsicum annuum / C. frutescens)",
    "Onion (Allium cepa)",
    "Okra (Abelmoschus esculentus)",
    "African Eggplant / Garden Egg (Solanum aethiopicum)",
    "Amaranth & Indigenous Leafy Vegetables (Amaranthus spp.)",
    "Watermelon (Citrullus lanatus)",
    
    # Industrial, Oilseeds & Cash Export Crops
    "Cocoa (Theobroma cacao)",
    "Oil Palm (Elaeis guineensis)",
    "Coffee - Arabica & Robusta (Coffea spp.)",
    "Cashew (Anacardium occidentale)",
    "Sesame / Benniseed (Sesamum indicum)",
    "Cotton (Gossypium hirsutum)",
    "Sugarcane (Saccharum officinarum)",
    
    # Custom Option
    "➕ Enter Any Other African Crop (Custom Input)"
]

PAN_AFRICAN_ENVIRONMENTS = [
    "Sahelian Savanna (Mali, Niger, Senegal, Northern Burkina Faso)",
    "Sudan Savanna (Northern Nigeria, Southern Mali, Burkina Faso, Northern Ghana)",
    "Northern Guinea Savanna (Kaduna, Bauchi, Northern Benin, Northern Togo)",
    "Southern Guinea Savanna & Middle Belt (Central Nigeria, Central Ghana)",
    "Derived Savanna & Transition Zone (South-West Nigeria, Ashanti Ghana)",
    "Lowland Humid Rainforest Belt (Southern Nigeria, Coastal Ghana, Ivory Coast, Cameroon)",
    "East African Highlands (Central Kenya, Rift Valley, Uganda Highlands, Rwanda)",
    "Lake Victoria Basin (Western Kenya, Uganda Lakeshore, NW Tanzania)",
    "Southern Highlands & Miombo Plateau (Tanzania Highlands, Zambia, Malawi)",
    "Southern Africa Highveld & Bushveld (South Africa, Zimbabwe, Botswana)",
    "Horn of Africa Montane & ASAL (Ethiopian Highlands, Northern Kenya ASAL)",
    "Mediterranean & Winter-Rainfall Belt (Western Cape South Africa)",
    "➕ Enter Custom Agro-Ecological Environment"
]

def get_crop_breeding_profile(crop_name: str, custom_crop_text: str = "") -> dict:
    """Returns biological breeding traits, default weights, genomic QTLs, and germplasm strategy."""
    c_lower = (custom_crop_text if "custom" in crop_name.lower() and custom_crop_text else crop_name).lower()
    
    # 1. Roots & Tubers
    if any(k in c_lower for k in ["cassava", "yam", "potato", "tuber", "cocoyam", "enset"]):
        return {
            "category": "Roots, Tubers & Bananas",
            "traits": [
                ("Viral Resistance (CMD2/CMD3 & CBSD Field Immunity)", 85),
                ("Dry Matter % & Starch Pasting Viscosity", 80),
                ("Fresh Storage Root / Tuber Yield (t/ha)", 75),
                ("PPD Delay & Underground Storage Longevity", 70)
            ],
            "germplasm": "Deploy elite virus-indexed tissue-culture clones (e.g. TME 419, NAROCASS 1, or Obasanjo-2 background) possessing broad-spectrum immunity.",
            "genomics": "• Chromosome 12 CMD2 monogenic locus & CMD3 epistatic polygenic QTLs for begomovirus immunity.<br>• Candidate starch synthase (GBSS1) alleles conferring high dry matter (>32%) and low post-harvest physiological deterioration (PPD).",
            "trials": "Multi-Environment Trials (MET) across 6 harvest dates (9, 12, 15 months) using AMMI/GGE biplots to evaluate root rot resistance and bulking speed.",
            "adoption": "Ensure poundability / gari swelling ratio >3.2x and minimal root cyanogenic glucosides (<10 mg HCN/kg fresh weight) for farmer and market acceptance."
        }
    
    # 2. Grain Legumes
    elif any(k in c_lower for k in ["cowpea", "soybean", "groundnut", "peanut", "pigeonpea", "chickpea", "bambara", "bean", "legume"]):
        return {
            "category": "Grain Legumes & Pulses",
            "traits": [
                ("Pod Borer (Maruca) & Alectra/Striga Resistance", 85),
                ("Biological Nitrogen Fixation (BNF) & Nodulation", 80),
                ("Grain Yield Potential & Pod Load (t/ha)", 75),
                ("Drought Escape (Short Duration < 65 d)", 70)
            ],
            "germplasm": "Deploy modern dual-purpose grain-fodder varieties (e.g. SAMPEA 20-T / Songotra Bt background or TGx soybean lines) with promiscuous nodulation.",
            "genomics": "• Cry1Ab endotoxin cassette & candidate Maruca resistance QTLs on Linkage Group 7.<br>• Host-plant signaling gene loci (NFR1/NFR5) optimizing symbiotic recognition with indigenous Bradyrhizobium strains.",
            "trials": "Split-plot trials across 6 rangeland sites evaluating nodule dry weight, nitrogen harvest index, and pod borer damage under zero vs micro-dose phosphorus.",
            "adoption": "Ensure seed coat color, cooking time (<45 minutes), and high fodder digestibility (>60% IVDMD) to support livestock integration."
        }
        
    # 3. Vegetables & Horticulture
    elif any(k in c_lower for k in ["tomato", "pepper", "onion", "okra", "eggplant", "vegetable", "chili", "watermelon", "amaranth"]):
        return {
            "category": "Horticulture & Vegetables",
            "traits": [
                ("Viral Vector Resistance (TYLCV / Whitefly Defense)", 85),
                ("Abiotic Heat Resilience & Blossom-End Rot Defense", 80),
                ("Marketable Fruit Yield & BRIX Soluble Solids", 75),
                ("Pericarp Firmness & Transport Bruising Resistance", 70)
            ],
            "germplasm": "Deploy F1 determinate/indeterminate hybrids introgressed with Ty-1/Ty-3 begomovirus resistance genes and heat-tolerant pollen viability.",
            "genomics": "• Introgressed Solanum chilense Ty-1/Ty-3 and Ty-5 loci suppressing viral DNA accumulation.<br>• Calcium xylem-partitioning and membrane stability QTLs preventing apoplastic calcium leakage under high vapor pressure deficit (VPD).",
            "trials": "Protected vs open-field randomized block trials across dry season and wet season cycles assessing whitefly counts and fruit quality grades.",
            "adoption": "Thick pericarp (>6 mm) ensuring extended shelf-life (>14 days at 25°C) for long-distance transport to terminal urban wholesale markets."
        }
        
    # 4. Cash, Oilseeds & Tree Crops
    elif any(k in c_lower for k in ["cocoa", "coffee", "oil palm", "cashew", "sesame", "cotton", "sugarcane", "rubber"]):
        return {
            "category": "Industrial, Oilseeds & Cash Export Crops",
            "traits": [
                ("Fungal & Insect Resistance (Black Pod / Rust / Mirids)", 85),
                ("Canopy Thermotolerance & Water-Use Efficiency", 80),
                ("Commercial Export Yield (Bean / Oil / Fiber kg/ha)", 75),
                ("Specialty Quality Grade (Fat %, Acidity, Fiber Micronaire)", 70)
            ],
            "germplasm": "Deploy clonal hybrid seed gardens or clonal cuttings bred for early bearing, dwarfing habit, and disease tolerance.",
            "genomics": "• Resistance gene analogs (RGAs) and NBS-LRR disease resistance clusters on major linkage groups.<br>• Fatty acid / bean secondary metabolite biosynthetic pathways ensuring export-grade organoleptic properties.",
            "trials": "Multi-year clonal evaluation trials across varied rainfall gradients assessing pod/fruit load, canopy light interception, and harvest index.",
            "adoption": "Compliance with international buyer standards (e.g. EU deforestation regulation, zero chemical residue tolerances, high premium grades)."
        }
        
    # 5. Cereals & Default Universal
    else:
        return {
            "category": "Cereal Crops & Savanna Grains",
            "traits": [
                ("Drought Escape / Tolerance (Short ASI < 2.5 d)", 85),
                ("Canopy Stay-Green & Cell Membrane Stability", 80),
                ("Grain Yield Potential (t/ha)", 75),
                ("Biotic Stress (Striga hermonthica / Stem Borer)", 70)
            ],
            "germplasm": "Deploy extra-early to early maturity composites and single-cross hybrids possessing synchronized flowering and drought escape.",
            "genomics": "• Chromosome 1 and Chromosome 8 QTLs governing stay-green functional canopy duration and delayed senescence.<br>• Striga hermonthica germination stimulant reduction genes (lgs1) suppressing parasitic weed attachment.",
            "trials": "Multi-Environment Trials (MET) across at least 6 representative agro-ecological sites using AMMI or GGE biplots for G×E stability analysis.",
            "adoption": "Flint endosperm hardness (>70%) preventing storage weevil damage, combined with preferred traditional food flour milling and swelling quality."
        }

def get_crop_climate_profile(crop_name: str, custom_crop_text: str = "") -> dict:
    """Returns baseline yield, unit, price, and climate vulnerability factors."""
    c_lower = (custom_crop_text if "custom" in crop_name.lower() and custom_crop_text else crop_name).lower()
    
    if any(k in c_lower for k in ["cassava"]):
        return {"name": "Cassava", "unit": "t/ha", "base_yield": 28.5, "price_per_unit": 65_000, "growing_days": "300-360 days", "water_sens": 0.85}
    elif any(k in c_lower for k in ["yam"]):
        return {"name": "Yam", "unit": "t/ha", "base_yield": 18.0, "price_per_unit": 120_000, "growing_days": "210-240 days", "water_sens": 0.95}
    elif any(k in c_lower for k in ["sweet potato", "irish potato"]):
        return {"name": "Potato", "unit": "t/ha", "base_yield": 22.0, "price_per_unit": 70_000, "growing_days": "110-130 days", "water_sens": 0.90}
    elif any(k in c_lower for k in ["enset", "plantain", "banana", "cocoyam", "taro", "tuber", "root"]):
        return {"name": custom_crop_text or "Roots / Tubers / Musa", "unit": "t/ha", "base_yield": 20.0, "price_per_unit": 95_000, "growing_days": "240-360 days", "water_sens": 0.90}
    elif any(k in c_lower for k in ["rice"]):
        return {"name": "Rice", "unit": "t/ha", "base_yield": 4.5, "price_per_unit": 520_000, "growing_days": "115-130 days", "water_sens": 1.40}
    elif any(k in c_lower for k in ["fonio", "teff"]):
        return {"name": custom_crop_text or "Indigenous Cereal (Fonio/Teff)", "unit": "t/ha", "base_yield": 1.4, "price_per_unit": 850_000, "growing_days": "70-90 days", "water_sens": 0.75}
    elif any(k in c_lower for k in ["sorghum", "millet"]):
        return {"name": "Sorghum/Millet", "unit": "t/ha", "base_yield": 3.2, "price_per_unit": 380_000, "growing_days": "90-110 days", "water_sens": 0.80}
    elif any(k in c_lower for k in ["cowpea", "bean", "legume", "bambara", "chickpea", "pigeonpea"]):
        return {"name": "Grain Legume (Cowpea/Bean)", "unit": "t/ha", "base_yield": 1.8, "price_per_unit": 750_000, "growing_days": "65-80 days", "water_sens": 1.05}
    elif any(k in c_lower for k in ["soybean"]):
        return {"name": "Soybean", "unit": "t/ha", "base_yield": 2.4, "price_per_unit": 620_000, "growing_days": "100-115 days", "water_sens": 1.15}
    elif any(k in c_lower for k in ["groundnut", "peanut"]):
        return {"name": "Groundnut", "unit": "t/ha", "base_yield": 2.2, "price_per_unit": 680_000, "growing_days": "95-110 days", "water_sens": 1.00}
    elif any(k in c_lower for k in ["tomato", "pepper", "onion", "okra", "eggplant", "amaranth", "vegetable", "chili", "watermelon"]):
        return {"name": custom_crop_text or "Vegetables & Horticulture", "unit": "t/ha", "base_yield": 26.0, "price_per_unit": 190_000, "growing_days": "75-95 days", "water_sens": 1.45}
    elif any(k in c_lower for k in ["cocoa", "coffee", "oil palm", "cashew", "sesame", "cotton", "sugarcane"]):
        return {"name": custom_crop_text or "Cash / Oilseed / Export", "unit": "t/ha", "base_yield": 1.6, "price_per_unit": 2_400_000, "growing_days": "120 d / Perennial", "water_sens": 1.10}
    elif any(k in c_lower for k in ["cattle", "livestock", "pasture", "ruminant", "forage"]):
        return {"name": "Pasture / Livestock", "unit": "t/ha DM", "base_yield": 6.5, "price_per_unit": 150_000, "growing_days": "Perennial", "water_sens": 1.25}
    else:
        # Default Cereal
        disp_name = custom_crop_text if custom_crop_text else crop_name
        return {"name": disp_name, "unit": "t/ha", "base_yield": 4.8, "price_per_unit": 450_000, "growing_days": "105-120 days", "water_sens": 1.20}

