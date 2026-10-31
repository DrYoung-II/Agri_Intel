"""
AgroBiometrix - Internationalization (i18n) Engine
Bilingual Infrastructure: English (🇬🇧) & Français (🇫🇷)
Engineered for Pan-African National Agricultural Research Systems (NARS),
CGIAR centers, agricultural faculties, and agribusiness across West, Central, East, and Southern Africa.
"""

import streamlit as st

TRANSLATIONS = {
    "en": {
        # App Identity
        "app_name": "AgroBiometrix",
        "app_motto": "AGRICULTURE • RESEARCH • DATA • INSIGHT",
        "app_subtitle": "The Quantitative Biometrics & Generative Intelligence Platform for Agriculture",
        "app_tagline": "Africa-First, Globally Relevant: The Intelligence Infrastructure Behind Resilient Agriculture",
        "hero_title": "AgroBiometrix",
        "hero_sub": "Quantitative Biometrics & Generative Multi-Agent Intelligence for Agriculture",
        "hero_framework": "Institutional Evidence Engine &bull; NARS, CGIAR & Academic Peer-Review Standards",
        "hero_badge": "Institutional Agricultural Intelligence",
        "hero_cert_badge": "AFRICA-FIRST BIOMETRICS",
        "hero_cert_sub": "100% Offline &bull; Live Multi-Agent AI",

        # Sidebar & Controls
        "lang_selector_label": "🌐 Language / Langue :",
        "region_selector_label": "🌍 Regional Context & Currency :",
        "region_selector_help": "Adapts local currency, input pricing, agro-ecological zones, and NARS research protocols.",
        "suite_selector_label": "Intelligence Suites :",
        "connect_gemini_label": "🔑 Connect Google Gemini (Optional Free Key)",
        "gemini_key_prompt": "Google Gemini Key:",
        "gemini_active": "🟢 Live Google Gemini Engine Active",
        "gemini_secured": "Cloud Verified &bull; Secrets Secured",
        "founder_story_label": "📖 Founder Story & Vision",
        "founder_story_text": (
            "\"I trained as an animal geneticist, spent years working with agricultural research problems, "
            "transitioned into data science and artificial intelligence, and realised that one of Africa's "
            "biggest agricultural problems is not merely lack of knowledge—it is the inability to connect "
            "agricultural knowledge, data, research and decision-making at scale.\""
        ),
        "edition_label": "AgroBiometrix v2.4 &bull; Africa-First Institutional Edition",
        "powered_by": "POWERED BY",
        "unlocking_data": "Unlocking the power of data",

        # Suites Titles (Clean, balanced, single-line fit without emojis)
        "suite_orchestrator": "Multi-Agent Orchestrator",
        "suite_biometrics": "Biometrics & Plant Breeding",
        "suite_scientist": "AI Research Scientist Studio",
        "suite_agro": "Agro-Ecosystems, Soil & Climate",
        "suite_livestock": "Livestock & Veterinary Care",
        "suite_policy": "Policy & Economic Simulator",
        "suite_api": "Knowledge Graph & Developer API",
        "suite_radio": "Last-Mile Vernacular Radio & Voice",

        # Orchestrator
        "orch_header": "Multi-Agent Orchestration Layer",
        "orch_quote": (
            "A normal agricultural AI says: <i>'Upload a picture of your tomato leaf, and I will tell you what disease it has.'</i><br>"
            "<b>AgroBiometrix says</b>: <i>'Give me a crop, animal, location, genotype, soil condition, climate scenario, production objective, "
            "research question or policy problem—and I will assemble the relevant evidence, analyze the available data, run appropriate models, "
            "explain the results, and recommend what should be done.'</i>"
        ),
        "orch_ask_label": "Ask AgroBiometrix Anything (Cross-Agent Query)",
        "orch_ask_sub": "Cross-disciplinary reasoning across agronomy, genetics, soil science, veterinary pathology, climate and economics.",
        "orch_preset_label": "💡 Quick-Select Strategic Inquiry (or choose Custom to write your own):",
        "orch_custom_choice": "-- Type Your Own Custom Query Below --",
        "orch_query_label": "Enter Agricultural Inquiry:",
        "orch_query_placeholder": "Type any crop, livestock, poultry, fish, soil, or climate question here (e.g. The best breed of rabbit for the Nigerian climate)...",
        "orch_engine_mode": "Intelligence Engine Mode",
        "orch_engine_select": "Select Engine:",
        "orch_engine_gemini": "🟢 Live Google Gemini API (Cloud Multi-Agent Reasoning)",
        "orch_engine_offline": "⚡ Built-in African Agronomic Science Engine (Offline • Local Biometrics)",
        "orch_engine_help": "Select whether AgroBiometrix runs with live Google Gemini cloud reasoning or local offline African scientific models.",
        "orch_gemini_active_msg": "🟢 **Google Gemini Live Intelligence Active**: Cloud multi-agent reasoning is connected and secured via server secrets. Zero client-side key entry required.",
        "orch_offline_active_msg": "🌿 **Built-in African Agronomic Science Engine Active**: Operates 100% offline with zero external API calls. Powered by calibrated agronomic, edaphic, and genomic models for Western Nigeria (NIHORT, IITA), Northern Savanna, and East Africa.",
        "orch_btn_run": "🚀 Invoke Agent Ensemble",
        "orch_status_label": "Current Engine Status:",
        "orch_status_live": "🟢 Live Cloud LLM (Gemini)",
        "orch_status_offline": "⚡ Offline Deterministic Expert Mode (100% Free)",
        "orch_query_warning": "⚠️ Please enter a question or select one of the strategic presets above.",
        "orch_spinner": "Decomposing question and dispatching specialized agents...",
        "orch_complete": "✅ Multi-Agent Consultation Complete!",
        "orch_roster_title": "Multi-Agent Dispatch Roster",
        "orch_roster_sub": "Specialized Disciplines",
        "orch_advisory_tab": "📑 Consolidated Scientific Advisory & Action Plan",
        "orch_agents_tab": "👥 Individual Specialist Agent Deliberations",
        "orch_consultations_title": "👥 Disciplinary Consultations from Dispatched Agents",
        "orch_consultations_sub": "Inspect the granular domain-specific reasoning contributed by each specialized agent:",

        # Footer
        "footer_badge": "ENTERPRISE AGRO-INTELLIGENCE INFRASTRUCTURE",
        "footer_title": "AgroBiometrix Platform",
        "footer_subtitle": "Quantitative Biometrics, Genomic Breeding & Generative Multi-Agent Intelligence for Agriculture",
        "footer_legal": "Designed for Pan-African NARS, CGIAR Centers, Agricultural Universities & Enterprise Agribusinesses.",
        "footer_rights": "© 2026 AgroBiometrix &bull; Powered by Naysa-84 Labs. All rights reserved.",
        "footer_meta": "Pan-African AgTech &bull; Offline & Cloud Intelligence &bull; Production v2.4",
    },
    "fr": {
        # App Identity
        "app_name": "AgroBiometrix",
        "app_motto": "AGRICULTURE • RECHERCHE • DONNÉES • PERSPECTIVE",
        "app_subtitle": "Plateforme de Biométrie Quantitative & d'Intelligence Générative pour l'Agriculture",
        "app_tagline": "Priorité à l'Afrique, Portée Mondiale : L'Infrastructure d'Intelligence au Service d'une Agriculture Résiliente",
        "hero_title": "AgroBiometrix",
        "hero_sub": "Biométrie Quantitative & Intelligence Artificielle Générative pour l'Agriculture",
        "hero_framework": "Moteur de Preuves Institutionnelles &bull; Normes Scientifiques SNRA, CGIAR & Universités",
        "hero_badge": "Intelligence Agronomique Institutionnelle",
        "hero_cert_badge": "BIOMÉTRIE PANAFRICAINE",
        "hero_cert_sub": "100% Hors-ligne &bull; IA Multi-Agents",

        # Sidebar & Controls
        "lang_selector_label": "🌐 Langue / Language :",
        "region_selector_label": "🌍 Contexte Régional & Devise :",
        "region_selector_help": "Adapte la monnaie locale, le barème des intrants, les zones agro-écologiques et les protocoles SNRA.",
        "suite_selector_label": "Suites d'Intelligence :",
        "connect_gemini_label": "🔑 Connecter Google Gemini (Clé Gratuite Optionnelle)",
        "gemini_key_prompt": "Clé API Google Gemini :",
        "gemini_active": "🟢 Moteur Google Gemini Actif & Sécurisé",
        "gemini_secured": "Vérifié sur le Cloud &bull; Secrets Protégés",
        "founder_story_label": "📖 Histoire & Vision du Fondateur",
        "founder_story_text": (
            "« Formé en tant que généticien animalier, j'ai consacré des années à résoudre des problématiques de recherche "
            "agronomique, avant d'évoluer vers la science des données et l'intelligence artificielle. J'ai alors compris que "
            "l'un des plus grands défis de l'agriculture en Afrique n'est pas simplement un manque de connaissances — c'est "
            "l'incapacité à relier les savoirs agronomiques, les données, la recherche et la prise de décision à grande échelle. »"
        ),
        "edition_label": "AgroBiometrix v2.4 &bull; Édition Institutionnelle Panafricaine",
        "powered_by": "PROPULSÉ PAR",
        "unlocking_data": "Libérer la puissance des données",

        # Suites Titles (Clean, balanced, single-line fit without emojis)
        "suite_orchestrator": "Orchestrateur Multi-Agents",
        "suite_biometrics": "Biométrie & Sélection Végétale",
        "suite_scientist": "Chercheur IA & Studio de Thèse",
        "suite_agro": "Agro-Écosystèmes, Sols & Climat",
        "suite_livestock": "Élevage & Santé Vétérinaire",
        "suite_policy": "Politiques & Économie Agricole",
        "suite_api": "Graphe de Connaissances & API",
        "suite_radio": "Radio Vernaculaire & Voix du Dernier Kilomètre",

        # Orchestrator
        "orch_header": "Couche d'Orchestration Multi-Agents",
        "orch_quote": (
            "Une IA agricole ordinaire dit : <i>'Téléversez une photo de votre feuille de tomate, et je vous dirai quelle maladie elle a.'</i><br>"
            "<b>AgroBiometrix déclare</b> : <i>'Indiquez-moi une culture, un animal, une localité, un génotype, l'état du sol, un scénario climatique, "
            "un objectif de production, une problématique de recherche ou de politique agricole—et je rassemblerai les preuves pertinentes, analyserai "
            "les données disponibles, exécuterai les modèles appropriés, expliquerai les résultats et recommanderai les actions optimales.'</i>"
        ),
        "orch_ask_label": "Poser une Question à AgroBiometrix (Requête Transversale)",
        "orch_ask_sub": "Raisonnement interdisciplinaire unifié combinant agronomie, génétique, pédologie, pathologie vétérinaire, climatologie et économie.",
        "orch_preset_label": "💡 Sélection Rapide de Requête Stratégique (ou Personnalisée) :",
        "orch_custom_choice": "-- Saisir votre propre question personnalisée ci-dessous --",
        "orch_query_label": "Saisir la Requête Agricole :",
        "orch_query_placeholder": "Posez votre question sur les cultures, l'élevage, la volaille, la pisciculture, le sol ou le climat ici (ex. Meilleure race de lapin pour le climat ouest-africain)...",
        "orch_engine_mode": "Mode du Moteur d'Intelligence",
        "orch_engine_select": "Sélectionner le Moteur :",
        "orch_engine_gemini": "🟢 API Google Gemini en Direct (Raisonnement Cloud Multi-Agents)",
        "orch_engine_offline": "⚡ Moteur Agronomique Africain Intégré (Hors-ligne • Biométrie Locale)",
        "orch_engine_help": "Choisissez si AgroBiometrix s'exécute avec le raisonnement cloud Google Gemini en direct ou les modèles scientifiques africains hors-ligne.",
        "orch_gemini_active_msg": "🟢 **Intelligence Active Google Gemini en Direct** : Le raisonnement multi-agents sur le cloud est connecté et sécurisé via les secrets du serveur. Aucune saisie de clé requise.",
        "orch_offline_active_msg": "🌿 **Moteur Scientifique Agronomique Africain Intégré Actif** : Fonctionne à 100% hors-ligne sans aucun appel API externe. Alimenté par des modèles agronomiques, édaphiques et génomiques calibrés pour l'Afrique de l'Ouest, Centrale et de l'Est.",
        "orch_btn_run": "🚀 Lancer la Synthèse Multi-Agents",
        "orch_status_label": "Statut actuel du moteur :",
        "orch_status_live": "🟢 LLM Cloud en Direct (Gemini)",
        "orch_status_offline": "⚡ Mode Expert Déterministe Hors-ligne (100% Gratuit)",
        "orch_query_warning": "⚠️ Veuillez saisir une question ou sélectionner l'une des requêtes stratégiques ci-dessus.",
        "orch_spinner": "Décomposition de la question et mobilisation des agents spécialisés...",
        "orch_complete": "✅ Consultation Multi-Agents Terminée !",
        "orch_roster_title": "Comité Multi-Agents Mobilisé",
        "orch_roster_sub": "Disciplines Spécialisées",
        "orch_advisory_tab": "📑 Avis Scientifique Consolidé & Plan d'Action",
        "orch_agents_tab": "👥 Délibérations Individuelles des Agents Spécialistes",
        "orch_consultations_title": "👥 Consultations Disciplinaires des Agents Spécialistes",
        "orch_consultations_sub": "Examinez le raisonnement spécialisé apporté par chaque discipline mobilisée :",

        # Footer
        "footer_badge": "INFRASTRUCTURE D'INTELLIGENCE AGRONOMIQUE D'ENTREPRISE",
        "footer_title": "Plateforme AgroBiometrix",
        "footer_subtitle": "Biométrie Quantitative, Amélioration Génomique & Intelligence Artificielle pour l'Agriculture",
        "footer_legal": "Conçu pour les SNRA d'Afrique subsaharienne, les centres CGIAR, Universités & Entreprises Agrobusiness.",
        "footer_rights": "© 2026 AgroBiometrix &bull; Développé & Propulsé par Naysa-84 Labs. Tous droits réservés.",
        "footer_meta": "AgTech Panafricaine &bull; Intelligence Autonome & Cloud &bull; Version 2.4",
    }
}

# Translated Agent Names Dictionary
AGENT_NAMES_FR = {
    # Core Specialist Roles
    "Soil & Edaphology Specialist": "Spécialiste Sols & Édaphologie",
    "Plant Breeder & Geneticist": "Généticien & Sélectionneur Végétal",
    "Agronomist & Crop Management": "Agronome & Conduite des Cultures",
    "Livestock & Veterinary Scientist": "Zootechnicien & Vétérinaire",
    "Agro-Climatologist": "Agro-Climatologue",
    "Socio-Economist & Policy Analyst": "Économiste & Analyste des Politiques",
    "Biometrician & Lead Synthesizer": "Biométricien & Synthétiseur Principal",
    "Precision Irrigation Specialist": "Spécialiste Irrigation & Gestion de l'Eau",
    "Fisheries & Aquaculture Specialist": "Spécialiste Pêche & Aquaculture",
    "Entomologist & Pest Biosecurity": "Entomologiste & Biosécurité des Ravageurs",
    "Heliculture & Snail Farming Specialist": "Spécialiste Héliciculture (Élevage d'Escargots)",
    "Apiculture & Pollination Specialist": "Spécialiste Apiculture & Pollinisation",
    "Swine Production & Biosecurity Specialist": "Spécialiste Porciculture & Biosécurité",
    "Cocoa & Tree Crops Agronomist": "Agronome Cultures Pérennes & Cacao",
    "Cassava & Root Crops Agronomist": "Agronome Manioc & Plantes à Racines",
    "Rabbits & Cuniculture Specialist": "Spécialiste Cuniculture (Élevage Cunicole)",
    "Poultry Production & Bioclimatics Specialist": "Spécialiste Aviculture & Bioclimatologie",

    # Dispatched Multi-Agent Swarm Names
    "Veterinary Pathology & Epidemiology Agent": "Agent de Pathologie Vétérinaire & Épidémiologie",
    "Breeding Herd Health & Reproductive Physiology Agent": "Agent de Santé du Troupeau & Physiologie de Reproduction",
    "Agro-Climatology & Vector Dynamics Agent": "Agent d'Agro-Climatologie & Dynamique des Vecteurs",
    "Agro-Climatology & Vector Dynamics Agent (North-East / Regional)": "Agent d'Agro-Climatologie & Vecteurs Régionaux",
    "Preventive Biosecurity & NVRI Vaccination Protocol Agent": "Agent de Biosécurité Préventive & Protocoles Vaccinaux",
    "Preventive Biosecurity & Vaccination Protocol Agent": "Agent de Biosécurité Préventive & Protocoles Vaccinaux",
    "Herd Economics & Production Loss Agent": "Agent d'Économie Pastorale & Pertes de Production",
    "Institutional Evidence Agent": "Agent de Preuves Scientifiques Institutionnelles",
    "Animal Genetics & Breed Architecture Agent": "Agent de Génétique Animale & Architecture des Races",
    "Animal Genetics & Breeding Agent": "Agent de Génétique & Sélection Animale",
    "Breed Genetics & Conformation Agent": "Agent de Génétique Raciale & Conformation",
    "Nutrition & Feed Management Agent": "Agent de Nutrition Animale & Conduite Alimentaire",
    "Ruminant Nutrition & Feed Science Agent": "Agent de Nutrition des Ruminants & Zootechnie",
    "Rumen Microbiology & Urea Ammoniation Agent": "Agent de Microbiologie Ruminale & Traitement à l'Urée",
    "Pasture & Maternal Nutrition Agent": "Agent des Pâturages & Nutrition Maternelle",
    "Fodder Conservation & Nutrition Agent": "Agent de Conservation des Fourrages & Ensilage",
    "Bioenergetic Feeding & FCR Optimization Agent": "Agent de Nutrition Bioénergétique & Optimisation de l'IC",
    "Non-Conventional Feed Formulation Agent": "Agent de Formulation d'Aliments Non-Conventionnels",
    "Caprine & Ovine Respiratory Complex Agent": "Agent du Complexe Respiratoire Caprin & Ovin",
    "Small Ruminant Epidemiology & Viral Pathology Agent": "Agent d'Épidémiologie & Virologie des Petits Ruminants",
    "Small Ruminant Pathology & PPR Defense Agent": "Agent de Pathologie des Petits Ruminants & Défense contre la PPR",
    "Parasitology & Helminth Resistance Agent": "Agent de Parasitologie & Résistance aux Helminthes",
    "Avian Pathology & Infectious Disease Agent": "Agent de Pathologie Aviaire & Maladies Infectieuses",
    "Poultry Health & Biosecurity Agent": "Agent de Santé Avicole & Biosécurité",
    "Poultry Science & Housing Agent": "Agent de Zootechnie Avicole & Bâtiments d'Élevage",
    "Bioclimatic Housing & Airborne Vector Agent": "Agent de Bâtiments Bioclimatiques & Vecteurs Aériens",
    "Tropical Housing & Thermal Cooling Agent": "Agent d'Habitat Tropical & Refroidissement Thermique",
    "Tropical Climate & Heat Stress Agent": "Agent de Climat Tropical & Gestion du Stress Thermique",
    "Colony Thermoregulation & Hive Shading Agent": "Agent de Thermorégulation des Colonies & Ombrage des Ruches",
    "Cuniculture Science & Housing Agent": "Agent des Sciences Cunicoles & Aménagement des Clapiers",
    "Rabbit Health & Disease Defense Agent": "Agent de Santé Cunicole & Prévention Sanitaire",
    "Rabbit Nutrition & Forage Agent": "Agent de Nutrition Cunicole & Gestion des Fourrages",
    "Porcine Pathology & Epizootiology Agent": "Agent de Pathologie Porcine & Épizootiologie",
    "Swine Biosecurity & ASFV Exclusion Agent": "Agent de Biosécurité Porcine & Prévention PPA",
    "Aquaculture Engineering & Water Quality Agent": "Agent d'Ingénierie Aquacole & Qualité de l'Eau",
    "Fish Pathology & Bacterial Disease Agent": "Agent de Pathologie Piscicole & Maladies Bactériennes",
    "Hatchery Phenomics & Fingerling Grading Agent": "Agent d'Écloserie & Calibrage des Alevins",
    "Heliculture Systems & Gastropod Biology Agent": "Agent des Systèmes Hélicicoles & Biologie des Escargots",
    "Microclimate Relative Humidity & Aestivation Agent": "Agent de Microclimat, Hygrométrie & Estivation",
    "Mantle Biomineralization & Calcium Nutrition Agent": "Agent de Biominéralisation & Nutrition Calcique",
    "Apiculture Science & Apiary Architecture Agent": "Agent des Sciences Apicoles & Architecture du Rucher",
    "Absconding Prevention & Floral Calendar Agent": "Agent de Prévention de la Désertion & Calendrier Apicole",
    "Honey Quality & Moisture Refractometry Agent": "Agent de Qualité du Miel & Réfractométrie",
    "Cereal Agronomy & Crop Physiology Agent": "Agent d'Agronomie des Céréales & Physiologie Végétale",
    "Pathology & Fall Armyworm Defense Agent": "Agent de Phytopathologie & Lutte contre la Légionnaire",
    "Root & Tuber Agronomy Agent": "Agent d'Agronomie des Plantes à Racines & Tubercules",
    "Viral Disease Defense Agent (CMD/CBSD)": "Agent de Lutte contre les Viroses (CMD/CBSD)",
    "Grain Legume Physiology Agent": "Agent de Physiologie des Légumineuses à Grain",
    "Pod Borer & Insect Defense Agent": "Agent de Protection contre le Foreur des Gousses",
    "Biological Nitrogen Fixation Agent": "Agent de Fixation Biologique de l'Azote",
    "Horticultural Pathology & Disease Defense Agent": "Agent de Pathologie Horticole & Protection Sanitaire",
    "Canopy Architecture & Shade Ecology Agent": "Agent d'Architecture Foliaire & Agroforesterie",
    "Phytopathology & Black Pod Defense Agent": "Agent de Phytopathologie & Lutte contre la Pourriture Brune",
    "Perennial Tree Crop Physiology Agent": "Agent de Physiologie des Cultures Pérennes",
    "Soil Chemistry & Mineral Fertility Agent": "Agent de Chimie des Sols & Fertilité Minérale",
    "Soil Fertility & Balanced ISFM Agent": "Agent de Fertilité des Sols & GIFS Équilibrée",
    "Integrated Soil Fertility Management (ISFM) Agent": "Agent de Gestion Intégrée de la Fertilité des Sols",
    "Precision Micro-Dosing & Liming Agent": "Agent de Micro-Dosage de Précision & Chaulage",
    "Edaphic Microbiome & Mycorrhizal Agent": "Agent du Microbiome Édaphique & Mycorhizes",
    "Phosphorus Priming & Edaphic Agent": "Agent d'Apport Phospaté & Dynamique Édaphique",
    "Soil Potassium & Edaphic Nutrition Agent": "Agent du Potassium Édaphique & Nutrition Minérale",
    "Soil Mineral Nutrition & Mulching Agent": "Agent de Nutrition Minérale & Paillage",
    "Soil Fertility & Calcium Nutrition Agent": "Agent de Fertilité des Sols & Nutrition Calcique",
    "Substrate Formulation & Soil Microbiology Agent": "Agent de Formulation des Substrats & Microbiologie",
    "Agro-Climatology & Drought Escape Agent": "Agent d'Agro-Climatologie & Échappement à la Sécheresse",
    "Agro-Climatic Thermal Resilience Agent": "Agent de Résilience Thermique Agro-Climatique",
    "Agro-Climatology & Water Security Agent": "Agent d'Agro-Climatologie & Sécurité Hydrique",
    "Agro-Climatology & Grazing Agent": "Agent d'Agro-Climatologie & Conduite Pastorale",
    "Agro-Climatic Bulking Agent": "Agent de Conditions Agro-Climatiques de Tubérisation",
    "Agro-Climatology & Protected Cultivation Agent": "Agent d'Agro-Climatologie & Cultures Protégées",
    "Flock Mortality & Enterprise Economics Agent": "Agent d'Économie Avicole & Réduction de la Mortalité",
    "Farm Economics & Festive Market Agent": "Agent d'Économie d'Exploitation & Marchés Festifs",
    "Feed Cost & Gross Margin Economics Agent": "Agent du Coût Alimentaire & Marges Brutes",
    "Piggery Enterprise Economics Agent": "Agent d'Économie de l'Entreprise Porcine",
    "Aquaculture Commercial Economics Agent": "Agent d'Économie Commerciale Aquacole",
    "Heliculture Enterprise Economics Agent": "Agent d'Économie de l'Entreprise Hélicicole",
    "Beekeeping Value Chain Economics Agent": "Agent de la Chaîne de Valeur Apicole",
    "Grain Commodity Economics Agent": "Agent d'Économie de la Filière Céréalière",
    "Starch Processing & Market Economics Agent": "Agent de Transformation Féculière & Marchés",
    "Grain Legume Market Economics Agent": "Agent du Marché des Légumineuses à Grain",
    "Value Chain & Fresh Produce Market Agent": "Agent des Filières & Marchés Maraîchers",
    "Export Quality & EUDR Compliance Agent": "Agent de Qualité Export & Conformité RDUE",
    "Fertilizer Input Economics Agent": "Agent d'Économie des Intrants & Engrais",
    "Livestock Economics Agent": "Agent d'Économie de l'Élevage",
    "Livestock Valuation & Pedigree Economics Agent": "Agent de Valorisation du Bétail & Pédigrée",
    "Ram Fattening & Festive Market Agent": "Agent d'Embouche Ovine & Marché du Tabaski",
    "Micro-Livestock Economics Agent": "Agent d'Économie du Mini-Élevage",
    "Vaccination Protocol & Cold-Chain Agent": "Agent de Protocoles Vaccinaux & Chaîne du Froid",
    "Biosecurity & NVRI Homologous Vaccine Agent": "Agent de Biosécurité & Vaccins Homologues",
    "Electrolyte & Nutritional Support Agent": "Agent de Réhydratation & Soutien Électrolytique",
    "Entomology & Insect Vector Control Agent": "Agent d'Entomologie & Lutte Anti-Vectorielle",
    "Reproductive Technologies & AI Agent": "Agent des Biotechnologies de la Reproduction & IA",
    "Rangeland Forage & Legume Agronomy Agent": "Agent des Pâturages & Légumineuses Fourragères",
    "Rangeland & Soil Agent": "Agent des Parcours Pastoraux & Sols",
    "Pathology, Biosecurity & Integrated Protection Agent": "Agent de Pathologie, Biosécurité & Protection Intégrée",
    "Evidence & Research Standards Agent": "Agent de Rigueur & Normes de Recherche",
    "Evidence & Standards Agent": "Agent de Preuves & Standards Scientifiques",
    "Climate & Agro-Ecosystems Agent": "Agent Climat & Agro-Écosystèmes",
    "Climate & Bioclimatic Housing Agent": "Agent Climat & Bâtiments Bioclimatiques",
    "Livestock & Pastoral Science Agent": "Agent des Sciences Pastorales & de l'Élevage",
    "Soil Edaphic & Nutritional Dynamics Agent": "Agent de Dynamique Édaphique & Nutritionnelle",

    # Generic & Single-Domain Agents
    "Genetics Agent": "Agent de Génétique & Sélection",
    "Soil Agent": "Agent des Sols & Agronomie Édaphique",
    "Climate Agent": "Agent d'Agro-Météorologie & Climat",
    "Economics Agent": "Agent d'Économie & Analyse des Filières",
    "Evidence Agent": "Agent de Preuves & Synthèse Scientifique",
    "Crop Science Agent": "Agent des Sciences Végétales & Agronomie"
}



def get_current_lang() -> str:
    """Returns currently selected language code ('en' or 'fr')."""
    if "app_lang" in st.session_state:
        return st.session_state["app_lang"]
    if "app_language_toggle" in st.session_state:
        return "fr" if "Français" in st.session_state["app_language_toggle"] else "en"
    return "en"


def t(key: str, lang: str = None) -> str:
    """
    Translates a translation key according to the active language.
    Falls back to English if the key is missing in French.
    """
    if not lang:
        lang = get_current_lang()
    lang = lang.lower()
    
    catalog = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    if key in catalog:
        return catalog[key]
    
    # Fallback to English
    return TRANSLATIONS["en"].get(key, key)


def translate_agent_name(agent_name: str, lang: str = None) -> str:
    """
    Translates an agent title to French if lang == 'fr', with comprehensive exact-match
    lookup across all 14 domains and intelligent dynamic pattern translation.
    """
    if not lang:
        lang = get_current_lang()
    if lang == "fr":
        if agent_name in AGENT_NAMES_FR:
            return AGENT_NAMES_FR[agent_name]
        
        # Dynamic prefix replacements for contextual Swarm agents
        if agent_name.startswith("Institutional Evidence Agent ("):
            return agent_name.replace("Institutional Evidence Agent (", "Agent de Preuves Institutionnelles (")
        if agent_name.startswith("Institutional Standards Agent ("):
            return agent_name.replace("Institutional Standards Agent (", "Agent de Normes Institutionnelles (")
        if agent_name.startswith("Regional Agro-Climatology & Risk Agent ("):
            return agent_name.replace("Regional Agro-Climatology & Risk Agent (", "Agent d'Agro-Climatologie & Risques Régionaux (")
        if agent_name.startswith("Commodity Value Chain & Farmgate Economics Agent ("):
            return agent_name.replace("Commodity Value Chain & Farmgate Economics Agent (", "Agent de la Chaîne de Valeur & Économie Rurale (")
        if agent_name.startswith("Specialist Agronomic & Bio-Systems Agent ("):
            return agent_name.replace("Specialist Agronomic & Bio-Systems Agent (", "Agent Spécialiste Agro-Biosystèmes (")
        
        # General fallback if title ends with ' Agent'
        if agent_name.endswith(" Agent"):
            base = agent_name[:-6]
            return f"Agent de {base}"
    return agent_name
