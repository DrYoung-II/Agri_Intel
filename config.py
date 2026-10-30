"""
AgroBiometrix - Configuration and API Directory
Leaf Green Theme & Comprehensive Domain Directory
"""

import os

APP_NAME = "AgroBiometrix"
APP_SUBTITLE = "The Quantitative Biometrics & Generative Intelligence Platform for Agriculture"
APP_TAGLINE = "Africa-First, Globally Relevant: The Intelligence Infrastructure Behind Resilient Agriculture"
APP_MOTTO = "AGRICULTURE • RESEARCH • DATA • INSIGHT"
LOGO_PATH = os.path.join("assets", "agrobiometrix_logo.png")
ICON_PATH = os.path.join("assets", "agrobiometrix_icon.png")
COMPANY_NAME = "Naysa-84 Labs"
COMPANY_TAGLINE = "Unlocking the power of data"
NAYSA_LOGO_PATH = os.path.join("assets", "naysa84_labs_logo.png")

FOUNDER_STORY = (
    '"I trained as an animal geneticist, spent years working with agricultural research problems, '
    'transitioned into data science and artificial intelligence, and realised that one of Africa\'s '
    'biggest agricultural problems is not merely lack of knowledge—it is the inability to connect '
    'agricultural knowledge, data, research and decision-making at scale."'
)

FOUNDER_STORY_FR = (
    '« Formé en tant que généticien animalier, j\'ai consacré des années à résoudre des problématiques de recherche '
    'agronomique, avant d\'évoluer vers la science des données et l\'intelligence artificielle. J\'ai alors compris que '
    'l\'un des plus grands défis de l\'agriculture en Afrique n\'est pas simplement un manque de connaissances — c\'est '
    'l\'incapacité à relier les savoirs agronomiques, les données, la recherche et la prise de décision à grande échelle. »'
)

# Theme Palette: Leaf Green & Digital Circuit Fusion (Matching Official Logo)
THEME = {
    "primary": "#2E7D32",       # Forest Leaf Green
    "primary_dark": "#1B5E20",  # Deep Foliage Green
    "primary_light": "#4CAF50", # Vibrant Grass Green
    "accent": "#81C784",        # Sprout Green
    "circuit_teal": "#00BFA5",  # Digital Circuit Node Cyan
    "circuit_glow": "#64FFDA",  # Bioluminescent Node Glow
    "circuit_amber": "#FFD54F", # Circuit Trace Gold
    "accent_light": "#E8F5E9",  # Soft Leaf Mist
    "accent_border": "#C8E6C9", # Pale Leaf Border
    "text_dark": "#1B3B1D",     # Deep Forest Text
    "warning": "#F57F17",       # Sun Amber
    "info": "#0277BD",          # River Blue
    "danger": "#C62828",        # Rust Red
    "background_card": "#FFFFFF",
}

# API Directory & Subscriptions
API_DIRECTORY = [
    {
        "category": "African Voice AI & Tonal Speech",
        "name": "YarnGPT Voice AI",
        "provider": "YarnGPT / African Speech Intelligence",
        "link": "https://yarngpt.ai/",
        "is_paid": True,
        "pricing": "Free starter testing tier; affordable pay-as-you-go per character for production extension broadcasts.",
        "how_to_subscribe": "1. Visit https://yarngpt.ai/ \n2. Create an account and navigate to API Keys.\n3. Generate an API token and connect it to AgroBiometrix for authentic Yorùbá, Ìgbò, Hausa, and Pidgin broadcast synthesis.",
        "usage_in_app": "Native tonal audio generation (High/Mid/Low Dò-Re-Mí tones) for rural radio extension bulletins without English intonation.",
        "accessible_domain": "yarngpt.ai, api.yarngpt.ai",
    },
    {
        "category": "Global Generative Voice AI & Voice Cloning",
        "name": "ElevenLabs Multilingual Speech",
        "provider": "ElevenLabs Inc.",
        "link": "https://elevenlabs.io/",
        "is_paid": True,
        "pricing": "Free tier (10,000 characters/month); Starter plan from $5/month. Pay-per-character for enterprise broadcasting.",
        "how_to_subscribe": "1. Sign up at https://elevenlabs.io/ \n2. Go to Profile -> API Keys -> Create Key.\n3. Supports Multilingual v2 model and custom voice cloning of native African radio broadcasters.",
        "usage_in_app": "Broadcast-grade agricultural advisory voiceover with emotional resonance and voice cloning.",
        "accessible_domain": "elevenlabs.io, api.elevenlabs.io",
    },
    {
        "category": "Open-Source Indigenous Neural Speech",
        "name": "Meta MMS (Massively Multilingual Speech)",
        "provider": "Meta AI / Hugging Face",
        "link": "https://huggingface.co/facebook/mms-tts-yor",
        "is_paid": False,
        "pricing": "100% FREE & Open-Source (VITS neural architecture checkpoints for yor, ibo, hau, swa).",
        "how_to_subscribe": "Open weights on Hugging Face: https://huggingface.co/facebook/mms-tts-yor. Can be deployed locally via transformers or queried via Hugging Face Inference API.",
        "usage_in_app": "Zero-cost local neural synthesis of indigenous African languages with native speaker acoustic training.",
        "accessible_domain": "huggingface.co",
    },
    {
        "category": "GenAI & Multi-Agent Reasoning",
        "name": "Google Gemini API",
        "provider": "Google DeepMind / Google Cloud",
        "link": "https://ai.google.dev/",
        "is_paid": True,
        "pricing": "Generous FREE tier (15 requests/min free on Gemini 1.5/2.0 Flash); Pay-as-you-go thereafter (~$0.075-$0.30/1M tokens).",
        "how_to_subscribe": "1. Visit https://aistudio.google.com/ \n2. Sign in with a Google account.\n3. Click 'Get API key' -> 'Create API key in new project'.\n4. Copy the key into AgroBiometrix settings.",
        "usage_in_app": "Powering multi-agent synthesis, thesis tutoring, research question ideation, and literature matrix summaries.",
        "accessible_domain": "ai.google.dev, aistudio.google.com",
    },
    {
        "category": "Agro-Weather & Environmental Data",
        "name": "Open-Meteo Weather API",
        "provider": "Open-Meteo GmbH",
        "link": "https://open-meteo.com/en/docs",
        "is_paid": False,
        "pricing": "100% FREE for non-commercial, academic, and development use (up to 10,000 daily calls, no API key required). Paid commercial plans start from €29/month.",
        "how_to_subscribe": "No key needed! Direct REST endpoint access: https://api.open-meteo.com/v1/forecast. Commercial tier available at https://open-meteo.com/en/pricing.",
        "usage_in_app": "Historical and real-time precipitation, temperature, relative humidity, solar radiation, and soil moisture across African coordinates.",
        "accessible_domain": "open-meteo.com, api.open-meteo.com",
    },
    {
        "category": "Agro-Climatology & Solar Radiation",
        "name": "NASA POWER API",
        "provider": "NASA Langley Research Center",
        "link": "https://power.larc.nasa.gov/docs/",
        "is_paid": False,
        "pricing": "100% FREE & Public Domain. No authentication key required.",
        "how_to_subscribe": "Open access. Documentation at https://power.larc.nasa.gov/docs/services/api/.",
        "usage_in_app": "Agro-climatological daily solar radiation, evapotranspiration, and precipitation records worldwide for crop growth simulation.",
        "accessible_domain": "power.larc.nasa.gov",
    },
    {
        "category": "Commercial Weather Services",
        "name": "OpenWeatherMap API",
        "provider": "OpenWeather Ltd",
        "link": "https://openweathermap.org/api",
        "is_paid": True,
        "pricing": "Free tier includes 1,000 API calls/day (One Call 3.0). Paid usage is $0.0015 per call beyond free limit.",
        "how_to_subscribe": "1. Sign up at https://home.openweathermap.org/users/sign_up \n2. Go to 'My API Keys' and generate a key.\n3. Activate the One Call 3.0 subscription (first 1,000 calls/day free).",
        "usage_in_app": "High-resolution localized current weather alerts and forecast indices.",
        "accessible_domain": "openweathermap.org, api.openweathermap.org",
    },
    {
        "category": "Soil Intelligence & Spatial Mapping",
        "name": "ISRIC SoilGrids REST API",
        "provider": "ISRIC - World Soil Information",
        "link": "https://www.isric.org/explore/soilgrids/faq-soilgrids",
        "is_paid": False,
        "pricing": "100% FREE Open Data (Creative Commons 4.0).",
        "how_to_subscribe": "Public open API endpoint: https://rest.isric.org/soilgrids/v2.0/properties/query.",
        "usage_in_app": "Automated retrieval of soil pH, Nitrogen, Organic Carbon, Sand/Clay texture, and CEC for any latitude/longitude in Africa.",
        "accessible_domain": "isric.org, rest.isric.org",
    },
    {
        "category": "Scientific Research & Literature",
        "name": "Crossref REST API",
        "provider": "Crossref",
        "link": "https://www.crossref.org/documentation/retrieve-metadata/rest-api/",
        "is_paid": False,
        "pricing": "100% FREE open bibliographic API (request polite pool by providing email header).",
        "how_to_subscribe": "Free open access: https://api.crossref.org/works?query=...",
        "usage_in_app": "Verification of peer-reviewed agricultural papers, DOI retrieval, metadata validation.",
        "accessible_domain": "crossref.org, api.crossref.org",
    },
    {
        "category": "Biomedical & Genetic Literature",
        "name": "NCBI PubMed E-Utilities API",
        "provider": "National Center for Biotechnology Information (NCBI / NIH)",
        "link": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        "is_paid": False,
        "pricing": "100% FREE. Up to 3 requests/sec without key; up to 10 requests/sec with free NCBI API key.",
        "how_to_subscribe": "1. Create free NCBI account at https://www.ncbi.nlm.nih.gov/account/ \n2. Go to Account Settings -> 'API Key Management' -> 'Create an API Key'.",
        "usage_in_app": "Genetic trait and QTL literature extraction for cattle, sheep, goats, poultry, and crops.",
        "accessible_domain": "ncbi.nlm.nih.gov, eutils.ncbi.nlm.nih.gov",
    },
    {
        "category": "Global Agricultural Statistics",
        "name": "FAOSTAT API & Data Service",
        "provider": "Food and Agriculture Organization of the United Nations (FAO)",
        "link": "https://www.fao.org/faostat/en/#data",
        "is_paid": False,
        "pricing": "100% FREE open UN statistical repository.",
        "how_to_subscribe": "Direct access via FAOSTAT bulk download API or endpoints at https://fenixservices.fao.org/faostat/api/v1/.",
        "usage_in_app": "National crop yields, trade flows, fertilizer consumption, and livestock populations.",
        "accessible_domain": "fao.org, fenixservices.fao.org",
    },
]

# Pan-African Regional Context & Multi-Currency System
PAN_AFRICAN_REGIONS = {
    "🇳🇬 Nigeria (NGN ₦)": {
        "country": "Nigeria",
        "currency_symbol": "₦",
        "currency_code": "NGN",
        "fx_to_usd": 1500.0,
        "flag": "🇳🇬",
        "budget_unit": "₦1.0 Billion",
        "commercial_bag_price": 38_000,
        "base_maize_price": 450_000,
        "base_fert_cost": 240_000,
        "base_other_cost": 180_000,
        "total_smallholders": 18_000_000,
        "agro_zones": ["Sudan Savanna", "Guinea Savanna", "Rainforest", "Derived Savanna"],
    },
    "🇨🇮 Côte d'Ivoire (XOF FCFA)": {
        "country": "Côte d'Ivoire",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "fx_to_usd": 610.0,
        "flag": "🇨🇮",
        "budget_unit": "500 Millions FCFA",
        "commercial_bag_price": 16_000,
        "base_maize_price": 190_000,
        "base_fert_cost": 110_000,
        "base_other_cost": 80_000,
        "total_smallholders": 3_500_000,
        "agro_zones": ["Zone Forestière Humide", "Zone Pré-Forestière", "Savane Soudanaise (Nord)", "Zone Montagneuse (Ouest)"],
    },
    "🇸🇳 Sénégal (XOF FCFA)": {
        "country": "Sénégal",
        "currency_symbol": "FCFA ",
        "currency_code": "XOF",
        "fx_to_usd": 610.0,
        "flag": "🇸🇳",
        "budget_unit": "400 Millions FCFA",
        "commercial_bag_price": 15_500,
        "base_maize_price": 185_000,
        "base_fert_cost": 105_000,
        "base_other_cost": 75_000,
        "total_smallholders": 1_900_000,
        "agro_zones": ["Bassin Arachidier", "Vallée du Fleuve Sénégal", "Zone Sylvopastorale", "Casamance"],
    },
    "🇨🇲 Cameroun (XAF FCFA)": {
        "country": "Cameroun",
        "currency_symbol": "FCFA ",
        "currency_code": "XAF",
        "fx_to_usd": 610.0,
        "flag": "🇨🇲",
        "budget_unit": "500 Millions FCFA",
        "commercial_bag_price": 16_500,
        "base_maize_price": 195_000,
        "base_fert_cost": 115_000,
        "base_other_cost": 85_000,
        "total_smallholders": 2_600_000,
        "agro_zones": ["Hauts Plateaux de l'Ouest", "Forêt Équatoriale Humide", "Zone Soudano-Sahélienne", "Zone Côtière"],
    },
    "🇰🇪 Kenya (KES KSh)": {
        "country": "Kenya",
        "currency_symbol": "KSh ",
        "currency_code": "KES",
        "fx_to_usd": 130.0,
        "flag": "🇰🇪",
        "budget_unit": "KSh 100 Million",
        "commercial_bag_price": 3_500,
        "base_maize_price": 42_000,
        "base_fert_cost": 22_000,
        "base_other_cost": 16_000,
        "total_smallholders": 4_500_000,
        "agro_zones": ["Rift Valley", "Western Highlands", "Central Highlands", "Semi-Arid East"],
    },
    "🇬🇭 Ghana (GHS GH₵)": {
        "country": "Ghana",
        "currency_symbol": "GH₵ ",
        "currency_code": "GHS",
        "fx_to_usd": 15.5,
        "flag": "🇬🇭",
        "budget_unit": "GH₵ 10 Million",
        "commercial_bag_price": 420,
        "base_maize_price": 5_200,
        "base_fert_cost": 2_700,
        "base_other_cost": 1_900,
        "total_smallholders": 2_800_000,
        "agro_zones": ["Northern Savanna", "Transitional Zone", "Forest Zone", "Coastal Savanna"],
    },
    "🇪🇹 Ethiopia (ETB Br)": {
        "country": "Ethiopia",
        "currency_symbol": "Br ",
        "currency_code": "ETB",
        "fx_to_usd": 120.0,
        "flag": "🇪🇹",
        "budget_unit": "Br 100 Million",
        "commercial_bag_price": 3_200,
        "base_maize_price": 38_000,
        "base_fert_cost": 20_000,
        "base_other_cost": 15_000,
        "total_smallholders": 14_000_000,
        "agro_zones": ["Highlands (Dega)", "Midlands (Weyna Dega)", "Lowlands (Kolla)", "Rift Valley"],
    },
    "🇿🇦 South Africa (ZAR R)": {
        "country": "South Africa",
        "currency_symbol": "R ",
        "currency_code": "ZAR",
        "fx_to_usd": 18.0,
        "flag": "🇿🇦",
        "budget_unit": "R 15 Million",
        "commercial_bag_price": 480,
        "base_maize_price": 5_600,
        "base_fert_cost": 3_000,
        "base_other_cost": 2_200,
        "total_smallholders": 2_100_000,
        "agro_zones": ["Highveld Maize Quad", "Free State", "KwaZulu-Natal Coast", "Eastern Cape"],
    },
    "🌐 Pan-Africa & Global (USD $)": {
        "country": "Global / Pan-Africa",
        "currency_symbol": "$",
        "currency_code": "USD",
        "fx_to_usd": 1.0,
        "flag": "🌐",
        "budget_unit": "$1.0 Million",
        "commercial_bag_price": 26,
        "base_maize_price": 300,
        "base_fert_cost": 160,
        "base_other_cost": 120,
        "total_smallholders": 50_000_000,
        "agro_zones": ["Sub-Saharan Africa Cereal Belt", "Humid Tropics", "Semi-Arid Tropics", "East African Plateau"],
    },
}

