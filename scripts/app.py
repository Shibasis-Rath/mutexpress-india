import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="MutExpress-India", page_icon="🧬", layout="wide")
st.title("🧬 MutExpress-India Dashboard")

# Define base path to results
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "results"))

# 1. Load Main Data FIRST
csv_path = os.path.join(RESULTS_DIR, "mutexpress_india_output.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path) # Now 'df' is created

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("HIGH Priority", len(df[df["MutExpress_Priority"] == "HIGH"]))
    c2.metric("MEDIUM_V", len(df[df["MutExpress_Priority"] == "MEDIUM_V"]))
    c3.metric("MEDIUM_E", len(df[df["MutExpress_Priority"] == "MEDIUM_E"]))

    # Show Pie Chart
    counts = df["MutExpress_Priority"].value_counts().reset_index()
    counts.columns = ["Priority", "count"] # Explicitly set column names
    fig = px.pie(counts, names="Priority", values="count", title="Priority Distribution")
    st.plotly_chart(fig)

    # Show Enrichment Tabs
    st.header("Phase 5: Pathway Enrichment")
    tab1, tab2 = st.tabs(["GO Enrichment", "KEGG Enrichment"])

    with tab1:
        img_path = os.path.join(RESULTS_DIR, "GO_dotplot.png")
        csv_path_go = os.path.join(RESULTS_DIR, "GO_enrichment.csv")
        if os.path.exists(img_path):
            st.image(img_path)
            st.dataframe(pd.read_csv(csv_path_go))
        else:
            st.warning("GO plots or data not found.")

    with tab2:
        img_path_kegg = os.path.join(RESULTS_DIR, "KEGG_dotplot.png")
        csv_path_kegg = os.path.join(RESULTS_DIR, "KEGG_enrichment.csv")
        if os.path.exists(img_path_kegg):
            st.image(img_path_kegg)
            st.dataframe(pd.read_csv(csv_path_kegg))
        else:
            st.warning("KEGG plots or data not found.")
else:
    st.error(f"Cannot find the data file at: {csv_path}. Check your results folder path.")