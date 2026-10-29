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
from modules.mod8_designer import render_experiment_designer
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


def _is_fr() -> bool:
    """Helper to detect active French interface."""
    return st.session_state.get("app_lang", "en") == "fr"


def render_suite_biometrics():
    """
    Suite: Agricultural Biometrics & Breeding Suite
    Consolidates Experiment Design, Statistical ANOVA/DMRT, and Plant Breeding Cultivar Selection.
    """
    if _is_fr():
        st.markdown("## 🧬 Biométrie Agricole & Sélection Végétale")
        st.caption("Intelligence biométrique de bout en bout : de la modélisation des plans expérimentaux (RCBD, Split-Plot, Alpha-Lattice) jusqu'à la séparation de moyennes (DMRT/Tukey) et la sélection variétale quantitative.")
        tab_titles = [
            "📐 Conception & Dispositifs Expérimentaux",
            "📊 Statistiques Biométriques & DMRT",
            "🌽 Sélection Variétale & Sélection Génomique"
        ]
    else:
        st.markdown("## 🧬 Agricultural Biometrics & Breeding Suite")
        st.caption("End-to-end biometrical intelligence: from experimental field layout design to rigorous ANOVA mean separation (DMRT) and quantitative breeding selection.")
        tab_titles = [
            "📐 Experiment Designer & Layouts",
            "📊 Biometric Statistics & DMRT",
            "🌽 Quantitative Breeding & Cultivar Selection"
        ]
    
    tab_design, tab_stats, tab_breeding = st.tabs(tab_titles)
    
    with tab_design:
        render_experiment_designer()
        
    with tab_stats:
        render_statistical_geneticist()
        
    with tab_breeding:
        render_plant_breeding()


def render_suite_research_studio():
    """
    Suite: AI Research Scientist & Proposal Studio
    Consolidates Proposal Generator, PRISMA Systematic Literature Review, Thesis Mentor, and Copilot Evidence/Radio.
    """
    if _is_fr():
        st.markdown("## 🔬 Chercheur IA & Studio de Thèse / Projets")
        st.caption("Cycle complet de la recherche agronomique : de la revue systématique de la littérature (PRISMA) au mentorat socratique de thèse et à la génération de projets de subvention.")
        tab_titles = [
            "📝 Générateur Intégral de Projet de Recherche",
            "📖 Revue Systématique de Littérature (PRISMA)",
            "🎓 Mentor de Thèse & Préparation à la Soutenance",
            "📚 Matrice de Preuves & Radio Vernaculaire"
        ]
    else:
        st.markdown("## 🔬 AI Research Scientist & Proposal Studio")
        st.caption("Complete academic research lifecycle: from PRISMA systematic literature reviews and Socratic thesis defense tutoring to publication-grade 7-part grant proposals and vernacular extension.")
        tab_titles = [
            "📝 Full Research Proposal Generator",
            "📖 PRISMA Systematic Literature Review",
            "🎓 Thesis Mentor & Defense Tutor",
            "📚 Evidence Matrix & Vernacular Radio"
        ]
    
    tab_proposal, tab_prisma, tab_tutor, tab_copilot = st.tabs(tab_titles)
    
    with tab_proposal:
        render_research_scientist()
        
    with tab_prisma:
        render_literature_scientist()
        
    with tab_tutor:
        render_student_tutor()
        
    with tab_copilot:
        render_research_copilot()


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
    render_livestock_intelligence()


def render_suite_policy():
    """
    Suite: Agricultural Policy & Economic Simulator
    """
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
