import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="MutExpress-India", page_icon="🧬", layout="wide")
st.title("🧬 MutExpress-India Dashboard")

# Find the results folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "results"))

# Load data
df = pd.read_csv(os.path.join(RESULTS_DIR, "mutexpress_india_output.csv"))

# Show Pie Chart
counts = df["MutExpress_Priority"].value_counts().reset_index()
fig = px.pie(counts, names="Priority", values="count", title="Priority Distribution")
st.plotly_chart(fig)

# Show Enrichment Tabs
st.header("Phase 5: Pathway Enrichment")
tab1, tab2 = st.tabs(["GO Enrichment", "KEGG Enrichment"])

with tab1:
    st.image(os.path.join(RESULTS_DIR, "GO_dotplot.png"))
    st.dataframe(pd.read_csv(os.path.join(RESULTS_DIR, "GO_enrichment.csv")))

with tab2:
    st.image(os.path.join(RESULTS_DIR, "KEGG_dotplot.png"))
    st.dataframe(pd.read_csv(os.path.join(RESULTS_DIR, "KEGG_enrichment.csv")))