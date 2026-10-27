"""
Module 13: Agricultural Knowledge Graph Viewer
Interactive visual exploration of connected genetics, edaphics, climate, and economics
"""

import streamlit as st
from core.knowledge_graph import create_knowledge_graph_figure, NODES, EDGES
import pandas as pd


def render_knowledge_graph_view():
    st.markdown("### 🕸️ African Agricultural Knowledge Graph")
    st.caption("Moving beyond isolated LLM text to a structured, connected biological and edaphic knowledge network.")

    col1, col2 = st.columns([2, 1])
    with col1:
        domain = st.radio("Filter Graph Sub-Network:", ["All", "Livestock Only", "Crops Only"], horizontal=True)
    with col2:
        st.markdown("**Legend**: 🟢 Genetics/Traits | 🌲 Breeds/Crops | 🟠 Soil/Climate | 🔵 Phenotype | 🟣 Economics/Policy")

    fig = create_knowledge_graph_figure(domain_filter=domain)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🔍 Knowledge Graph Node & Entity Inspector")
    df_nodes = pd.DataFrame(NODES)[["label", "category", "desc"]]
    df_nodes.columns = ["Entity Name", "Category", "Biological / Agro Description"]
    st.dataframe(df_nodes, use_container_width=True)

    with st.expander("🔗 View Verified Relational Edges"):
        df_edges = pd.DataFrame(EDGES, columns=["Source Entity", "Target Entity", "Relationship Type"])
        st.dataframe(df_edges, use_container_width=True)
