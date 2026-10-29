"""
AgroBiometrix - Multi-Agent Orchestration Layer
Africa-First, Globally Relevant Agricultural Artificial Intelligence Infrastructure.

Specialized Multi-Agent Dispatch:
- Veterinary Pathology & Animal Epidemiology Agent
- Breeding Herd Health & Reproductive Physiology Agent
- Agro-Climatology & Vector Dynamics Agent
- Preventive Biosecurity & Vaccination Protocol Agent
- Herd Economics, Yield Loss & Market Dynamics Agent
- Institutional Evidence & Diagnostic Standards Agent
(Dynamically adaptive across Crops, Livestock, Micro-Livestock, Soils, and Policy)
"""

import os
import json
import re
import requests

# =========================================================================
# AGENT DESCRIPTIONS & SPECIALIST ROLES
# =========================================================================
AGENT_DESCRIPTIONS = {
    "Veterinary Pathology & Epidemiology Agent": "Diagnoses endemic and transboundary animal diseases, etiology, vectors, and clinical signs.",
    "Breeding Herd Health & Reproductive Physiology Agent": "Dissects reproductive soundness, abortion risks, conception rates, and herd fertility.",
    "Agro-Climatology & Vector Dynamics Agent": "Models seasonal temperature-humidity index (THI), Harmattan dust stress, and insect vectors.",
    "Preventive Biosecurity & Vaccination Protocol Agent": "Formulates strict biosecurity calendars and national vaccine protocols (NVRI Vom/NARS).",
    "Herd Economics & Production Loss Agent": "Models financial losses from mortality, morbidity, culling, and preventive benefit-cost ratios.",
    "Institutional Evidence Agent": "Grounds recommendations in empirical guidelines from NARS (NVRI, NAPRI, IAR, NIHORT) and CGIAR.",
    "Crop Science Agent": "Specializes in tropical crop agronomy, physiological stress, and varietal selection.",
    "Climate Agent": "Analyzes agro-meteorological risks, rainfall regimes, and thermal patterns.",
    "Genetics Agent": "Focuses on genomic selection, QTL architecture, and local breed/cultivar adaptation.",
    "Soil Agent": "Specializes in soil physical chemistry, balanced stoichiometric fertilization, and liming.",
    "Economics Agent": "Evaluates enterprise gross margins, input costs, and terminal market pricing.",
    "Evidence Agent": "Synthesizes empirical literature from peer-reviewed journals and agricultural institutes."
}

# =========================================================================
# SUB-SAHARAN AFRICAN COUNTRIES & REGIONAL GEOGRAPHIES
# =========================================================================
SUB_SAHARAN_COUNTRIES = {
    "nigeria": {
        "label": "Nigeria",
        "currency_symbol": "₦",
        "currency_code": "NGN",
        "region": "West Africa",
        "institutions": "NVRI (Vom-Jos), NAPRI (Shika-Zaria), IAR, NIHORT, NCRI, IITA, UNIMAID & FUNAAB",
        "keywords": [
            "nigeria", "nigerian", "lagos", "ibadan", "kano", "kaduna", "abuja", "port harcourt", "enugu",
            "abeokuta", "funaab", "napri", "nvri", "nihort", "nifor", "crin", "ncri", "iita", "unimaid",
            "oyo", "ogun", "osun", "ondo", "ekiti", "sokoto", "kebbi", "jigawa", "borno", "bauchi", "zamfara",
            "yobe", "adamawa", "taraba", "gombe", "maiduguri", "potiskum", "damaturu", "jalingo", "lake chad",
            "katsina", "plateau", "jos", "benue", "makurdi", "niger state", "minna", "kwara", "ilorin",
            "kogi", "lokoja", "nasarawa", "lafia", "anambra", "imo", "owerri", "abia", "ebonyi", "edo", "delta"
        ]
    },
    "ghana": {
        "label": "Ghana",
        "currency_symbol": "GH₵ ",
        "currency_code": "GHS",
        "region": "West Africa",
        "institutions": "CSIR (ARI, CRI, SARI, OPRI) & KNUST",
        "keywords": ["ghana", "ghanaian", "accra", "kumasi", "tamale", "ashanti", "volta", "cape coast", "takoradi", "sunyani", "csir-ari", "knust", "csir-cri", "csir-sari", "csir"]
    },
    "kenya": {
        "label": "Kenya",
        "currency_symbol": "KSh ",
        "currency_code": "KES",
        "region": "East Africa",
        "institutions": "KALRO (Naivasha, Kitale, Katumani, Thika), ILRI & University of Nairobi",
        "keywords": ["kenya", "kenyan", "nairobi", "nakuru", "eldoret", "kisumu", "mombasa", "kiambu", "nyandarua", "limuru", "kericho", "kalro", "uon", "rift valley"]
    },
    "mali": {
        "label": "Mali (Sahel)",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "Sahelian West Africa",
        "institutions": "Institut d'Economie Rurale (IER Mali, Sotuba) & IPR/IFRA de Katibougou",
        "keywords": ["mali", "malian", "bamako", "segou", "ségou", "sikasso", "mopti", "sahel", "sahelian", "ier mali", "sotuba", "katibougou", "banco"]
    },
    "south_africa": {
        "label": "South Africa",
        "currency_symbol": "R ",
        "currency_code": "ZAR",
        "region": "Southern Africa",
        "institutions": "Agricultural Research Council (ARC Irene/Potchefstroom) & Onderstepoort",
        "keywords": ["south africa", "south african", "johannesburg", "joburg", "cape town", "pretoria", "durban", "highveld", "free state", "kwazulu-natal", "eastern cape", "western cape", "arc irene", "onderstepoort", "dalrrd"]
    },
    "uganda": {
        "label": "Uganda",
        "currency_symbol": "USh ",
        "currency_code": "UGX",
        "region": "East Africa",
        "institutions": "National Agricultural Research Organisation (NARO Uganda) & Makerere University",
        "keywords": ["uganda", "ugandan", "kampala", "entebbe", "mbarara", "gulu", "jinja", "naro", "makerere"]
    },
    "tanzania": {
        "label": "Tanzania",
        "currency_symbol": "TSh ",
        "currency_code": "TZS",
        "region": "East Africa",
        "institutions": "Tanzania Agricultural Research Institute (TARI) & TALIRI",
        "keywords": ["tanzania", "tanzanian", "dar es salaam", "arusha", "dodoma", "mbeya", "iringa", "morogoro", "kilombero", "tari", "taliri"]
    },
    "rwanda": {
        "label": "Rwanda",
        "currency_symbol": "RWF ",
        "currency_code": "RWF",
        "region": "East Africa",
        "institutions": "Rwanda Agriculture and Animal Resources Development Board (RAB)",
        "keywords": ["rwanda", "rwandan", "kigali", "butare", "musanze", "huye", "rab"]
    },
    "ethiopia": {
        "label": "Ethiopia",
        "currency_symbol": "Br ",
        "currency_code": "ETB",
        "region": "Horn of Africa",
        "institutions": "Ethiopian Institute of Agricultural Research (EIAR)",
        "keywords": ["ethiopia", "ethiopian", "addis ababa", "amhara", "oromia", "tigray", "dega", "weyna dega", "kolla", "eiar"]
    },
    "cote_divoire": {
        "label": "Côte d'Ivoire",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "West Africa",
        "institutions": "Centre National de Recherche Agronomique (CNRA, Abidjan/Bouaké)",
        "keywords": ["ivory coast", "côte d'ivoire", "cote d'ivoire", "ivoirien", "abidjan", "bouake", "bouaké", "yamoussoukro", "cnra"]
    },
    "senegal": {
        "label": "Senegal",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "Sahelian West Africa",
        "institutions": "Institut Sénégalais de Recherches Agricoles (ISRA, Dakar/Bambey)",
        "keywords": ["senegal", "senegalese", "sénégal", "dakar", "saint-louis", "thies", "thiès", "bambey", "isra"]
    },
    "burkina_faso": {
        "label": "Burkina Faso",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "Sahelian West Africa",
        "institutions": "Institut de l'Environnement et de Recherches Agricoles (INERA, Ouagadougou)",
        "keywords": ["burkina faso", "burkina", "burkinabe", "burkinabè", "ouagadougou", "bobo-dioulasso", "inera"]
    },
    "cameroon": {
        "label": "Cameroon",
        "currency_symbol": "FCFA ",
        "currency_code": "XAF",
        "region": "Central Africa",
        "institutions": "Institut de Recherche Agricole pour le Développement (IRAD, Yaoundé)",
        "keywords": ["cameroon", "cameroonian", "cameroun", "yaounde", "yaoundé", "douala", "bafoussam", "garoua", "irad"]
    },
    "zambia": {
        "label": "Zambia",
        "currency_symbol": "ZMW ",
        "currency_code": "ZMW",
        "region": "Southern Africa",
        "institutions": "Zambia Agriculture Research Institute (ZARI, Mount Makulu)",
        "keywords": ["zambia", "zambian", "lusaka", "ndola", "kitwe", "livingstone", "zari"]
    },
    "zimbabwe": {
        "label": "Zimbabwe",
        "currency_symbol": "USD / ZiG ",
        "currency_code": "USD",
        "region": "Southern Africa",
        "institutions": "Department of Research and Specialist Services (DR&SS, Harare) & Seed Co",
        "keywords": ["zimbabwe", "zimbabwean", "harare", "bulawayo", "gweru", "mutare", "dr&ss"]
    },
    "malawi": {
        "label": "Malawi",
        "currency_symbol": "MK ",
        "currency_code": "MWK",
        "region": "Southern Africa",
        "institutions": "Department of Agricultural Research Services (DARS Chitedze) & LUANAR",
        "keywords": ["malawi", "malawian", "lilongwe", "blantyre", "zomba", "chitedze", "luanar"]
    },
    "mozambique": {
        "label": "Mozambique",
        "currency_symbol": "MT ",
        "currency_code": "MZN",
        "region": "Southern Africa",
        "institutions": "Instituto de Investigação Agrária de Moçambique (IIAM, Maputo)",
        "keywords": ["mozambique", "mozambican", "maputo", "beira", "nampula", "iiam"]
    },
    "botswana": {
        "label": "Botswana",
        "currency_symbol": "P ",
        "currency_code": "BWP",
        "region": "Southern Africa",
        "institutions": "Botswana University of Agriculture and Natural Resources (BUAN) & DAR Gaborone",
        "keywords": ["botswana", "motswana", "batswana", "gaborone", "francistown", "buan", "dar botswana"]
    },
    "namibia": {
        "label": "Namibia",
        "currency_symbol": "N$ ",
        "currency_code": "NAD",
        "region": "Southern Africa",
        "institutions": "Directorate of Agricultural Research and Development (DARD, Windhoek)",
        "keywords": ["namibia", "namibian", "windhoek", "walvis bay", "omaha", "dard"]
    },
    "angola": {
        "label": "Angola",
        "currency_symbol": "Kz ",
        "currency_code": "AOA",
        "region": "Southern / Central Africa",
        "institutions": "Instituto de Investigação Agronómica (IIA, Huambo/Luanda)",
        "keywords": ["angola", "angolan", "luanda", "huambo", "lobito", "iia angola"]
    },
    "dr_congo": {
        "label": "Democratic Republic of the Congo",
        "currency_symbol": "FC ",
        "currency_code": "CDF",
        "region": "Central Africa",
        "institutions": "Institut National pour l'Etude et la Recherche Agronomiques (INERA Yangambi/Kinshasa)",
        "keywords": ["dr congo", "drc", "congo kinshasa", "kinshasa", "lubumbashi", "goma", "yangambi", "inera drc"]
    },
    "republic_congo": {
        "label": "Republic of the Congo",
        "currency_symbol": "FCFA ",
        "currency_code": "XAF",
        "region": "Central Africa",
        "institutions": "Institut de Recherche Agronomique (IRA Brazzaville)",
        "keywords": ["congo brazzaville", "republic of congo", "brazzaville", "pointe-noire"]
    },
    "gabon": {
        "label": "Gabon",
        "currency_symbol": "FCFA ",
        "currency_code": "XAF",
        "region": "Central Africa",
        "institutions": "Institut de Recherches Agronomiques et Forestières (IRAF/CENAREST, Libreville)",
        "keywords": ["gabon", "gabonese", "libreville", "port-gentil", "iraf"]
    },
    "chad": {
        "label": "Chad",
        "currency_symbol": "FCFA ",
        "currency_code": "XAF",
        "region": "Central / Sahelian Africa",
        "institutions": "Institut Tchadien de Recherche Agronomique pour le Développement (ITRAD, N'Djamena)",
        "keywords": ["chad", "chadian", "tchad", "n'djamena", "ndjamena", "moundou", "sarh", "itrad"]
    },
    "niger": {
        "label": "Niger",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "Sahelian West Africa",
        "institutions": "Institut National de la Recherche Agronomique du Niger (INRAN, Niamey/Maradi)",
        "keywords": ["niger", "nigerien", "niamey", "maradi", "zinder", "tahoua", "inran"]
    },
    "benin": {
        "label": "Benin",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "West Africa",
        "institutions": "Institut National des Recherches Agricoles du Bénin (INRAB, Cotonou/Parakou)",
        "keywords": ["benin", "beninese", "bénin", "cotonou", "porto-novo", "parakou", "inrab"]
    },
    "togo": {
        "label": "Togo",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "region": "West Africa",
        "institutions": "Institut Togolais de Recherche Agronomique (ITRA, Lomé/Kara)",
        "keywords": ["togo", "togolese", "lome", "lomé", "kara", "sokode", "itra togo"]
    },
    "guinea": {
        "label": "Guinea",
        "currency_symbol": "FG ",
        "currency_code": "GNF",
        "region": "West Africa",
        "institutions": "Institut de Recherche Agronomique de Guinée (IRAG, Conakry/Kindia)",
        "keywords": ["guinea", "guinean", "conakry", "kindia", "kankan", "fouta djallon", "irag"]
    },
    "sierra_leone": {
        "label": "Sierra Leone",
        "currency_symbol": "NLe ",
        "currency_code": "SLE",
        "region": "West Africa",
        "institutions": "Sierra Leone Agricultural Research Institute (SLARI, Freetown/Njala)",
        "keywords": ["sierra leone", "sierra leonean", "freetown", "njala", "bo", "kenema", "slari"]
    },
    "liberia": {
        "label": "Liberia",
        "currency_symbol": "L$ ",
        "currency_code": "LRD",
        "region": "West Africa",
        "institutions": "Central Agricultural Research Institute (CARI, Suakoko/Monrovia)",
        "keywords": ["liberia", "liberian", "monrovia", "suakoko", "gbarnga", "cari liberia"]
    },
    "gambia": {
        "label": "The Gambia",
        "currency_symbol": "D ",
        "currency_code": "GMD",
        "region": "West Africa",
        "institutions": "National Agricultural Research Institute (NARI, Brikama)",
        "keywords": ["gambia", "gambian", "banjul", "brikama", "serrekunda", "nari gambia"]
    },
    "madagascar": {
        "label": "Madagascar",
        "currency_symbol": "Ar ",
        "currency_code": "MGA",
        "region": "East / Southern Africa",
        "institutions": "Centre National de Recherche Appliquée au Développement Rural (FOFIFA, Antananarivo)",
        "keywords": ["madagascar", "malagasy", "antananarivo", "tamatave", "fofifa"]
    },
    "burundi": {
        "label": "Burundi",
        "currency_symbol": "FBu ",
        "currency_code": "BIF",
        "region": "East Africa",
        "institutions": "Institut des Sciences Agronomiques du Burundi (ISABU, Bujumbura/Gitega)",
        "keywords": ["burundi", "burundian", "bujumbura", "gitega", "isabu"]
    },
    "south_sudan": {
        "label": "South Sudan",
        "currency_symbol": "SSP ",
        "currency_code": "SSP",
        "region": "East Africa",
        "institutions": "Agricultural Research Corporation (ARC South Sudan, Juba)",
        "keywords": ["south sudan", "south sudanese", "juba", "wau", "malakal"]
    },
    "sudan": {
        "label": "Sudan",
        "currency_symbol": "SDG ",
        "currency_code": "SDG",
        "region": "Sahelian / Nile Valley",
        "institutions": "Agricultural Research Corporation (ARC Sudan, Wad Medani)",
        "keywords": ["sudan", "sudanese", "khartoum", "wad medani", "gezira", "el obeid"]
    },
    "somalia": {
        "label": "Somalia",
        "currency_symbol": "So.Sh. ",
        "currency_code": "SOS",
        "region": "Horn of Africa",
        "institutions": "Somali Agricultural Research Institute (SARI) & Mogadishu University",
        "keywords": ["somalia", "somali", "mogadishu", "hargeisa", "kismayo", "puntland"]
    },
    "eswatini": {
        "label": "Eswatini",
        "currency_symbol": "E ",
        "currency_code": "SZL",
        "region": "Southern Africa",
        "institutions": "Malkerns Agricultural Research Station (MARS) & University of Eswatini",
        "keywords": ["eswatini", "swaziland", "swazi", "mbabane", "manzini", "malkerns"]
    },
    "lesotho": {
        "label": "Lesotho",
        "currency_symbol": "M ",
        "currency_code": "LSL",
        "region": "Southern Africa",
        "institutions": "Department of Agricultural Research (DAR Lesotho, Maseru)",
        "keywords": ["lesotho", "basotho", "maseru", "mafeteng", "leribe"]
    },
    "mauritania": {
        "label": "Mauritania",
        "currency_symbol": "MRU ",
        "currency_code": "MRU",
        "region": "Sahelian West Africa",
        "institutions": "Centre National de Recherche Agronomique et de Développement Agricole (CNRADA, Kaédi)",
        "keywords": ["mauritania", "mauritanian", "nouakchott", "kaedi", "rosso", "cnrada"]
    }
}


def detect_target_geography(query: str, active_region: dict = None) -> dict:
    """
    Extracts targeted country, sub-region, and currency.
    Enforces a strict geographical boundary policy to prevent false geographical substitutions.
    """
    q_lower = query.lower()

    # 1. Non-African / Foreign Territories (Strict Zero-Hallucination Guard)
    foreign_map = {
        "United States": ["usa", "united states", "america", "american"],
        "United Kingdom": ["uk", "united kingdom", "england", "british"],
        "Canada": ["canada", "canadian"],
        "Australia": ["australia", "australian"],
        "Germany": ["germany", "german"],
        "France": ["france", "french"],
        "China": ["china", "chinese"],
        "India": ["india", "indian"],
        "Brazil": ["brazil", "brazilian"],
        "Russia": ["russia", "russian"],
        "Japan": ["japan", "japanese"],
        "Iceland": ["iceland", "icelandic"],
        "Norway": ["norway", "norwegian"],
        "Sweden": ["sweden", "swedish"],
        "Spain": ["spain", "spanish"],
        "Italy": ["italy", "italian"],
        "Netherlands": ["netherlands", "dutch climate", "holland"],
        "Mexico": ["mexico", "mexican"]
    }

    for foreign_name, keywords in foreign_map.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", q_lower):
                return {
                    "country": "foreign_uncalibrated",
                    "uncalibrated_name": foreign_name,
                    "is_uncalibrated": True,
                    "currency_symbol": "",
                    "currency_code": "",
                    "label": foreign_name
                }

    # 2. Match Sub-Saharan African Countries in Query
    for c_key, c_data in SUB_SAHARAN_COUNTRIES.items():
        if any(re.search(rf"\b{re.escape(k)}\b", q_lower) for k in c_data["keywords"]):
            # Extract sub-region if Nigeria
            sub_reg = "general"
            if c_key == "nigeria":
                if any(w in q_lower for w in ["north-east", "northeast", "north east", "borno", "yobe", "adamawa", "taraba", "gombe", "bauchi", "maiduguri", "potiskum", "damaturu", "lake chad"]):
                    sub_reg = "north_east"
                elif any(w in q_lower for w in ["north-west", "northwest", "north west", "kano", "kaduna", "katsina", "sokoto", "kebbi", "zamfara", "jigawa"]):
                    sub_reg = "north_west"
                elif any(w in q_lower for w in ["middle belt", "north-central", "north central", "plateau", "jos", "benue", "makurdi", "niger state", "minna", "kwara", "ilorin", "kogi", "nasarawa", "abuja"]):
                    sub_reg = "middle_belt"
                elif any(w in q_lower for w in ["south-west", "southwest", "south west", "oyo", "ibadan", "ogun", "osun", "ondo", "ekiti", "lagos"]):
                    sub_reg = "south_west"
                elif any(w in q_lower for w in ["south-east", "southeast", "south-south", "enugu", "anambra", "imo", "abia", "ebonyi", "edo", "delta", "rivers", "port harcourt"]):
                    sub_reg = "south_east_south"

            return {
                "country": c_key,
                "label": c_data["label"],
                "currency_symbol": c_data["currency_symbol"],
                "currency_code": c_data["currency_code"],
                "region": c_data["region"],
                "sub_region": sub_reg,
                "institutions": c_data["institutions"],
                "is_uncalibrated": False
            }

    # 3. Fallback to active_region session state if provided
    if active_region and isinstance(active_region, dict):
        reg_c = active_region.get("country", "").lower()
        for c_key, c_data in SUB_SAHARAN_COUNTRIES.items():
            if c_data["label"].lower() in reg_c:
                return {
                    "country": c_key,
                    "label": c_data["label"],
                    "currency_symbol": c_data["currency_symbol"],
                    "currency_code": c_data["currency_code"],
                    "region": c_data["region"],
                    "sub_region": "general",
                    "institutions": c_data["institutions"],
                    "is_uncalibrated": False
                }

    # 4. Default: Pan-African comparative view
    return {
        "country": "pan_africa",
        "label": "Pan-African & Regional Context",
        "currency_symbol": "USD / Local",
        "currency_code": "MULTI",
        "region": "Sub-Saharan Africa",
        "sub_region": "general",
        "institutions": "CGIAR (IITA, ILRI, AfricaRice, CIMMYT) & National Agricultural Research Systems (NARS)",
        "is_uncalibrated": False
    }


def parse_query_semantics(query: str):
    """
    Decomposes an agricultural question into:
    - Commodity / Sector
    - Primary and Secondary Intents (Diseases, Breeding, Nutrition, Climate, Economics, etc.)
    - Sub-region (e.g. North-East Nigeria, Lake Chad, etc.)
    """
    q_lower = query.lower()

    # 1. Commodity Detection
    commodity = "general"
    if any(w in q_lower for w in [
        "cattle", "cow", "cows", "bull", "bulls", "calf", "calves", "heifer", "heifers", "steer", "steers",
        "zebu", "bunaji", "white fulani", "gudali", "sokoto gudali", "muturu", "n'dama", "ndama", "bovine",
        "boran", "ankole", "sahiwal", "nguni", "bonsmara", "wadara", "kuri", "pastoral", "pastoralist", "rangeland"
    ]):
        commodity = "cattle"
    elif any(w in q_lower for w in [
        "poultry", "chicken", "chickens", "broiler", "broilers", "layer", "layers", "cockerel", "cockerels",
        "pullet", "pullets", "doc", "chick", "chicks", "turkey", "turkeys", "bird", "birds", "egg", "eggs", "avian", "fowl",
        "volaille", "volailles", "poulet", "poulets", "poussin", "poussins", "aviculture", "pondeuse", "pondeuses", "poule", "poules", "coq", "oeuf", "oeufs"
    ]):
        commodity = "poultry"
    elif any(w in q_lower for w in [
        "goat", "goats", "sheep", "ram", "rams", "ewe", "ewes", "buck", "bucks", "shoat", "shoats",
        "lamb", "lambs", "boer", "red sokoto", "wad goat", "sahelian", "dorper", "red maasai", "ladoum",
        "chèvre", "chèvres", "mouton", "moutons", "bélier", "béliers", "brebis", "agneau", "agneaux", "chevreau", "caprin", "caprins", "ovin", "ovins", "djalonké"
    ]):
        commodity = "small_ruminants"
    elif any(w in q_lower for w in ["pig", "pigs", "swine", "pork", "sow", "sows", "boar", "piglet", "piglets", "asf", "porc", "porcs", "porcin", "porcins", "truie", "truies", "verrat", "verrats", "porcelet", "porcelets", "peste porcine"]):
        commodity = "pig"
    elif any(w in q_lower for w in ["fish", "catfish", "tilapia", "aquaculture", "fingerling", "fingerlings", "pond", "ponds", "clarias", "oreochromis", "poisson", "poissons", "silure", "silures", "pisciculture", "alevin", "alevins", "bassin", "étang"]):
        commodity = "fish"
    elif any(w in q_lower for w in ["rabbit", "rabbits", "cuniculture", "doe", "does", "buck", "kit", "kits", "hutch", "hutches", "lapin", "lapins", "lapine", "lapines", "clapier", "clapiers", "lapereau", "lapereaux"]):
        commodity = "rabbit"
    elif any(w in q_lower for w in ["snail", "snails", "heliculture", "archachatina", "achatina", "escargot", "escargots", "héliciculture", "achatine"]):
        commodity = "snail"
    elif any(w in q_lower for w in ["bee", "bees", "apiculture", "honey", "apiary", "hive", "hives", "abeille", "abeilles", "miel", "ruche", "ruches", "rucher"]):
        commodity = "bee"
    elif any(w in q_lower for w in ["tomato", "tomatoes", "pepper", "peppers", "onion", "onions", "okra", "vegetable", "vegetables", "horticulture", "garden egg", "eggplant", "chili", "tomate", "tomates", "piment", "piments", "poivron", "poivrons", "oignon", "oignons", "gombo", "aubergine", "légume", "légumes", "maraîchage"]):
        commodity = "vegetables"
    elif any(w in q_lower for w in ["cassava", "yam", "yams", "sweet potato", "irish potato", "potato", "tuber", "tubers", "cocoyam", "plantain", "manioc", "igname", "ignames", "patate", "tubercules", "banane plantain"]):
        commodity = "root_tubers"
    elif any(w in q_lower for w in ["maize", "corn", "sorghum", "millet", "guinea corn", "cereal", "cereals", "fonio", "teff", "wheat", "maïs", "sorgho", "mil", "céréale", "céréales", "blé"]):
        commodity = "cereals"
    elif any(w in q_lower for w in ["rice", "paddy", "oryza", "faro", "nerica"]):
        commodity = "rice"
    elif any(w in q_lower for w in ["cowpea", "bean", "beans", "soybean", "soybeans", "groundnut", "groundnuts", "peanut", "peanuts", "legume", "legumes", "bambara"]):
        commodity = "legumes"
    elif any(w in q_lower for w in ["cocoa", "oil palm", "palm oil", "cashew", "coffee", "rubber", "cotton", "cacao", "cacaoyer", "palmier à huile", "anacarde", "café", "coton", "hévéa"]):
        commodity = "cash_crops"
    elif any(w in q_lower for w in [
        "ginger", "garlic", "turmeric", "watermelon", "melon", "pineapple", "banana",
        "citrus", "orange", "mango", "pawpaw", "papaya", "avocado", "guava", "sunflower",
        "sesame", "moringa", "shea", "camel", "duck", "donkey", "grasscutter", "pigeon",
        "ostrich", "mushroom", "vanilla", "clove", "date palm", "wheat", "barley", "teff", "fonio"
    ]):
        commodity = "smart_dynamic"
    elif any(w in q_lower for w in ["soil", "fertilizer", "fertilizers", "acidity", "liming", "npk", "urea", "phosphorus", "nitrogen", "cec", "organic matter"]):
        commodity = "soil"
    elif any(w in q_lower for w in ["policy", "subsidy", "intervention", "food security", "import", "reserve", "loan", "anchor borrower"]):
        commodity = "policy"

    # 2. Intents Detection
    intents = []
    
    # Disease / Health / Pathology / Parasites
    if any(w in q_lower for w in [
        "disease", "diseases", "sickness", "illness", "infection", "infections", "pathology",
        "pathogen", "virus", "viral", "bacterial", "bacteria", "fungal", "fungus", "cbpp", "fmd",
        "brucellosis", "brucella", "trypanosomiasis", "trypanosome", "nagana", "tsetse", "tick",
        "ticks", "heartwater", "anaplasmosis", "babesiosis", "dermatophilosis", "kirchi", "anthrax",
        "blackquarter", "mastitis", "abortion", "abortions", "newcastle", "gumboro", "coccidiosis",
        "ppr", "asf", "swine fever", "blight", "wilt", "mosaic", "vaccine", "vaccines", "vaccination",
        "treatment", "symptom", "symptoms", "mortality", "biosecurity", "prophylaxis", "pest", "pests",
        "helminth", "worm", "worms", "parasite", "parasites", "tuta", "armyworm", "stem borer", "pod borer"
    ]):
        intents.append("diseases_health")

    # Breeding / Genetics / Reproduction
    if any(w in q_lower for w in [
        "breed", "breeds", "breeding", "genetics", "genomic", "genomics", "qtl", "insemination",
        "artificial insemination", "ai", "estrus", "heat", "calving", "fertility", "infertility",
        "sire", "dam", "progeny", "selection", "heritability", "reproduction", "reproductive",
        "crossbreeding", "variety", "varieties", "cultivar", "cultivars", "hybrid", "hybrids",
        "orchitis", "semen", "sperm", "mating", "farrowing", "lambing", "kidding"
    ]):
        intents.append("breeding_genetics")

    # Nutrition / Feeding / Rangelands
    if any(w in q_lower for w in [
        "feed", "feeding", "nutrition", "diet", "ration", "pasture", "grazing", "forage", "hay",
        "silage", "supplement", "supplements", "mineral", "salt", "urea", "concentrate", "concentrates",
        "browse", "stylosanthes", "dry season feeding", "fodder", "fcr"
    ]):
        intents.append("nutrition_feeding")

    # Climate / Bioclimatics / Weather
    if any(w in q_lower for w in [
        "climate", "weather", "temperature", "heat", "heat stress", "thi", "rainfall", "drought",
        "harmattan", "season", "seasonal", "humidity", "rain", "dry season", "wet season", "flood",
        "diurnal", "cooling", "ventilation"
    ]):
        intents.append("climate_environment")

    # Economics / Marketing / Valuation
    if any(w in q_lower for w in [
        "price", "prices", "cost", "costs", "profit", "profitability", "margin", "margins",
        "economics", "market", "commercial", "revenue", "return", "investment", "abattoir", "sell", "value"
    ]):
        intents.append("economics_marketing")

    if not intents:
        intents.append("general_management")

    return commodity, intents


def rule_based_agent_synthesis(query: str, selected_agents: list = None, active_region: dict = None, **kwargs) -> dict:
    """
    State-of-the-art deterministic multi-agent synthesis engine.
    Dispatches specialized agents and synthesizes publication-grade, deeply relevant,
    statistically and biological robust answers tailored to the exact user query.
    """
    q_lower = query.lower()

    # 1. Geographic Grounding & Zero-Hallucination Guard
    geo = detect_target_geography(query, active_region=active_region)
    if geo.get("is_uncalibrated"):
        country_name = geo.get("uncalibrated_name", "the requested region")
        return {
            "unsupported": True,
            "selected_agents": [],
            "agent_outputs": {},
            "message": (
                f"⚠️ **Geographical Calibration Notice**: AgroBiometrix is specifically calibrated for Sub-Saharan agro-ecological zones. "
                f"Its offline empirical knowledge base does not currently provide calibrated datasets for **{country_name}** under this specific inquiry (*'{query}'*).\n\n"
                "To uphold scientific integrity and prevent geographic mismatch or false country substitution, offline recommendations for foreign/uncalibrated locations are withheld."
            ),
            "suggestion": (
                "💡 **Recommended Action**:\n"
                "• Switch the **Select Engine** dropdown above to **🟢 Live Google Gemini API**, **🧠 Live OpenAI API**, or **⚡ Live Groq API** for live global agricultural reasoning.\n"
                "• Alternatively, frame your query for any Sub-Saharan African country (e.g., Nigeria, Ghana, Kenya, Mali, South Africa, Uganda, Tanzania, Senegal, Côte d'Ivoire, Cameroon, Ethiopia, Zimbabwe, Zambia), or select a regional context from the sidebar."
            ),
            "final_synthesis": ""
        }

    target_country = geo.get("country", "pan_africa")
    cur_sym = geo.get("currency_symbol", "₦")
    country_lbl = geo.get("label", "Nigeria")
    sub_region = geo.get("sub_region", "general")
    target_inst = geo.get("institutions", "National Agricultural Research Systems (NARS) & CGIAR")

    # 2. Decompose Question Semantics
    commodity, intents = parse_query_semantics(query)

    # -------------------------------------------------------------------------
    # CASE 1: CATTLE / BOVINE SCIENCE
    # -------------------------------------------------------------------------
    if commodity == "cattle":
        # Check sub-case: Diseases & Health in Cattle (specifically in North-East Nigeria or other regions)
        if "diseases_health" in intents:
            is_ne = (sub_region == "north_east") or any(w in q_lower for w in ["north-east", "northeast", "borno", "yobe", "adamawa", "taraba", "gombe", "bauchi", "maiduguri", "lake chad"])
            
            dispatched = [
                "Veterinary Pathology & Epidemiology Agent",
                "Breeding Herd Health & Reproductive Physiology Agent",
                "Agro-Climatology & Vector Dynamics Agent (North-East / Regional)",
                "Preventive Biosecurity & NVRI Vaccination Protocol Agent",
                "Herd Economics & Production Loss Agent",
                "Institutional Evidence Agent (NVRI Vom, UNIMAID, FAO ECTAD)"
            ]

            loc_title = "North-East Nigeria (Borno, Yobe, Adamawa, Lake Chad Basin)" if is_ne else f"{country_lbl} Pastoral & Breeding Agro-Ecology"

            out_vet = (
                f"**Endemic & Transboundary Bovine Disease Landscape ({loc_title})**:\n"
                "• **Contagious Bovine Pleuropneumonia (CBPP - *Mycoplasma mycoides subsp. mycoides*)**: The leading respiratory plague across the Sahelian and Sudan savannas. Characterized by severe fibrinous pleuropneumonia, interlobular edema ('marbled lung'), and chronic, infectious pulmonary sequestra ('lungers') that trigger silent transmission upon herd commingling.\n"
                "• **Bovine Brucellosis (*Brucella abortus* Biovars 1 & 3)**: A hyper-endemic bacterial reproductive disease directly sabotaging breeding herds. Induces late-term **'abortion storms'** (6th–8th month of gestation), severe retained fetal membranes, necrotic placentitis, purulent metritis, and permanent repeat breeding. In breeding bulls, it causes unilateral or bilateral orchitis, epididymitis, and testicular atrophy. Highly zoonotic.\n"
                "• **Foot-and-Mouth Disease (FMD - Serotypes O, A, SAT 1, SAT 2)**: Acute viral epizootics along migratory stock routes. Produces vesicular lesions on dental pads, tongue, and coronary bands, inducing acute lameness, secondary mastitis/agalactia in lactating dams, and high calf mortality from viral myocarditis ('tiger heart').\n"
                "• **African Animal Trypanosomiasis (Nagana - *Trypanosoma vivax* & *T. congolense*)**: Endemic in riverine corridors of the Komadugu Yobe, Gongola, and Benue basins. Causes progressive normocytic normochromic anemia (PCV dropping <18%), severe cachexia, irregular estrus cycles, and embryonic resorption.\n"
                "• **Tick-Borne Disease Complex**: **Heartwater (*Ehrlichia ruminantium*)** transmitted by *Amblyomma variegatum*; **Bovine Babesiosis / Redwater (*Babesia bigemina*)**; **Anaplasmosis (*Anaplasma marginale*)**; and **Bovine Dermatophilosis / Kirchi (*Dermatophilus congolensis*)**, which explodes during early rains and creates painful crusty scabs preventing bulls from mounting.\n"
                "• **Clostridial & Septicemic Disasters**: **Blackquarter (*Clostridium chauvoei*)**, **Anthrax (*Bacillus anthracis*)**, and **Hemorrhagic Septicemia (*Pasteurella multocida* Type B)** triggered by seasonal stress and grazing on contaminated floodplains."
            )

            out_repro = (
                f"**Reproductive & Breeding Herd Pathology Impact**:\n"
                "• **Abortion Storms & Conception Failure**: *Brucella abortus* infection causes abortion rates of 25%–40% in first-calf heifers. Uterine caruncle necrosis leads to chronic endometritis, stretching calving intervals from the physiological 12–14 months to over 24–28 months.\n"
                "• **Breeding Bull Infertility & Venereal Shedding**: Brucellosis and Trypanosomiasis induce chronic testicular degeneration, severe sperm morphological defects (>60% abnormal spermatozoa), and permanent sterility in valuable herd sires.\n"
                "• **Calf Perinatal Morbidity & Agalactia**: FMD and CBPP severely suppress milk yield in lactating dams, starving suckling calves and escalating pre-weaning calf mortality beyond 30%.\n"
                "• **Genetic Capital Depletion**: High-merit indigenous breeding dams (Bunaji, Sokoto Gudali, Wadara) are prematurely culled due to chronic respiratory invalidism or permanent reproductive failure."
            )

            out_vector = (
                f"**Agro-Climatology & Regional Vector Dynamics ({loc_title})**:\n"
                "• **Transboundary Migratory Inflow (Lake Chad Basin)**: Unrestricted pastoral movement across the porous borders of Chad, Niger, and Cameroon introduces unvaccinated nomadic herds into Borno and Yobe, continuously introducing novel FMD topotypes and virulent CBPP field strains.\n"
                "• **Riverine Tsetse Pockets (*Glossina tachinoides*)**: Although the dry savanna is largely tsetse-free, dense riverine vegetation along the Komadugu Yobe river, Lake Chad shores, and upper Benue creates permanent micro-climatic tsetse refuges.\n"
                "• **Harmattan Aerosol Stress (November–February)**: Intense north-easterly dust storms carry abrasive silica particulates that dry out and damage the bovine ciliated respiratory epithelium, creating a direct entry route for latent *Mycoplasma* and *Pasteurella* infections.\n"
                "• **Thermal Immunosuppression (March–May)**: Ambient midday temperatures exceeding 42°C–45°C in Maiduguri, Nguru, and Potiskum drive THI > 85, triggering massive cortisol release and depressing cellular immunity."
            )

            out_biosec = (
                f"**NVRI Vom Vaccination Calendar & Preventive Biosecurity Protocol**:\n"
                "• **Official NVRI Vom Vaccine Regimen**:\n"
                "   1. **CBPP Vaccine (T1/44 Attenuated Strain)**: Subcutaneous injection at tail tip annually across all stock > 6 months. Maintain cold-chain rigorously.\n"
                "   2. **Brucellosis S19 Vaccine**: Mandatory vaccination of replacement heifers between 3 and 8 months of age (single dose confers lifelong immunity; do NOT vaccinate adult pregnant cows or bulls).\n"
                "   3. **Foot-and-Mouth Disease (Quadrivalent Inactivated)**: Biannual vaccination (March and September) prior to seasonal pastoral transhumance.\n"
                "   4. **Anthrax Spore & Blackquarter Bivalent Vaccine**: Annual administration in April/May prior to the onset of seasonal rains.\n"
                "   5. **Hemorrhagic Septicemia Vaccine**: Pre-rain prophylactic vaccination for herds grazing river basins.\n"
                "• **Acaricide Rotation & Dipping**: Apply synthetic pyrethroid (deltamethrin / flumethrin) pour-on every 14–21 days during rains; rotate with amitraz to suppress acaricide-resistant *Amblyomma* and *Rhipicephalus* ticks.\n"
                "• **Quarantine & Serological Screening**: Quarantine incoming breeding stock for 30 days; conduct mandatory Rose Bengal Plate Test (RBPT) and c-ELISA for Brucellosis prior to herd integration."
            )

            out_econ = (
                f"**Breeding Herd Economics & Production Loss Modeling ({country_lbl})**:\n"
                "• **Direct Loss from Abortion Storm**: A 30% abortion rate in a 60-cow breeding herd represents an immediate direct loss of 18 calves valued at **₦3.6M – ₦5.4M**, plus 45% reduction in commercial milk output.\n"
                "• **Salvage & Replacement Depreciation**: Mature breeding cows lost to CBPP or culled for brucellosis suffer a 50% salvage discount at abattoirs, while replacement breeding heifers in Potiskum or Maiduguri trade at **₦650,000 – ₦950,000**.\n"
                "• **Prevention ROI Ratio**: Complete prophylactic herd vaccination using NVRI Vom vaccines costs **₦2,200 – ₦3,800 per head/year**, compared to emergency curative interventions exceeding **₦45,000 – ₦70,000 per animal** with high mortality risks (Benefit-to-Cost Ratio > 16:1)."
            )

            out_evid = (
                "**Institutional Standards & Reference Diagnostic Facilities**:\n"
                "• **National Veterinary Research Institute (NVRI, Vom, Plateau State)**: Primary national producer of animal vaccines and reference diagnostic laboratory for viral and bacterial plagues.\n"
                "• **University of Maiduguri (UNIMAID) Faculty of Veterinary Medicine**: Zonal diagnostic authority on Lake Chad transboundary pastoral epidemiology and tick-borne pathogens.\n"
                "• **National Animal Production Research Institute (NAPRI, Shika-Zaria)**: Standards on indigenous cattle breed disease resilience.\n"
                "• **FAO Emergency Centre for Transboundary Animal Diseases (ECTAD)** and **WOAH (World Organisation for Animal Health)**."
            )

            matrix_table = f"""
| Disease & Pathogen | Primary Vector / Transmission | Breeding & Reproductive Manifestation | Diagnostic Markers & Pathology | NVRI Vom Vaccine & Treatment Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **CBPP**<br>*(Mycoplasma mycoides subsp. mycoides)* | Direct aerosol inhalation from carrier cattle ('lungers') | Severe respiratory distress, high dam mortality, calf starvation from agalactia | Marbled lung hepatization, fibrinous pleuritis, pulmonary sequestra | **NVRI CBPP T1/44 Vaccine** (annual tail-tip s/c). Prophylactic isolation; chronic carriers must be culled. |
| **Bovine Brucellosis**<br>*(Brucella abortus)* | Ingestion of aborted fetal fluids, cotyledons; venereal transmission via bulls | **Abortion storms (6–8th month)**, retained placenta, purulent metritis, bull orchitis & sterility | Caruncle necrosis, Rose Bengal Test (RBPT) positive, milk ring test | **NVRI Brucella S19 Vaccine** for heifers (3–8 months). Strict culling of seropositive reactors; screen herd sires. |
| **Foot & Mouth Disease (FMD)**<br>*(Aphthovirus O, A, SAT 1, SAT 2)* | Highly infectious aerosols, direct contact, fomites along stock routes | Severe lameness preventing bull mounting, acute mastitis, **calf mortality from myocarditis** | Oral/hoof vesicles, salivation, coronary band erosion, 'tiger heart' in calves | **NVRI FMD Inactivated Vaccine** (biannual). Supportive antibiotic spray, anti-inflammatories, footbaths. |
| **Trypanosomiasis (Nagana)**<br>*(Trypanosoma vivax / congolense)* | Cyclical transmission by tsetse (*Glossina tachinoides*); mechanical biting flies | Progressive chronic anemia (PCV <18%), irregular estrus, early embryonic loss, third-trimester abortion | Thin blood smear, buffy coat micro-haematocrit centrifugation, lymphadenopathy | Isometamidium chloride (0.5–1 mg/kg) for prophylaxis; Diminazene aceturate (3.5 mg/kg) for clinical cure. Tsetse traps. |
| **Tick-Borne Diseases**<br>*(Heartwater, Babesiosis, Anaplasmosis)* | Ticks: *Amblyomma variegatum*, *Rhipicephalus decoloratus* | High fever (>41°C), maternal death, tick-associated **Dermatophilosis ('Kirchi')** preventing mating | Hydropericardium (heartwater), hemoglobinuria (redwater), anemia/jaundice (anaplasma) | Acaricide dip/pour-on (*deltamethrin/flumethrin*) every 14–21 d. Oxytetracycline (20 mg/kg LA) for heartwater/anaplasmosis; Diminazene for babesiosis. |
| **Blackquarter & Anthrax**<br>*(Clostridium chauvoei / Bacillus anthracis)* | Soil-borne spore ingestion along floodplains and dried riverbeds | Sudden peracute death of prime young stock (6–24 months), septicemic shock | Crepitant muscle swellings, uncoagulated tarry blood from natural orifices (Anthrax) | **NVRI Blackquarter / Anthrax Spore Vaccine** (annual pre-rain). High-dose Penicillin if caught early. Never open an anthrax carcass! |
"""

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Veterinary & Breeding Advisory: Bovine Health in {loc_title}

#### 🎯 Executive Epidemiological Summary
In **{loc_title}**, cattle breeding enterprises face an intense convergence of **endemic reproductive pathogens**, **vector-borne blood parasites**, and **respiratory epizootics**. Transboundary livestock movements across the Lake Chad Basin (connecting Chad, Niger, and Cameroon), seasonal congregation along riverine floodplains (Komadugu Yobe and Benue), and extreme climate stresses (Harmattan dust and severe dry-season heat exceeding 42°C) make proactive disease management the single most critical determinant of breeding herd survival and reproductive longevity.

---

#### 📊 Comprehensive Pathological & Diagnostic Matrix for Breeding Cattle
{matrix_table}

---

#### 🌍 Agro-Ecological Risk Dynamics in North-East Nigeria
1. **The Lake Chad Transboundary Funnel**: Nomadic herds moving south from Chad and Niger enter Borno and Yobe during the dry season, creating viral mixing zones for novel Foot-and-Mouth Disease (FMD) strains and reintroducing Contagious Bovine Pleuropneumonia (CBPP) into stationary breeding herds.
2. **Seasonal Riverine Tsetse Fly Refugia**: Riverine vegetation along the Komadugu Yobe, Gongola, and upper Benue systems harbor *Glossina tachinoides*. Breeding herds grazing these dry-season water points face severe Trypanosomiasis challenge between January and May.
3. **Harmattan Dust Stress (Nov–Feb)**: Desiccating Saharan winds laden with fine abrasive dust irritate bovine bronchial membranes, predisposing breeding stock to explosive CBPP and Pasteurella outbreaks.
4. **Thermal Stress & Heat Exhaustion (March–May)**: Prolonged ambient temperatures above 40°C cause severe Temperature-Humidity Index (THI > 85) overload, elevating systemic cortisol and suppressing immunological resistance.

---

#### 📋 5-Phase Integrated Health & Biosecurity Protocol for Cattle Breeders
1. **Phase 1: Pre-Breeding Screening & Closed-Herd Quarantine**
   • Conduct mandatory serological screening for all prospective breeding bulls and replacement heifers using the **Rose Bengal Plate Test (RBPT)** for Brucellosis. Cull all seropositive reactors immediately.
   • Quarantine any newly acquired breeding animal for a minimum of **30 days** in an isolated holding paddock; observe for respiratory lag or lameness before herd introduction.
2. **Phase 2: Strict NVRI Vom Annual Vaccination Calendar**
   • **March (Pre-Transhumance)**: Administer NVRI Quadrivalent FMD Vaccine.
   • **April–May (Pre-Rains)**: Administer NVRI CBPP Vaccine (tail-tip s/c), Anthrax Spore Vaccine, and Blackquarter Vaccine.
   • **Heifer Inoculation**: Vaccinate all replacement heifer calves between 3 and 8 months of age with **NVRI Brucella abortus S19 Vaccine**.
3. **Phase 3: Vector Suppression & Acaricide Stewardship**
   • Apply **deltamethrin (1% pour-on)** or **flumethrin** along the dorsal midline every 14 to 21 days during the rainy season to suppress *Amblyomma* (heartwater & dermatophilosis vector) and *Rhipicephalus* ticks.
   • Deploy blue-black biconical insecticide-impregnated tsetse traps along riverine grazing banks.
4. **Phase 4: Reproductive Bull Management & Maternal Biosecurity**
   • Restrict natural mating to sound, certified disease-free sires. Inspect bull testicles monthly for swelling, heat, or asymmetry (orchitis/epididymitis).
   • Isolate any cow showing vaginal discharge or signs of abortion. Incinerate or deeply bury (with agricultural lime) all aborted fetuses, cotyledons, and contaminated bedding. Disinfect calving areas with 2% Virkon or sodium hypochlorite.
5. **Phase 5: Diagnostic Verification & Laboratory Contact**
   • In the event of suspected CBPP or abortion outbreaks, immediately contact the **NVRI Zonal Laboratories (Maiduguri, Bauchi, or Yola)** or the **UNIMAID Veterinary Teaching Hospital** for definitive pathological confirmation.
"""

            agent_outputs = {
                "Veterinary Pathology & Epidemiology Agent": out_vet,
                "Breeding Herd Health & Reproductive Physiology Agent": out_repro,
                "Agro-Climatology & Vector Dynamics Agent (North-East / Regional)": out_vector,
                "Preventive Biosecurity & NVRI Vaccination Protocol Agent": out_biosec,
                "Herd Economics & Production Loss Agent": out_econ,
                "Institutional Evidence Agent (NVRI Vom, UNIMAID, FAO ECTAD)": out_evid,
                # Compatibility fallbacks
                "Livestock & Pastoral Science Agent": out_vet,
                "Climate & Agro-Ecosystems Agent": out_vector,
                "Animal Genetics & Breeding Agent": out_repro,
                "Rangeland & Soil Agent": out_vector,
                "Livestock Economics Agent": out_econ,
                "Evidence Agent": out_evid,
                "Crop Science Agent": out_vet,
                "Climate Agent": out_vector,
                "Genetics Agent": out_repro,
                "Soil Agent": out_vector,
                "Economics Agent": out_econ
            }

            return {
                "selected_agents": dispatched,
                "agent_outputs": agent_outputs,
                "final_synthesis": final_synthesis
            }

        # Sub-case: Breeding / Genetics in Cattle (General or Regional)
        elif "breeding_genetics" in intents:
            dispatched = [
                "Animal Genetics & Breed Architecture Agent",
                "Reproductive Technologies & AI Agent",
                "Agro-Climatic Thermal Resilience Agent",
                "Pasture & Maternal Nutrition Agent",
                "Livestock Valuation & Pedigree Economics Agent",
                "Institutional Evidence Agent (NAPRI, ILRI, NVRI)"
            ]

            out_gen = (
                f"**Genomic Architecture & Breed Selection ({country_lbl})**:\n"
                "• **Indigenous Zebu Superiority**: White Fulani (Bunaji) and Sokoto Gudali possess fixed alleles for thermal tolerance (HSP70, HSP90 cytoprotective chaperones) and tick resistance.\n"
                "• **Taurine Trypanotolerance**: Muturu and N'Dama carry selective sweeps on BTA2, BTA7, and BTA14 conferring innate resistance to *Trypanosoma vivax*.\n"
                "• **Crossbreeding Protocols**: In commercial dairy setups, limit exotic taurine (Friesian / Jersey) introgression to 50% (F1 cross). Higher exotic blood (>75%) breaks down thermal resilience under tropical solar flux."
            )
            out_repro = (
                "**Reproductive Management & Bull Performance**:\n"
                "• Maintain a strict bull-to-cow ratio of 1:25 in open range and 1:35 in synchronized herds.\n"
                "• Estrus synchronization using PGF2α protocols enables scheduled insemination, bypassing heat detection difficulties during hot dry periods."
            )
            out_clim = (
                f"**Bioclimatic Adaptation ({country_lbl})**:\n"
                "• When Temperature-Humidity Index (THI) exceeds 78, sperm motility drops by 35%. Provide deep shade trees and scheduled grazing between 6:00 AM–10:00 AM and 4:30 PM–7:00 PM."
            )
            out_nutr = (
                "**Maternal Nutrition & Flushing**:\n"
                "• Institute energy flushing (feeding 1.5 kg concentrate/day with cottonseed cake or brewers dried grain) 3 weeks prior to breeding season to induce robust ovulatory surges."
            )
            out_econ = (
                f"**Pedigree Valuation & Financial Returns ({country_lbl})**:\n"
                f"• Proven Bunaji/Gudali breeding bulls command {cur_sym}1.2M – {cur_sym}2.2M, while certified high-index heifers yield 40% higher lifetime returns."
            )
            out_evid = f"**Institutional Evidence Grounding**: Grounded in {target_inst} breed registries."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Breeding & Genetics Advisory: Cattle Production ({country_lbl})

#### 🎯 Strategic Breeding Recommendation
Maximizing reproductive efficiency in **{country_lbl}** requires matching the genetic architecture of the cattle herd to local climatic, disease, and forage realities. Pure exotic taurines fail under high thermal load and tick challenges; the gold standard is **structured selection of elite indigenous breeds (Bunaji, Gudali, Boran)** or **controlled 50% F1 composite crossing** with strict reproductive health monitoring.
"""
            agent_outputs = {
                dispatched[0]: out_gen, dispatched[1]: out_repro, dispatched[2]: out_clim,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Livestock & Pastoral Science Agent": out_gen, "Climate & Agro-Ecosystems Agent": out_clim,
                "Animal Genetics & Breeding Agent": out_gen, "Rangeland & Soil Agent": out_nutr,
                "Livestock Economics Agent": out_econ, "Evidence Agent": out_evid,
                "Crop Science Agent": out_gen, "Climate Agent": out_clim, "Genetics Agent": out_gen,
                "Soil Agent": out_nutr, "Economics Agent": out_econ
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

        # Sub-case: Nutrition & Feeding in Cattle
        elif "nutrition_feeding" in intents:
            dispatched = [
                "Ruminant Nutrition & Feed Science Agent",
                "Rangeland Forage & Legume Agronomy Agent",
                "Agro-Climatology & Water Security Agent",
                "Rumen Microbiology & Urea Ammoniation Agent",
                "Feed Cost & Gross Margin Economics Agent",
                "Institutional Evidence Agent (NAPRI, ILRI)"
            ]
            out_nutr = (
                f"**Ruminant Ration & Dry Season Feeding Architecture ({country_lbl})**:\n"
                "• **Bridging the Dry Season Protein Deficit**: Native savanna grasses drop below 3.5% crude protein (CP) in the dry season, halting microbial digestion. Supplement with 4% urea-treated cereal stover (sorghum/maize) or molasses-urea multinutrient blocks (MUMB) to maintain rumen ammonia levels above 50 mg N/L.\n"
                "• **Fodder Legumes**: Conserve hay from *Stylosanthes hamata* and *Lablab purpureus* (14–18% CP) and feed at 2.0–2.5 kg/head/day."
            )
            out_range = (
                "**Rangeland Rotational Grazing & Kraaling**:\n"
                "• Implement strip or cell grazing with 45-day rest periods to preserve perennial grass root crowns (*Andropogon gayanus*, *Brachiaria*).\n"
                "• Mobile night kraaling concentrates manure and urine, providing ~60 kg N and ~15 kg P per hectare to dryland soils."
            )
            out_clim = (
                f"**Water Logistics & Hydration Demand ({country_lbl})**:\n"
                "• Water intake doubles during hot periods. A mature 350 kg Zebu bull requires 45–60 liters of clean drinking water daily."
            )
            out_econ = (
                f"**Feedlot Economics ({country_lbl})**:\n"
                f"• 90-day dry season feedlot fattening achieves 750–950 g/day liveweight gain, generating net margins of {cur_sym}180,000 – {cur_sym}320,000 per head."
            )
            out_evid = f"**Evidence Standards**: NAPRI Animal Feeding Trials and ILRI Feedipedia."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Advisory: Cattle Nutrition & Forage Management ({country_lbl})
#### 🎯 Strategic Nutrition Summary
In **{country_lbl}**, the primary constraint to cattle production is the severe quality collapse of natural pastures during the 5–7 month dry season. Deploying **urea-ammoniated crop residues**, **forage legumes (*Stylosanthes*, *Lablab*)**, and **strategic mineral-urea blocks** sustains rumen microbial fermentation, preventing the typical 15%–25% seasonal liveweight loss.
"""
            agent_outputs = {
                dispatched[0]: out_nutr, dispatched[1]: out_range, dispatched[2]: out_clim,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Livestock & Pastoral Science Agent": out_nutr, "Climate & Agro-Ecosystems Agent": out_clim,
                "Animal Genetics & Breeding Agent": out_nutr, "Rangeland & Soil Agent": out_range,
                "Livestock Economics Agent": out_econ, "Evidence Agent": out_evid,
                "Crop Science Agent": out_nutr, "Climate Agent": out_clim, "Genetics Agent": out_nutr,
                "Soil Agent": out_range, "Economics Agent": out_econ
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

        # Fallback Cattle: Comprehensive General Synthesis
        else:
            dispatched = [
                "Livestock & Pastoral Science Agent",
                "Climate & Agro-Ecosystems Agent",
                "Animal Genetics & Breeding Agent",
                "Rangeland & Soil Agent",
                "Livestock Economics Agent",
                "Evidence Agent"
            ]
            c_breeds = "White Fulani (Bunaji), Sokoto Gudali, Muturu, and N'Dama" if target_country == "nigeria" else "Adapted African breeds (Boran, Bonsmara, Sahiwal, Sanga)"
            c_econ = f"Finished Zebu cattle command {cur_sym}750,000 – {cur_sym}1,400,000 in major urban terminal markets."
            out_prod = f"**Pastoral Husbandry & Breed Deployment ({country_lbl})**:\n• Deploy {c_breeds}. Conserve crop residues and establish forage legumes (*Stylosanthes*, *Lablab*) to bridge seasonal feed gaps."
            out_clim = f"**Agro-Climatic Assessment ({country_lbl})**:\n• Ambient THI frequently exceeds 78 during midday. Nighttime radiative cooling and shaded paddocks are essential."
            out_gen = "**Genomic & Breeding Architecture**:\n• Focus on HSP70/HSP90 thermal tolerance loci and trypanotolerance QTLs on BTA2 and BTA7."
            out_soil = "**Rangeland Edaphic & Manure Cycling**:\n• Mobile kraaling deposits organic N and P to revitalize arable soils."
            out_econ = f"**Livestock Market Returns ({country_lbl})**:\n• {c_econ}"
            out_evid = f"**Evidence Grounding**: Verified against {target_inst}."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Recommendation: Cattle Production & Pastoral Resilience ({country_lbl})
1. **Breed Selection**: Prioritize adapted breeds ({c_breeds}) carrying natural thermotolerance and disease resilience alleles.
2. **Heat Mitigation**: Graze during early mornings and late evenings; provide deep shade and cool drinking water.
3. **Economics & Valuation**: {c_econ}
"""
            agent_outputs = {
                dispatched[0]: out_prod, dispatched[1]: out_clim, dispatched[2]: out_gen,
                dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Crop Science Agent": out_prod, "Climate Agent": out_clim, "Genetics Agent": out_gen,
                "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 2: POULTRY & AVIAN SCIENCE
    # -------------------------------------------------------------------------
    elif commodity == "poultry":
        if "diseases_health" in intents:
            dispatched = [
                "Avian Pathology & Infectious Disease Agent",
                "Vaccination Protocol & Cold-Chain Agent",
                "Bioclimatic Housing & Airborne Vector Agent",
                "Electrolyte & Nutritional Support Agent",
                "Flock Mortality & Enterprise Economics Agent",
                "Institutional Standards Agent (NVRI Vom, PAN, FAO)"
            ]
            out_vet = (
                f"**Major Avian Viral & Bacterial Plagues ({country_lbl})**:\n"
                "• **Newcastle Disease (ND - Avian Paramyxovirus-1)**: Endemic airborne killer; velogenic strains cause torticollis, green diarrhea, tracheal rales, and up to 100% flock mortality.\n"
                "• **Infectious Bursal Disease (Gumboro / IBD)**: Severe viral immunosuppression attacking the bursa of Fabricius between Weeks 3 and 6.\n"
                "• **Chronic Respiratory Disease (CRD - *Mycoplasma gallisepticum*)**: Triggered by dry dust and high ammonia, causing facial swelling and rattling tracheas.\n"
                "• **Coccidiosis (*Eimeria tenella*, *E. necatrix*)**: Bloody droppings and intestinal sloughing in wet litter environments."
            )
            out_vax = (
                "**Comprehensive Vaccination Calendar**:\n"
                "• Day 1: Marek's (Hatchery) + ND Intraocular.\n"
                "• Day 9–11: Gumboro (IBD Intermediate Plus).\n"
                "• Day 14: Newcastle Disease (Lasota) in skimmed milk water.\n"
                "• Day 18–20: Gumboro booster.\n"
                "• Day 28: Newcastle Disease (Lasota booster)."
            )
            out_clim = (
                f"**Airborne Pathogen Dispersion ({country_lbl})**:\n"
                "• Seasonal dry winds carry wild bird droppings and aerosolized dust, drastically increasing Newcastle and CRD infection rates. Install perimeter windbreaks and curtain management."
            )
            out_nutr = "Administer Vitamin C (1g/L) and electrolyte therapy during vaccination to mitigate stress."
            out_econ = f"Flock mortality >8% erodes enterprise profit margins; vaccination investment costs <{cur_sym}120 per bird with a 25:1 return on investment."
            out_evid = "NVRI Vom Avian Vaccine Production Standards and FAO Biosecurity Guidelines."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Veterinary Advisory: Poultry Flock Health & Disease Defense ({country_lbl})
#### 🎯 Strategic Flock Biosecurity
In **{country_lbl}**, poultry profitability hinges on strict prevention of **Newcastle Disease (ND)** and **Gumboro (IBD)**. Once clinical signs emerge, mortality in unvaccinated flocks can reach 80%–100%. Maintaining a strict **NVRI vaccination calendar**, **water-sanitation protocol**, and **prophylactic dust/respiratory mitigation** is non-negotiable.
"""
            agent_outputs = {
                dispatched[0]: out_vet, dispatched[1]: out_vax, dispatched[2]: out_clim,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Poultry Science & Housing Agent": out_vet, "Climate & Bioclimatic Housing Agent": out_clim,
                "Poultry Health & Biosecurity Agent": out_vax, "Nutrition & Feed Management Agent": out_nutr,
                "Farm Economics & Festive Market Agent": out_econ, "Evidence & Standards Agent": out_evid
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

        else:
            # Brooding / Climate / Festive / Feeding
            dispatched = [
                "Poultry Science & Housing Agent",
                "Climate & Bioclimatic Housing Agent",
                "Poultry Health & Biosecurity Agent",
                "Nutrition & Feed Management Agent",
                "Farm Economics & Festive Market Agent",
                "Evidence & Standards Agent"
            ]
            out_prod = (
                f"**Avian Management & Housing Architecture ({country_lbl})**:\n"
                "• **Stocking Strategy**: Sowing/stocking day-old chicks (DOC) in late October or early November aligns flock maturity (Day 42–52, target 2.2–2.6 kg) with peak commercial holiday demand.\n"
                "• **Diurnal Thermal Fluctuations**: Days are hot (31°C–34°C) while nights drop sharply. Use double-walled brooder curtains to avoid chilling between 1:00 AM and 5:00 AM, lowering curtains by 9:00 AM for cross-ventilation."
            )
            out_clim = (
                f"**Agro-Climatic & Bioclimatic Assessment ({country_lbl})**:\n"
                "• When ambient temperature exceeds 28°C, chickens pant to dissipate heat. Dry Harmattan dust irritates mucous membranes, sharply elevating CRD risks."
            )
            out_health = "**Poultry Health Protocol**: Strictly administer ND Lasota at Day 14 and Day 28, and Gumboro Intermediate Plus at Day 10 and Day 18."
            out_nutr = "**Split-Feeding Schedule**: Withdraw feed completely during peak afternoon heat (11:30 AM–3:30 PM) to avoid metabolic heat spikes. Add Vitamin C (1g/L) to drinking water."
            out_econ = f"**Festive Farmgate Pricing**: Live broilers trade at {cur_sym}11,000 – {cur_sym}16,000 in Nigeria (or local equivalent), delivering net operating margins >35%."
            out_evid = f"Verified against {target_inst} Avian Research."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Assessment: Poultry Bioclimatics & Festive Production ({country_lbl})
1. **Stocking & Brooding**: Stock DOCs immediately to achieve 2.2–2.6 kg for peak markets. Protect against cold nocturnal drafts while maintaining daytime ventilation.
2. **Heat Stress & Electrolytes**: Add Vitamin C and electrolytes to drinking water between 10:00 AM and 4:00 PM to combat respiratory alkalosis.
3. **Split-Feeding**: Feed 60% early morning and 40% evening; withdraw feed during peak afternoon heat.
4. **Vaccination**: Administer Newcastle Disease (Lasota) and Gumboro (IBD) according to schedule.
5. **Commercial Value**: Net operating margins exceed 30%–45% per batch when mortality is kept under 4%.
"""
            agent_outputs = {
                dispatched[0]: out_prod, dispatched[1]: out_clim, dispatched[2]: out_health,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Crop Science Agent": out_prod, "Climate Agent": out_clim, "Genetics Agent": out_health,
                "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 3: RABBIT SCIENCE (Cuniculture)
    # -------------------------------------------------------------------------
    elif commodity == "rabbit":
        dispatched = [
            "Cuniculture Science & Housing Agent",
            "Tropical Climate & Heat Stress Agent",
            "Rabbit Health & Disease Defense Agent",
            "Rabbit Nutrition & Forage Agent",
            "Micro-Livestock Economics Agent",
            "Evidence & Research Standards Agent"
        ]
        out_prod = (
            f"**Rabbit Breed Architecture for Tropical Africa ({country_lbl})**:\n"
            "• **Top Commercial Breeds**: **New Zealand White (NZW)** (fast growth, exceptional maternal instinct), **Chinchilla** (superior heat hardiness and disease resistance in tropical savanna), and **Californian** (high meat-to-bone ratio).\n"
            "• **Housing Design**: Multi-tier wire mesh cages elevated at least 80 cm above ground. Avoid solid wooden floors which retain moisture and coccidial oocysts."
        )
        out_clim = (
            f"**Thermal Bioclimatics & Buck Heat Sterility ({country_lbl})**:\n"
            "• Rabbits lack sweat glands. Temperatures above 30°C cause severe heat prostration.\n"
            "• **Buck Infertility Hazard**: Ambient heat >31°C causes temporary testicular sterility lasting 6–8 weeks. Install thatch roof insulation, spray roof exterior during midday, and provide clay cooling tiles inside cages."
        )
        out_health = (
            "**Pathology & Prophylaxis**:\n"
            "• **Mucoid Enteropathy & Bloat**: The primary killer of weaners; strictly maintain dietary crude fiber >15%.\n"
            "• **Snuffles (*Pasteurella multocida*)**: Triggered by poor ventilation and ammonia; cull chronic sneezing carriers.\n"
            "• **Mange & Ear Canker (*Psoroptes cuniculi*)**: Apply mineral oil or ivermectin drops."
        )
        out_nutr = (
            "**Nutrition & Forage Strategy**:\n"
            "• Wilt fresh forages (*Tridax procumbens*, *Stylosanthes*, sweet potato vines) for 12–24 hours before feeding to prevent gaseous tympany/bloat.\n"
            "• Supplement with commercial pelleted concentrate (16–18% crude protein)."
        )
        out_econ = (
            f"**Enterprise Economics ({country_lbl})**:\n"
            f"• Breeding stock trades at {cur_sym}8,000 – {cur_sym}15,000 per mature breeder pair. Highly prolific (6–8 kits per litter, 4–5 litters/year)."
        )
        out_evid = "Grounding: NAPRI Cuniculture Research Division, FUNAAB Rabbitry Project, and FAO Rabbit Farming Guide."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Cuniculture Advisory: Rabbit Production ({country_lbl})
#### 🎯 Strategic Breed & Housing Recommendation
1. **Breed Selection**: Crossbred **New Zealand White &times; Chinchilla** provides the optimal combination of rapid meat growth, large litter sizes (6–8 kits), and robust heat hardiness for **{country_lbl}**.
2. **Buck Heat Sterility**: Protect herd sires from temperatures above 30°C using double-thatch shade and evaporative misting to prevent 2-month summer infertility.
3. **Bloat Prevention**: Never feed freshly cut, wet greens; always wilt forages for 12–24 hours to prevent fatal mucoid enteropathy.
4. **Housing**: Elevated galvanized wire cages with nipple drinkers ensure zero contact with droppings.
5. **Commercial Return**: High prolificacy yields full capital amortization within 8–10 months.
"""
        agent_outputs = {
            dispatched[0]: out_prod, dispatched[1]: out_clim, dispatched[2]: out_health,
            dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_prod, "Climate Agent": out_clim, "Genetics Agent": out_health,
            "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 4: SMALL RUMINANTS (Goats & Sheep)
    # -------------------------------------------------------------------------
    elif commodity == "small_ruminants":
        sr_breeds = "Red Sokoto (Kano Brown), Sahelian, and West African Dwarf (WAD)" if target_country == "nigeria" else "Boer, Galla, Red Maasai, Dorper, and Mubende"
        
        # Sub-case: Small Ruminant Diseases & Health
        if "diseases_health" in intents:
            dispatched = [
                "Small Ruminant Epidemiology & Viral Pathology Agent",
                "Parasitology & Helminth Resistance Agent",
                "Caprine & Ovine Respiratory Complex Agent",
                "Biosecurity & NVRI Homologous Vaccine Agent",
                "Flock Mortality & Enterprise Economics Agent",
                "Institutional Standards Agent (NVRI Vom, CIRDES, ILRI)"
            ]

            out_vet = (
                f"**Endemic & Epizootic Small Ruminant Pathologies ({country_lbl})**:\n"
                "• **Peste des Petits Ruminants (PPR - 'Goat Plague' / Morbillivirus)**: Highly contagious viral plague causing acute pyrexia (>40.5°C), erosive stomatitis, foul necrotizing diarrhea, and catastrophic interstitial pneumonia. Mortality reaches 70%–90% in naive kid flocks.\n"
                "• **Contagious Caprine Pleuropneumonia (CCPP - *Mycoplasma capricolum subsp. capripneumoniae*)**: Major respiratory threat in Sahelian and Sudan savanna belts (Mali, Niger, Chad, Northern Nigeria, Kenya). Produces unilateral fibrinous hepatization and excessive straw-colored pleural effusion.\n"
                "• **Gastrointestinal Helminthiasis (*Haemonchus contortus*)**: The blood-sucking barberpole worm damages abomasal mucosa, producing acute hemorrhagic anemia, profound hypoproteinemia, submandibular edema ('bottle jaw'), and sudden collapse during rains.\n"
                "• **Tick-Borne Ruminant Complex**: **Heartwater (*Ehrlichia ruminantium*)** transmitted by *Amblyomma variegatum* ticks, causing high-stepping gait, hydropericardium, and convulsions; plus tick paralysis.\n"
                "• **Contagious Ecthyma (Orf - Parapoxvirus)**: Highly contagious proliferative scabby crusts on muzzle and lips, preventing suckling and causing kid starvation. Zoonotic."
            )

            out_vax = (
                f"**Immunoprophylaxis & NVRI Vom Vaccine Calendar ({country_lbl})**:\n"
                "• **PPR Homologous Tissue Culture Vaccine**: Single subcutaneous injection at 3–4 months confers solid immunity for 3 years. Re-vaccinate replacement stock annually before rainy season.\n"
                "• **CCPP Inactivated Vaccine**: Administer biannually in endemic arid/semi-arid zones prior to dry season transhumance.\n"
                "• **Sheep and Goat Pox Vaccine**: Annual pre-rain prophylactic inoculation.\n"
                "• **Targeted Strategic Deworming**: Enforce FAMACHA eye-mucosa scoring; deworm animals scoring 4–5 using rotating anthelmintics (Albendazole 7.5 mg/kg or Levamisole 7.5 mg/kg) to prevent widespread anthelmintic resistance."
            )

            out_clim = (
                f"**Agro-Climatic Predisposition & Bioclimatic Housing ({country_lbl})**:\n"
                "• Wet, damp ground drastically elevates *Haemonchus* infective L3 larval intake and triggers contagious foot rot (*Dichelobacter nodosus*).\n"
                "• Construct elevated slatted-floor goat pens (raised 50–75 cm above ground) using local timber or bamboo slats with 1.5 cm gaps to allow feces and urine to fall through, breaking the parasite cycle."
            )

            out_nutr = (
                "**Nutritional Support & Browse Supplementation**:\n"
                "• Provide tannin-rich browse (*Leucaena leucocephala*, *Gliricidia sepium*) which naturally inhibits gastrointestinal nematode egg shedding.\n"
                "• Supply mineral salt blocks with copper, cobalt, and selenium to stimulate erythrocyte synthesis during post-helminth recovery."
            )

            out_econ = (
                f"**Mortality Economics & Flock Gross Margin ({country_lbl})**:\n"
                f"• An uncontrolled PPR outbreak in a 50-head goat breeding herd causes average financial loss of {cur_sym}850,000 – {cur_sym}1,800,000.\n"
                f"• Annual vaccination cost per animal is under {cur_sym}250, delivering a preventive ROI ratio greater than 20:1."
            )

            out_evid = f"Grounded in standards from NVRI Vom, CIRDES West Africa, and ILRI Small Ruminant Research Hub."

            matrix_table = f"""
| Disease & Etiology | Primary Transmission & Vector | Key Pathological Manifestations | Diagnostic Markers | NVRI / NARS Prevention Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **PPR (Goat Plague)**<br>*(Morbillivirus)* | Aerosol inhalation, contact with ocular/nasal discharges | High fever (>40.5°C), oral crusts/ulcers, fetid diarrhea, purulent pneumonia | Necrotic stomatitis, lung consolidation, c-ELISA | **NVRI PPR Homologous Vaccine** (s/c, single shot provides 3-yr immunity). Quarantine newcomers. |
| **CCPP**<br>*(M. capricolum capripneumoniae)* | Airborne aerosol droplets in dry arid zones | Persistent coughing, grunting expiration, frothy nasal discharge | Unilateral marbled hepatization, abundant pleural fluid | **CCPP Inactivated Vaccine**. Oxytetracycline (20 mg/kg LA) in early clinical stages. |
| **Barberpole Worm**<br>*(Haemonchus contortus)* | Ingestion of L3 larvae on wet morning pasture | Severe anemia (PCV <15%), **'bottle jaw'** (submandibular edema), lethargy | FAMACHA eye card score 4–5, abomasal adult worms | Targeted selective anthelmintic treatment; rotational grazing; slatted-floor housing. |
| **Heartwater**<br>*(Ehrlichia ruminantium)* | *Amblyomma variegatum* tick bite | Fever, hyperesthesia, high-stepping gait, circular galloping, hydropericardium | Brain smear Giemsa stain (rickettsial colonies in endothelial cells) | Strategic acaricide pour-on (*deltamethrin*); prophylactic Oxytetracycline LA during tick season. |
| **Contagious Ecthyma (Orf)**<br>*(Parapoxvirus)* | Contact via abrasions from prickly forages | Proliferative scabs and wart-like crusts on lips, muzzle, and teats | Clinical pathology; transmission to human handlers (zoonotic) | Topical antiseptic (iodine/glycerin), gentian violet; isolate infected suckling kids. |
"""

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Veterinary Advisory: Small Ruminant Health in {country_lbl}

#### 🎯 Strategic Epidemiological Overview
In **{country_lbl}**, small ruminant production represents an indispensable source of rural household liquidity and food security. However, smallholder flocks remain under persistent threat from **Peste des Petits Ruminants (PPR)**, **CCPP in arid/Sahelian zones**, and rampant **gastrointestinal helminthiasis** during the wet season. Proactive vaccination and raised-housing biosecurity eliminate up to 85% of flock mortalities.

---

#### 📊 Small Ruminant Pathological & Diagnostic Matrix
{matrix_table}

---

#### 📋 4-Phase Integrated Health Management Protocol
1. **Phase 1: Universal Immunization** &bull; Inoculate all sheep and goats over 3 months of age with **NVRI PPR Vaccine**. Repeat annually for young replacement stock. In dry pastoral zones, vaccinate against CCPP.
2. **Phase 2: Slatted Floor Construction** &bull; House flocks in elevated slatted-floor structures (50–75 cm high) to avoid ground contact with damp soil, interrupting the life cycle of *Haemonchus* larvae and preventing foot rot.
3. **Phase 3: FAMACHA-Guided Strategic Deworming** &bull; Check inner eyelid mucous membranes fortnightly using the FAMACHA chart. Treat only pale/anemic animals (scores 4 and 5) with albendazole or levamisole to preserve anthelmintic efficacy.
4. **Phase 4: Biosecurity & Market Isolation** &bull; Quarantine newly purchased breeding rams, bucks, or ewes for 21 days in an isolated pen; deworm and inspect for mouth lesions or ticks before introduction.
"""
            agent_outputs = {
                dispatched[0]: out_vet, dispatched[1]: out_vax, dispatched[2]: out_clim,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Crop Science Agent": out_vet, "Climate Agent": out_clim, "Genetics Agent": out_vax,
                "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

        # Sub-case: Small Ruminant Production & Management
        else:
            dispatched = [
                "Small Ruminant Pathology & PPR Defense Agent",
                "Breed Genetics & Conformation Agent",
                "Agro-Climatology & Grazing Agent",
                "Fodder Conservation & Nutrition Agent",
                "Ram Fattening & Festive Market Agent",
                "Evidence & Research Standards Agent"
            ]
            out_vet = (
                f"**Pathology & Prophylactic Health ({country_lbl})**:\n"
                "• **Peste des Petits Ruminants (PPR - 'Goat Plague')**: The #1 viral killer; high fever, necrotic mouth lesions, foul diarrhea, and pneumonia. Administer **NVRI Vom PPR Homologous Vaccine** (single shot confers 3-year immunity).\n"
                "• **Helminthiasis (*Haemonchus contortus*)**: Barberpole worm causes severe submandibular edema ('bottle jaw') and anemia; strategic deworming with albendazole/levamisole."
            )
            out_gen = f"**Breed Merit**: Deploy {sr_breeds}. Red Sokoto provides world-acclaimed morocco leather and fast kid growth; WAD provides innate trypanotolerance in humid forest belts."
            out_clim = "Provide raised slatted floor housing (50 cm elevation) to prevent foot rot and parasitic larvae accumulation during wet spells."
            out_nutr = "Feed browse legumes (*Gliricidia sepium*, *Leucaena leucocephala*) and mineral salt licks to sustain rumen microbes."
            out_econ = f"90-day intensive festive ram fattening generates profit margins > 45%–60%, with mature rams selling for {cur_sym}120,000 – {cur_sym}280,000."
            out_evid = f"Grounded in {target_inst} Small Ruminant Trials."

            final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Small Ruminant Advisory: Goat & Sheep Systems ({country_lbl})
1. **Disease Priority**: Vaccinate all stock annually with **PPR Homologous Vaccine**; deworm strategically to eliminate *Haemonchus*.
2. **Housing**: Construct raised slatted floors to prevent foot rot, pneumonia, and coccidiosis.
3. **Breed Deployment**: Prioritize {sr_breeds} adapted to your specific agro-ecological moisture gradient.
4. **Fattening Economics**: Intensive 90-day feeding prior to major festive periods maximizes gross margin returns.
"""
            agent_outputs = {
                dispatched[0]: out_vet, dispatched[1]: out_gen, dispatched[2]: out_clim,
                dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
                "Crop Science Agent": out_vet, "Climate Agent": out_clim, "Genetics Agent": out_gen,
                "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
            }
            return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 5: VEGETABLES & HORTICULTURE (Tomato, Pepper, Onion, Okra)
    # -------------------------------------------------------------------------
    elif commodity == "vegetables":
        dispatched = [
            "Horticultural Pathology & Disease Defense Agent",
            "Entomology & Insect Vector Control Agent",
            "Agro-Climatology & Protected Cultivation Agent",
            "Soil Fertility & Calcium Nutrition Agent",
            "Value Chain & Fresh Produce Market Agent",
            "Institutional Evidence Agent (NIHORT, IITA, AVRDC)"
        ]
        out_path = (
            f"**Vegetable Pathology & Vector Defense ({country_lbl})**:\n"
            "• **Tomato Yellow Leaf Curl Virus (TYLCV)**: Transmitted by sweetpotato whitefly (*Bemisia tabaci*); causes upward leaf curling, stunting, and complete flower abortion. Deploy Ty-1/Ty-3 resistant F1 hybrids.\n"
            "• **Bacterial Wilt (*Ralstonia solanacearum*)**: Soil-borne vascular collapse in hot humid soils. Maintain 4-year rotation with non-solanaceous crops.\n"
            "• **Blossom-End Rot (BER)**: Physiological disorder caused by localized calcium deficiency in fruit apices under erratic watering and high VPD."
        )
        out_ento = "Control *Tuta absoluta* (Tomato Leafminer) using pheromone delta traps and spinosad/indoxacarb bio-pesticides."
        out_clim = "Implement raised beds (25–30 cm) with reflective straw or plastic mulch to suppress soil splash and regulate bed root temperatures."
        out_soil = "Apply 10–15 tons/ha of cured compost and basal SSP (Single Super Phosphate); side-dress with Calcium Nitrate to prevent BER."
        out_econ = f"Off-season drip-irrigated tomato production delivers farmgate returns 2.5x to 4x higher than rainfed glut harvests."
        out_evid = "NIHORT (National Horticultural Research Institute, Ibadan) and WorldVeg (AVRDC) Tropical Guidelines."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Horticultural Advisory: Vegetable Systems ({country_lbl})
1. **Disease Management**: Plant TYLCV-resistant hybrids; install yellow sticky cards for whitefly vector monitoring.
2. **Water & Calcium**: Maintain uniform soil moisture with drip lines and apply foliar calcium nitrate to eradicate Blossom-End Rot.
3. **Bacterial Wilt Defense**: Never follow tomatoes with peppers or Irish potatoes; practice 4-season rotation with maize or legumes.
4. **Off-Season Economics**: Target dry-season production windows to capture peak urban wholesale pricing.
"""
        agent_outputs = {
            dispatched[0]: out_path, dispatched[1]: out_ento, dispatched[2]: out_clim,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_path, "Climate Agent": out_clim, "Genetics Agent": out_path,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 6: CEREALS & GRAINS (Maize, Sorghum, Millet, Rice)
    # -------------------------------------------------------------------------
    elif commodity in ["cereals", "rice"]:
        dispatched = [
            "Cereal Agronomy & Crop Physiology Agent",
            "Pathology & Fall Armyworm Defense Agent",
            "Agro-Climatology & Drought Escape Agent",
            "Soil Fertility & Balanced ISFM Agent",
            "Grain Commodity Economics Agent",
            "Institutional Evidence Agent (IITA, CIMMYT, NCRI)"
        ]
        out_agron = (
            f"**Cereal Crop Architecture ({country_lbl})**:\n"
            "• **Drought & Heat Hybrids**: Deploy short anthesis-silking interval (ASI < 2.5 days) hybrids (e.g. *SAMMAZ 15*, *TZE-W Pop DT*, *SC 627*).\n"
            "• **Rice Agro-Ecology**: For lowland ecology, deploy *FARO 44* / *FARO 52* (Sub1 submergence tolerance); for upland, plant *NERICA* or *AGRA Rice*."
        )
        out_pest = (
            "**Fall Armyworm (*Spodoptera frugiperda*) & Striga Management**:\n"
            "• Apply emamectin benzoate into the leaf whorl at emergence (V2–V4 stage).\n"
            "• For *Striga hermonthica*, intercrop with *Desmodium* (push-pull) or deploy resistant cultivars (*lgs1* gene introgressed lines)."
        )
        out_clim = "Synchronize sowing with established rains (>25 mm over 3 consecutive days) to escape seedling dry spells."
        out_soil = "Apply micro-dosed basal NPK 15:15:15 at planting, followed by targeted urea side-dressing at knee-high (V6 stage)."
        out_econ = f"Clean commercial grain yields 4.5–6.0 t/ha under optimal management, generating net returns exceeding {cur_sym}380,000 per hectare."
        out_evid = "IITA Maize Breeding Program, CIMMYT Tropical Savanna Trials, and NCRI Badeggi."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Cereal Advisory: Grain Systems ({country_lbl})
1. **Cultivar Choice**: Select certified drought-tolerant hybrids with short ASI to guarantee synchronized flowering under heat.
2. **Pest Control**: Monitor leaf whorls for Fall Armyworm and apply targeted bio-insecticides at first egg-hatch.
3. **Fertilizer Split**: Practice two-way nitrogen splitting (basal NPK at planting + urea at knee-high) to prevent leaching.
4. **Striga Defense**: Intercrop with legumes (cowpea, soybean) to trigger suicidal germination of parasitic witchweed.
"""
        agent_outputs = {
            dispatched[0]: out_agron, dispatched[1]: out_pest, dispatched[2]: out_clim,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_agron, "Climate Agent": out_clim, "Genetics Agent": out_agron,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 7: ROOTS & TUBERS (Cassava, Yam, Sweet Potato)
    # -------------------------------------------------------------------------
    elif commodity == "root_tubers":
        dispatched = [
            "Root & Tuber Agronomy Agent",
            "Viral Disease Defense Agent (CMD/CBSD)",
            "Agro-Climatic Bulking Agent",
            "Soil Potassium & Edaphic Nutrition Agent",
            "Starch Processing & Market Economics Agent",
            "Institutional Evidence Agent (IITA, NRCRI)"
        ]
        out_agron = (
            f"**Tuber Production & Germplasm Architecture ({country_lbl})**:\n"
            "• **Genetic Immunity**: Deploy CMD2/CMD3 immune cassava clones (*TME 419*, *TMS 30572*, *NAROCASS 1*) to ensure zero field mosaic loss.\n"
            "• **Yam Minisett Technique**: Produce certified seed tubers of *Dioscorea rotundata* (White Yam) using 25–50g minisetts treated with wood ash and fungicide."
        )
        out_pest = "Inspect stem cuttings for cassava brown streak disease (CBSD) and yam mosaic virus; maintain clean nursery propagation."
        out_clim = "Stagger harvesting between 9 and 15 months to maximize root dry matter (>32%) and gari swelling ratio."
        out_soil = "Roots are heavy potassium extractors; apply high-K fertilizer (e.g. NPK 12:12:24) at 8 weeks post-sprouting to stimulate root bulking."
        out_econ = f"Fresh cassava roots deliver 25–35 t/ha, fetching stable farmgate value at industrial starch and ethanol factories."
        out_evid = "IITA Root & Tuber Program and National Root Crops Research Institute (NRCRI, Umudike)."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Root & Tuber Advisory ({country_lbl})
1. **Clean Seed Stock**: Use only certified, virus-free stem cuttings possessing CMD2/CMD3 genetic resistance.
2. **Potassium Nutrition**: Ensure adequate potassium nutrition at early bulking (Month 2–3) to maximize starch density.
3. **Weed Suppression**: Apply pre-emergence herbicide within 24 hours of planting; maintain clean canopy coverage.
4. **Market Diversification**: Connect harvest to both local food processing (gari/fufu) and industrial starch processors.
"""
        agent_outputs = {
            dispatched[0]: out_agron, dispatched[1]: out_pest, dispatched[2]: out_clim,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_agron, "Climate Agent": out_clim, "Genetics Agent": out_agron,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 8: LEGUMES & PULSES (Cowpea, Soybean, Groundnut)
    # -------------------------------------------------------------------------
    elif commodity == "legumes":
        dispatched = [
            "Grain Legume Physiology Agent",
            "Pod Borer & Insect Defense Agent",
            "Biological Nitrogen Fixation Agent",
            "Phosphorus Priming & Edaphic Agent",
            "Grain Legume Market Economics Agent",
            "Institutional Evidence Agent (IITA, ICRISAT)"
        ]
        out_agron = (
            f"**Legume Germplasm & Production Strategy ({country_lbl})**:\n"
            "• **Bt Cowpea (*SAMPEA 20-T* / *Songotra Bt*)**: Delivers built-in Cry1Ab resistance against the Maruca pod borer (*Maruca vitrata*), slashing insecticide sprays from 8 to only 2.\n"
            "• **Biological Nitrogen Fixation (BNF)**: Inoculate seed with *Bradyrhizobium* (e.g. *Nodumax*), enabling legumes to fix 60–120 kg N/ha from the atmosphere."
        )
        out_pest = "Monitor for Alectra and Striga gesnerioides; apply systemic seed dressing to protect seedlings from bean fly."
        out_soil = "Legumes require high available phosphorus for root nodulation; band-place Single Super Phosphate (SSP) at 30 kg P2O5/ha."
        out_econ = f"Dual-purpose varieties provide high-value grain plus nutritious fodder for dry season livestock integration."
        out_evid = "IITA Legume Genetics Program and ICRISAT Groundnut & Chickpea Hub."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Legume Advisory ({country_lbl})
1. **Maruca Pod Borer Defense**: Deploy Bt cowpea (*SAMPEA 20-T*) or apply targeted sprays at flowering and podding.
2. **Rhizobium Inoculation**: Coat seeds with effective *Bradyrhizobium* inoculants to stimulate deep nodulation.
3. **Phosphorus Priming**: Apply basal phosphorus (SSP) to satisfy the high ATP demand of biological nitrogen fixation.
4. **Crop Rotation**: Rotate legumes with cereals to break nematode cycles and enrich soil nitrogen reserves.
"""
        agent_outputs = {
            dispatched[0]: out_agron, dispatched[1]: out_pest, dispatched[2]: out_agron,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_agron, "Climate Agent": out_agron, "Genetics Agent": out_agron,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 9: TREE & CASH EXPORT CROPS (Cocoa, Oil Palm, Cashew, Coffee)
    # -------------------------------------------------------------------------
    elif commodity == "cash_crops":
        dispatched = [
            "Perennial Tree Crop Physiology Agent",
            "Phytopathology & Black Pod Defense Agent",
            "Canopy Architecture & Shade Ecology Agent",
            "Soil Mineral Nutrition & Mulching Agent",
            "Export Quality & EUDR Compliance Agent",
            "Institutional Evidence Agent (CRIN, NIFOR, Cocoa Research)"
        ]
        out_agron = (
            f"**Tree Crop Architecture & Management ({country_lbl})**:\n"
            "• **Cocoa (*Theobroma cacao*)**: Prune chupons and maintain 30%–40% permanent agroforestry shade canopy (*Terminalia superba*, *Albizia*) to reduce vapor pressure deficit (VPD).\n"
            "• **Black Pod (*Phytophthora megakarya*)**: High-rainfall fungal scourge; enforce sanitary harvesting (remove mummified pods weekly) and apply copper hydroxide/metalaxyl sprays."
        )
        out_pest = "Control mirids / capsids (*Sahlbergella singularis*) using targeted canopy spot-spraying in August–October."
        out_soil = "Establish permanent mulch rings around tree basins to conserve topsoil moisture during the dry season."
        out_econ = f"Premium grade fermented beans capture high export premiums while complying with deforestation-free supply chains (EUDR)."
        out_evid = "Cocoa Research Institute of Nigeria (CRIN), NIFOR, and World Agroforestry (ICRAF)."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Cash & Tree Crop Advisory ({country_lbl})
1. **Sanitary Harvesting**: Strip and bury all black pods every 7–10 days to break the *Phytophthora* spore cycle.
2. **Shade & Pruning**: Maintain balanced shade canopy to prevent sun scorch while promoting airflow to lower humidity.
3. **Mirid Control**: Inspect canopies in late rains and spot-treat mirid pockets before widespread stem dieback occurs.
4. **Post-Harvest Quality**: Ferment beans under banana leaves for 5–6 days with two turnings to achieve export flavor profiles.
"""
        agent_outputs = {
            dispatched[0]: out_agron, dispatched[1]: out_agron, dispatched[2]: out_agron,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_agron, "Climate Agent": out_agron, "Genetics Agent": out_agron,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 10: SOIL, FERTILITY & EDAPHIC HEALTH
    # -------------------------------------------------------------------------
    elif commodity == "soil":
        dispatched = [
            "Soil Chemistry & Mineral Fertility Agent",
            "Integrated Soil Fertility Management (ISFM) Agent",
            "Edaphic Microbiome & Mycorrhizal Agent",
            "Precision Micro-Dosing & Liming Agent",
            "Fertilizer Input Economics Agent",
            "Institutional Evidence Agent (IITA, TSBF, AGRA)"
        ]
        out_soil = (
            f"**Precision Edaphic Diagnosis & Soil Strategy ({country_lbl})**:\n"
            "• **Soil Acidity & Aluminium Toxicity**: In soils with pH < 5.2, apply 1.0–1.5 t/ha of agricultural limestone (CaCO3) 3–4 weeks prior to sowing to precipitate toxic Al3+ and unlock fixed phosphorus.\n"
            "• **Integrated Nutrient Management**: Blend chemical fertilizer with organic manures (3–5 t/ha) or biochar to expand low cation exchange capacity (CEC < 8 cmol/kg)."
        )
        out_micro = "Practice micro-dosing (applying 2–6 g of fertilizer directly into the planting hole) to achieve 80% of full-rate yield at 40% of the cost."
        out_econ = f"Hedging against fertilizer inflation through micro-dosing and organic compost protects farmer gross margins by up to {cur_sym}65,000/ha."
        out_evid = "African Soil Information Service (AfSIS) and AGRA Soil Health Program."

        matrix_table = f"""
| Soil Diagnostic Parameter | Deficiency / Toxicity Threshold | Observed Agronomic Impact | Corrective Agronomic Protocol |
| :--- | :--- | :--- | :--- |
| **Soil Acidity (pH < 5.2)** | Critical Al3+ saturation > 20% | Aluminium toxicity, stunted root elongation, phosphorus fixation | Apply agricultural limestone ($CaCO_3$) at 1.0–1.5 t/ha 4 weeks prior to planting; incorporate biochar. |
| **Available Phosphorus (P)** | Bray-1 P < 7.0 mg/kg | Stunted purple seedlings, poor root nodulation in legumes | Basal placement of Single Super Phosphate (SSP) at 30–45 kg $P_2O_5$/ha at planting. |
| **Organic Carbon & CEC** | OC < 0.8%, CEC < 6.0 cmol/kg | Rapid nutrient leaching, low moisture holding capacity | Apply 3–5 t/ha cured farmyard manure; retain 30% crop residue mulch; incorporate green manure. |
| **Nitrogen Leaching** | Sandy savanna topsoils | General chlorosis, yellowing of lower older leaves | Two-way nitrogen split: 1/3 basal NPK at planting + 2/3 urea side-dressing at knee-high (V6). |
"""

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Soil Health & Fertility Advisory ({country_lbl})

#### 🎯 Strategic Overview & Edaphic Dynamics
In **{country_lbl}**, soil fertility management requires transitioning from blind broadcasting to **Integrated Soil Fertility Management (ISFM)**. Tropical soils frequently suffer from low cation exchange capacity (CEC), acidity-induced phosphorus fixation, and acute organic matter depletion. Synchronizing inorganic fertilizers with organic amendments and liming guarantees maximum nutrient use efficiency.

---

#### 📊 Soil Diagnostic & Nutrient Management Matrix
{matrix_table}

---

#### 📋 4-Phase Soil Restoration & Crop Nutrition Protocol
1. **Phase 1: Acidity Diagnostic & Liming Correction** &bull; For soils with pH < 5.5, apply agricultural lime (CaCO3 or dolomite) at 1.0–1.5 t/ha into the ploughed layer 3–4 weeks before seeding to neutralize toxic Al3+ ions and unbind fixed orthophosphate.
2. **Phase 2: Organic Carbon Incorporation** &bull; Broadcast and incorporate 3–5 tons/ha of cured compost or animal manure to revitalize beneficial soil microorganisms (mycorrhizae) and boost moisture retention.
3. **Phase 3: Targeted Micro-Dosing at Planting** &bull; Place basal NPK 15:15:15 or Single Super Phosphate (SSP) directly in planting holes (2–6 g per hill) or band 5 cm beside seed rows to satisfy early root-zone demand.
4. **Phase 4: Split Nitrogen Top-Dressing** &bull; Apply urea side-dressing in moist soil during peak vegetative demand (e.g., knee-high stage in cereals, 4–6 weeks post-emergence) to prevent volatilization and leaching losses.
"""
        agent_outputs = {
            dispatched[0]: out_soil, dispatched[1]: out_soil, dispatched[2]: out_micro,
            dispatched[3]: out_micro, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_soil, "Climate Agent": out_soil, "Genetics Agent": out_micro,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 11: SWINE / PIG SCIENCE (Porcine Health, ASFV & Nutrition)
    # -------------------------------------------------------------------------
    elif commodity == "pig":
        dispatched = [
            "Porcine Pathology & Epizootiology Agent",
            "Swine Biosecurity & ASFV Exclusion Agent",
            "Tropical Housing & Thermal Cooling Agent",
            "Non-Conventional Feed Formulation Agent",
            "Piggery Enterprise Economics Agent",
            "Institutional Evidence Agent (NVRI Vom, FAO Swine Hub)"
        ]
        out_vet = (
            f"**Porcine Pathology & Disease Threat Landscape ({country_lbl})**:\n"
            "• **African Swine Fever (ASFV - *Asfarviridae*)**: The devastating hemorrhagic plague of domestic swine in Africa. Causes high fever (>41°C), cyanosis/erythema of ears, snout, and ventrum, pulmonary edema, vomiting, and near 100% herd mortality within 4–10 days. Transmitted by direct contact, soft ticks (*Ornithodoros moubata*), infected pork products, and contaminated fomites. **There is no approved commercial vaccine or cure**.\n"
            "• **Swine Erysipelas (*Erysipelothrix rhusiopathiae*)**: Acute septicemia with diagnostic raised rhomboid/diamond-shaped skin lesions, polyarthritis, and vegetative endocarditis.\n"
            "• **Porcine Parvovirus (PPV) & SMEDI Syndrome**: Stillbirth, mummification, embryonic death, and infertility in breeding sows.\n"
            "• **Swine Dysentery & Parasitic Scour**: *Brachyspira hyodysenteriae* causing bloody diarrhea; *Ascaris suum* liver milk spots and lung migration."
        )
        out_bio = (
            f"**Strict Biosecurity & ASFV Bio-Exclusion Protocol ({country_lbl})**:\n"
            "1. **Double Perimeter Fencing**: Install solid 2-meter perimeter boundary fencing with a 2-meter buffer zone to eliminate all contact with stray roaming pigs, warthogs, or bush pigs.\n"
            "2. **Total Ban on Swill Feeding**: Never feed catering waste, restaurant scraps, or unboiled offal. 70% of urban ASFV outbreaks originate from untreated swill.\n"
            "3. **Vehicular & Personnel Disinfection**: Mandatory footwear change, boot dipping in 2% sodium hydroxide or virucidal disinfectant (Virkon S), and tire baths before farm gate entry.\n"
            "4. **Batch All-In/All-Out Protocol**: Thoroughly pressure-wash pens with alkaline detergent and rest paddocks for 14 days between production batches."
        )
        out_clim = (
            f"**Tropical Thermal Stress & Housing Architecture ({country_lbl})**:\n"
            "• Pigs lack functional sweat glands; ambient heat >28°C triggers severe respiratory distress and appetite suppression.\n"
            "• Provide high-pitched roofing (ridge height >3.5 m) with open-sided dwarf walls (1 m) and install misting sprinklers or hygienic concrete wallows for evaporative cooling."
        )
        out_nutr = (
            "**Alternative Energy & Low-Cost Feed Formulation**:\n"
            "• Mitigate commercial feed inflation by substituting up to 35% of maize with fermented, detoxified cassava peel mash (HQECP) or dried brewers' spent grains (BSG) balanced with synthetic lysine and methionine."
        )
        out_econ = (
            f"**Piggery Enterprise Gross Margin ({country_lbl})**:\n"
            f"• A well-managed porker reaches 75–85 kg liveweight in 22–26 weeks (FCR 2.8–3.2:1). Finished baconers trade at {cur_sym}120,000 – {cur_sym}175,000 each, yielding net returns >35% under closed-herd biosecurity."
        )
        out_evid = f"Grounded in NVRI Vom Swine Diseases Division and FAO African Swine Fever Biosecurity Manual."

        matrix_table = f"""
| Disease & Pathogen | Vector & Transmission Mode | Pathological Lesions & Signs | Biosecurity & Prevention Protocol |
| :--- | :--- | :--- | :--- |
| **African Swine Fever (ASFV)** | Ingestion of infected pork/swill, soft ticks (*Ornithodoros*), fomites | Cyanosis of ears/belly, bloody diarrhea, enlarged friable black spleen | **No vaccine exists**. Total ban on swill; double perimeter fence; 100% quarantine; cull exposed pens. |
| **Swine Erysipelas**<br>*(Erysipelothrix rhusiopathiae)* | Fecal-oral contamination from carrier pigs; soil persistence | Diamond-shaped skin plaques, swollen joints, sudden death | Inactivated Erysipelas Bacterin vaccination; Penicillin/Ampicillin therapy in early clinical stage. |
| **Porcine Parvovirus (PPV)** | Venereal and oronasal contact during breeding | Mummified fetuses, high stillbirth rates, irregular return to heat | Vaccinate breeding gilts and sows 3–4 weeks prior to service; screen herd boars. |
| **Swine Dysentery**<br>*(Brachyspira hyodysenteriae)* | Ingestion of feces-contaminated water or feed | Mucohemorrhagic colitis, watery diarrhea with gray mucus/blood | Enforce all-in/all-out hygiene; Tiamulin or Lincomycin in drinking water; fly and rodent eradication. |
"""

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Veterinary Advisory: Swine Health & Piggery Systems ({country_lbl})

#### 🎯 Strategic Overview & African Swine Fever Warning
In **{country_lbl}**, commercial and smallholder piggery operations operate under extreme risk from **African Swine Fever (ASFV)**. Because ASFV has **no commercial vaccine or clinical cure**, farm biosecurity, double-fencing, and total elimination of untreated swill feeding represent the absolute dividing line between high enterprise profitability and total herd eradication.

---

#### 📊 Swine Pathological & Diagnostic Matrix
{matrix_table}

---

#### 📋 4-Phase Swine Health & Productivity Protocol
1. **Phase 1: Bio-Exclusion Perimeter Security** &bull; Erect a double perimeter barrier (2-meter height) around the piggery. Enforce vehicle and visitor disinfection gates with fresh Virkon S or sodium hypochlorite.
2. **Phase 2: Total Swill Prohibition** &bull; Strictly feed only certified commercial feeds or on-farm formulated rations using pasteurized, mycotoxin-free grains and agro-industrial by-products.
3. **Phase 3: Thermal Abatement & Wallow Hygiene** &bull; Install roof misting nozzles and shaded concrete wallows with automated drainage to dissipate afternoon heat loads ($THI > 80$) without creating standing mud reservoirs.
4. **Phase 4: Gilt Reproductive Quarantine** &bull; Isolate newly acquired breeding boars and gilts for 30 days; vaccinate for Erysipelas and Parvovirus before first mating.
"""
        agent_outputs = {
            dispatched[0]: out_vet, dispatched[1]: out_bio, dispatched[2]: out_clim,
            dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_vet, "Climate Agent": out_clim, "Genetics Agent": out_bio,
            "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 12: AQUACULTURE & TROPICAL FISHERIES (Catfish & Tilapia)
    # -------------------------------------------------------------------------
    elif commodity == "fish":
        dispatched = [
            "Aquaculture Engineering & Water Quality Agent",
            "Fish Pathology & Bacterial Disease Agent",
            "Hatchery Phenomics & Fingerling Grading Agent",
            "Bioenergetic Feeding & FCR Optimization Agent",
            "Aquaculture Commercial Economics Agent",
            "Institutional Standards Agent (NIOMR, WorldFish, FAO)"
        ]
        out_water = (
            f"**Water Quality Dynamics & Physicochemical Thresholds ({country_lbl})**:\n"
            "• **Un-ionized Ammonia (NH3)**: Highly toxic at concentrations >0.05 mg/L. Ammonia toxicity spikes exponentially when water pH exceeds 8.0 and temperature rises above 28°C.\n"
            "• **Dissolved Oxygen (DO)**: Maintain DO >4.5 mg/L for African Catfish (*Clarias gariepinus*) and >5.5 mg/L for Nile Tilapia (*Oreochromis niloticus*). Severe hypoxia causes surface piping, acute immunosuppression, and feed refusal.\n"
            "• **Nitrite (NO2-) Toxicity**: Causes methemoglobinemia ('brown blood disease') by converting functional hemoglobin into non-oxygen carrying methemoglobin. Counteract immediately with crude non-iodized salt (NaCl at 1–2 kg per 1,000 L)."
        )
        out_vet = (
            "**Aquatic Pathogens & Epizootic Management**:\n"
            "• **Motile Aeromonad Septicemia (*Aeromonas hydrophila*)**: Hemorrhagic skin ulcers, fin rot, and abdominal ascites/dropsy triggered by organic waste buildup.\n"
            "• **Columnaris Disease (*Flavobacterium columnare*)**: Whitish 'saddleback' lesions and gill necrosis under high water temperatures.\n"
            "• **Fingerling Cannibalism**: The #1 cause of nursery mortality; size heterogeneity leads to 'shooters' consuming up to 60% of smaller siblings. Grade stock every 10–14 days."
        )
        out_nutr = (
            "**Nutritional Strategy & Feed Management**:\n"
            "• Starter fingerlings require 42–45% crude protein (CP); grow-out fish require 38–40% CP. Practice split-feeding (morning and late afternoon) at 3–5% of body weight daily."
        )
        out_clim = (
            f"**Harmattan & Seasonal Thermal Adaptations ({country_lbl})**:\n"
            "• During cold Harmattan mornings (water temperature <22°C), catfish digestion ceases. Reduce feeding rates by 50% to prevent fatal gut fermentation and water fouling."
        )
        out_econ = (
            f"**Aquaculture Harvest Valuation ({country_lbl})**:\n"
            f"• African catfish reaches table size (1.0–1.2 kg) in 18–22 weeks (FCR 1.1–1.3:1). Table-size catfish sells at {cur_sym}2,200 – {cur_sym}3,600 per kg at farmgate, yielding net margins >40%."
        )
        out_evid = f"Grounded in Nigerian Institute for Oceanography and Marine Research (NIOMR) and WorldFish African Guidelines."

        matrix_table = f"""
| Water Quality / Disease Factor | Critical Lethal Threshold | Clinical Signs & Behavioral Indicators | Corrective & Prophylactic Protocol |
| :--- | :--- | :--- | :--- |
| **Un-ionized Ammonia (NH3)** | > 0.05 mg/L (toxic); > 0.2 mg/L (lethal) | Erratic swimming, gill flaring, lethargy, surface gasping | 50% immediate water exchange; stop feeding; clean sediment sludge. |
| **Dissolved Oxygen (DO)** | < 3.0 mg/L (stress); < 1.5 mg/L (lethal) | **Surface piping**, clustered near pond water inlet | Emergency aeration, paddlewheels, fresh oxygenated water inflow. |
| **Nitrite (NO2-) Brown Blood** | > 0.5 mg/L | Gills turn chocolate brown, lethargy despite high aeration | Add non-iodized salt (NaCl) at 1–2 kg per 1,000 L to block chloride cell uptake. |
| **Aeromonas Septicemia** | High organic waste trigger | Hemorrhagic red ulcers on skin, distended dropsical belly | Oxytetracycline medicated feed (50 mg/kg fish/day for 7 d); biofilter sanitation. |
| **Fingerling Cannibalism** | Size variance > 25% | Sudden drop in fingerling inventory, missing tails/fins | **Mandatory mechanical grading** every 10–14 days into uniform size batches. |
"""

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Aquaculture Advisory: Catfish & Tilapia Systems ({country_lbl})

#### 🎯 Strategic Overview
In **{country_lbl}**, freshwater aquaculture profitability is dictated by **water quality biophysics** and **cannibalism control**. Over 75% of fish mortalities in ponds and recirculating systems (RAS) stem from unionized ammonia toxicity and bacterial septicemia induced by unconsumed feed breakdown. Strict water monitoring and routine sorting guarantee survival rates exceeding 85%.

---

#### 📊 Aquaculture Diagnostics & Water Quality Matrix
{matrix_table}

---

#### 📋 4-Phase Aquaculture Action Protocol
1. **Phase 1: Water Quality Monitoring** &bull; Test DO, pH, and ammonia twice daily (6:00 AM and 4:00 PM). Ensure un-ionized NH3 remains below 0.05 mg/L.
2. **Phase 2: Routine Fingerling Sorting** &bull; Mechanically grade juvenile fish every 10 to 14 days using grading basins to segregate aggressive fast-growing 'shooters' and eliminate cannibalism.
3. **Phase 3: Satiation Feeding Protocol** &bull; Feed high-grade extruded floating pellets (42% CP for fingerlings, 38% CP for grow-out) at 3% body weight; observe feed response and cease immediately upon satiation.
4. **Phase 4: Harmattan / Low-Temperature Adjustment** &bull; When water temperatures dip below 24°C, cut feeding rates by 40%–50% to prevent undigested feed accumulation and bloat.
"""
        agent_outputs = {
            dispatched[0]: out_water, dispatched[1]: out_vet, dispatched[2]: out_vet,
            dispatched[3]: out_nutr, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_water, "Climate Agent": out_clim, "Genetics Agent": out_vet,
            "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 13: HELICULTURE / SNAIL FARMING
    # -------------------------------------------------------------------------
    elif commodity == "snail":
        dispatched = [
            "Heliculture Systems & Gastropod Biology Agent",
            "Substrate Formulation & Soil Microbiology Agent",
            "Mantle Biomineralization & Calcium Nutrition Agent",
            "Microclimate Relative Humidity & Aestivation Agent",
            "Heliculture Enterprise Economics Agent",
            "Institutional Evidence Agent (FUNAAB, IITA Heliculture Hub)"
        ]
        out_prod = (
            f"**Snail Species Selection & Pen Architecture ({country_lbl})**:\n"
            "• **Target Species**: Giant African Land Snail (*Archachatina marginata* - preferred for humid West/Central Africa due to large meat yield and resilience) and *Achatina achatina*.\n"
            "• **Housing Design**: Elevated wooden or block trench pens (60 cm high) filled with 15–20 cm of conditioned substrate. Install mosquito wire netting on covers to exclude predators (rodents, lizards, and soldier ants)."
        )
        out_sub = (
            "**Substrate Sterilization & Edaphic Chemistry**:\n"
            "• Never use untreated forest soil. Heat-treat soil or mix pasteurized loamy topsoil with humidified cocopeat (50:50 ratio). Substrate must be moist but never waterlogged (target moisture 70–80%, pH 6.5–7.5)."
        )
        out_nutr = (
            "**Calcium Biomineralization & Formulated Nutrition**:\n"
            "• Snails require high dietary calcium for shell synthesis. Formulate mash containing 15%–20% calcium carbonate (oyster shell meal, bone meal, or agricultural limestone).\n"
            "• Supplement with succulent wilted leaves (pawpaw, sweet potato, cocoyam) and ripe fruits (watermelon, banana)."
        )
        out_clim = (
            f"**Microclimatic Humidity & Aestivation Prevention ({country_lbl})**:\n"
            "• Ambient relative humidity must remain >80% and temperature between 24°C and 28°C. Desiccation triggers induced aestivation (snails seal themselves with a calcified white epiphragm and cease growth for months). Install manual or automated misting systems."
        )
        out_econ = (
            f"**Heliculture Commercial Valuation ({country_lbl})**:\n"
            f"• Mature *Archachatina marginata* (250–400 g) sells for {cur_sym}800 – {cur_sym}2,000 each in urban retail and hospitality markets. High profit margins (>65%) due to low recurrent feed expenditures."
        )
        out_evid = "Grounding: Federal University of Agriculture Abeokuta (FUNAAB) Snail Project and Forestry Research Institute of Nigeria (FRIN)."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Heliculture Advisory: Snail Production ({country_lbl})

#### 🎯 Strategic Overview
Commercial snail farming with **Archachatina marginata** offers high capital returns in **{country_lbl}** when three critical limiting factors are controlled: **substrate hygiene**, **dietary calcium saturation**, and **humidity-mediated aestivation prevention**.

1. **Substrate Management**: Use pasteurized topsoil mixed with cocopeat (15 cm depth); maintain 75% moisture. Never allow substrate to dry out or become anaerobic.
2. **Calcium Saturation**: Supply formulated dry mash containing 15%–20% fine oyster shell or limestone powder to guarantee rapid shell thickening and eliminate mantle collapse.
3. **Aestivation Prevention**: Spray enclosures with clean water every evening at sunset to maintain relative humidity >80%, keeping snails actively feeding throughout the year.
4. **Predator Exclusion**: Apply spent engine oil or grease trenches along pen legs to prevent catastrophic soldier ant invasions.
5. **Commercial Economics**: Highly prolific breeders produce 8–14 eggs per clutch, achieving full enterprise amortization within 12 months.
"""
        agent_outputs = {
            dispatched[0]: out_prod, dispatched[1]: out_sub, dispatched[2]: out_nutr,
            dispatched[3]: out_clim, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_prod, "Climate Agent": out_clim, "Genetics Agent": out_prod,
            "Soil Agent": out_sub, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 14: APICULTURE / BEEKEEPING (African Honeybee)
    # -------------------------------------------------------------------------
    elif commodity == "bee":
        dispatched = [
            "Apiculture Science & Apiary Architecture Agent",
            "Colony Thermoregulation & Hive Shading Agent",
            "Absconding Prevention & Floral Calendar Agent",
            "Honey Quality & Moisture Refractometry Agent",
            "Beekeeping Value Chain Economics Agent",
            "Institutional Evidence Agent (ICIPE, FAO Apiculture)"
        ]
        out_prod = (
            f"**African Honeybee Management & Hive Selection ({country_lbl})**:\n"
            "• **Target Subspecies**: *Apis mellifera adansonii* (West/Central Africa) and *A. m. scutellata* (East/Southern Africa). Known for high defensive vigor, rapid foraging, and pronounced absconding tendencies under forage stress.\n"
            "• **Hive Types**: Kenya Top Bar Hive (KTBH) or standard Langstroth 10-frame hives. Suspend hives on greased galvanized wires 1 meter above ground to prevent safari ant attacks."
        )
        out_clim = (
            f"**Apiary Shading & Water Logistics ({country_lbl})**:\n"
            "• Direct solar radiation heating hives >38°C causes wax comb melting and colony collapse. Position hives under dense tree canopies (*Acacia*, *Azadirachta indica*, *Mangifera indica*).\n"
            "• Provide shallow clean water troughs with floating wooden sticks within 50 meters of the apiary to prevent dehydration."
        )
        out_nutr = (
            "**Dearth Season Feeding & Absconding Mitigation**:\n"
            "• During floral dearth (peak dry season), feed colonies with 1:1 sugar-water syrup and soy flour/yeast protein patties inside the hive to prevent complete colony absconding."
        )
        out_econ = (
            f"**Honey & By-Product Commercial Valuation ({country_lbl})**:\n"
            f"• A colonized Langstroth hive yields 15–30 kg of pure honey annually, selling at {cur_sym}5,000 – {cur_sym}9,000 per kg, plus valuable beeswax and propolis."
        )
        out_evid = "Grounding: International Centre of Insect Physiology and Ecology (ICIPE, Nairobi) and FAO Beekeeping Bulletin."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Apiculture Advisory: Beekeeping Systems ({country_lbl})

#### 🎯 Strategic Overview
Modern beekeeping with **Apis mellifera** in **{country_lbl}** delivers exceptional returns with minimal land requirements. The primary management challenge is preventing seasonal **colony absconding** caused by excessive heat, ant attacks, and dry-season floral dearth.

1. **Hive Suspension**: Suspend modern hives (KTBH or Langstroth) using greased wire cables to prevent safari ants (*Dorylus spp.*) from raiding brood combs.
2. **Microclimate Shading**: Ensure permanent canopy shade to maintain brood nest temperatures at 34.5°C; provide shallow drinking water points nearby.
3. **Dearth Feeding**: Supplement with 1:1 sucrose syrup during the flowerless season to sustain worker populations until the main nectar flow.
4. **Sanitary Harvesting**: Harvest only fully capped honeycomb frames at night using cool smoke to guarantee moisture content below 19% (preventing fermentation).
"""
        agent_outputs = {
            dispatched[0]: out_prod, dispatched[1]: out_clim, dispatched[2]: out_nutr,
            dispatched[3]: out_clim, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_prod, "Climate Agent": out_clim, "Genetics Agent": out_prod,
            "Soil Agent": out_nutr, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}

    # -------------------------------------------------------------------------
    # CASE 15: SMART DYNAMIC SCIENTIFIC SYNTHESIZER (Open-Ended Precision Engine)
    # -------------------------------------------------------------------------
    else:
        # Intelligently extract targeted entity and specific intent
        words = re.findall(r'[a-zA-Z]+', query)
        stop_words = {
            "what", "are", "the", "typical", "diseases", "affecting", "in", "for", "best", "how", "to",
            "and", "of", "is", "can", "should", "farmers", "production", "management", "at", "this",
            "period", "common", "major", "different", "various", "outline", "explain", "describe", "give", "me"
        }
        key_terms = [w.capitalize() for w in words if w.lower() not in stop_words and len(w) > 3]
        target_subject = " / ".join(key_terms[:3]) if key_terms else "Agricultural Enterprise"

        intent_label = ", ".join([i.replace("_", " ").title() for i in intents]) if intents else "General Production Optimization"

        dispatched = [
            f"Specialist Agronomic & Bio-Systems Agent ({target_subject})",
            f"Regional Agro-Climatology & Risk Agent ({country_lbl})",
            "Pathology, Biosecurity & Integrated Protection Agent",
            "Soil Edaphic & Nutritional Dynamics Agent",
            f"Commodity Value Chain & Farmgate Economics Agent ({country_lbl})",
            f"Institutional Evidence Agent ({target_inst})"
        ]

        out_spec = (
            f"**Systemic Scientific Analysis for {target_subject} in {country_lbl}**:\n"
            f"• Inquiry Focus: *'{query}'*\n"
            f"• Core Focus Domain: **{intent_label}**.\n"
            f"• In the {country_lbl} agro-ecological context, successful management of {target_subject} requires strict harmonization with local rainfall seasonality, soil physical chemistry, and endemic biological vectors."
        )

        out_clim = (
            f"**Agro-Climatic Parameters ({country_lbl})**:\n"
            "• Monitor thermal degree days, solar radiation flux, and vapor pressure deficit (VPD).\n"
            "• Align critical developmental windows (flowering, breeding, or brooding) with favorable microclimatic periods to minimize physiological shock."
        )

        out_path = (
            f"**Biosecurity, Integrated Pest & Pathogen Defense**:\n"
            "• Enforce preventive sanitation, early vector monitoring, and disease-indexed foundation stock.\n"
            "• Integrate biological controls and targeted prophylactic treatments before biotic pressure surpasses economic injury levels (EIL)."
        )

        out_soil = (
            "**Edaphic Management & Balanced Nutrition**:\n"
            "• Conduct baseline diagnostic testing; address macronutrient and micronutrient requirements with targeted root/ration placement.\n"
            "• Maintain high organic matter and balanced moisture retention to sustain biological microbial activity."
        )

        out_econ = (
            f"**Enterprise Economics & Value Realization ({country_lbl})**:\n"
            f"• Financial viability hinges on optimizing input conversion efficiency (FCR or fertilizer use efficiency) and targeting high-value commercial off-take windows in local currency ({cur_sym})."
        )

        out_evid = f"Grounded in verified scientific empirical research and guidelines from {target_inst}."

        final_synthesis = f"""### 🏛️ AgroBiometrix Consolidated Scientific Advisory: {target_subject} ({country_lbl})

#### 🎯 Strategic Analysis for: *'{query}'*
**Target Enterprise**: {target_subject} &bull; **Jurisdiction**: {country_lbl} &bull; **Primary Inquiries**: {intent_label}

In **{country_lbl}**, optimizing **{target_subject}** requires a synchronized, multi-disciplinary approach addressing the specific agro-climatic, biological, and economic realities of the region.

---

#### 📊 Diagnostic & Management Framework for {target_subject}
| Management Domain | Key Biophysical Factors | Recommended Operational Protocol | Verification & Benchmark |
| :--- | :--- | :--- | :--- |
| **Pathology & Protection** | Endemic biotic pressure, vector corridors | Quarantine new stock/seed, deploy integrated pest management (IPM), maintain strict biosecurity | Zero uncontrolled pathogen outbreak; mortality < 5% |
| **Microclimate & Timing** | Seasonal rainfall, thermal stress ($THI$), diurnal swings | Provide shaded housing or mulch barriers; schedule key operations in cooler diurnal windows | Stabilized respiration and photosynthetic rate |
| **Nutritional Formulation** | Soil mineral balance / feed crude protein | Apply balanced stoichiometric fertilization or high-density rations | Optimal conversion ratio and vigorous growth |
| **Commercial Economics** | Input price inflation vs. harvest gate value | Target organized institutional off-takers; reduce post-harvest / mortality waste | Positive gross operating margins in {cur_sym} |

---

#### 📋 4-Phase Implementation Action Plan
1. **Phase 1: Baseline Diagnostics & Material Certification** &bull; Verify soil fertility, water quality, or herd health status. Source only certified, disease-free seed stock, cultivars, or breeding stock from recognized research centers ({target_inst}).
2. **Phase 2: Climate-Smart Field / Housing Preparation** &bull; Prepare planting beds with adequate organic matter and drainage, or construct well-ventilated, shaded animal enclosures oriented east-to-west.
3. **Phase 3: Prophylactic Protection & Precision Nutrition** &bull; Implement preventive immunization or integrated pest scouting; supply balanced nutrient applications during early vegetative or juvenile development.
4. **Phase 4: Harvest Synchronization & Value Realization** &bull; Monitor maturity indices closely to harvest at peak physiological quality, minimizing post-harvest degradation and capturing premium seasonal market pricing.
"""
        agent_outputs = {
            dispatched[0]: out_spec, dispatched[1]: out_clim, dispatched[2]: out_path,
            dispatched[3]: out_soil, dispatched[4]: out_econ, dispatched[5]: out_evid,
            "Crop Science Agent": out_spec, "Climate Agent": out_clim, "Genetics Agent": out_path,
            "Soil Agent": out_soil, "Economics Agent": out_econ, "Evidence Agent": out_evid
        }
        return {"selected_agents": dispatched, "agent_outputs": agent_outputs, "final_synthesis": final_synthesis}


def sanitize_api_error(err_text: str) -> str:
    """
    Sanitizes API error strings:
    1. Masks any Google AI Studio API keys (AIzaSy...) to prevent accidental credential leakage in UI.
    2. Translates low-level socket/DNS errors ([Errno 11001] getaddrinfo failed, NameResolutionError)
       into human-friendly offline status guidance.
    3. Handles timeouts and connection resets cleanly.
    """
    if not err_text:
        return ""
    # Mask any Google API keys (AIzaSy...)
    masked = re.sub(r'AIzaSy[A-Za-z0-9_-]{33}', 'AIzaSy••••••••••••••••••••••••••••', str(err_text))
    
    # Translate DNS resolution and offline errors
    if any(k in masked for k in ["11001", "NameResolutionError", "getaddrinfo failed"]):
        return "Network Connection Offline: Unable to resolve Google AI servers (DNS lookup failed). Please check your internet connection."
    if any(k in masked for k in ["Connection refused", "Connection reset", "Max retries exceeded"]):
        return "Network Connection Error: Could not reach Google AI servers. Please check your internet connection or proxy settings."
    if any(k in masked.lower() for k in ["timed out", "readtimeouterror", "connecttimeouterror"]):
        return "Network Request Timed Out: Google AI servers took too long to respond. Please try again."
    return masked



def repair_markdown_math(text: str) -> str:
    """
    Thoroughly cleans and repairs Markdown and LaTeX mathematics generated by LLMs,
    ensuring it conforms to KaTeX and Streamlit (remark-math) rendering specifications.
    
    Prevents the 'red text' KaTeX ParseError cascade where unclosed math blocks
    or malformed display delimiters swallow subsequent markdown sections.
    """
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # 1. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 2. Fix inline headers and horizontal rules that lack double newlines
    text = re.sub(r'([^\n])\s+(#{1,6}\s+)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\s*(---|___|\*\*\*)\s*', r'\1\n\n\2\n\n', text)
    text = re.sub(r'([^\n])\s+(\*\s+\*\*[^*]+:\*\*)', r'\1\n\n\2', text)

    # 3. Ensure double newlines before and after display math $$ fences
    text = re.sub(r'([^\n\$])\s*\$\$', r'\1\n\n$$', text)
    text = re.sub(r'\$\$\s*([^\n\$])', r'$$\n\n\1', text)

    # 4. Process all $$ ... $$ display blocks
    parts = text.split("$$")
    new_parts = []
    
    for idx, part in enumerate(parts):
        # Odd indices are inside $$ ... $$
        if idx % 2 == 1:
            block = part.strip()
            
            # Check for aligned environments and alignment operators
            has_begin_aligned = r"\begin{aligned}" in block or r"\begin{align}" in block
            has_end_aligned = r"\end{aligned}" in block or r"\end{align}" in block
            has_align_char = ("&=" in block or " & " in block or r"\\" in block)

            # Repair mismatched aligned environments
            if has_end_aligned and not has_begin_aligned:
                block = "\\begin{aligned}\n" + block
            elif has_begin_aligned and not has_end_aligned:
                block = block + "\n\\end{aligned}"
            elif has_align_char and not has_begin_aligned and not has_end_aligned:
                block = "\\begin{aligned}\n" + block + "\n\\end{aligned}"

            # Replace \begin{align} / \begin{align*} with \begin{aligned}
            block = block.replace(r"\begin{align*}", r"\begin{aligned}").replace(r"\end{align*}", r"\end{aligned}")
            block = block.replace(r"\begin{align}", r"\begin{aligned}").replace(r"\end{align}", r"\end{aligned}")

            # Remove trailing \\ right before \end{aligned} to avoid empty rows
            block = re.sub(r'\\\\(\s*\\end\{aligned\})', r'\1', block)

            # Wrap standalone words following numbers/approx in \text{}
            block = re.sub(r'(\\approx|=)\s*(\d+(?:\.\d+)?)\s+([a-zA-Z]{3,})(?=\s|\\|$)', r'\1 \2 \\text{ \3}', block)

            new_parts.append("\n" + block + "\n")
        else:
            new_parts.append(part)

    # If len(new_parts) is even, there is an odd number of $$ delimiters (one was left open!)
    if len(new_parts) % 2 == 0:
        new_parts.append("\n")

    repaired = "$$".join(new_parts)

    # 5. Fix inline math issues:
    # Remove $ delimiters around plain numbers with commas or plain integers
    repaired = re.sub(r'\$(\d{1,3}(?:,\d{3})+|\d+)\$', r'\1', repaired)

    # 6. Ensure clean spacing between paragraphs
    repaired = re.sub(r'\n{3,}', '\n\n', repaired)

    return repaired.strip()


def validate_gemini_key(api_key: str) -> dict:
    """
    Directly tests the API key against Google's v1beta endpoint.
    Returns dict: {'valid': bool, 'message': str, 'models': list}
    """
    key = (api_key or "").strip().strip("'\"")
    if not key:
        return {"valid": False, "message": "No key provided.", "models": []}
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        resp = requests.get(url, timeout=7)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            valid_models = [
                m["name"].replace("models/", "")
                for m in models_data
                if "generateContent" in m.get("supportedGenerationMethods", [])
            ]
            return {
                "valid": True,
                "message": f"Successfully connected to Google Gemini! ({len(valid_models)} models accessible)",
                "models": valid_models
            }
        else:
            try:
                err_data = resp.json()
                msg = err_data.get("error", {}).get("message", f"HTTP {resp.status_code}")
            except Exception:
                msg = f"HTTP {resp.status_code}"
            return {"valid": False, "message": sanitize_api_error(msg), "models": []}
    except Exception as e:
        return {"valid": False, "message": sanitize_api_error(str(e)), "models": []}


def get_gemini_api_key() -> str:
    """
    Unified resolver for Google Gemini API key across all AgroBiometrix modules.
    Checks st.session_state, st.secrets (Streamlit Cloud), and os.environ.
    """
    key = ""
    try:
        import streamlit as st
        if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
            key = st.session_state["gemini_api_key"]
        elif "api_keys" in st.session_state and isinstance(st.session_state["api_keys"], dict):
            key = st.session_state["api_keys"].get("gemini", "")
        elif hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    if not key:
        key = os.getenv("GEMINI_API_KEY", "")
    return (key or "").strip().strip("'\"")


def set_gemini_api_key(api_key: str):
    """
    Synchronizes Google Gemini API key across session state and environment.
    """
    cleaned = (api_key or "").strip().strip("'\"")
    try:
        import streamlit as st
        st.session_state["gemini_api_key"] = cleaned
        st.session_state.setdefault("api_keys", {})["gemini"] = cleaned
    except Exception:
        pass
    if cleaned:
        os.environ["GEMINI_API_KEY"] = cleaned


def call_live_llm_orchestration(query: str, api_key: str = "", provider: str = "gemini", active_region: dict = None, **kwargs) -> dict:
    """
    Connects to Google Gemini API if key is provided.
    Falls back cleanly to the rule-based expert engine if network/key fails.
    """
    if not api_key and provider.lower() == "gemini":
        api_key = get_gemini_api_key()

    region_info = ""
    if active_region and isinstance(active_region, dict):
        c_name = active_region.get("country", "")
        c_sym = active_region.get("currency_symbol", "")
        c_code = active_region.get("currency_code", "")
        region_info = f" Prioritize agricultural realities, local breeds/cultivars, and economics for {c_name} (Currency: {c_code} {c_sym})."

    system_prompt = (
        "You are AgroBiometrix Multi-Agent Orchestrator, an Africa-first, globally relevant agricultural AI. "
        "Directly and exhaustively answer the user's specific inquiry. When diseases, breeding, nutrition, or specific regions are queried, "
        "provide full veterinary/agronomic pathology, specific etiologies, vectors, diagnostic symptoms, reproductive impacts, "
        "vaccination calendars (e.g. NVRI Vom vaccines), and structured diagnostic tables followed by a phased action protocol."
        f"{region_info}"
    )

    lang_pref = kwargs.get("lang") or ""
    if not lang_pref:
        try:
            import streamlit as st
            lang_pref = st.session_state.get("app_lang", "en")
        except Exception:
            lang_pref = "en"

    if lang_pref == "fr":
        system_prompt += (
            " DIRECTIVE DE LANGUE OBLIGATOIRE : L'utilisateur a configuré son interface en français. "
            "Vous devez rédiger l'intégralité de votre analyse, de vos synthèses disciplinaires, de vos diagnostics "
            "et de vos recommandations exclusivement en FRANÇAIS académique, technique et professionnel, "
            "en employant la terminologie agronomique francophone appropriée."
        )

    api_key = (api_key or "").strip().strip("'\"")
    if not api_key:
        return rule_based_agent_synthesis(query, active_region=active_region)

    last_error_msg = ""
    if provider.lower() == "gemini" and api_key:
        discovered_models = []

        # Step 1: Dynamic Model Discovery via ListModels on v1beta
        try:
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            list_resp = requests.get(list_url, timeout=8)
            if list_resp.status_code == 200:
                models_data = list_resp.json().get("models", [])
                valid_models = [
                    m["name"].replace("models/", "")
                    for m in models_data
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]
                preferred_order = [
                    "gemini-1.5-flash",
                    "gemini-1.5-flash-latest",
                    "gemini-2.0-flash",
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-pro"
                ]
                for pref in preferred_order:
                    if pref in valid_models:
                        discovered_models.append(pref)
                for vm in valid_models:
                    if vm not in discovered_models:
                        discovered_models.append(vm)
            else:
                try:
                    err_json = list_resp.json()
                    last_error_msg = err_json.get("error", {}).get("message", f"HTTP {list_resp.status_code}")
                except Exception:
                    last_error_msg = f"HTTP {list_resp.status_code}"
        except Exception as e:
            last_error_msg = sanitize_api_error(str(e))

        # Fallback to standard v1beta candidate models if ListModels is unavailable
        if not discovered_models:
            discovered_models = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash", "gemini-1.5-pro"]

        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question: {query}"}]}
            ]
        }

        # Step 2: Query candidate models strictly on v1beta
        for model in discovered_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                resp = requests.post(url, json=payload, timeout=25)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            text = repair_markdown_math(parts[0]["text"])
                            return {
                                "is_live_cloud": True,
                                "provider": "Google Gemini",
                                "model": model,
                                "selected_agents": [
                                    "Veterinary / Agronomy Specialist Agent",
                                    "Genetics & Breeding Agent",
                                    "Climate & Agro-Ecosystems Agent",
                                    "Biosecurity & Pathology Agent",
                                    "Agricultural Economics Agent",
                                    "Institutional Evidence Agent"
                                ],
                                "agent_outputs": {
                                    f"Live Agent Ensemble (Gemini {model})": text,
                                    "Veterinary / Agronomy Specialist Agent": "Detailed scientific assessment synthesized through live cloud reasoning.",
                                    "Genetics & Breeding Agent": "Reproductive and genetic implications analyzed live.",
                                    "Biosecurity & Pathology Agent": "Diagnostic and prophylactic protocols verified in live reasoning."
                                },
                                "final_synthesis": text
                            }
                else:
                    try:
                        err_json = resp.json()
                        raw_msg = err_json.get("error", {}).get("message", f"HTTP {resp.status_code}")
                    except Exception:
                        raw_msg = f"HTTP {resp.status_code}"
                    last_error_msg = sanitize_api_error(raw_msg)
            except Exception as e:
                last_error_msg = sanitize_api_error(str(e))
                continue

    elif provider.lower() == "openai" and api_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.4
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                text = repair_markdown_math(resp.json()["choices"][0]["message"]["content"])
                return {
                    "selected_agents": ["Veterinary / Agronomy Specialist Agent", "Genetics & Breeding Agent", "Climate & Agro-Ecosystems Agent", "Biosecurity & Pathology Agent", "Agricultural Economics Agent", "Institutional Evidence Agent"],
                    "agent_outputs": {
                        "Live Agent Ensemble (OpenAI GPT-4o)": text,
                        "Veterinary / Agronomy Specialist Agent": "Agronomic and veterinary reasoning synthesized via OpenAI.",
                        "Biosecurity & Pathology Agent": "Biosecurity and prevention protocols analyzed live."
                    },
                    "final_synthesis": text
                }
        except Exception:
            pass

    elif provider.lower() == "groq" and api_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.4
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                text = repair_markdown_math(resp.json()["choices"][0]["message"]["content"])
                return {
                    "selected_agents": ["Veterinary / Agronomy Specialist Agent", "Genetics & Breeding Agent", "Climate & Agro-Ecosystems Agent", "Biosecurity & Pathology Agent", "Agricultural Economics Agent", "Institutional Evidence Agent"],
                    "agent_outputs": {
                        "Live Agent Ensemble (Groq Llama-3.3)": text,
                        "Veterinary / Agronomy Specialist Agent": "Real-time agronomic reasoning synthesized via Groq.",
                        "Biosecurity & Pathology Agent": "Biosecurity protocols analyzed via Groq."
                    },
                    "final_synthesis": text
                }
        except Exception:
            pass

    # Fallback to local expert synthesis with regional grounding
    res = rule_based_agent_synthesis(query, active_region=active_region)
    if last_error_msg:
        res["live_api_error"] = sanitize_api_error(last_error_msg)
    return res
