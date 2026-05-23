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

df["gnomAD_SAS_AF"] = pd.to_numeric(
    df["gnomAD_SAS_AF"], errors="coerce").fillna(0)
df["SIFT"] = df["SIFT"].fillna("")
df["PolyPhen"] = df["PolyPhen"].fillna("")
df["IMPACT"] = df["IMPACT"].fillna("")

rare_sas = df["gnomAD_SAS_AF"] < 0.01
functional = df["Variant_Classification"].isin([
    "Missense_Mutation", "Nonsense_Mutation", "Splice_Site",
    "Frame_Shift_Del", "Frame_Shift_Ins",
    "In_Frame_Del", "In_Frame_Ins", "Nonstop_Mutation"
])
sift_dam = df["SIFT"].str.startswith("deleterious")
pp2_dam = (df["PolyPhen"].str.startswith("probably_damaging") |
           df["PolyPhen"].str.startswith("possibly_damaging"))
high_impact = df["IMPACT"].isin(["HIGH", "MODERATE"])
any_damaging = sift_dam | pp2_dam | high_impact

priority = df[rare_sas & functional & any_damaging].copy()
print(f"Priority variants after filtering: {len(priority)}")

priority["damage_score"] = (
    sift_dam[priority.index].astype(int) +
    pp2_dam[priority.index].astype(int) +
    high_impact[priority.index].astype(int)
)
priority = priority.sort_values("damage_score", ascending=False)

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
