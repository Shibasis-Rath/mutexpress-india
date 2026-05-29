suppressPackageStartupMessages(library(DESeq2))
suppressPackageStartupMessages(library(EnhancedVolcano))
suppressPackageStartupMessages(library(org.Hs.eg.db))

cat("Loading count matrix and clinical data...\n")
counts_raw <- read.table("../data/rnaseq/GSE62944_BRCA_counts.txt", header=TRUE, row.names=1, sep="\t", check.names=FALSE)
clinical <- read.table("../data/rnaseq/GSE62944_clinical.txt", header=TRUE, sep="\t", row.names=1, check.names=FALSE)

# Ensure integer counts (DESeq2 requires this)
counts <- round(as.matrix(counts_raw))

# Align columns to clinical rows
common_samples <- intersect(colnames(counts), rownames(clinical))
counts <- counts[, common_samples]
clinical_matched <- clinical[common_samples, , drop=FALSE]

# Define tumor/normal conditions
condition <- factor(ifelse(clinical_matched$SampleType == "Tumor", "tumor", "normal"))
cat("Tumor samples:", sum(condition=="tumor"), "| Normal samples:", sum(condition=="normal"), "\n")

# Remove low-count genes to speed up processing
counts <- counts[rowSums(counts) > 10, ]

cat("Building DESeq2 dataset...\n")
coldata <- data.frame(condition=condition, row.names=colnames(counts))
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)

cat("Running DESeq2 (This will take 5-10 minutes. Grab a coffee!)...\n")
dds <- DESeq(dds)

# Extract results
res <- results(dds, contrast=c("condition", "tumor", "normal"), alpha=0.05)
res_df <- as.data.frame(res)

cat("Converting Gene IDs to HGNC Symbols...\n")
keys <- gsub("\\..*", "", rownames(res_df))

# Auto-detect ID type (Ensembl vs Entrez vs already Symbol)
if(any(grepl("^ENSG", keys))) {
    key_type <- "ENSEMBL"
} else if(any(grepl("^[0-9]+$", keys))) {
    key_type <- "ENTREZID"
} else {
    key_type <- "SYMBOL"
}

if(key_type != "SYMBOL") {
    res_df$gene <- mapIds(org.Hs.eg.db, keys=keys, column="SYMBOL", keytype=key_type, multiVals="first")
} else {
    res_df$gene <- keys
}

# Drop genes that couldn't be mapped
res_df <- res_df[!is.na(res_df$gene), ]

cat("Filtering significant DEGs...\n")
sig_degs <- res_df[!is.na(res_df$padj) & res_df$padj < 0.05 & abs(res_df$log2FoldChange) > 1.5, ]
sig_degs$direction <- ifelse(sig_degs$log2FoldChange > 0, "UP", "DOWN")

cat("Total significant DEGs:", nrow(sig_degs), "\n")
write.csv(sig_degs, "../results/significant_degs.csv", row.names=FALSE)
cat("Saved DEGs to results/significant_degs.csv\n")

cat("Generating Volcano Plot...\n")
# Make unique rownames for the plot
rownames(res_df) <- make.unique(as.character(res_df$gene))

png("../results/volcano_plot.png", width=1200, height=900, res=150)
p <- EnhancedVolcano(res_df,
                lab=rownames(res_df),
                x="log2FoldChange",
                y="pvalue",
                title="BRCA Tumor vs Normal (GSE62944 | DESeq2)",
                pCutoff=0.05,
                FCcutoff=1.5,
                selectLab=c("BRCA1", "BRCA2", "TP53", "PIK3CA", "ERBB2"),
                drawConnectors=TRUE)
print(p)
dev.off()

cat("Saved Volcano Plot to results/volcano_plot.png\n")
cat("Phase 2 Complete!\n")
