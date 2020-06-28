cuffnorm -o cuffnorm_out -p 35 \
--library-type fr-firststrand -q --no-update-check \
-L ERR2596796,ERR2596797
merged_asm/merged.gtf \
ERR2596796.tophat/cuffquant/abundances.cxb \
ERR2596797.tophat/cuffquant/abundances.cxb
