library(clusterProfiler)
library(org.Hs.eg.db)

args = commandArgs(T)
df <- read.table(args[1]); colnames(df) <- c("gene")	# dont_edit_spe.hg38.txt
edited <- bitr(df$gene, fromType = "SYMBOL", toType=c("ENTREZID"), OrgDb="org.Hs.eg.db")

editedBP <- enrichGO(gene = edited$ENTREZID, OrgDb = org.Hs.eg.db, ont = "BP", readable = TRUE)
editedBP_simp <- simplify(editedBP)

write.table(as.data.frame(editedBP_simp@result), file = args[2], quote = F, sep = "\t")
