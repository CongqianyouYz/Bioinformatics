fastq_phred=/home/disk/pengying/bin/fastq_phred.pl
trimmomatic=/home/disk/pengying/tools/Trimmomatic-0.38/trimmomatic-0.38.jar
fastqc_res=/home/disk/pengying/project/rna-seq/star/res/fastqc

list=`ls *fastq`
for data in ${list[@]}
do
    if [[ $data =~ .*_1\.fastq ]]; then
        srr=${data%%_*}
        read1=${srr}_1.fastq
        read2=${srr}_2.fastq
        unzip $fastqc_res/${data%%.fastq}_fastqc.zip -d $fastqc_res
        phred=`$fastq_phred $read1`
        headcrop=`grep "Per base sequence content" $fastqc_res/${srr}_1_fastqc/summary.txt | cut -f 1`

        if [ $headcrop = FAIL ] || [ $headcrop = WARN ]
        then
            java -jar $trimmomatic PE -phred$phred $read1 $read2 ${read1}.map ${read1}.unmap ${read2}.map ${read2}.unmap HEADCROP:12 SLIDINGWINDOW:5:20
        else
            java -jar $trimmomatic PE -phred$phred $read1 $read2 ${read1}.map ${read1}.unmap ${read2}.map ${read2}.unmap SLIDINGWINDOW:5:20
        fi

    elif [[ $data =~ [A-Za-z]+[0-9]+\.fastq ]]; then
        srr=${data%%.*}
        read1=${data}
        unzip $fastqc_res/${data%%.fastq}_fastqc.zip -d $fastqc_res
        phred=`$fastq_phred.pl $read1`
        headcrop=`grep "Per base sequence content" $fastqc_res/${srr}_fastqc/summary.txt | cut -f 1`

        if [ $headcrop = FAIL ] || [ $headcrop = WARN ]
        then
            java -jar $trimmomatic SE -phred$phred $read1 ${read1}.map HEADCROP:12 SLIDINGWINDOW:5:20
        else
            java -jar $trimmomatic SE -phred$phred $read1 ${read1}.map SLIDINGWINDOW:5:20
        fi
    fi
done
