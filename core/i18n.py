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
        "hero_cert_badge": "PAN-AFRICAN & GLOBAL PLATFORM",
        "hero_cert_sub": "Enterprise Research Infrastructure",

        # Sidebar & Controls
        "lang_selector_label": "🌐 Interface Language / Langue:",
        "region_selector_label": "🌍 Regional Context & Currency:",
        "region_selector_help": "Adapts local currency, input pricing, agro-ecological zones, and NARS research protocols.",
        "suite_selector_label": "SELECT INTELLIGENCE SUITE:",
        "connect_gemini_label": "🔑 Connect Google Gemini (Optional Free Key)",
        "gemini_key_prompt": "Google Gemini Key:",
        "gemini_active": "🟢 Live Google Gemini Engine Active",
        "gemini_secured": "Cloud Verified &bull; Secrets Secured",
        "founder_story_label": "📖 Founder Story & Vision",
        "edition_label": "AgroBiometrix v2.4 &bull; Africa-First Institutional Edition",
        "powered_by": "POWERED BY",
        "unlocking_data": "Unlocking the power of data",

        # Suites Titles
        "suite_orchestrator": "🌟 Multi-Agent Orchestrator",
        "suite_biometrics": "🧬 Agricultural Biometrics & Breeding Suite",
        "suite_scientist": "🔬 AI Research Scientist & Proposal Studio",
        "suite_agro": "🌍 Agro-Ecosystems: Soil & Climate Intelligence",
        "suite_livestock": "🐄 Livestock & Veterinary Intelligence",
        "suite_policy": "🏛️ Agricultural Policy & Economic Simulator",
        "suite_api": "⚙️ Knowledge Graph & Developer API Hub",

        # Orchestrator
        "orch_header": "🤖 Multi-Agent Orchestration Layer",
        "orch_quote": (
            "A normal agricultural AI says: <i>'Upload a picture of your tomato leaf, and I will tell you what disease it has.'</i><br>"
            "<b>AgroBiometrix says</b>: <i>'Give me a crop, animal, location, genotype, soil condition, climate scenario, production objective, "
            "research question or policy problem—and I will assemble the relevant evidence, analyze the available data, run appropriate models, "
            "explain the results, and recommend what should be done.'</i>"
        ),
        "orch_ask_label": "💬 Ask AgroBiometrix Anything (Cross-Disciplinary Inquiry):",
        "orch_ask_placeholder": "e.g., How does high temperature-humidity index (THI) affect conception rate in Bunaji dairy cows, and what nutritional biosecurity interventions are recommended?",
        "orch_btn": "🚀 Run Multi-Agent Cross-Disciplinary Synthesis",
        "orch_advisory_tab": "📑 Consolidated Scientific Advisory & Action Plan",
        "orch_agents_tab": "👥 Individual Specialist Agent Deliberations",
        "orch_preset_label": "🎯 Strategic Cross-Agent Scenarios (Click to Load):",

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
        "hero_cert_badge": "PLATEFORME PANAFRICAINE & MONDIALE",
        "hero_cert_sub": "Infrastructure de Recherche d'Entreprise",

        # Sidebar & Controls
        "lang_selector_label": "🌐 Langue de l'Interface / Language :",
        "region_selector_label": "🌍 Contexte Régional & Devise :",
        "region_selector_help": "Adapte la monnaie locale, le barème des intrants, les zones agro-écologiques et les protocoles SNRA.",
        "suite_selector_label": "SÉLECTIONNER LA SUITE D'INTELLIGENCE :",
        "connect_gemini_label": "🔑 Connecter Google Gemini (Clé Gratuite Optionnelle)",
        "gemini_key_prompt": "Clé API Google Gemini :",
        "gemini_active": "🟢 Moteur Google Gemini Actif & Sécurisé",
        "gemini_secured": "Vérifié sur le Cloud &bull; Secrets Protégés",
        "founder_story_label": "📖 Histoire & Vision du Fondateur",
        "edition_label": "AgroBiometrix v2.4 &bull; Édition Institutionnelle Panafricaine",
        "powered_by": "PROPULSÉ PAR",
        "unlocking_data": "Libérer la puissance des données",

        # Suites Titles
        "suite_orchestrator": "🌟 Orchestrateur Multi-Agents",
        "suite_biometrics": "🧬 Biométrie Agricole & Sélection Végétale",
        "suite_scientist": "🔬 Chercheur IA & Studio de Thèse / Projets",
        "suite_agro": "🌍 Agro-Écosystèmes : Sols & Climatologie",
        "suite_livestock": "🐄 Intelligence Vétérinaire & Zootechnique",
        "suite_policy": "🏛️ Simulateur de Politiques & Économie Agricole",
        "suite_api": "⚙️ Graphe de Connaissances & Hub API Développeur",

        # Orchestrator
        "orch_header": "🤖 Couche d'Orchestration Multi-Agents",
        "orch_quote": (
            "Une IA agricole classique dit : <i>'Téléversez une photo de votre feuille de tomate, et je vous dirai quelle maladie elle a.'</i><br>"
            "<b>AgroBiometrix déclare</b> : <i>'Indiquez-moi une culture, un animal, une localité, un génotype, l'état du sol, un scénario climatique, "
            "un objectif de production, une problématique de recherche ou de politique agricole—et je rassemblerai les preuves pertinentes, analyserai "
            "les données disponibles, exécuterai les modèles appropriés, expliquerai les résultats et recommanderai les actions optimales.'</i>"
        ),
        "orch_ask_label": "💬 Poser une Question à AgroBiometrix (Requête Pluridisciplinaire) :",
        "orch_ask_placeholder": "Ex: Quel est l'impact de l'indice température-humidité (THI) sur la reproduction des vaches Zébu Gobra ou Baoulé, et quels protocoles nutritionnels et de biosécurité préconiser ?",
        "orch_btn": "🚀 Lancer la Synthèse Multi-Agents Transversale",
        "orch_advisory_tab": "📑 Avis Scientifique Consolidé & Protocole d'Action",
        "orch_agents_tab": "👥 Délibérations Détaillées des Agents Spécialistes",
        "orch_preset_label": "🎯 Scénarios Stratégiques Prédéfinis (Cliquez pour Charger) :",

        # Footer
        "footer_badge": "INFRASTRUCTURE D'INTELLIGENCE AGRONOMIQUE D'ENTREPRISE",
        "footer_title": "Plateforme AgroBiometrix",
        "footer_subtitle": "Biométrie Quantitative, Amélioration Génomique & Intelligence Artificielle pour l'Agriculture",
        "footer_legal": "Conçu pour les SNRA d'Afrique subsaharienne, les centres CGIAR, Universités & Entreprises Agrobusiness.",
        "footer_rights": "© 2026 AgroBiometrix &bull; Développé & Propulsé par Naysa-84 Labs. Tous droits réservés.",
        "footer_meta": "AgTech Panafricaine &bull; Intelligence Autonome & Cloud &bull; Version 2.4",
    }
}


def get_current_lang() -> str:
    """Returns currently selected language code ('en' or 'fr')."""
    if "app_lang" in st.session_state:
        return st.session_state["app_lang"]
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
