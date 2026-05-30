import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MutExpress-India",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Fonts ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Root variables ────────────────────────────── */
:root {
    --bg:        #0B0F17;
    --surface:   #111722;
    --border:    #1E2A3A;
    --teal:      #00D4C8;
    --teal-dim:  rgba(0,212,200,0.12);
    --orange:    #F4793B;
    --blue:      #4A9EFF;
    --green:     #3DDC84;
    --red:       #FF5B5B;
    --text:      #E8EDF5;
    --muted:     #7A8FA6;
}

/* ─── Global reset ──────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background-color: var(--bg) !important; }

/* ─── Hide Streamlit chrome ─────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1400px !important; }

/* ─── Hero banner ───────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0d1f2e 0%, #0B1929 60%, #081420 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal);
    border-radius: 4px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(0,212,200,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--teal);
    border: 1px solid rgba(0,212,200,0.35);
    padding: 3px 10px;
    border-radius: 2px;
    margin-bottom: 0.9rem;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero h1 span { color: var(--teal); }
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
    max-width: 620px;
}
.badge-row { display: flex; gap: 0.6rem; margin-top: 1.2rem; flex-wrap: wrap; }
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 4px 10px;
    border-radius: 2px;
    letter-spacing: 0.08em;
}
.badge-python { background: rgba(74,158,255,0.15); color: var(--blue); border: 1px solid rgba(74,158,255,0.3); }
.badge-r      { background: rgba(61,220,132,0.12); color: var(--green); border: 1px solid rgba(61,220,132,0.3); }
.badge-tcga   { background: rgba(244,121,59,0.12); color: var(--orange); border: 1px solid rgba(244,121,59,0.3); }
.badge-gnomad { background: rgba(0,212,200,0.10); color: var(--teal); border: 1px solid rgba(0,212,200,0.3); }

/* ─── Metric cards ──────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.high::after   { background: var(--red); }
.metric-card.med_v::after  { background: var(--orange); }
.metric-card.med_e::after  { background: var(--blue); }
.metric-card.total::after  { background: var(--teal); }

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-card.high   .metric-value { color: var(--red); }
.metric-card.med_v  .metric-value { color: var(--orange); }
.metric-card.med_e  .metric-value { color: var(--blue); }
.metric-card.total  .metric-value { color: var(--teal); }
.metric-sub {
    font-size: 0.75rem;
    color: var(--muted);
}

/* ─── Section headers ───────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.section-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--teal);
    background: var(--teal-dim);
    padding: 2px 8px;
    border-radius: 2px;
}
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text);
}

/* ─── Chart containers ──────────────────────────── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.chart-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}

/* ─── Ablation table ────────────────────────────── */
.abl-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
.abl-table th {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0.6rem 1rem;
    border-bottom: 1px solid var(--border);
    text-align: left;
}
.abl-table td {
    font-size: 0.88rem;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(30,42,58,0.6);
    color: var(--text);
}
.abl-table tr:last-child td { border-bottom: none; }
.abl-table tr.best td { color: var(--teal); }
.abl-table tr.best td:first-child { font-weight: 600; }
.pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
}
.pill-high   { background: rgba(255,91,91,0.15);  color: var(--red); }
.pill-medv   { background: rgba(244,121,59,0.15); color: var(--orange); }
.pill-mede   { background: rgba(74,158,255,0.15); color: var(--blue); }
.pill-dual   { background: rgba(0,212,200,0.12);  color: var(--teal); }

/* ─── Info box ──────────────────────────────────── */
.info-box {
    background: rgba(0,212,200,0.06);
    border: 1px solid rgba(0,212,200,0.2);
    border-left: 3px solid var(--teal);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: var(--muted);
    line-height: 1.6;
    margin: 1rem 0;
}
.info-box strong { color: var(--teal); }

/* ─── Tab styling ───────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.7rem 1.4rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom: 2px solid var(--teal) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    padding: 1.5rem !important;
}

/* ─── Dataframe overrides ───────────────────────── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg) !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
}

/* ─── File uploader ─────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border) !important;
    background: var(--surface) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
}

/* ─── Divider ───────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "results"))

def rp(filename):
    return os.path.join(RESULTS_DIR, filename)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_main():
    p = rp("mutexpress_india_output.csv")
    if os.path.exists(p):
        return pd.read_csv(p)
    return None

@st.cache_data
def load_ablation():
    p = rp("ablation_summary.csv")
    if os.path.exists(p):
        return pd.read_csv(p)
    return None

@st.cache_data
def load_degs():
    p = rp("significant_degs.csv")
    if os.path.exists(p):
        return pd.read_csv(p)
    return None

df       = load_main()
abl_df   = load_ablation()
degs_df  = load_degs()

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">MSc Bioinformatics · May 2026</div>
  <h1>Mut<span>Express</span>-India</h1>
  <p>Indian-population-aware dual-layer variant + expression prioritization pipeline for Breast Cancer genomics.</p>
  <div class="badge-row">
    <span class="badge badge-python">Python 3.10</span>
    <span class="badge badge-r">R · DESeq2</span>
    <span class="badge badge-tcga">TCGA-BRCA</span>
    <span class="badge badge-gnomad">gnomAD SAS</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── METRIC CARDS ───────────────────────────────────────────────────────────────
if df is not None:
    high  = len(df[df["MutExpress_Priority"] == "HIGH"])
    med_v = len(df[df["MutExpress_Priority"] == "MEDIUM_V"])
    med_e = len(df[df["MutExpress_Priority"] == "MEDIUM_E"])
    total = high + med_v + med_e

    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card high">
        <div class="metric-label">🔴 HIGH Priority</div>
        <div class="metric-value">{high:,}</div>
        <div class="metric-sub">Rare variant + DEG evidence</div>
      </div>
      <div class="metric-card med_v">
        <div class="metric-label">🟠 MEDIUM — Variant</div>
        <div class="metric-value">{med_v:,}</div>
        <div class="metric-sub">Rare SAS variant only</div>
      </div>
      <div class="metric-card med_e">
        <div class="metric-label">🔵 MEDIUM — Expression</div>
        <div class="metric-value">{med_e:,}</div>
        <div class="metric-sub">Significant DEG only</div>
      </div>
      <div class="metric-card total">
        <div class="metric-label">⬜ Total Genes</div>
        <div class="metric-value">{total:,}</div>
        <div class="metric-sub">All tiers combined</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 · Priority Overview",
    "02 · HIGH Priority Genes",
    "03 · Pathway Enrichment",
    "04 · Ablation Validation",
    "05 · Upload Your Data"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PRIORITY OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="info-box">
      <strong>About this pipeline:</strong> MutExpress-India integrates two independent lines of 
      computational evidence — South Asian allele-frequency-aware somatic variant filtering 
      (gnomAD SAS AF &lt; 1%) and DESeq2 differential expression analysis on TCGA-BRCA RNA-Seq 
      counts (GSE62944). Genes flagged by <strong>both</strong> layers are classified as HIGH priority.
    </div>
    """, unsafe_allow_html=True)

    if df is not None:
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown('<div class="chart-card"><div class="chart-title">Priority tier distribution</div>', unsafe_allow_html=True)
            counts = df["MutExpress_Priority"].value_counts().reset_index()
            counts.columns = ["Priority", "Count"]
            color_map = {
                "HIGH":     "#FF5B5B",
                "MEDIUM_V": "#F4793B",
                "MEDIUM_E": "#4A9EFF",
                "LOW":      "#1E2A3A"
            }
            fig_pie = px.pie(
                counts, names="Priority", values="Count",
                color="Priority", color_discrete_map=color_map,
                hole=0.55
            )
            fig_pie.update_traces(
                textfont=dict(family="Space Mono", size=11, color="#E8EDF5"),
                hovertemplate="<b>%{label}</b><br>%{value:,} genes<extra></extra>"
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#7A8FA6"),
                legend=dict(
                    font=dict(family="Space Mono", size=10, color="#7A8FA6"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="chart-card"><div class="chart-title">Top 15 most mutated genes (HIGH tier)</div>', unsafe_allow_html=True)
            high_df = df[df["MutExpress_Priority"] == "HIGH"]
            if not high_df.empty:
                top15 = high_df["gene"].value_counts().head(15).reset_index()
                top15.columns = ["Gene", "Count"]
                fig_bar = px.bar(
                    top15, x="Count", y="Gene", orientation="h",
                    color_discrete_sequence=["#00D4C8"]
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(
                        autorange="reversed",
                        tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"),
                        gridcolor="rgba(30,42,58,0.5)"
                    ),
                    xaxis=dict(
                        tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"),
                        gridcolor="rgba(30,42,58,0.5)"
                    ),
                    font=dict(family="DM Sans", color="#7A8FA6"),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=320
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Priority tier descriptions
        st.markdown("""
        <div class="section-header">
          <span class="section-num">TIER GUIDE</span>
          <span class="section-title">Priority Classification Logic</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""<div class="chart-card">
            <div class="metric-label" style="color:#FF5B5B">🔴 HIGH</div>
            <p style="font-size:0.82rem;color:#7A8FA6;margin-top:0.5rem">
            Rare damaging variant <em>AND</em> significant expression change.
            Both independent computational layers agree. Strongest evidence.
            </p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="chart-card">
            <div class="metric-label" style="color:#F4793B">🟠 MEDIUM_V</div>
            <p style="font-size:0.82rem;color:#7A8FA6;margin-top:0.5rem">
            Rare damaging variant in South Asian population only. 
            No significant expression change detected.
            </p></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class="chart-card">
            <div class="metric-label" style="color:#4A9EFF">🔵 MEDIUM_E</div>
            <p style="font-size:0.82rem;color:#7A8FA6;margin-top:0.5rem">
            Significant expression dysregulation only.
            No rare South Asian variant in this dataset.
            </p></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown("""<div class="chart-card">
            <div class="metric-label" style="color:#3B4A5A">⚪ LOW</div>
            <p style="font-size:0.82rem;color:#7A8FA6;margin-top:0.5rem">
            Neither criterion met in this analysis.
            No supporting evidence from either layer.
            </p></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — HIGH PRIORITY GENES
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    if df is not None:
        high_df = df[df["MutExpress_Priority"] == "HIGH"].dropna(
            subset=["log2FoldChange", "damage_score"]
        ).copy()

        st.markdown("""
        <div class="section-header">
          <span class="section-num">KEY FIGURE</span>
          <span class="section-title">Expression Change vs Variant Severity</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          Each point is a <strong>HIGH priority gene</strong>. 
          X-axis = Log₂ fold change in tumor vs normal (DESeq2). 
          Y-axis = Damage score (1–3, sum of SIFT + PolyPhen + IMPACT tools predicting damage).
          <strong>Top-right quadrant</strong> = strongest candidates (upregulated AND highly damaging).
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">HIGH priority gene landscape — hover for gene names</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            high_df,
            x="log2FoldChange", y="damage_score",
            hover_name="gene",
            color="direction",
            color_discrete_map={"UP": "#FF5B5B", "DOWN": "#4A9EFF"},
            opacity=0.75,
            labels={
                "log2FoldChange": "Log₂ Fold Change (Tumor / Normal)",
                "damage_score": "Damage Score (1–3)"
            }
        )
        fig_scatter.add_vline(
            x=0, line_dash="dot", line_color="#1E2A3A",
            annotation_text="No change", annotation_font_color="#7A8FA6",
            annotation_font_size=10
        )
        fig_scatter.add_hline(
            y=2, line_dash="dot", line_color="#1E2A3A",
            annotation_text="High damage", annotation_font_color="#7A8FA6",
            annotation_font_size=10
        )
        fig_scatter.update_traces(
            marker=dict(size=7, line=dict(width=0.5, color="#0B0F17"))
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,23,34,1)",
            font=dict(family="DM Sans", color="#7A8FA6"),
            xaxis=dict(
                tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"),
                gridcolor="rgba(30,42,58,0.7)", zerolinecolor="#1E2A3A"
            ),
            yaxis=dict(
                tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"),
                gridcolor="rgba(30,42,58,0.7)", zerolinecolor="#1E2A3A"
            ),
            legend=dict(
                font=dict(family="Space Mono", size=10, color="#7A8FA6"),
                bgcolor="rgba(11,15,23,0.8)",
                bordercolor="#1E2A3A", borderwidth=1
            ),
            height=480,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Top genes table
        st.markdown("""
        <div class="section-header">
          <span class="section-num">TABLE</span>
          <span class="section-title">Top 20 HIGH priority genes</span>
        </div>
        """, unsafe_allow_html=True)

        display_cols = [c for c in ["gene","gnomAD_SAS_AF","log2FoldChange","padj","direction","damage_score","Variant_Classification"]
                       if c in high_df.columns]
        top20 = high_df.sort_values("damage_score", ascending=False).head(20)[display_cols]
        st.dataframe(
            top20.style.format({
                "gnomAD_SAS_AF": "{:.4f}",
                "log2FoldChange": "{:.3f}",
                "padj": "{:.2e}"
            }),
            use_container_width=True
        )

        csv_download = high_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download HIGH Priority Genes CSV",
            data=csv_download,
            file_name="mutexpress_high_priority.csv",
            mime="text/csv"
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — PATHWAY ENRICHMENT
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="section-header">
      <span class="section-num">PHASE 5.2</span>
      <span class="section-title">Biological Pathway Validation</span>
    </div>
    <div class="info-box">
      GO and KEGG pathway enrichment analysis performed on <strong>1,702 HIGH priority genes</strong> 
      using clusterProfiler (R/Bioconductor). Non-circular validation — these databases were not used 
      anywhere in the filtering pipeline.
    </div>
    """, unsafe_allow_html=True)

    t_go, t_kegg = st.tabs(["Gene Ontology (GO)", "KEGG Pathways"])

    with t_go:
        go_img = rp("GO_dotplot.png")
        go_csv = rp("GO_enrichment.csv")
        if os.path.exists(go_img):
            st.markdown('<div class="chart-card"><div class="chart-title">GO Biological Process — top enriched terms</div>', unsafe_allow_html=True)
            st.image(go_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if os.path.exists(go_csv):
            go_df = pd.read_csv(go_csv)
            st.markdown('<div class="chart-card"><div class="chart-title">GO enrichment table</div>', unsafe_allow_html=True)
            show_cols = [c for c in ["Description","GeneRatio","BgRatio","p.adjust","Count"] if c in go_df.columns]
            st.dataframe(go_df[show_cols].head(20), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("GO enrichment files not found. Run pathway_enrichment.R to generate them.")

    with t_kegg:
        kegg_img = rp("KEGG_dotplot.png")
        kegg_csv = rp("KEGG_enrichment.csv")
        if os.path.exists(kegg_img):
            st.markdown('<div class="chart-card"><div class="chart-title">KEGG Pathways — top enriched disease pathways</div>', unsafe_allow_html=True)
            st.image(kegg_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if os.path.exists(kegg_csv):
            kegg_df = pd.read_csv(kegg_csv)
            st.markdown('<div class="chart-card"><div class="chart-title">KEGG enrichment table</div>', unsafe_allow_html=True)
            show_cols = [c for c in ["Description","GeneRatio","BgRatio","p.adjust","Count"] if c in kegg_df.columns]
            st.dataframe(kegg_df[show_cols].head(20), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("KEGG enrichment files not found. Run pathway_enrichment.R to generate them.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ABLATION VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div class="section-header">
      <span class="section-num">PHASE 5.1</span>
      <span class="section-title">Ablation Testing vs COSMIC CGC Gold Standard</span>
    </div>
    <div class="info-box">
      Benchmarked against <strong>20 known BRCA driver genes</strong> from the COSMIC Cancer Gene Census.
      Measures whether adding the second layer (RNA-Seq expression) improves precision over 
      using variants alone. Higher precision = less noise, more clinically actionable candidates.
    </div>
    """, unsafe_allow_html=True)

    if abl_df is not None:
        st.markdown('<div class="chart-card"><div class="chart-title">Ablation test results</div>', unsafe_allow_html=True)

        rows_html = ""
        for _, row in abl_df.iterrows():
            cond = str(row.get("Condition", ""))
            is_dual = "MutExpress" in cond or "Dual" in cond
            cls = "best" if is_dual else ""
            total_f = int(row.get("Total Genes Flagged", 0))
            cgc_f   = int(row.get("CGC Drivers Found", 0))
            recall  = float(row.get("Recall (%)", 0))
            prec    = float(row.get("Precision (%)", 0))

            if "VCF" in cond:
                pill = '<span class="pill pill-medv">VCF-ONLY</span>'
            elif "DEG" in cond:
                pill = '<span class="pill pill-mede">DEG-ONLY</span>'
            else:
                pill = '<span class="pill pill-dual">DUAL-LAYER</span>'

            rows_html += f"""
            <tr class="{cls}">
              <td>{pill}&nbsp; {cond}</td>
              <td style="font-family:Space Mono">{total_f:,}</td>
              <td style="font-family:Space Mono">{cgc_f}</td>
              <td style="font-family:Space Mono">{recall:.1f}%</td>
              <td style="font-family:Space Mono">{'<b>'+str(round(prec,2))+'%</b>' if is_dual else str(round(prec,2))+'%'}</td>
            </tr>"""

        st.markdown(f"""
        <table class="abl-table">
          <thead>
            <tr>
              <th>Condition</th>
              <th>Genes Flagged</th>
              <th>CGC Drivers Found</th>
              <th>Recall</th>
              <th>Precision</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Precision bar chart
        st.markdown('<div class="chart-card" style="margin-top:1rem"><div class="chart-title">Precision comparison — dual-layer vs single-layer</div>', unsafe_allow_html=True)
        if "Precision (%)" in abl_df.columns and "Condition" in abl_df.columns:
            colors = []
            for c in abl_df["Condition"]:
                if "Dual" in str(c) or "MutExpress" in str(c):
                    colors.append("#00D4C8")
                elif "VCF" in str(c):
                    colors.append("#F4793B")
                else:
                    colors.append("#4A9EFF")

            fig_abl = go.Figure(go.Bar(
                x=abl_df["Condition"],
                y=abl_df["Precision (%)"],
                marker_color=colors,
                text=[f"{v:.2f}%" for v in abl_df["Precision (%)"]],
                textposition="outside",
                textfont=dict(family="Space Mono", size=11, color="#E8EDF5")
            ))
            fig_abl.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,23,34,1)",
                font=dict(family="DM Sans", color="#7A8FA6"),
                xaxis=dict(tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"), gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(tickfont=dict(family="Space Mono", size=10, color="#7A8FA6"), gridcolor="rgba(30,42,58,0.6)", title="Precision (%)"),
                height=280, margin=dict(t=30, b=20)
            )
            st.plotly_chart(fig_abl, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-top:1rem">
      <strong>Interpretation:</strong> The dual-layer MutExpress-India filter achieves 
      <strong style="color:#00D4C8">4× higher precision</strong> than VCF-only analysis 
      by eliminating over 11,000 false-positive candidate genes, while maintaining 
      recovery of known BRCA driver genes. This demonstrates that requiring both 
      genomic and transcriptomic evidence substantially reduces noise.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — UPLOAD YOUR DATA
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div class="section-header">
      <span class="section-num">DYNAMIC MODE</span>
      <span class="section-title">Run the pipeline on your own data</span>
    </div>
    <div class="info-box">
      Upload your own <strong>annotated variant file</strong> (TSV with columns: gene, gnomAD_SAS_AF, damage_score) 
      and <strong>DESeq2 results CSV</strong> (columns: gene, log2FoldChange, padj, direction) 
      to run the MutExpress dual-layer integration on any dataset.
    </div>
    """, unsafe_allow_html=True)

    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("**Genomic Layer — Variant File (TSV)**")
        vcf_file = st.file_uploader("Upload priority_variants.tsv", type=["tsv", "csv"], key="vcf")
    with col_u2:
        st.markdown("**Transcriptomic Layer — DEG File (CSV)**")
        deg_file = st.file_uploader("Upload significant_degs.csv", type=["csv"], key="deg")

    if vcf_file and deg_file:
        with st.spinner("Running MutExpress dual-layer integration..."):
            try:
                sep = "\t" if vcf_file.name.endswith(".tsv") else ","
                u_variants = pd.read_csv(vcf_file, sep=sep, low_memory=False)
                u_degs     = pd.read_csv(deg_file)
                u_degs.columns = u_degs.columns.str.strip().str.strip('"').str.lower()
                if "gene" in u_degs.columns:
                    u_degs["gene"] = u_degs["gene"].astype(str).str.strip().str.strip('"')
                u_variants.columns = u_variants.columns.str.strip().str.strip('"')

                if "Hugo_Symbol" in u_variants.columns:
                    u_variants.rename(columns={"Hugo_Symbol": "gene"}, inplace=True)

                var_agg = u_variants.groupby("gene").agg({
                    "damage_score": "max",
                    "gnomAD_SAS_AF": "min"
                }).reset_index()

                # Normalize column names to lowercase for matching
                u_degs.columns = [c.lower() for c in u_degs.columns]
                if "gene" in u_degs.columns:
                    u_degs["gene"] = u_degs["gene"].astype(str).str.strip().str.strip('"')
                # Rename log2foldchange back to standard name
                col_map = {c: c for c in u_degs.columns}
                if "log2foldchange" in u_degs.columns:
                    u_degs = u_degs.rename(columns={"log2foldchange": "log2FoldChange"})
                if "hugo_symbol" in u_degs.columns:
                    u_degs = u_degs.rename(columns={"hugo_symbol": "gene"})
                deg_cols = [c for c in ["gene","log2FoldChange","padj","direction"] if c in u_degs.columns]
                merged = pd.merge(var_agg, u_degs[deg_cols], on="gene", how="outer")

                def assign_priority(row):
                    hv = pd.notna(row.get("damage_score"))
                    hd = pd.notna(row.get("log2FoldChange"))
                    if hv and hd: return "HIGH"
                    elif hv:      return "MEDIUM_V"
                    elif hd:      return "MEDIUM_E"
                    else:         return "LOW"

                merged["MutExpress_Priority"] = merged.apply(assign_priority, axis=1)
                order = {"HIGH":0,"MEDIUM_V":1,"MEDIUM_E":2,"LOW":3}
                merged["_s"] = merged["MutExpress_Priority"].map(order)
                merged = merged.sort_values(["_s","damage_score"], ascending=[True,False]).drop("_s", axis=1)

                st.success("Integration complete!")

                u_high  = len(merged[merged["MutExpress_Priority"]=="HIGH"])
                u_med_v = len(merged[merged["MutExpress_Priority"]=="MEDIUM_V"])
                u_med_e = len(merged[merged["MutExpress_Priority"]=="MEDIUM_E"])

                st.markdown(f"""
                <div class="metric-grid" style="grid-template-columns:repeat(3,1fr)">
                  <div class="metric-card high">
                    <div class="metric-label">HIGH Priority</div>
                    <div class="metric-value">{u_high:,}</div>
                  </div>
                  <div class="metric-card med_v">
                    <div class="metric-label">MEDIUM_V</div>
                    <div class="metric-value">{u_med_v:,}</div>
                  </div>
                  <div class="metric-card med_e">
                    <div class="metric-label">MEDIUM_E</div>
                    <div class="metric-value">{u_med_e:,}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Show pie chart for uploaded results
                import plotly.express as px
                up_counts = merged["MutExpress_Priority"].value_counts().reset_index()
                up_counts.columns = ["Priority", "Count"]
                color_map = {"HIGH":"#FF5B5B","MEDIUM_V":"#F4793B","MEDIUM_E":"#4A9EFF","LOW":"#1E2A3A"}
                fig_up = px.pie(up_counts, names="Priority", values="Count",
                               color="Priority", color_discrete_map=color_map, hole=0.55,
                               title="Your Results — Priority Distribution")
                fig_up.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans", color="#7A8FA6"),
                    legend=dict(font=dict(family="Space Mono", size=10, color="#7A8FA6"), bgcolor="rgba(0,0,0,0)"),
                    margin=dict(t=40,b=10,l=10,r=10), height=320
                )
                st.plotly_chart(fig_up, use_container_width=True)

                st.dataframe(merged.head(50), use_container_width=True)
                dl = merged.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download Full Results", data=dl,
                                   file_name="mutexpress_custom_results.csv", mime="text/csv")

            except Exception as e:
                st.error(f"Error: {e}. Check that your files have the required columns.")
    else:
        st.markdown("""
        <div style="background:var(--surface);border:1px dashed var(--border);border-radius:4px;
                    padding:3rem;text-align:center;margin-top:1rem">
          <div style="font-family:Space Mono;font-size:0.7rem;letter-spacing:0.15em;
                      text-transform:uppercase;color:var(--muted)">
            Upload both files above to run the pipeline
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:0.5rem 0;margin-top:0.5rem">
  <div style="font-family:Space Mono;font-size:0.62rem;letter-spacing:0.1em;color:#3B4A5A">
    MUTEXPRESS-INDIA · MSc BIOINFORMATICS · MAY 2026
  </div>
  <div style="font-family:Space Mono;font-size:0.62rem;color:#3B4A5A">
    TCGA-BRCA · GSE62944 · gnomAD SAS · COSMIC CGC
  </div>
</div>
""", unsafe_allow_html=True)