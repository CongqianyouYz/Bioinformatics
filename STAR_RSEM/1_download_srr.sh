parallel=/home/disk/pengying/tools/parallel/bin/parallel
fastq-dump=/home/disk/RNAediting_Cancer/tools/sratoolkit.2.8.2-centos_linux64/bin/fastq-dump

cat U87MG.txt | $parallel $fastq-dump --split-3 -O ./
list=`cat U87MG.txt`
for srr in ${list[@]}
do
	if [ -e /home/disk/pengying/ncbi/public/sra/${srr}* ]; then rm /home/disk/pengying/ncbi/public/sra/${srr}* ; fi
done
