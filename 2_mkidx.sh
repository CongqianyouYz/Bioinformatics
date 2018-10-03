perl get_iso.pl

time STAR \
--runThreadN 35 \
--runMode genomeGenerate \
--genomeDir /local/pengying/data/anno/STAR \
--genomeFastaFiles /local/pengying/data/anno/hg38.fa \
--sjdbGTFfile /local/pengying/data/anno/Homo_sapiens.GRCh38.87.chr.gtf \
--sjdbOverhang 100


time /local/pengying/tools/RSEM-1.3.1/rsem-prepare-reference \
--gtf /local/pengying/data/anno/Homo_sapiens.GRCh38.87.chr.gtf \
--transcript-to-gene-map /local/pengying/data/anno/knownIsoforms.txt \
--star \
--star-path /local/pengying/tools/STAR-2.6.0a/bin/Linux_x86_64 \
-p 35 \
/local/pengying/data/anno/hg38.fa \
/local/pengying/data/anno/RSEM/hg10
