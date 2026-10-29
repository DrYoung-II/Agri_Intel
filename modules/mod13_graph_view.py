"""
Module 13: Agricultural Knowledge Graph Viewer
Interactive visual exploration of connected genetics, edaphics, climate, and economics
"""

import streamlit as st
from core.knowledge_graph import create_knowledge_graph_figure, NODES, EDGES
import pandas as pd


def render_knowledge_graph_view():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 🕸️ Graphe de Connaissances Agricoles Panafricain")
        st.caption("Au-delà du texte brut des LLM : un réseau relationnel structuré de connaissances biologiques, édaphiques et climatiques.")
        filter_lbl = "Filtrer le Sous-Réseau :"
        filter_opts = ["Tous", "Élevage Uniquement", "Cultures Uniquement"]
        legend_txt = "**Légende** : 🟢 Génétique/Caractères | 🌲 Races/Cultures | 🟠 Sol/Climat | 🔵 Phénotype | 🟣 Économie/Politiques"
    else:
        st.markdown("### 🕸️ African Agricultural Knowledge Graph")
        st.caption("Moving beyond isolated LLM text to a structured, connected biological and edaphic knowledge network.")
        filter_lbl = "Filter Graph Sub-Network:"
        filter_opts = ["All", "Livestock Only", "Crops Only"]
        legend_txt = "**Legend**: 🟢 Genetics/Traits | 🌲 Breeds/Crops | 🟠 Soil/Climate | 🔵 Phenotype | 🟣 Economics/Policy"

    col1, col2 = st.columns([2, 1])
    with col1:
        domain_choice = st.radio(filter_lbl, filter_opts, horizontal=True)
        domain = "Livestock Only" if "Élevage" in domain_choice else ("Crops Only" if "Cultures" in domain_choice else "All")
    with col2:
        st.markdown(legend_txt)

    fig = create_knowledge_graph_figure(domain_filter=domain)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🔍 Inspecteur de Nœuds & d'Entités du Graphe" if is_fr else "#### 🔍 Knowledge Graph Node & Entity Inspector")
    df_nodes = pd.DataFrame(NODES)[["label", "category", "desc"]]
    df_nodes.columns = ["Entity Name", "Category", "Biological / Agro Description"]
    st.dataframe(df_nodes, use_container_width=True)

    exp_edge_lbl = "🔗 Afficher les Relations Vérifiées (Arêtes)" if is_fr else "🔗 View Verified Relational Edges"
    with st.expander(exp_edge_lbl):
        df_edges = pd.DataFrame(EDGES, columns=["Source Entity", "Target Entity", "Relationship Type"])
        st.dataframe(df_edges, use_container_width=True)
