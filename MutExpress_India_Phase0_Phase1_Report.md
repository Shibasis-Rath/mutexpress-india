# MutExpress-India — Phase 0 & Phase 1 Analysis Report

**Project:** MutExpress-India — Indian-Population-Aware Variant + Expression Prioritization Pipeline  
**Author:** Shibasis Rath  
**Degree:** MSc Bioinformatics  
**Date:** May 2026  
**System:** MacBook Air M5, 16GB RAM, 512GB Storage, macOS  

---

## Table of Contents

1. Project Overview
2. Phase 0 — Environment Setup
3. Phase 1 — VCF Layer: Variant Annotation & Indian-Aware Filtering
4. Results Summary
5. Key Findings
6. Files Generated
7. Next Steps

---

## 1. Project Overview

MutExpress-India is a dual-layer bioinformatics pipeline that prioritizes disease-relevant genes by integrating:

- **Layer 1 (VCF):** Population-aware somatic variant analysis using TCGA-BRCA MAF files filtered against Indian/South Asian allele frequencies (gnomAD SAS)
- **Layer 2 (RNA-Seq):** Differential gene expression analysis using DESeq2 on GSE62944

Genes showing both a **rare damaging mutation in the South Asian population context AND significant expression dysregulation** are flagged as HIGH priority candidates.

**Disease Model:** Breast Cancer (BRCA) — TCGA-BRCA dataset  
**Key Innovation:** Indian/South Asian population-aware filtering using gnomAD_SAS_AF < 0.01 threshold

---

## 2. Phase 0 — Environment Setup

### 2.1 System Requirements Met

| Component | Specification |
|---|---|
| Machine | MacBook Air M5 (Apple Silicon) |
| RAM | 16 GB |
| Storage | 512 GB |
| OS | macOS (Unix-based — no Linux/WSL2 needed) |

### 2.2 Installation Steps

#### Step 1 — Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, add to PATH:

```bash
echo >> /Users/shibasisrath/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> /Users/shibasisrath/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
```

Verify:
```bash
brew --version
# Result: Homebrew 5.1.12
```

#### Step 2 — Install Miniconda

```bash
brew install --cask miniconda
conda init zsh
# Close and reopen Terminal
conda --version
```

Accept Terms of Service (one-time):
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

#### Step 3 — Create Project Environment

```bash
conda create -n mutexpress python=3.10 -y
conda activate mutexpress
# Prompt shows: (mutexpress) shibasisrath@MacBook-Air
```

**Why Python 3.10:** All bioinformatics libraries have stable pre-built wheels for 3.10. Python 3.13 (default in base) causes compilation failures for some packages on Apple Silicon.

#### Step 4 — Install Bioinformatics Tools

```bash
conda install -c bioconda -c conda-forge \
  hisat2 samtools subread \
  fastqc trimmomatic bcftools tabix -y
```

**Tools installed and their roles:**

| Tool | Version | Purpose in Project |
|---|---|---|
| bcftools | 1.23.1 | VCF filtering and manipulation (Phase 1) |
| samtools | 1.23.1 | BAM/SAM file handling (Phase 2) |
| hisat2 | 2.2.2 | RNA-Seq alignment to human genome (Phase 2) |
| tabix | 1.23.1 | VCF indexing for fast lookup (Phase 1) |
| fastqc | 0.12.1 | Quality control on FASTQ files (Phase 2) |
| trimmomatic | 0.40 | Adapter removal (Phase 2) |
| subread/featureCounts | 2.1.1 | Read counting for DESeq2 (Phase 2) |

#### Step 5 — Install Python Libraries

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit biopython scipy openpyxl
```

Verify:
```bash
python -c "import pandas,numpy,matplotlib,seaborn,plotly,streamlit,scipy; print('ALL OK')"
# Result: Python libs OK
```

#### Step 6 — Install R and Bioconductor Packages

```bash
conda install -c conda-forge r-base r-ggplot2 r-pheatmap -y
conda install -c conda-forge r-locfit -y
conda install -c conda-forge r-deseq2 -y
conda install -c conda-forge -c bioconda \
  bioconductor-ggtree bioconductor-enrichplot \
  bioconductor-clusterprofiler bioconductor-enhancedvolcano \
  bioconductor-org.hs.eg.db bioconductor-annotationdbi -y
```

**R packages installed:**

| Package | Source | Purpose |
|---|---|---|
| DESeq2 | Bioconductor | Differential expression analysis (Phase 2) |
| clusterProfiler | Bioconductor | GO/KEGG pathway enrichment (Phase 5) |
| org.Hs.eg.db | Bioconductor | Human gene ID mapping Ensembl to HGNC (Phase 3) |
| AnnotationDbi | Bioconductor | Gene annotation queries (Phase 3) |
| EnhancedVolcano | Bioconductor | Publication-quality volcano plots (Phase 2) |
| ggplot2 | CRAN | General plotting (Phase 4) |
| pheatmap | CRAN | Gene expression heatmaps (Phase 4) |

Verify:
```bash
R -e "library(DESeq2);library(clusterProfiler);library(org.Hs.eg.db);cat('ALL R PACKAGES OK\n')" --quiet
# Result: ALL R PACKAGES OK
```

#### Step 7 — Git Setup

```bash
git config --global user.name "Shibasis Rath"
git config --global user.email "your@email.com"
# GitHub Desktop installed for visual repository management
git --version
# Result: git version 2.50.1 (Apple Git-155)
```

#### Step 8 — Project Folder Structure

```bash
mkdir -p ~/mutexpress-india/data
mkdir -p ~/mutexpress-india/results
mkdir -p ~/mutexpress-india/scripts
mkdir -p ~/mutexpress-india/reference
mkdir -p ~/mutexpress-india/annovar
```

Final structure:
```
mutexpress-india/
├── data/           ← TCGA MAF files, GSE62944 counts
├── reference/      ← hg38 genome, GTF annotation
├── results/        ← all output files
├── scripts/        ← Python and R scripts
├── annovar/        ← ANNOVAR tool and databases
├── README.md       ← auto-created by GitHub Desktop
└── LICENSE         ← auto-created by GitHub Desktop
```

#### Step 9 — Save Environment

```bash
conda list > ~/mutexpress-india/mutexpress_environment.txt
git add .
git commit -m "Phase 0 complete - all tools verified"
git push origin main
```

### 2.3 Phase 0 Final Verification

```bash
conda activate mutexpress && \
echo "=== TOOLS ===" && \
bcftools --version | head -1 && \
samtools --version | head -1 && \
hisat2 --version 2>&1 | head -1 && \
echo "=== PYTHON ===" && \
python --version && \
python -c "import pandas,numpy,matplotlib,seaborn,plotly,streamlit,scipy; print('Python libs OK')" && \
echo "=== R ===" && \
R -e "library(DESeq2);library(clusterProfiler);cat('R OK\n')" --quiet && \
echo "=== GIT ===" && \
git --version && \
echo "=== PROJECT FOLDER ===" && \
ls ~/mutexpress-india && \
echo "=== ALL GOOD ==="
```

**Result:**
```
=== TOOLS ===
bcftools 1.23.1
samtools 1.23.1
hisat2-align-s version 2.2.2
=== PYTHON ===
Python 3.10.20
Python libs OK
=== R ===
R packages OK
=== GIT ===
git version 2.50.1 (Apple Git-155)
=== PROJECT FOLDER ===
data  results  scripts  reference  README.md  LICENSE
=== ALL GOOD ===
```

**Phase 0 Status: COMPLETE ✓**

---

## 3. Phase 1 — VCF Layer: Variant Annotation & Indian-Aware Filtering

### 3.1 Overview

Phase 1 builds a Python pipeline that:
1. Downloads TCGA-BRCA somatic mutation MAF files
2. Merges all patient files into one combined dataset
3. Filters for variants rare in the Indian/South Asian population
4. Scores variants by predicted pathogenicity
5. Outputs a ranked priority variant list

**Key discovery:** The TCGA-BRCA Masked Somatic MAF files already contain gnomAD South Asian allele frequencies (`gnomAD_SAS_AF` column), eliminating the need for ANNOVAR re-annotation for the SAS filtering step.

### 3.2 Install GDC Data Transfer Tool

The GDC portal requires a command-line tool for bulk downloads. Version 1.6.1 links are dead; version 2.3 is current.

```bash
# Download from: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool
# Select: MAC OSX x64 (Silicon Processor)
cd ~/Downloads
unzip gdc-client_2.3_OSX_x64-py3.8-macos-14.zip
unzip gdc-client_2.3_OSX_x64.zip
sudo mv gdc-client /usr/local/bin/
sudo xattr -d com.apple.quarantine /usr/local/bin/gdc-client

gdc-client --version
# Result: 2.3
```

### 3.3 Download TCGA-BRCA MAF Files

Instead of using the GDC portal browser (which had filter issues), the GDC API was queried directly:

#### Query GDC API for file list

```bash
cd ~/mutexpress-india/data
mkdir -p tcga_maf
cd tcga_maf

curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"filters":{"op":"and","content":[
    {"op":"in","content":{"field":"cases.project.project_id","value":["TCGA-BRCA"]}},
    {"op":"in","content":{"field":"files.data_type","value":["Masked Somatic Mutation"]}},
    {"op":"in","content":{"field":"files.access","value":["open"]}}
  ]},"format":"TSV","fields":"file_id,file_name,cases.submitter_id,access","size":"500"}' \
  "https://api.gdc.cancer.gov/files" \
  -o gdc_manifest.txt
```

**Result:** 501 lines (500 files + header), all showing `open` access with `.maf.gz` format.

#### Build manifest and download

```bash
# Extract file IDs
tail -n +2 gdc_manifest.txt | cut -f3 > file_ids.txt
wc -l file_ids.txt
# Result: 500 file_ids.txt

# Build proper manifest format for gdc-client
echo -e "id\tfilename\tmd5\tsize\tstate" > proper_manifest.txt
tail -n +2 gdc_manifest.txt | awk -F'\t' '{print $3"\t"$4"\t.\t.\tdownloaded"}' >> proper_manifest.txt

# Download all 500 MAF files
gdc-client download -m proper_manifest.txt -d ./
```

**Result:** 504 folders downloaded (500 MAF files + manifest files)

```bash
ls ~/mutexpress-india/data/tcga_maf | wc -l
# Result: 504
```

### 3.4 Verify MAF File Contents

```bash
gunzip -c ./e10420ac-.../0d50d383-...wxs.aliquot_ensemble_masked.maf.gz | grep "^Hugo" | head -1
```

**Key columns confirmed present:**
- `Hugo_Symbol` — gene name
- `Variant_Classification` — mutation type
- `HGVSp_Short` — protein change
- `gnomAD_SAS_AF` — South Asian allele frequency (THE key filter)
- `SIFT` — functional prediction
- `PolyPhen` — functional prediction
- `IMPACT` — VEP impact score

**Important finding:** `gnomAD_SAS_AF` is already present in the TCGA MAF files — ANNOVAR annotation is not needed for the Indian-aware filtering step.

### 3.5 Merge All MAF Files

```bash
cd ~/mutexpress-india/data/tcga_maf

# Extract header
gunzip -c $(find . -name "*.maf.gz" | head -1) | grep "^Hugo" > ../combined_brca.maf

# Add all data rows
find . -name "*.maf.gz" | while read f; do
    gunzip -c "$f" | grep -v "^#" | grep -v "^Hugo"
done >> ../combined_brca.maf

echo "Done merging"
wc -l ../combined_brca.maf
```

**Result:**
```
Done merging
47845 ../combined_brca.maf
```

Verify merged file:
```bash
head -2 ~/mutexpress-india/data/combined_brca.maf | cut -f1-10
```

**Output:**
```
Hugo_Symbol   Entrez_Gene_Id  Center  NCBI_Build  Chromosome  Start_Position  End_Position  Strand  Variant_Classification  Variant_Type
ACAP3         116983          WUGSC   GRCh38      chr1        1300640         1300640       +       Missense_Mutation       SNP
```

### 3.6 Indian-Aware Filtering Script

**Script:** `~/mutexpress-india/scripts/filter_variants.py`

```python
import pandas as pd
import numpy as np

print("Loading MAF file...")
df = pd.read_csv(
    "../data/combined_brca.maf",
    sep="\t",
    low_memory=False,
    comment="#"
)
print(f"Total variants loaded: {len(df)}")

# Convert SAS allele frequency to numeric
df["gnomAD_SAS_AF"] = pd.to_numeric(
    df["gnomAD_SAS_AF"], errors="coerce").fillna(0)
df["SIFT"] = df["SIFT"].fillna("")
df["PolyPhen"] = df["PolyPhen"].fillna("")
df["IMPACT"] = df["IMPACT"].fillna("")

# FILTER 1: Rare in South Asian population (< 1%)
# Standard rare variant definition — Karczewski et al. 2020, Nature (gnomAD)
rare_sas = df["gnomAD_SAS_AF"] < 0.01

# FILTER 2: Only functional variants (affect protein)
functional = df["Variant_Classification"].isin([
    "Missense_Mutation", "Nonsense_Mutation", "Splice_Site",
    "Frame_Shift_Del", "Frame_Shift_Ins",
    "In_Frame_Del", "In_Frame_Ins", "Nonstop_Mutation"
])

# FILTER 3: Predicted damaging (OR logic — increases sensitivity)
sift_dam = df["SIFT"].str.startswith("deleterious")
pp2_dam = (df["PolyPhen"].str.startswith("probably_damaging") |
           df["PolyPhen"].str.startswith("possibly_damaging"))
high_impact = df["IMPACT"].isin(["HIGH", "MODERATE"])
any_damaging = sift_dam | pp2_dam | high_impact

# Apply all filters
priority = df[rare_sas & functional & any_damaging].copy()
print(f"Priority variants after filtering: {len(priority)}")

# Damage score (0-3, higher = more tools agree it's damaging)
priority["damage_score"] = (
    sift_dam[priority.index].astype(int) +
    pp2_dam[priority.index].astype(int) +
    high_impact[priority.index].astype(int)
)
priority = priority.sort_values("damage_score", ascending=False)

# Save priority variants
cols = [
    "Hugo_Symbol", "Chromosome", "Start_Position", "End_Position",
    "Variant_Classification", "Variant_Type",
    "Reference_Allele", "Tumor_Seq_Allele2",
    "HGVSp_Short", "Tumor_Sample_Barcode",
    "gnomAD_SAS_AF", "SIFT", "PolyPhen", "IMPACT", "damage_score"
]
priority[cols].to_csv(
    "../results/priority_variants.tsv",
    sep="\t", index=False
)

print("Saved: results/priority_variants.tsv")
print("\nTop 10 priority genes:")
print(priority["Hugo_Symbol"].value_counts().head(10))

key_genes = ["BRCA1", "BRCA2", "TP53", "PIK3CA", "ERBB2"]
found = [g for g in key_genes if g in priority["Hugo_Symbol"].values]
print(f"\nKey cancer genes found: {found}")
```

**Run command:**
```bash
cd ~/mutexpress-india/scripts
python filter_variants.py
```

---

## 4. Results Summary

### 4.1 Filtering Statistics

| Stage | Count |
|---|---|
| Total MAF files downloaded | 500 (504 folders) |
| Total variants before filtering | 47,844 |
| Priority variants after all filters | 36,106 |
| Filtered out (common in SAS / non-damaging) | 11,738 |

### 4.2 Filter Logic Explained

| Filter | Criteria | Scientific Rationale |
|---|---|---|
| Indian-aware | gnomAD_SAS_AF < 0.01 | Standard rare variant definition (MAF < 1%). Karczewski et al. 2020, Nature |
| Functional | Missense, Nonsense, Splice Site, Frameshift, Indel | Intronic variants rarely affect protein function |
| Pathogenicity | SIFT=deleterious OR PolyPhen=damaging OR IMPACT=HIGH/MODERATE | OR logic increases sensitivity; damage_score quantifies concordance |

### 4.3 Top 10 Priority Genes

```
Hugo_Symbol   Count
PIK3CA        175
TP53          169
TTN           163
MUC16          73
GATA3          70
CDH1           62
MAP3K1         55
KMT2C          53
DST            42
RYR2           36
```

### 4.4 Key Cancer Gene Validation

```
Key cancer genes found: ['BRCA1', 'BRCA2', 'TP53', 'PIK3CA', 'ERBB2']
```

All 5 major BRCA-relevant cancer genes were recovered in the priority variant list, confirming the pipeline is functioning correctly.

---

## 5. Key Findings

**Finding 1 — Indian-aware filtering works:**
The gnomAD_SAS_AF column was already present in the TCGA Masked Somatic MAF files, allowing direct Indian/South Asian population-aware filtering without requiring ANNOVAR re-annotation.

**Finding 2 — Known drivers recovered:**
PIK3CA (175 variants) and TP53 (169 variants) are the top mutated genes — consistent with published TCGA-BRCA literature. BRCA1, BRCA2, and ERBB2 also confirmed present.

**Finding 3 — Pipeline is scalable:**
500 patient MAF files were processed in under 5 minutes on the M5 MacBook Air, demonstrating feasibility for the full dataset.

---

## 6. Files Generated

| File | Location | Description |
|---|---|---|
| combined_brca.maf | data/combined_brca.maf | Merged MAF: 47,844 variants from 500 BRCA patients |
| priority_variants.tsv | results/priority_variants.tsv | 36,106 Indian-aware priority variants |
| filter_variants.py | scripts/filter_variants.py | Python filtering script |
| gdc_manifest.txt | data/tcga_maf/gdc_manifest.txt | GDC file manifest |
| mutexpress_environment.txt | mutexpress_environment.txt | Conda environment snapshot |

---

## 7. Next Steps — Phase 2

Phase 2 downloads and processes the GSE62944 RNA-Seq dataset for DESeq2 differential expression analysis.

**Immediate tasks:**
1. Download GSE62944 TCGA-BRCA RNA-Seq count matrix from NCBI GEO
2. Filter for BRCA tumor vs normal samples
3. Run DESeq2 differential expression analysis
4. Convert Ensembl IDs to HGNC gene symbols
5. Generate volcano plot
6. Output: `significant_degs.csv` + `volcano_plot.png`

**Command to start Phase 2:**
```bash
cd ~/mutexpress-india/data
mkdir -p rnaseq
cd rnaseq
wget "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62944/suppl/GSE62944_06_01_15_TCGA_24_548_Clinical_Variables_9264_Samples.txt.gz" -O clinical.txt.gz
```

---

## Appendix — Daily Workflow Commands

```bash
# Start every session with:
conda activate mutexpress
cd ~/mutexpress-india

# Run Python script:
python scripts/scriptname.py

# Run R script:
Rscript scripts/scriptname.R

# Save to GitHub:
git add .
git commit -m "description of what you did"
git push origin main

# Check disk space:
df -h ~

# Check what's installed:
conda list | grep -E "hisat2|samtools|bcftools"
pip list | grep -E "pandas|numpy|streamlit"
```

---

*Report generated: May 2026 | MutExpress-India Phase 0 + Phase 1*
