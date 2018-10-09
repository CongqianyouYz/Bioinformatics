cpu=6
STAR=/home/disk/pengying/tools/STAR-2.6.0a/bin/Linux_x86_64_static/STAR
STAR_res=/home/disk/pengying/project/rna-seq/star/res/STAR
STAR_index=/home/genomewide/RNA-seq_idx/hg38/STAR

list=`ls *fastq`
for data in ${list[@]}
do
    if [[ $data =~ .*_1\.fastq ]]; then
        srr=${data%%_*}
        read1=${srr}_1.fastq
        read2=${srr}_2.fastq

        mkdir $STAR_res/$srr/
        $STAR --runThreadN $cpu --twopassMode Basic --outSAMstrandField intronMotif --genomeDir $STAR_index --readFilesIn ${read1}.map ${read2}.map --outFileNamePrefix $STAR_res/$srr/ --outSAMtype BAM SortedByCoordinate --quantMode GeneCounts TranscriptomeSAM

    elif [[ $data =~ [A-Za-z]+[0-9]+\.fastq ]]; then
        srr=${data%%.*}
        read1=${data}

        mkdir $STAR_res/$srr/
        $STAR --runThreadN $cpu --twopassMode Basic --outSAMstrandField intronMotif --genomeDir $STAR_index --readFilesIn ${read1}.map --outFileNamePrefix $STAR_res/$srr/ --outSAMtype BAM SortedByCoordinate --quantMode GeneCounts TranscriptomeSAM
    fi
done
