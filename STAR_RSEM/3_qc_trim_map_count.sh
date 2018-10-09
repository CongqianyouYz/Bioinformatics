## ******************** setting ********************
cpu=6
fastqc=/home/disk/pengying/tools/FastQC/fastqc
trimmomatic=/home/disk/pengying/tools/Trimmomatic-0.38/trimmomatic-0.38.jar
STAR=/home/disk/pengying/tools/STAR-2.6.0a/bin/Linux_x86_64_static/STAR
RSEM=/home/disk/pengying/tools/RSEM-1.3.1/rsem-calculate-expression
fastq_phred=/home/disk/pengying/bin/fastq_phred.pl
infer_experiment=/home/disk/pengying/tools/RSeQC-2.6.5/scripts/infer_experiment.py
strand_test=/home/disk/pengying/rna_editing/scr/strand.sh

STAR_index=/home/genomewide/RNA-seq_idx/hg38/STAR
RSEM_index=/home/genomewide/RNA-seq_idx/hg38/RSEM/hg38
RefSeq=/home/genomewide/RNA-seq_idx/hg38/hg38_RefSeq.bed
fastqc_res=/home/disk/pengying/project/rna-seq/star/res/fastqc
STAR_res=/home/disk/pengying/project/rna-seq/star/res/STAR
RSEM_res=/home/disk/pengying/project/rna-seq/star/res/RSEM
log_file=/home/disk/pengying/project/rna-seq/star/res/quantity_log.txt

cd /home/disk/pengying/project/rna-seq/star/data

## ******************** doing ********************
list=`ls *fastq`
for data in ${list[@]}
do
    if [[ $data =~ .*_1\.fastq ]]; then
        srr=${data%%_*}
        read1=${srr}_1.fastq
        read2=${srr}_2.fastq

        echo "$srr analysis start at "`date` >> $log_file
        $fastqc $read1 -o $fastqc_res -t $cpu
        $fastqc $read2 -o $fastqc_res -t $cpu
        unzip $fastqc_res/${data%%.fastq}_fastqc.zip -d $fastqc_res

        phred=`$fastq_phred $read1`
        echo -e "\tphred: $phred" >> $log_file
        headcrop=`grep "Per base sequence content" $fastqc_res/${srr}_1_fastqc/summary.txt | cut -f 1`
        echo -e "\theadcrop: $headcrop" >> $log_file
        if [ $headcrop = FAIL ] || [ $headcrop = WARN ]
        then
            java -jar $trimmomatic PE -phred$phred $read1 $read2 ${read1}.map ${read1}.unmap ${read2}.map ${read2}.unmap HEADCROP:12 SLIDINGWINDOW:5:20
        else
            java -jar $trimmomatic PE -phred$phred $read1 $read2 ${read1}.map ${read1}.unmap ${read2}.map ${read2}.unmap SLIDINGWINDOW:5:20
        fi
        
        mkdir $STAR_res/$srr/
        $STAR --runThreadN $cpu --twopassMode Basic --outSAMstrandField intronMotif --genomeDir $STAR_index --readFilesIn ${read1}.map ${read2}.map --outFileNamePrefix $STAR_res/$srr/ --outSAMtype BAM SortedByCoordinate --quantMode GeneCounts TranscriptomeSAM

        $infer_experiment -i $STAR_res/$srr/Aligned.sortedByCoord.out.bam -r $RefSeq > $STAR_res/$srr/strand.txt
        strand=`sh $strand_test $STAR_res/$srr/strand.txt`
        echo -e "\tstrand: $strand" >> $log_file
        $RSEM -p $cpu --bam --paired-end --forward-prob $strand $STAR_res/$srr/Aligned.toTranscriptome.out.bam $RSEM_index $RSEM_res/$srr

        mv ${srr}*fastq to_tar
        rm -r ${srr}*map $fastqc_res/${srr}*fastqc $RSEM_res/${srr}.transcript.bam $RSEM_res/${srr}.stat $STAR_res/$srr
        echo "$srr done at "`date` >> $log_file
        echo >> $log_file
        
    elif [[ $data =~ [A-Za-z]+[0-9]+\.fastq ]]; then
        srr=${data%%.*}
        read1=${data}
        "$srr analysis start at "`date` >> $time_log
        $fastqc $data -o $fastqc_res -t $cpu
        unzip $fastqc_res/${data%%.fastq}_fastqc.zip -d $fastqc_res

        phred=`$fastq_phred.pl $read1`
        echo -e "\tphred: $phred" >> $log_file
        headcrop=`grep "Per base sequence content" $fastqc_res/${srr}_fastqc/summary.txt | cut -f 1`
        echo -e "\theadcrop: $headcrop" >> $log_file
        if [ $headcrop = FAIL ] || [ $headcrop = WARN ]
        then
            java -jar $trimmomatic SE -phred$phred $read1 ${read1}.map HEADCROP:12 SLIDINGWINDOW:5:20
        else
            java -jar $trimmomatic SE -phred$phred $read1 ${read1}.map SLIDINGWINDOW:5:20
        fi

        mkdir $STAR_res/$srr/
        $STAR --runThreadN $cpu --twopassMode Basic --outSAMstrandField intronMotif --genomeDir $STAR_index --readFilesIn ${read1}.map --outFileNamePrefix $STAR_res/$srr/ --outSAMtype BAM SortedByCoordinate --quantMode GeneCounts TranscriptomeSAM

        $infer_experiment -i $STAR_res/$srr/Aligned.sortedByCoord.out.bam -r $RefSeq > $STAR_res/$srr/strand.txt
        strand=`sh $strand_test $STAR_res/$srr/strand.txt`
        echo -e "\tstrand: $strand" >> $log_file
        $RSEM -p $cpu --bam --forward-prob $strand $STAR_res/$srr/Aligned.toTranscriptome.out.bam $RSEM_index $RSEM_res/$srr

        mv ${srr}*fastq to_tar
        rm -r ${srr}*map $fastqc_res/${srr}*fastqc $RSEM_res/${srr}.transcript.bam $RSEM_res/${srr}.stat $STAR_res/$srr
        echo "$srr done at "`date` >> $log_file
        echo >> $log_file
    fi
done
