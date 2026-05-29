import pandas as pd
import numpy as np

print("Loading Phase 1 (Variants) and Phase 2 (Expression) results...")
variants = pd.read_csv("../results/priority_variants.tsv", sep="\t", low_memory=False)
degs = pd.read_csv("../results/significant_degs.csv")

# Standardize the gene name column so they match perfectly
variants.rename(columns={"Hugo_Symbol": "gene"}, inplace=True)

print("Aggregating variant data per gene...")
# If a gene has multiple mutations, we take the worst-case damage score and lowest allele frequency
var_agg = variants.groupby("gene").agg({
    "damage_score": "max",
    "gnomAD_SAS_AF": "min",
    "Variant_Classification": lambda x: ", ".join(x.unique())
}).reset_index()

print("Merging layers (Outer Join)...")
# Outer join is critical so we don't lose genes that only have variants or only have expression changes
merged = pd.merge(var_agg, degs[["gene", "log2FoldChange", "padj", "direction"]], on="gene", how="outer")

print("Assigning MutExpress Priority Tiers...")
def assign_priority(row):
    has_variant = pd.notna(row.get("damage_score"))
    has_deg = pd.notna(row.get("log2FoldChange"))
    
    if has_variant and has_deg: return "HIGH"
    elif has_variant: return "MEDIUM_V"
    elif has_deg: return "MEDIUM_E"
    else: return "LOW"

merged["MutExpress_Priority"] = merged.apply(assign_priority, axis=1)

# Sort: HIGH first, then by damage score descending
order = {"HIGH": 0, "MEDIUM_V": 1, "MEDIUM_E": 2, "LOW": 3}
merged["_s"] = merged["MutExpress_Priority"].map(order)
merged = merged.sort_values(["_s", "damage_score"], ascending=[True, False]).drop("_s", axis=1)

# Save the final masterpiece
merged.to_csv("../results/mutexpress_india_output.csv", index=False)

print("\n=== FINAL INTEGRATION RESULTS ===")
print(merged["MutExpress_Priority"].value_counts())

print("\n=== TOP 10 HIGH PRIORITY GENES ===")
high_genes = merged[merged["MutExpress_Priority"] == "HIGH"].head(10)
print(high_genes[["gene", "gnomAD_SAS_AF", "log2FoldChange", "direction"]])

print("\nPhase 3 Complete! Saved to results/mutexpress_india_output.csv")
