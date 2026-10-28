"""
AgroBiometrix - Agricultural Knowledge Graph Engine
Connects: Gene -> Trait -> Breed/Crop -> Soil -> Climate -> Phenotype -> Economic Outcome -> Policy
Interactive visual graph visualization with Plotly
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Knowledge Graph Nodes and Edges
NODES = [
    # Livestock Nodes
    {"id": "GENE_HSP70", "label": "HSP70 Gene", "category": "Genetics", "color": "#2E7D32", "x": -2.0, "y": 2.5, "desc": "Heat Shock Protein 70; cellular cytoprotection"},
    {"id": "GENE_PRLR", "label": "PRLR (Slick Hair)", "category": "Genetics", "color": "#2E7D32", "x": -2.2, "y": 1.5, "desc": "Prolactin receptor mutation conferring short slick hair"},
    {"id": "TRAIT_THERMO", "label": "Thermotolerance", "category": "Trait", "color": "#4CAF50", "x": -1.0, "y": 2.0, "desc": "Lower rectal temperature & respiration rate under heat"},
    {"id": "BREED_NDAMA", "label": "N'Dama Cattle", "category": "Breed/Commodity", "color": "#1B5E20", "x": 0.0, "y": 2.5, "desc": "West African humpless taurine, trypanotolerant & heat-adapted"},
    {"id": "BREED_FULANI", "label": "White Fulani (Bunaji)", "category": "Breed/Commodity", "color": "#1B5E20", "x": 0.0, "y": 1.5, "desc": "Pastoral Zebu, high walking ability, dual milk/meat"},
    {"id": "CLIM_THI", "label": "Sahelian Climate (THI > 78)", "category": "Environment", "color": "#F57F17", "x": 1.0, "y": 2.0, "desc": "High solar radiation and temperature-humidity index"},
    {"id": "PHENO_MILK", "label": "Milk & Weight Retention", "category": "Phenotype", "color": "#0288D1", "x": 2.0, "y": 2.0, "desc": "Sustained lactation during heat wave shocks"},
    {"id": "ECON_LIVESTOCK", "label": "Pastoralist Income Security", "category": "Economic Outcome", "color": "#7B1FA2", "x": 3.0, "y": 2.0, "desc": "Reduced mortality, steady dairy revenue"},
    
    # Crop Nodes (Maize)
    {"id": "GENE_QTL_ASI", "label": "Chr 1 & 8 Drought QTLs", "category": "Genetics", "color": "#2E7D32", "x": -2.0, "y": -1.5, "desc": "Short anthesis-silking interval & osmotic adjustment"},
    {"id": "TRAIT_STAYGREEN", "label": "Functional Stay-Green", "category": "Trait", "color": "#4CAF50", "x": -1.0, "y": -1.5, "desc": "Prolonged foliar chlorophyll retention during grain filling"},
    {"id": "CROP_MAIZE", "label": "Drought Maize (SAMMAZ 15)", "category": "Breed/Commodity", "color": "#1B5E20", "x": 0.0, "y": -1.5, "desc": "IITA/IAR elite open-pollinated/hybrid cultivar"},
    {"id": "SOIL_SAVANNA", "label": "Savanna Alfisol Soil", "category": "Environment", "color": "#E65100", "x": 0.0, "y": -2.5, "desc": "Low organic carbon, P-deficient, responsive to micro-dosing"},
    {"id": "CLIM_DROUGHT", "label": "Sudan Savanna Rainfall (-15%)", "category": "Environment", "color": "#F57F17", "x": 1.0, "y": -1.5, "desc": "Early cessation of rainy season, dry spells"},
    {"id": "PHENO_YIELD", "label": "Grain Yield (4.5 t/ha)", "category": "Phenotype", "color": "#0288D1", "x": 2.0, "y": -1.5, "desc": "Resilient cob filling without catastrophic barrenness"},
    {"id": "ECON_FOODSEC", "label": "Smallholder Profit & Food Security", "category": "Economic Outcome", "color": "#7B1FA2", "x": 3.0, "y": -1.5, "desc": "Downside harvest protection, improved return on investment"},
    
    # Policy Node
    {"id": "POLICY_NATIONAL", "label": "National Seed & Subsidy Policy", "category": "Policy", "color": "#C2185B", "x": 1.5, "y": 0.2, "desc": "Government certified seed distribution & targeted input subsidy"}
]

EDGES = [
    # Livestock Relationships
    ("GENE_HSP70", "TRAIT_THERMO", "Up-regulates"),
    ("GENE_PRLR", "TRAIT_THERMO", "Lowers core temp"),
    ("TRAIT_THERMO", "BREED_NDAMA", "Expressed in"),
    ("TRAIT_THERMO", "BREED_FULANI", "Selected in"),
    ("BREED_NDAMA", "CLIM_THI", "Adapts to"),
    ("BREED_FULANI", "CLIM_THI", "Exposed to"),
    ("CLIM_THI", "PHENO_MILK", "Buffers impact on"),
    ("PHENO_MILK", "ECON_LIVESTOCK", "Drives"),
    
    # Crop Relationships
    ("GENE_QTL_ASI", "TRAIT_STAYGREEN", "Controls"),
    ("TRAIT_STAYGREEN", "CROP_MAIZE", "Selected in"),
    ("CROP_MAIZE", "SOIL_SAVANNA", "Grown in"),
    ("CROP_MAIZE", "CLIM_DROUGHT", "Withstands"),
    ("SOIL_SAVANNA", "PHENO_YIELD", "Provides nutrition for"),
    ("CLIM_DROUGHT", "PHENO_YIELD", "Risk factor for"),
    ("PHENO_YIELD", "ECON_FOODSEC", "Generates"),
    
    # Policy Relationships
    ("POLICY_NATIONAL", "CROP_MAIZE", "Subsidizes adoption"),
    ("POLICY_NATIONAL", "ECON_FOODSEC", "Scales national impact")
]


def create_knowledge_graph_figure(domain_filter="All"):
    """
    Renders an interactive 2D network diagram of the Agricultural Knowledge Graph using Plotly.
    """
    # Filter nodes
    if domain_filter == "Livestock Only":
        active_ids = {n["id"] for n in NODES if n["y"] > 0 or n["category"] == "Policy"}
    elif domain_filter == "Crops Only":
        active_ids = {n["id"] for n in NODES if n["y"] < 0 or n["category"] == "Policy"}
    else:
        active_ids = {n["id"] for n in NODES}
        
    filtered_nodes = [n for n in NODES if n["id"] in active_ids]
    node_id_to_data = {n["id"]: n for n in filtered_nodes}
    
    edge_x = []
    edge_y = []
    edge_text = []
    
    for u, v, rel in EDGES:
        if u in active_ids and v in active_ids:
            n1 = node_id_to_data[u]
            n2 = node_id_to_data[v]
            edge_x.extend([n1["x"], n2["x"], None])
            edge_y.extend([n1["y"], n2["y"], None])
            
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.8, color="#A5D6A7"),
        hoverinfo='none',
        mode='lines'
    )
    
    node_x = [n["x"] for n in filtered_nodes]
    node_y = [n["y"] for n in filtered_nodes]
    node_color = [n["color"] for n in filtered_nodes]
    node_text = [f"<b>{n['label']}</b><br>Type: {n['category']}<br>{n['desc']}" for n in filtered_nodes]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[n['label'] for n in filtered_nodes],
        textposition="top center",
        hovertext=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=24,
            line=dict(width=2, color='#FFFFFF')
        ),
        textfont=dict(size=11, color="#1B3B1D")
    )
    
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text="<b>AgroBiometrix Agricultural Knowledge Graph</b><br><sup>Tracing Gene ➔ Trait ➔ Breed ➔ Environment ➔ Phenotype ➔ Economic Outcome</sup>",
                font=dict(size=15, color="#1B5E20")
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=50),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="#F8FAF8",
            paper_bgcolor="#FFFFFF",
            height=540
        )
    )
    return fig
