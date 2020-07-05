require(AnnotationHub)
hub <- AnnotationHub()
query(hub, "Ory")

rabbit <- hub[['AH72393']]

saveDb(rabbit, "rabbit-AH72393.sqlite")

database <- loadDb("/home/disk/pengying/data/foranno/rabbit.AH72393.sqlite")
args = commandArgs(T)
df <- read.table(args[1]); df <- as.character(df$V1)
edited <- mapIds(x=database, keys=df, keytype="SYMBOL", column="ENTREZID"); na.omit(edited)

editedBP <- enrichGO(gene = edited, OrgDb = database, ont = "BP", readable = TRUE)
editedBP_simp <- simplify(editedBP)

write.table(as.data.frame(editedBP_simp@result), file = args[2], quote = F, sep = "\t")

if(TRUE){
    kk <- enrichKEGG(gene = edited, organism = "ocu")
    df.tmp <- kk@result
    df.tmp <- df.tmp[which(df.tmp$p.adjust < 0.05),]
    write.table(as.data.frame(df.tmp), file = args[3], quote = F, sep = "\t")
}
