cpu=6
RSEM=/home/disk/pengying/tools/RSEM-1.3.1/rsem-calculate-expression
strand_test=/home/disk/pengying/rna_editing/scr/strand.sh
infer_experiment=/home/disk/pengying/tools/RSeQC-2.6.5/scripts/infer_experiment.py
RSEM_index=/home/genomewide/RNA-seq_idx/hg38/RSEM/hg38
STAR_res=/home/disk/pengying/project/rna-seq/star/res/STAR
RSEM_res=/home/disk/pengying/project/rna-seq/star/res/RSEM
RefSeq=/home/genomewide/RNA-seq_idx/hg38/hg38_RefSeq.bed

list=`ls *fastq`
for data in ${list[@]}
do
    if [[ $data =~ .*_1\.fastq ]]; then
        srr=${data%%_*}
        read1=${srr}_1.fastq
        read2=${srr}_2.fastq

        $infer_experiment -i $STAR_res/$srr/Aligned.sortedByCoord.out.bam -r $RefSeq > $STAR_res/$srr/strand.txt
        strand=`sh $strand_test $STAR_res/$srr/strand.txt`
        $RSEM -p $cpu --bam --paired-end --forward-prob $strand $STAR_res/$srr/Aligned.toTranscriptome.out.bam $RSEM_index $RSEM_res/$srr

    elif [[ $data =~ [A-Za-z]+[0-9]+\.fastq ]]; then
        srr=${data%%.*}
        read1=${data}

        $infer_experiment -i $STAR_res/$srr/Aligned.sortedByCoord.out.bam -r $RefSeq > $STAR_res/$srr/strand.txt
        strand=`sh $strand_test $STAR_res/$srr/strand.txt`
        $RSEM -p $cpu --bam --forward-prob $strand $STAR_res/$srr/Aligned.toTranscriptome.out.bam $RSEM_index $RSEM_res/$srr
    fi
done
