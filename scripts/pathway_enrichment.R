# Load required Bioconductor packages
suppressPackageStartupMessages({
    library(clusterProfiler)
    library(org.Hs.eg.db)
    library(ggplot2)
})

cat("Loading MutExpress-India integrated results...\n")
df <- read.csv("../results/mutexpress_india_output.csv")

# Extract only the HIGH priority genes
high_genes <- df$gene[df$MutExpress_Priority == "HIGH"]
cat(paste("Found", length(high_genes), "HIGH priority genes for enrichment analysis.\n"))

cat("Converting HGNC Symbols to Entrez IDs...\n")
entrez_ids <- mapIds(org.Hs.eg.db, 
                     keys=as.character(high_genes), 
                     column="ENTREZID", 
                     keytype="SYMBOL", 
                     multiVals="first")

# Drop any genes that couldn't be mapped
entrez_ids <- na.omit(entrez_ids)

# ---------------------------------------------------------
# 1. Gene Ontology (GO) - Biological Process Enrichment
# ---------------------------------------------------------
cat("Running Gene Ontology (GO) Biological Process Enrichment...\n")
go_results <- enrichGO(gene          = entrez_ids,
                       OrgDb         = org.Hs.eg.db,
                       ont           = "BP",
                       pAdjustMethod = "BH",
                       pvalueCutoff  = 0.05,
                       qvalueCutoff  = 0.05,
                       readable      = TRUE)

if (!is.null(go_results) && nrow(go_results) > 0) {
    write.csv(as.data.frame(go_results), "../results/GO_enrichment.csv", row.names=FALSE)
    
    # Generate publication-ready Dot Plot
    png("../results/GO_dotplot.png", width=1200, height=900, res=150)
    p1 <- dotplot(go_results, showCategory=15, title="GO Enrichment: Top 15 Biological Processes")
    print(p1)
    dev.off()
    cat("Saved GO results to results/GO_enrichment.csv and results/GO_dotplot.png\n")
} else {
    cat("No significant GO terms found.\n")
}

# ---------------------------------------------------------
# 2. KEGG Pathway Enrichment
# ---------------------------------------------------------
cat("Running KEGG Pathway Enrichment...\n")
kegg_results <- enrichKEGG(gene          = entrez_ids,
                           organism      = "hsa",
                           pAdjustMethod = "BH",
                           pvalueCutoff  = 0.05)

if (!is.null(kegg_results) && nrow(kegg_results) > 0) {
    write.csv(as.data.frame(kegg_results), "../results/KEGG_enrichment.csv", row.names=FALSE)
    
    # Generate publication-ready Dot Plot
    png("../results/KEGG_dotplot.png", width=1200, height=900, res=150)
    p2 <- dotplot(kegg_results, showCategory=15, title="KEGG Enrichment: Top 15 Disease Pathways")
    print(p2)
    dev.off()
    cat("Saved KEGG results to results/KEGG_enrichment.csv and results/KEGG_dotplot.png\n")
} else {
    cat("No significant KEGG pathways found.\n")
}

cat("\nPhase 5 (Part 2) Complete! Pathway Enrichment Finished.\n")
