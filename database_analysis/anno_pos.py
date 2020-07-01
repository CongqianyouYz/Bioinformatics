import os
import re

with open('spe.txt') as fi: 
    for line in fi: 
        spe = line.strip()

dirs = os.listdir('pool_sites')
lst = []
for f in dirs:
    matchObj = re.match(r'redits\..*\.sig$', f, re.M|re.I)
    if matchObj:
        lst.append(f)

# --------------------------------------
# get genes
# --------------------------------------
if 1==0:
    d = {}
    with open('ALL_A_to_I.'+spe+'_multianno.txt') as fi: 
        for line in fi: 
            seq = line.strip().split('\t')
            if seq[0] == 'Chr':
                continue
            else:
                pos = 'chr'+seq[0]+':'+seq[1]+':'+seq[3]+seq[4]
                region = seq[5]
                gene = seq[6]
                d[pos] = [region, gene]
    
    for f in lst:
        fo = open('pool_sites/'+f+'.gene', 'w')
        with open('pool_sites/'+f) as fi: 
            for line in fi: 
                pos, pval = line.strip().split('\t')
                if pos == 'key':
                    fo.write(line.strip()+'\tregion\tgene\n')
                else:
                    fo.write(line.strip()+'\t'+d[pos][0]+'\t'+d[pos][1]+'\n')
        fo.close()

# --------------------------------------
# get EL profile
# --------------------------------------
if 1==0:
    for f in lst:
        d = {}
        matchObj = re.match(r'redits\.(.*)\.sig', f, re.M|re.I)
        tissue = matchObj.group(1)
        header = ''
        with open('pool_sites/header.'+tissue) as fi:
            for line in fi:
                header = header+'\t'+line.strip()

        with open('pool_sites/elMat.'+tissue+'.'+spe+'.txt') as fi:
            for line in fi:
                seq = line.strip().split('\t')
                if seq[0] == 'key':
                    continue
                d[seq[0]] = seq[1:]

        fo = open('pool_sites/'+f+'.gene.pro', 'w')
        with open('pool_sites/'+f+'.gene') as fi:
            for line in fi:
                seq = line.strip().split('\t')
                if seq[0] == 'key':
                    fo.write(line.strip()+header+'\n')
                else:
                    fo.write(line.strip()+'\t'+'\t'.join(d[seq[0]])+'\n')
        fo.close()
