import pandas as pd

print("Loading MutExpress-India integrated results...")
df = pd.read_csv("../results/mutexpress_india_output.csv")

# COSMIC Cancer Gene Census (CGC) - Breast Cancer Drivers (Core Set)
cgc_brca_genes = {"BRCA1", "BRCA2", "TP53", "PIK3CA", "ERBB2", "PTEN", "ATM", "CDH1", "CHEK2", "PALB2", "BARD1", "BRIP1", "RAD51C", "RAD51D", "AKT1", "GATA3", "MAP3K1", "KMT2C", "SF3B1", "CBFB"}

print(f"Benchmarking against {len(cgc_brca_genes)} known COSMIC BRCA drivers...")

# Define the conditions based on priority tiers
vcf_only = set(df[df["MutExpress_Priority"].isin(["HIGH", "MEDIUM_V"])]["gene"])
deg_only = set(df[df["MutExpress_Priority"].isin(["HIGH", "MEDIUM_E"])]["gene"])
dual_layer = set(df[df["MutExpress_Priority"] == "HIGH"]["gene"])

# Define metrics calculations
def calculate_metrics(test_set, gold_standard):
    overlap = test_set.intersection(gold_standard)
    recall = (len(overlap) / len(gold_standard)) * 100 if gold_standard else 0
    precision = (len(overlap) / len(test_set)) * 100 if test_set else 0
    return len(test_set), len(overlap), recall, precision

# Calculate metrics for each condition
v_total, v_overlap, v_rec, v_prec = calculate_metrics(vcf_only, cgc_brca_genes)
e_total, e_overlap, e_rec, e_prec = calculate_metrics(deg_only, cgc_brca_genes)
d_total, d_overlap, d_rec, d_prec = calculate_metrics(dual_layer, cgc_brca_genes)

summary = pd.DataFrame({
    "Condition": ["VCF-Only (Variants)", "DEG-Only (Expression)", "Dual-Layer (MutExpress)"],
    "Total Genes Flagged": [v_total, e_total, d_total],
    "CGC Drivers Found": [v_overlap, e_overlap, d_overlap],
    "Recall (%)": [round(v_rec, 2), round(e_rec, 2), round(d_rec, 2)],
    "Precision (%)": [round(v_prec, 2), round(e_prec, 2), round(d_prec, 2)]
})

print("\n=== ABLATION TESTING RESULTS ===")
print(summary.to_string(index=False))

summary.to_csv("../results/ablation_summary.csv", index=False)
print("\nSaved mathematically corrected ablation validation to results/ablation_summary.csv")
