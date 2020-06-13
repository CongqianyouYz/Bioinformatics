cat *sprint/A_to_I.res > ALL_A_to_I.res
bedtools sort -i ALL_A_to_I.res > ALL_A_to_I.res.sorted
cut -f 1-4 ALL_A_to_I.res.sorted | uniq > ALL_A_to_I.res.sorted.uniq.bed

rm ALL_A_to_I.res ALL_A_to_I.res.sorted


annovar=/home/disk/pengying/tools/annovar/table_annovar.pl
annodb=/home/disk/pengying/tools/annovar

spe=`cat spe.txt`

python ~/scr/becalled/a2_bed2avinput.py ALL_A_to_I.res.sorted.uniq.bed ALL_A_to_I.res.sorted.uniq.bed.avinput
$annovar ALL_A_to_I.res.sorted.uniq.bed.avinput ${annodb}/${spe}/ -buildver $spe -out ALL_A_to_I -remove -protocol refGene -operation g -nastring . -polish
