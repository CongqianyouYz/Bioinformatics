list=(
bosTau8
ce10
danRer11
dm6
galGal5
gorGor3
mm10
monDom5
ornAna2
panPan2
panTro3
ponAbe3
rheMac8
xenLae2
)
for spe in ${list[@]}
do
	annotate_variation.pl --downdb --buildver $spe gene $spe/
	annotate_variation.pl --buildver $spe --downdb seq $spe/${spe}_seq

:<<COMMENT
csplit -s -z ${spe}.fa '/>/' '{*}'
for i in xx* ; do \
	n=$(sed 's/>// ; s/ .*// ; 1q' "$i") ; \
	mv "$i" "$n.fa" ; \
done
COMMENT

	retrieve_seq_from_fasta.pl $spe/${spe}_refGene.txt -seqdir $spe/${spe}_seq -format refGene -outfile $spe/${spe}_refGeneMrna.fa
done

:<<COMMENT
annotate_variation.pl --downdb ensGene gorGor3 -build gorGor3
annotate_variation.pl --buildver gorGor3 --downdb seq gorGor3/gorGor3_seq
retrieve_seq_from_fasta.pl gorGor3/gorGor3_ensGene.txt -seqdir gorGor3/gorGor3_seq -format ensGene -outfile gorGor3/gorGor3_ensGeneMrna.fa
COMMENT
