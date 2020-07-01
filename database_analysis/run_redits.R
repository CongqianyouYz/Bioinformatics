#!/home/disk/pengying/R/bin/Rscript
library(doParallel)
library(foreach)
source("/home/disk/pengying/scr/others/REDIT_regression.R")

#initiate a cluster
noCores = 10
cl = makeCluster(noCores,outfile="")
registerDoParallel(cl,cores=noCores)

#create some data for illustration
files = list.files(path='pool_sites', pattern='txt.sub2.3.ad$', full.names=T)
spe = read.table('spe.txt'); spe = as.character(spe[1,1])
for(f in files){
    
    tissue = strsplit(f, "\\.")[[1]][2]

    df <- read.table(f,sep='\t',header=T); df <- df[,-1]; G_reads <- as.matrix(df)
    df <- read.table(gsub('sub2.3.ad','sub2.3.dp',f),sep='\t',header=T); pos <- df[,1]; df <- df[,-1]; A_reads <- as.matrix(df)
    df1 <- read.table(paste('pool_sites/header', tissue, sep='.'), header=F, col.names=c("age")); the_covariates = df1 
    number_of_editing_sites_to_test = dim(G_reads)[1]

    #run the parallelization
    output_matrix = foreach(i=1:number_of_editing_sites_to_test,.combine='rbind') %dopar%{
      G_reads_of_editing_site = G_reads[i,]
      A_reads_of_editing_site = A_reads[i,]
      regression_info = REDIT_regression(data=rbind(G_reads_of_editing_site,A_reads_of_editing_site), covariates=the_covariates)
      return(as.matrix(data.frame(p_value_age=regression_info$age.p.value)))
    }   
    
    adjusted_p_values = p.adjust(output_matrix, method='bonferroni')
    res = data.frame(key=pos, pval.dev_stage=adjusted_p_values)
    write.table(res, file=paste('pool_sites/redits', tissue, sep='.'), sep="\t", quote=F, row.names=F)
    
    res.sig = res[res$pval.dev_stage < 0.05,]
    write.table(res.sig, file=paste('pool_sites/redits', tissue, 'sig', sep='.'), sep="\t", quote=F, row.names=F)
}

stopCluster(cl) #to stop using the cluster you created
