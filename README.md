<div align="center">

# 🧬 MutExpress-India
**A novel Indian-population-aware dual-layer variant-expression prioritization pipeline for Breast Cancer.**

[![Python](https://img.shields.io/badge/Python-3.10-008080?style=for-the-badge&logo=python&logoColor=white)](#)
[![R](https://img.shields.io/badge/R-4.5.2-0055A4?style=for-the-badge&logo=r&logoColor=white)](#)
[![Bash](https://img.shields.io/badge/Terminal-Bash-008080?style=for-the-badge&logo=gnu-bash&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-0055A4?style=for-the-badge)](#)

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#%EF%B8%8F-project-status">Project Status</a> •
  <a href="#-installation">Installation</a>
</p>

</div>

---

## 🔬 Overview
MutExpress-India addresses a documented gap in South Asian precision medicine genomics. Existing tools often systematically misclassify variants that are rare in South Asian populations but common in European cohorts. 

This pipeline integrates two independent lines of computational evidence to prioritize disease-relevant genes in Breast Cancer (BRCA):
1. **Genomic Layer:** Population-aware variant analysis using TCGA Masked Somatic Mutation data, filtered against South Asian (SAS) allele frequencies via gnomAD v3.1.2.
2. **Transcriptomic Layer:** Differential gene expression analysis (RNA-Seq) using the DESeq2 negative binomial model on curated TCGA read counts.

## 🏗️ Architecture
The pipeline assigns a priority tier to every gene based on dual-layer evidence. A gene with BOTH a rare damaging variant in the Indian/South Asian population AND significant differential expression in tumor tissue represents the strongest computational case for disease involvement.

| Priority Tier | Criteria | Interpretation |
| :--- | :--- | :--- |
| 🔴 **HIGH** | Rare damaging variant (SAS AF < 1%) + Significant DEG | Both layers agree (Strongest Evidence) |
| 🟠 **MEDIUM_V** | Rare damaging variant only | Genetic evidence only |
| 🔵 **MEDIUM_E** | Significant DEG only | Transcriptomic evidence only |
| ⚪ **LOW** | Neither criterion met | Baseline / No evidence |

---

## 🏗️ Project Status

### Phase 0: Prerequisites & Environment Setup (✅ COMPLETE)
* **Environment:** Fully containerized Conda environment (`mutexpress`, Python 3.10).
* **Tooling:** All core bioinformatics tools (`bcftools`, `samtools`, `hisat2`, `tabix`) verified.

### Phase 1: VCF Layer & Variant Annotation (✅ COMPLETE)
* **Data Acquisition:** 504 open-access Masked Somatic Mutation MAF files downloaded (TCGA-BRCA).
* **Annotation & Filtering:** Successfully merged MAF files (47,844 variants). Ran `filter_variants.py` to produce `priority_variants.tsv` (36,106 priority variants identified).
* **Validation:** Confirmed key driver genes (BRCA1, BRCA2, TP53, PIK3CA, ERBB2) in high-priority output.

### Phase 2: RNA-Seq Layer (✅ COMPLETE)
* **Data Pre-processing:** Filtered 751MB multi-cancer RNA-Seq dataset (GSE62944) down to 1,119 BRCA tumor samples and 113 normal samples.
* **Differential Expression:** Executed DESeq2 negative binomial modeling in R. Successfully identified **3,306 significantly dysregulated genes** (padj < 0.05, |log2FC| > 1.5). Generated publication-ready volcano plot visualizations.

### Phase 3: Dual-Layer Integration (✅ COMPLETE)
* **Data Integration:** Engineered an outer-join integration script merging Phase 1 genomic data with Phase 2 transcriptomic data.
* **Results:** Filtered over 47,000 initial variants down to exactly **1,702 HIGH Priority targets** exhibiting both rare, damaging Indian-population mutations and significant expression dysregulation.

### Phase 4: Visualization & Web Dashboard (✅ COMPLETE)
* **Interactive Visualization:** Generated dynamic Plotly distributions (pie charts, dual-axis scatter plots).
* **UI Development:** Built and deployed a functional Streamlit web dashboard (`app.py`) to serve as a proof-of-concept user interface for the pipeline.

### Phase 5: Validation & Benchmarking (🚧 PARTIALLY COMPLETE)
* ✅ **Part 1 (Ablation Testing):** Benchmarked the dual-layer approach against single-layer models using a core set of 20 COSMIC Cancer Gene Census (CGC) drivers. Mathematically validated that the MutExpress dual-layer filter achieves superior precision (0.24%) by eliminating over 11,000 false positives present in variant-only approaches.
* ⏳ **Part 2 (Pathway Enrichment):** *Pending execution of GO/KEGG biological pathway enrichment analysis in R.*

---

## ⚙️ Installation
To reproduce the computational environment on macOS/Unix:

```bash
# 1. Clone the repository
git clone [https://github.com/Shibasis-Rath/mutexpress-india.git](https://github.com/Shibasis-Rath/mutexpress-india.git)
cd mutexpress-india

# 2. Create the conda environment
conda create -n mutexpress python=3.10 -y
conda activate mutexpress

# 3. Install core bioinformatics tools
conda install -c bioconda -c conda-forge hisat2 samtools subread fastqc trimmomatic bcftools tabix -y

# 4. Install Python dependencies
pip install pandas numpy matplotlib seaborn plotly streamlit biopython scipy openpyxl

# 5. Install R and Bioconductor packages
conda install -c conda-forge r-base r-ggplot2 r-pheatmap -y
R -e 'install.packages("BiocManager", repos="[https://cran.r-project.org](https://cran.r-project.org)"); BiocManager::install(c("DESeq2", "EnhancedVolcano", "clusterProfiler", "org.Hs.eg.db", "AnnotationDbi"), ask=FALSE)'
