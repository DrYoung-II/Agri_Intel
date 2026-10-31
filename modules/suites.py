"""
AgroBiometrix Consolidated Intelligence Suites
Organizes the 14 individual domain engines into 7 cohesive, publication-grade Power Suites:
1. Multi-Agent Orchestrator (Central Home)
2. Agricultural Biometrics & Breeding Suite (Design + DMRT/ANOVA + Trait Selection)
3. AI Research Scientist & Proposal Studio (Proposal + PRISMA Lit Review + Thesis Mentor + Copilot & Radio)
4. Agro-Ecosystems: Soil & Climate Intelligence (Soil NPK/pH + Climate/Drought Scenarios)
5. Livestock & Veterinary Intelligence (Genetics, Nutrition, Pathology)
6. Agricultural Policy & Economic Simulator (Subsidies, Trade, Food Security)
7. Knowledge Graph & Developer API Hub (Interactive Graph + Cloud AI Settings)
"""

import streamlit as st

# Import the existing, untampered domain renderers
from modules.mod8_designer import render_experiment_designer, render_dataset_health_auditor
from modules.mod3_geneticist import render_statistical_geneticist
from modules.mod4_plant_breeding import render_plant_breeding

from modules.mod2_scientist import render_research_scientist
from modules.mod9_literature import render_literature_scientist
from modules.mod10_tutor import render_student_tutor
from modules.mod1_copilot import render_research_copilot

from modules.mod5_soil import render_soil_intelligence
from modules.mod6_climate import render_climate_intelligence

from modules.mod7_livestock import render_livestock_intelligence
from modules.mod11_policy import render_policy_simulator

from modules.mod13_graph_view import render_knowledge_graph_view
from modules.mod15_api_hub import render_api_hub
from modules.mod14_radio import render_vernacular_radio_suite


def _is_fr() -> bool:
    """Helper to detect active French interface."""
    return st.session_state.get("app_lang", "en") == "fr"


def render_suite_biometrics():
    """
    Suite 2: Experimental Biometrics & Crop Breeding
    Consolidates Data Health Audit, Trial Design, Statistical ANOVA/DMRT, and Plant Breeding.
    """
    if _is_fr():
        st.markdown("## 🧬 Biométrie Expérimentale & Amélioration des Plantes")
        st.caption("Intelligence biométrique de bout en bout : de l'audit de santé des données (valeurs manquantes, équilibre) et des plans expérimentaux (RCBD, Split-Plot) jusqu'à la séparation de moyennes (DMRT/Tukey) et la sélection variétale quantitative.")
        tab_titles = [
            "🩺 Audit de Santé des Données & Hypothèses",
            "📐 Conception & Dispositifs Expérimentaux",
            "📊 Statistiques Biométriques & DMRT",
            "🌽 Sélection Végétale & Caractères Quantitatifs"
        ]
    else:
        st.markdown("## 🧬 Experimental Biometrics & Crop Breeding")
        st.caption("End-to-end biometrical intelligence: from pre-analysis data health audits (missingness, balance) and automated experimental design (RCBD, Split-Plot) to mean separation tests (DMRT/Tukey) and quantitative cultivar selection.")
        tab_titles = [
            "🩺 Pre-Analysis Data Health Auditor",
            "📐 Experimental Design & Layout",
            "📊 Statistical Biometrics & DMRT",
            "🌽 Plant Breeding & Cultivar Selection"
        ]

    tab_audit, tab_design, tab_stats, tab_breeding = st.tabs(tab_titles)

    with tab_audit:
        render_dataset_health_auditor()

    with tab_design:
        render_experiment_designer()

    with tab_stats:
        render_statistical_geneticist()

    with tab_breeding:
        render_plant_breeding()


def render_suite_research_studio():
    """
    Suite 3: AI Research Scientist Studio
    Chronological Academic Journey: Literature Review -> Evidence Matrix -> Grant Proposal -> Thesis Defense.
    """
    if _is_fr():
        st.markdown("## 🔬 Chercheur IA & Studio de Thèse / Projets")
        st.caption("Cycle académique chronologique : de la revue systématique de littérature (PRISMA) et la matrice de preuves à la génération de projets de subvention et au mentorat de thèse.")
        tab_titles = [
            "📖 Revue Systématique de Littérature (PRISMA)",
            "🔬 Matrice de Preuves & Lacunes de Recherche",
            "📝 Générateur Intégral de Projet de Recherche",
            "🎓 Mentor de Thèse & Préparation à la Soutenance"
        ]
    else:
        st.markdown("## 🔬 AI Research Scientist Studio")
        st.caption("Chronological postgraduate & research lifecycle: from PRISMA systematic literature reviews and evidence gap analysis to publication-grade 7-part grant proposals and Socratic thesis defense tutoring.")
        tab_titles = [
            "📖 PRISMA Systematic Literature Review",
            "🔬 Structured Evidence Matrix & Knowledge Gaps",
            "📝 Full Research Proposal Generator",
            "🎓 Thesis Mentor & Socratic Defense Tutor"
        ]

    tab_prisma, tab_evidence, tab_proposal, tab_tutor = st.tabs(tab_titles)

    with tab_prisma:
        render_literature_scientist()

    with tab_evidence:
        render_research_copilot()

    with tab_proposal:
        render_research_scientist()

    with tab_tutor:
        render_student_tutor()


def render_suite_agro_ecosystems():
    """
    Suite: Agro-Ecosystems: Soil & Climate Intelligence
    Consolidates Soil Chemistry/Nutrient Simulator and Climate Resilience/Anomalies.
    """
    if _is_fr():
        st.markdown("## 🌍 Agro-Écosystèmes : Sols & Climatologie")
        st.caption("Modélisation environnementale intégrée : dynamique des nutriments édaphiques (NPK, pouvoir tampon du pH) combinée à la résilience climatique et aux prévisions d'anomalies pluviométriques.")
        tab_titles = [
            "🌾 Fertilité des Sols & Simulateur Nutriments",
            "🌦️ Scénarios Climatiques & Stress Thermique"
        ]
    else:
        st.markdown("## 🌍 Agro-Ecosystems: Soil & Climate Intelligence")
        st.caption("Integrated environmental modeling: edaphic nutrient dynamics (NPK, pH buffering) combined with agro-ecological climate resilience and rainfall anomaly forecasting.")
        tab_titles = [
            "🌾 Soil Fertility & Nutrient Simulator",
            "🌦️ Climate Scenarios & Heat Stress"
        ]
    
    tab_soil, tab_climate = st.tabs(tab_titles)
    
    with tab_soil:
        render_soil_intelligence()
        
    with tab_climate:
        render_climate_intelligence()


def render_suite_livestock():
    """
    Suite: Livestock & Veterinary Intelligence
    """
    if _is_fr():
        st.markdown("## 🐄 Élevage & Sciences Zootechniques")
        st.caption("Intelligence vétérinaire et zootechnique intégrée : génétique animale, stress thermique (THI), formulation nutritionnelle et biosécurité aviaire, bovine et petits ruminants.")
    else:
        st.markdown("## 🐄 Livestock & Animal Sciences Intelligence")
        st.caption("Integrated animal science and veterinary intelligence: genomic breeding values, THI thermal stress, precision nutrition formulations, and tropical livestock pathology.")
    render_livestock_intelligence()


def render_suite_policy():
    """
    Suite: Agricultural Policy & Economic Simulator
    """
    if _is_fr():
        st.markdown("## 🏛️ Politiques & Simulateur Macroéconomique Agricole")
        st.caption("Modélisation des politiques publiques agricoles : impact des subventions aux intrants, tarifs douaniers, résilience des chaînes de valeur et sécurité alimentaire.")
    else:
        st.markdown("## 🏛️ Agricultural Policy & Macroeconomic Simulator")
        st.caption("Public policy and macroeconomic modeling: input subsidy optimization, cross-border tariffs, value-chain resilience, and national food security metrics.")
    render_policy_simulator()


def render_suite_tools():
    """
    Suite: Knowledge Graph & Developer API Hub
    Consolidates Interactive Entity Knowledge Graph and Cloud AI Model Management.
    """
    if _is_fr():
        st.markdown("## ⚙️ Graphe de Connaissances & Hub API Développeur")
        st.caption("Infrastructure d'intelligence sous-jacente : explorez le graphe relationnel agronomique et configurez les clés API d'intelligence artificielle.")
        tab_titles = [
            "🕸️ Graphe de Connaissances Agricoles Interactif",
            "🔌 Abonnements API & Gestionnaire de Modèles"
        ]
    else:
        st.markdown("## ⚙️ Knowledge Graph & Developer API Hub")
        st.caption("Underlying intelligence infrastructure: explore the multi-relational agronomic knowledge graph and manage cloud AI engine credentials.")
        tab_titles = [
            "🕸️ Interactive Agricultural Knowledge Graph",
            "🔌 API Subscriptions & Model Hub"
        ]
    
    tab_graph, tab_api = st.tabs(tab_titles)
    
    with tab_graph:
        render_knowledge_graph_view()
        
    with tab_api:
        render_api_hub()


def render_suite_radio():
    """
    Suite 8: Last-Mile Multilingual Radio & Voice Disseminator
    """
    render_vernacular_radio_suite()

