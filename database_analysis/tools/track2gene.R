#!/home/disk/pengying/R/bin/Rscript
setwd("cuffnorm_out")

library(dplyr)

anno <- read.csv('genes.attr_table', sep='\t', header=T)
matrix <- read.csv('genes.fpkm_table', sep='\t', header=T)
anno <- anno[,c("tracking_id","gene_short_name")]

exprSet <- merge(anno, matrix, by='tracking_id')
exprSet <- exprSet %>% dplyr::arrange(gene_short_name)
exprSet_symbol1 <- aggregate(x = exprSet[,3:ncol(exprSet)], by = list(exprSet$gene_short_name), FUN = mean)

write.table(exprSet_symbol1, file="genes.fpkm.symbol", quote=F, sep="\t", row.names =F)
