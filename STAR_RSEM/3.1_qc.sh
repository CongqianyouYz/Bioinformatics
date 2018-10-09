cpu=6
fastqc=/home/disk/pengying/tools/FastQC/fastqc
fastqc_res=/home/disk/pengying/project/rna-seq/star/res/fastqc

list=`ls *fastq`
for data in ${list[@]}
do
	$fastqc $data -o $fastqc_res -t $cpu
done
