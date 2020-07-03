import sys 
import re

d = {}
with open(sys.argv[1]) as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if '#' in seq[0]:
            continue
        anno = seq[8]
        matchObj = re.match(r'^gene_id "(.*?)".*gene_name "(.*?)".*', anno, re.M|re.I)
        if matchObj:
            d[matchObj.group(1)] = matchObj.group(2)
        else:
            matchObj = re.match(r'^gene_id "(.*?)".*', anno, re.M|re.I)
            d[matchObj.group(1)] = matchObj.group(1)

fo = open('id2sym'+sys.argv[2], 'w')
for k, v in d.items():
    fo.write(k+'\t'+v+'\n')
fo.close()
