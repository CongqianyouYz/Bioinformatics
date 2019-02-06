library(RcisTarget)

# Load gene sets to analyze. e.g.:
geneList1 <- read.table(file.path(system.file('examples', package='RcisTarget'), "hypoxiaGeneSet.txt"), stringsAsFactors=FALSE)[,1]
geneLists <- list(geneListName=geneList1)

# Select motif database to use (i.e. organism and distance around TSS)
data(motifAnnotations_hgnc)
motifRankings <- importRankings("hg19-500bp-upstream-7species.mc9nr.feather")

# Motif enrichment analysis:
motifEnrichmentTable_wGenes <- cisTarget(geneLists, motifRankings, motifAnnot=motifAnnotations_hgnc)

# Advanced use
# 1. Calculate AUC
motifs_AUC <- calcAUC(geneLists, motifRankings)

# 2. Select significant motifs, add TF annotation & format as table
motifEnrichmentTable <- addMotifAnnotation(motifs_AUC, motifAnnot=motifAnnotations_hgnc)

# 3. Identify significant genes for each motif
# (i.e. genes from the gene set in the top of the ranking)
# Note: Method 'iCisTarget' instead of 'aprox' is more accurate, but slower
motifEnrichmentTable_wGenes <- addSignificantGenes(motifEnrichmentTable, 
                                                   geneSets=geneLists,
                                                   rankings=motifRankings, 
                                                   nCores=1,
                                                   method="aprox")
                                                   
## cannot get "Required databases"!
