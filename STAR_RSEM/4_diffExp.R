library(DESeq)

## get dataframe
myfile <- Sys.glob("*.genes.results")
mydata <- c()
mysrr <- c()

for (file in myfile) {
  curdata <- read.table(file, header = TRUE)$expected_count
  mydata <- cbind(mydata, curdata)
  srr <- substr(file, 1, 9)
  mysrr <- c(mysrr, srr)
}
colnames(mydata) <- mysrr
rownames(mydata) <- read.table(file, header = TRUE)$gene_id

## create CountDataSet
type <- factor(c(rep("wt",2), rep("kd",2)))
database <- round(as.matrix(mydata))
cds <- newCountDataSet(database, type)

## calling differential expression
# ***** 1. Standard comparison between two experimental conditions *****
cds <- estimateSizeFactors(cds)
cds <- estimateDispersions(cds)
res <- nbinomTest(cds, "wt", "kd")

# ***** 2. Working partially without replicates *****
cds <- estimateSizeFactors(cds)
cds <- estimateDispersions(cds)
res <- nbinomTest(cds, "wt", "kd")

# ***** 3. Working without any replicates *****
cds <- estimateSizeFactors(cds)
cds <- estimateDispersions(cds, method="blind", fitType = "local", sharingMode="fit-only")
res <- nbinomTest(cds, "wt", "kd")

## summary and output
res <- res[order(res$padj),]
sum(res$padj <= 0.01, na.rm=TRUE)
write.csv(res, file="U87MG_wt_vs_kd_DESeq.csv")
