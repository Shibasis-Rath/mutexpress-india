import streamlit as st

st.set_page_config(
    page_title="MutExpress India | Home",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core styling with dark, cinematic aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{
    --bg:#0B0F17; --surface:#111722; --border:#1E2A3A;
    --teal:#00D4C8; --blue:#4A9EFF; --text:#E8EDF5; --muted:#7A8FA6;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }

/* Hero Banner */
.hero-box {
    background: linear-gradient(135deg, #0d1f2e, #081420);
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal);
    border-radius: 8px;
    padding: 3.5rem 2.5rem;
    margin-bottom: 3rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 3.2rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    color: var(--muted);
    font-size: 1.15rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Feature Cards */
.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 2.5rem;
    height: 100%;
    transition: all 0.3s ease;
}
.feature-card:hover {
    border-color: var(--blue);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.feature-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
    color: var(--teal);
    margin-bottom: 1.2rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.sidebar-note {
    text-align: center;
    color: var(--blue);
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px dashed var(--border);
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Render Hero Section
st.markdown("""
<div class="hero-box">
    <div class="hero-title">MutExpress <span style="color:#00D4C8">India</span></div>
    <div class="hero-subtitle">
        An advanced dual-layer bioinformatics pipeline for Indian-population-aware cancer variant prioritization. 
        Integrating genomic variant severity with transcriptomic expression to identify true clinical drivers.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sidebar-note">
    👈 Open the sidebar menu on the left to begin your analysis.
</div>
""", unsafe_allow_html=True)

# Render Module Cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">01 · Data Converter</div>
        <p style="color:#7A8FA6; line-height: 1.7; font-size: 0.95rem;">
            <strong>Start here if you have raw data.</strong> The universal converter automatically standardizes 
            cBioPortal, GDC, TCGA, or custom format files into the exact formats required by MutExpress: 
            <code>priority_variants.tsv</code> and <code>significant_degs.csv</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">02 · Main Dashboard</div>
        <p style="color:#7A8FA6; line-height: 1.7; font-size: 0.95rem;">
            <strong>Upload your processed files here.</strong> Run the dual-layer integration, apply 
            the South Asian (SAS) population filters, compute severity tiers (HIGH / MEDIUM), and execute live GO/KEGG pathway enrichment.
        </p>
    </div>
    """, unsafe_allow_html=True)
