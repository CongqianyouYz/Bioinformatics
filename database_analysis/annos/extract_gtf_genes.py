import sys, re

gene_all = set()
with open(sys.argv[1]) as fi:   # Homo_sapiens.GRCh38.88.chr.gtf
    for line in fi: 
        seq = line.strip().split('\t')
        if '#' in seq[0]:
            continue
        anno = seq[8]
        try:
            matchObj = re.match( r'.*gene_name "(.*?)".*gene_biotype "(.*?)".*', anno, re.M|re.I)
            if matchObj.group(2) == 'protein_coding':
                gene_all.add(re.sub(r'\.*', '', matchObj.group(1)))
        except:
            pass
            """
            matchObj = re.match( r'gene_id "(.*?)".*gene_biotype "(.*?)".*', anno, re.M|re.I)
            if matchObj.group(2) == 'protein_coding':
                 gene_all.add(re.sub(r'\.*', '', matchObj.group(1)))
            """
fo = open('coding_genes.'+sys.argv[2], 'w')
for gene in sorted(list(gene_all)):
    fo.write(gene+'\n')
fo.close()
