import pandas as pd

print("Loading metadata...")
tumor_meta = pd.read_csv("../data/rnaseq/cancer_type.txt", sep="\t", header=None, names=["Sample", "CancerType"])
normal_meta = pd.read_csv("../data/rnaseq/normal_cancer_type.txt", sep="\t", header=None, names=["Sample", "CancerType"])

brca_tumors = tumor_meta[tumor_meta["CancerType"] == "BRCA"]["Sample"].tolist()
brca_normals = normal_meta[normal_meta["CancerType"] == "BRCA"]["Sample"].tolist()
print(f"Found {len(brca_tumors)} tumor and {len(brca_normals)} normal BRCA samples.")

print("Loading count matrices (this will take 1-2 minutes, it's a huge file!)...")
tumor_counts = pd.read_csv("../data/rnaseq/tumor_counts.txt", sep="\t")
normal_counts = pd.read_csv("../data/rnaseq/normal_counts.txt", sep="\t")

gene_col_t = tumor_counts.columns[0]
gene_col_n = normal_counts.columns[0]

# Keep only the columns that actually exist in the data
valid_tumors = [s for s in brca_tumors if s in tumor_counts.columns]
valid_normals = [s for s in brca_normals if s in normal_counts.columns]

brca_t_df = tumor_counts[[gene_col_t] + valid_tumors]
brca_n_df = normal_counts[[gene_col_n] + valid_normals]

print("Merging tumor and normal counts into one matrix...")
brca_combined = pd.merge(brca_t_df, brca_n_df, left_on=gene_col_t, right_on=gene_col_n)
brca_combined.rename(columns={gene_col_t: "GeneID"}, inplace=True)

# Save the final matrix
brca_combined.to_csv("../data/rnaseq/GSE62944_BRCA_counts.txt", sep="\t", index=False)
print("Saved clean count matrix: GSE62944_BRCA_counts.txt")

print("Generating clinical metadata file...")
clin_t = pd.DataFrame({"SampleID": valid_tumors, "CancerType": "BRCA", "SampleType": "Tumor"})
clin_n = pd.DataFrame({"SampleID": valid_normals, "CancerType": "BRCA", "SampleType": "Normal"})
clinical = pd.concat([clin_t, clin_n])

clinical.to_csv("../data/rnaseq/GSE62944_clinical.txt", sep="\t", index=False)
print("Saved metadata: GSE62944_clinical.txt")
print("Data pre-processing complete! Ready for R and DESeq2.")
