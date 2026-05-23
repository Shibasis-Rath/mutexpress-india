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
  <a href="#-installation">Installation</a> •
  <a href="#-data-acquisition">Data</a>
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
The computational environment is fully containerized via Conda for Apple Silicon (ARM64) architecture.
* **Conda Environment:** `mutexpress` (Python 3.10)
* **Bioinformatics Suite:** `bcftools` (1.23.1), `samtools` (1.23.1), `hisat2` (2.2.2), `tabix` (1.23.1)
* **Python Stack:** `pandas`, `numpy`, `scipy`, `biopython`, `plotly`, `streamlit`
* **R Stack (v4.5.2):** `DESeq2`, `clusterProfiler`, `org.Hs.eg.db`, `EnhancedVolcano`

### Phase 1: VCF Layer & Variant Annotation (⏳ IN PROGRESS)
* ✅ **GDC Client:** Installed `gdc-client` v2.3.0.
* ✅ **Data Acquisition:** Successfully bulk-downloaded 500 open-access Masked Somatic Mutation MAF files for the TCGA-BRCA cohort.
* ⏳ **Annotation:** ANNOVAR registration and 15GB gnomAD database download pending.
* ⏳ **Filtering:** Custom Python filtering script (SAS AF < 1% + CADD > 20) pending.

### Future Phases
* ⏳ **Phase 2:** RNA-Seq Layer (DESeq2 on GSE62944)
* ⏳ **Phase 3:** Dual-Layer Integration
* ⏳ **Phase 4:** Visualization & Streamlit Web App
* ⏳ **Phase 5:** Validation (Ablation testing vs COSMIC Cancer Gene Census)

---

## ⚙️ Installation
To reproduce the computational environment on macOS/Unix:

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/mutexpress-india.git](https://github.com/yourusername/mutexpress-india.git)
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
