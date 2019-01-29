# https://gbiomed.kuleuven.be/apps/lcb/i-cisTarget/
# An integrative genomics method for the prediction of regulatory features and cis-regulatory modules

macs2 callpeak -t $data_dir/mCtrl-PDGFR-ATAC.rmdup.bam \
    -n ./mCtrl -B -f BAM --shift -75 --extsize 150 --nomodel \
    --call-summits --nolambda --keep-dup all -p 0
macs2 callpeak -t $data_dir/mEEDcKO-PDGFR-ATAC.rmdup.bam \
    -n ./mEEDcKO -B -f BAM --shift -75 --extsize 150 --nomodel \
    --call-summits --nolambda --keep-dup all -p 0

## send *_peaks.narrowPeak to i-cisTarget
## Comparative analysis and get combine.txt
