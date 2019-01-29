com_data <- read.table('combine.txt', sep = '\t', header = TRUE)
com_data1 <- com_data[c('Feature.ID', 'NES.for.results1', 'NES.for.results2')]
com_data1['diff'] <- abs(com_data1$NES.for.results1 - com_data1$NES.for.results2)
com_data1 <- com_data1[order(com_data1[,4], decreasing=T),]

this_data <- cbind(com_data1$NES.for.results1, com_data1$NES.for.results2)
colnames(this_data) <- c('wt', 'kd')
rownames(this_data) <- com_data1$Feature.ID
pheatmap(this_data[1:35,], cluster_row = T, cluster_col = FALSE,
         cellwidth = 20, cellheight= 10, border_color = 'grey',
         main = "Motif Enrichment",
         cex.main=1.2)
