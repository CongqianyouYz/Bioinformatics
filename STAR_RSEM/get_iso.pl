open FI, "Homo_sapiens.GRCh38.87.chr.gtf";
open FO, ">knownIsoforms_to_sort.txt";

while (<FI>) {
	chomp;
	next if (/^#/);
    
	@line = split "\t";
	$anno = $line[8];

	($gene_id)       = $_ =~ /gene_id \"([^\"]+)\"\;/;
	($transcript_id) = $_ =~ /transcript_id \"([^\"]+)\"\;/;

	print FO "$gene_id\t$transcript_id\n";
}

system "sort -V knownIsoforms_to_sort.txt | uniq > knownIsoforms.txt";

close FI;
close FO;
