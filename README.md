<div align="center">

# 🧬 MutExpress-India
**A novel Indian-population-aware dual-layer variant-expression prioritization pipeline for Breast Cancer.**

[![Python](https://img.shields.io/badge/Python-3.10-008080?style=for-the-badge&logo=python&logoColor=white)](#)
[![R](https://img.shields.io/badge/R-DESeq2-0055A4?style=for-the-badge&logo=r&logoColor=white)](#)
[![Bash](https://img.shields.io/badge/Terminal-Bash-008080?style=for-the-badge&logo=gnu-bash&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-0055A4?style=for-the-badge)](#)

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#%EF%B8%8F-installation">Installation</a> •
  <a href="#-usage">Usage</a>
</p>

</div>

---

## 🔬 Overview
MutExpress-India addresses a documented gap in South Asian precision medicine. Existing genomic tools systematically misclassify variants that are rare in South Asian populations but common in European cohorts. 

This pipeline integrates two independent lines of computational evidence to prioritize disease-relevant genes in Breast Cancer (BRCA):
1. **Genomic Layer:** Population-aware variant analysis using TCGA MAF data filtered against South Asian (SAS) allele frequencies via gnomAD.
2. **Transcriptomic Layer:** Differential gene expression analysis (RNA-Seq) using the DESeq2 negative binomial model.

## 🏗️ Architecture
The pipeline assigns a priority tier to every gene based on dual-layer evidence:

| Priority Tier | Criteria | Interpretation |
| :--- | :--- | :--- |
| 🔴 **HIGH** | Rare damaging variant (SAS AF < 1%) + Significant DEG | Both layers agree - strongest evidence |
| 🟠 **MEDIUM_V** | Rare damaging variant only | Genetic evidence, no expression change |
| 🔵 **MEDIUM_E** | Significant DEG only | Expression change, no somatic mutation |
| ⚪ **LOW** | Neither criterion met | No evidence in this analysis |

## ⚙️ Installation
*Instructions for setting up the Conda environment and downloading the ANNOVAR databases will be added upon pipeline completion.*

## 🚀 Usage
*Code execution commands and Streamlit web app instructions will be documented here.*

---
<div align="center">
  <i>~ SHIBASIS RATH</i>
</div>
