import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="MutExpress Converter", page_icon="🔄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{--bg:#0B0F17;--surface:#111722;--border:#1E2A3A;--teal:#00D4C8;--orange:#F4793B;--blue:#4A9EFF;--red:#FF5B5B;--text:#E8EDF5;--muted:#7A8FA6;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--bg)!important;color:var(--text)!important;}
.stApp{background-color:var(--bg)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:2rem!important;max-width:1200px!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:1.4rem;margin-bottom:1rem;}
.card-title{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin-bottom:0.8rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border);}
.info-box{background:rgba(0,212,200,0.06);border:1px solid rgba(0,212,200,0.2);border-left:3px solid var(--teal);border-radius:4px;padding:0.9rem 1.1rem;font-size:0.83rem;color:var(--muted);line-height:1.6;margin:0.8rem 0;}
.success-box{background:rgba(61,220,132,0.06);border:1px solid rgba(61,220,132,0.2);border-left:3px solid #3DDC84;border-radius:4px;padding:0.9rem 1.1rem;font-size:0.83rem;color:var(--muted);line-height:1.6;margin:0.8rem 0;}
.stTabs [data-baseweb="tab-list"]{background:var(--surface)!important;border-bottom:1px solid var(--border)!important;}
.stTabs [data-baseweb="tab"]{font-family:'Space Mono',monospace!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;color:var(--muted)!important;background:transparent!important;border:none!important;padding:0.6rem 1.2rem!important;}
.stTabs [aria-selected="true"]{color:var(--orange)!important;border-bottom:2px solid var(--orange)!important;}
.stTabs [data-baseweb="tab-panel"]{background:var(--surface)!important;border:1px solid var(--border)!important;border-top:none!important;padding:1.2rem!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0d1f2e,#081420);border:1px solid #1E2A3A;border-top:3px solid #F4793B;border-radius:4px;padding:2rem 2.5rem;margin-bottom:2rem">
  <div style="font-family:Space Mono,monospace;font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#F4793B;border:1px solid rgba(244,121,59,0.35);padding:3px 10px;border-radius:2px;display:inline-block;margin-bottom:0.8rem">Universal Data Converter</div>
  <h1 style="font-family:Space Mono,monospace;font-size:1.8rem;font-weight:700;margin:0 0 0.3rem 0">MutExpress <span style="color:#F4793B">Converter</span></h1>
  <p style="color:#7A8FA6;font-size:0.9rem;margin:0">Convert ANY cancer genomics format to MutExpress-India input files automatically. Supports cBioPortal, GDC, TCGA, custom CSV/TSV/TXT/XLSX.</p>
</div>
""", unsafe_allow_html=True)

GENE_COLS    = ["hugo_symbol","gene","gene_symbol","symbol","gene_name","hgnc_symbol","genename","gene_id"]
SAS_AF_COLS  = ["gnomad_sas_af","gnomad_genome_sas","sas_af","gnomad_af_sas","af_sas","south_asian_af","sas","gnomad_non_cancer_sas_af","1000g_sas_af"]
SIFT_COLS    = ["sift","sift_pred","sift_score"]
POLYPHEN_COLS= ["polyphen","polyphen2_hdiv_pred","polyphen2","pp2","polyphen_pred"]
CADD_COLS    = ["cadd_phred","cadd_score","cadd"]
IMPACT_COLS  = ["impact","vep_impact","functional_impact"]
VCLASS_COLS  = ["variant_classification","variantclassification","variant_class","mutation_type","consequence","one_consequence"]
LFC_COLS     = ["log2foldchange","log2fc","logfc","log2_fold_change","lfc","foldchange","fold_change","l2fc"]
PADJ_COLS    = ["padj","adj.p.val","adjusted_pvalue","fdr","p_adjusted","adj_pval","p.adj","bh","q.value","qvalue"]
PVAL_COLS    = ["pvalue","p.value","pval","p_value","p","prob"]

def find_col(df_cols, candidates):
    lower_cols = {c.lower().replace(" ","_").replace(".","_").replace("-","_"): c for c in df_cols}
    for cand in candidates:
        if cand in lower_cols:
            return lower_cols[cand]
    return None

def compute_damage_score(row, s_c, p_c, ca_c, i_c):
    score = 0
    if s_c:
        val = str(row.get(s_c,"")).lower()
        if "deleterious" in val and "tolerated" not in val: score += 1
    if p_c:
        val = str(row.get(p_c,"")).lower()
        if "probably_damaging" in val or "possibly_damaging" in val or val in ["d","p"]: score += 1
    if ca_c:
        try:
            if float(row.get(ca_c,0)) >= 20: score += 1
        except: pass
    if i_c:
        val = str(row.get(i_c,"")).upper()
        if val in ["HIGH","MODERATE"]: score += 1
    return min(score,3) if score > 0 else 1

def read_any_file(uploaded_file):
    name = uploaded_file.name.lower()
    try:
        if name.endswith((".xlsx",".xls")):
            return pd.read_excel(uploaded_file), "Excel"
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        if name.endswith(".vcf"):
            lines = [l for l in content.split("\n") if not l.startswith("##")]
            return pd.read_csv(io.StringIO("\n".join(lines)), sep="\t", low_memory=False), "VCF"
        if name.endswith(".maf"):
            lines = [l for l in content.split("\n") if not l.startswith("#")]
            return pd.read_csv(io.StringIO("\n".join(lines)), sep="\t", low_memory=False), "MAF"
        first = content.split("\n")[0]
        sep = "\t" if first.count("\t") > first.count(",") else ","
        return pd.read_csv(io.StringIO(content), sep=sep, low_memory=False), "TSV" if sep=="\t" else "CSV"
    except Exception as e:
        return None, str(e)

tab1, tab2, tab3 = st.tabs(["01 · Convert Variant File","02 · Convert Expression File","03 · Sample Files & Guide"])

with tab1:
    st.markdown('<div class="info-box"><strong>Upload any variant/mutation file</strong> — MAF, VCF, cBioPortal, GDC, custom CSV/TSV/XLSX/TXT.<br>Auto-detects columns and produces <strong>priority_variants.tsv</strong> for MutExpress.</div>', unsafe_allow_html=True)
    var_file = st.file_uploader("Upload variant/mutation file", type=["csv","tsv","txt","maf","vcf","xlsx","xls"], key="vf")
    if var_file:
        df_raw, fmt = read_any_file(var_file)
        if df_raw is None:
            st.error(f"Could not read: {fmt}")
        else:
            st.markdown(f'<div class="success-box">✅ Read as <strong>{fmt}</strong> — {len(df_raw):,} rows × {len(df_raw.columns)} columns</div>', unsafe_allow_html=True)
            df_raw.columns = df_raw.columns.str.strip().str.strip('"')
            with st.expander("View all columns"): st.write(list(df_raw.columns))
            gene_c = find_col(df_raw.columns, GENE_COLS)
            sas_c  = find_col(df_raw.columns, SAS_AF_COLS)
            sift_c = find_col(df_raw.columns, SIFT_COLS)
            pp2_c  = find_col(df_raw.columns, POLYPHEN_COLS)
            cadd_c = find_col(df_raw.columns, CADD_COLS)
            imp_c  = find_col(df_raw.columns, IMPACT_COLS)
            vc_c   = find_col(df_raw.columns, VCLASS_COLS)
            st.markdown('<div class="card"><div class="card-title">Column mapping — auto-detected (adjust if needed)</div>', unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            with c1:
                gene_s = st.selectbox("Gene column", [gene_c]+[c for c in df_raw.columns if c!=gene_c] if gene_c else list(df_raw.columns), key="gs")
            with c2:
                sas_opts = ["NOT FOUND (use default 0.0)"]+list(df_raw.columns)
                sas_def = sas_opts.index(sas_c) if sas_c and sas_c in sas_opts else 0
                sas_s = st.selectbox("gnomAD SAS AF column", sas_opts, index=sas_def, key="ss")
            with c3:
                vc_opts = ["NOT FOUND"]+list(df_raw.columns)
                vc_def = vc_opts.index(vc_c) if vc_c and vc_c in vc_opts else 0
                vc_s = st.selectbox("Variant classification", vc_opts, index=vc_def, key="vs")
            c4,c5,c6 = st.columns(3)
            with c4:
                s_opts = ["NOT FOUND"]+list(df_raw.columns)
                s_def = s_opts.index(sift_c) if sift_c and sift_c in s_opts else 0
                sift_s = st.selectbox("SIFT column", s_opts, index=s_def, key="sfs")
            with c5:
                p_opts = ["NOT FOUND"]+list(df_raw.columns)
                p_def = p_opts.index(pp2_c) if pp2_c and pp2_c in p_opts else 0
                pp2_s = st.selectbox("PolyPhen column", p_opts, index=p_def, key="pps")
            with c6:
                ca_opts = ["NOT FOUND"]+list(df_raw.columns)
                ca_def = ca_opts.index(cadd_c) if cadd_c and cadd_c in ca_opts else 0
                cadd_s = st.selectbox("CADD score column", ca_opts, index=ca_def, key="cas")
            st.markdown('</div>', unsafe_allow_html=True)
            sas_default = st.slider("Default SAS AF when missing", 0.0, 0.05, 0.0, 0.001, format="%.3f")
            if vc_s != "NOT FOUND":
                unique_vc = df_raw[vc_s].dropna().unique().tolist()
                keep_default = ["Missense_Mutation","Nonsense_Mutation","Splice_Site","Frame_Shift_Del","Frame_Shift_Ins","In_Frame_Del","In_Frame_Ins","Nonstop_Mutation","missense_variant","stop_gained","splice_acceptor_variant","splice_donor_variant","frameshift_variant"]
                sel_vc = st.multiselect("Keep only these variant types (empty = keep all)", unique_vc, default=[c for c in unique_vc if any(k.lower() in c.lower() for k in keep_default)])
            else:
                sel_vc = []
            if st.button("🔄 Convert to priority_variants.tsv"):
                with st.spinner("Converting..."):
                    try:
                        dw = df_raw.copy()
                        dw.rename(columns={gene_s:"Hugo_Symbol"}, inplace=True)
                        dw["Hugo_Symbol"] = dw["Hugo_Symbol"].astype(str).str.split(";").str[0].str.strip()
                        dw = dw[~dw["Hugo_Symbol"].isin(["","nan","Unknown","unknown","."])]
                        if sel_vc and vc_s != "NOT FOUND": dw = dw[dw[vc_s].isin(sel_vc)]
                        if sas_s != "NOT FOUND (use default 0.0)":
                            dw["gnomAD_SAS_AF"] = pd.to_numeric(dw[sas_s], errors="coerce").fillna(sas_default)
                        else:
                            dw["gnomAD_SAS_AF"] = sas_default
                        s_c2  = sift_s  if sift_s  != "NOT FOUND" else None
                        p_c2  = pp2_s   if pp2_s   != "NOT FOUND" else None
                        ca_c2 = cadd_s  if cadd_s  != "NOT FOUND" else None
                        i_c2  = imp_c   if imp_c and imp_c in dw.columns else None
                        dw["damage_score"] = dw.apply(lambda r: compute_damage_score(r,s_c2,p_c2,ca_c2,i_c2), axis=1)
                        dw["Variant_Classification"] = dw[vc_s] if vc_s != "NOT FOUND" and vc_s in dw.columns else "Missense_Mutation"
                        out = dw[["Hugo_Symbol","gnomAD_SAS_AF","damage_score","Variant_Classification"]].copy()
                        st.markdown(f'<div class="success-box">✅ <strong>{len(out):,} variants</strong> from <strong>{out["Hugo_Symbol"].nunique():,} genes</strong> converted!</div>', unsafe_allow_html=True)
                        st.dataframe(out.head(20), use_container_width=True)
                        m1,m2,m3 = st.columns(3)
                        m1.metric("Total variants", f"{len(out):,}")
                        m2.metric("Unique genes", f"{out['Hugo_Symbol'].nunique():,}")
                        m3.metric("Rare SAS (AF<1%)", f"{(out['gnomAD_SAS_AF']<0.01).sum():,}")
                        st.download_button("⬇ Download priority_variants.tsv", out.to_csv(sep="\t",index=False).encode(), "priority_variants.tsv", "text/tab-separated-values")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        import traceback; st.code(traceback.format_exc())

with tab2:
    st.markdown('<div class="info-box"><strong>Upload any differential expression file</strong> — DESeq2, edgeR, limma, GEO, cBioPortal, any CSV/TSV/XLSX.<br>Auto-detects columns and produces <strong>significant_degs.csv</strong> for MutExpress. Ensembl IDs auto-converted to HGNC.</div>', unsafe_allow_html=True)
    exp_file = st.file_uploader("Upload expression/DEG results file", type=["csv","tsv","txt","xlsx","xls"], key="ef")
    if exp_file:
        df_exp, fmt2 = read_any_file(exp_file)
        if df_exp is None:
            st.error(f"Could not read: {fmt2}")
        else:
            st.markdown(f'<div class="success-box">✅ Read as <strong>{fmt2}</strong> — {len(df_exp):,} rows × {len(df_exp.columns)} columns</div>', unsafe_allow_html=True)
            df_exp.columns = df_exp.columns.str.strip().str.strip('"')
            with st.expander("View all columns"): st.write(list(df_exp.columns))
            gene_c2 = find_col(df_exp.columns, GENE_COLS)
            lfc_c   = find_col(df_exp.columns, LFC_COLS)
            padj_c  = find_col(df_exp.columns, PADJ_COLS)
            pval_c  = find_col(df_exp.columns, PVAL_COLS)
            st.markdown('<div class="card"><div class="card-title">Column mapping</div>', unsafe_allow_html=True)
            e1,e2,e3 = st.columns(3)
            with e1:
                gene_s2 = st.selectbox("Gene column", [gene_c2]+[c for c in df_exp.columns if c!=gene_c2] if gene_c2 else list(df_exp.columns), key="gs2")
            with e2:
                lfc_opts = [lfc_c]+[c for c in df_exp.columns if c!=lfc_c] if lfc_c else list(df_exp.columns)
                lfc_s = st.selectbox("Log2 Fold Change column", lfc_opts, key="ls")
            with e3:
                padj_opts = ["Use p-value"]+([padj_c]+[c for c in df_exp.columns if c!=padj_c] if padj_c else list(df_exp.columns))
                padj_def = 1 if padj_c else 0
                padj_s = st.selectbox("Adjusted p-value column", padj_opts, index=padj_def, key="ps")
            if padj_s == "Use p-value":
                pval_s = st.selectbox("P-value column", [pval_c]+[c for c in df_exp.columns if c!=pval_c] if pval_c else list(df_exp.columns), key="pvs")
                real_padj = pval_s
            else:
                real_padj = padj_s
            st.markdown('</div>', unsafe_allow_html=True)
            t1,t2 = st.columns(2)
            with t1: pt = st.slider("Adjusted p-value threshold", 0.001, 0.1, 0.05, 0.001)
            with t2: lt = st.slider("|Log2FC| threshold", 0.0, 3.0, 1.0, 0.1)
            gene_type = st.radio("Gene ID format", ["HGNC Symbol (BRCA1)","Ensembl ID (ENSG...)","Entrez ID","Other"], key="gt")
            if st.button("🔄 Convert to significant_degs.csv"):
                with st.spinner("Converting..."):
                    try:
                        de = df_exp.copy()
                        if gene_s2 in de.columns:
                            de.rename(columns={gene_s2:"gene"}, inplace=True)
                        else:
                            de["gene"] = de.index.astype(str)
                        de["gene"] = de["gene"].astype(str).str.strip().str.strip('"')
                        if "Ensembl" in gene_type and de["gene"].str.startswith("ENSG").any():
                            try:
                                import requests
                                genes = de["gene"].dropna().unique().tolist()[:2000]
                                resp = requests.post("https://mygene.info/v3/gene", json={"ids":genes,"fields":"symbol"}, timeout=30)
                                if resp.status_code == 200:
                                    mapping = {r["query"]:r.get("symbol",r["query"]) for r in resp.json() if "query" in r}
                                    de["gene"] = de["gene"].map(mapping).fillna(de["gene"])
                                    st.success(f"Converted {len(mapping)} Ensembl IDs")
                            except Exception as eg:
                                st.warning(f"API conversion failed: {eg}")
                        de["log2FoldChange"] = pd.to_numeric(de[lfc_s], errors="coerce")
                        de["padj"] = pd.to_numeric(de[real_padj], errors="coerce")
                        de["direction"] = de["log2FoldChange"].apply(lambda x: "UP" if x>0 else "DOWN")
                        sig = de[de["padj"].notna()&(de["padj"]<pt)&de["log2FoldChange"].notna()&(de["log2FoldChange"].abs()>=lt)&(~de["gene"].isin(["","nan","NA","N/A","."]))].copy()
                        out_e = sig[["gene","log2FoldChange","padj","direction"]].copy()
                        st.markdown(f'<div class="success-box">✅ <strong>{len(out_e):,} significant DEGs</strong> from {len(de):,} total genes</div>', unsafe_allow_html=True)
                        st.dataframe(out_e.head(20), use_container_width=True)
                        m1,m2,m3 = st.columns(3)
                        m1.metric("Significant DEGs", f"{len(out_e):,}")
                        m2.metric("Upregulated", f"{(out_e['direction']=='UP').sum():,}")
                        m3.metric("Downregulated", f"{(out_e['direction']=='DOWN').sum():,}")
                        st.download_button("⬇ Download significant_degs.csv", out_e.to_csv(index=False).encode(), "significant_degs.csv", "text/csv")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        import traceback; st.code(traceback.format_exc())

with tab3:
    st.markdown('<div style="font-family:Space Mono;font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#7A8FA6;border-bottom:1px solid #1E2A3A;padding-bottom:0.5rem;margin-bottom:1rem">Download sample files to test MutExpress upload instantly</div>', unsafe_allow_html=True)
    sv = pd.DataFrame({"Hugo_Symbol":["TP53","BRCA1","BRCA2","PIK3CA","ERBB2","PTEN","KRAS","NRAS","BRAF","CDH1"],"gnomAD_SAS_AF":[0.0001,0.0003,0.0005,0.0012,0.0008,0.0002,0.0004,0.0006,0.0009,0.0001],"damage_score":[3,3,3,2,2,3,2,2,2,3],"Variant_Classification":["Missense_Mutation","Nonsense_Mutation","Frame_Shift_Del","Missense_Mutation","Missense_Mutation","Nonsense_Mutation","Missense_Mutation","Missense_Mutation","Missense_Mutation","Splice_Site"]})
    sd = pd.DataFrame({"gene":["TP53","BRCA1","BRCA2","PIK3CA","ERBB2","PTEN","MYC","CCND1","CDH1","EGFR"],"log2FoldChange":[-2.45,3.12,-1.89,2.34,3.56,-2.78,4.12,2.89,-3.45,2.67],"padj":[0.00001,0.000001,0.00034,0.0012,0.000003,0.00089,0.0000001,0.0023,0.000045,0.0034],"direction":["DOWN","UP","DOWN","UP","UP","DOWN","UP","UP","DOWN","UP"]})
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Sample priority_variants.tsv</div>', unsafe_allow_html=True)
        st.dataframe(sv, use_container_width=True)
        st.markdown('<div class="info-box"><strong>Required columns:</strong> Hugo_Symbol · gnomAD_SAS_AF · damage_score · Variant_Classification</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download sample_priority_variants.tsv", sv.to_csv(sep="\t",index=False).encode(), "sample_priority_variants.tsv", "text/tab-separated-values")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Sample significant_degs.csv</div>', unsafe_allow_html=True)
        st.dataframe(sd, use_container_width=True)
        st.markdown('<div class="info-box"><strong>Required columns:</strong> gene · log2FoldChange · padj · direction</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download sample_significant_degs.csv", sd.to_csv(index=False).encode(), "sample_significant_degs.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)
    p1,p2,p3 = st.columns(3)
    with p1: st.markdown('<div class="card"><div class="card-title" style="color:#F4793B">cBioPortal</div><p style="font-size:0.82rem;color:#7A8FA6;line-height:1.7">1. cbioportal.org<br>2. Select cancer study<br>3. Download → Mutations<br>4. Upload to Tab 1<br><strong>Gene:</strong> Hugo_Symbol<br><strong>SAS:</strong> not present → set 0</p></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="card"><div class="card-title" style="color:#00D4C8">GDC / TCGA</div><p style="font-size:0.82rem;color:#7A8FA6;line-height:1.7">1. portal.gdc.cancer.gov<br>2. Masked Somatic MAF<br>3. Download with gdc-client<br>4. Upload .maf to Tab 1<br><strong>Gene:</strong> Hugo_Symbol ✓<br><strong>SAS:</strong> gnomAD_SAS_AF ✓</p></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="card"><div class="card-title" style="color:#4A9EFF">GEO / DESeq2</div><p style="font-size:0.82rem;color:#7A8FA6;line-height:1.7">1. Download GEO supplementary<br>2. Any DESeq2/edgeR output<br>3. Upload to Tab 2<br>4. Ensembl IDs auto-converted<br><strong>Needs:</strong> gene + LFC + pvalue</p></div>', unsafe_allow_html=True)
