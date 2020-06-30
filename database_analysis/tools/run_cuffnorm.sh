# cufflinks - cuffmerge - cuffquant - cuffnorm

cuffnorm -o cuffnorm_out -p 36 \
--library-type fr-firststrand -q --no-update-check \
-L ERR2576379,ERR2576380,ERR2576381 \
merged_asm/merged.gtf \
ERR2576379.tophat/cuffquant/abundances.cxb \
ERR2576380.tophat/cuffquant/abundances.cxb \
ERR2576381.tophat/cuffquant/abundances.cxb
