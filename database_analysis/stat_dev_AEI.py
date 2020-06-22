from collections import defaultdict
from numpy import mean
import matplotlib.pyplot as plt 
import subprocess as sub 
import os

with open('spe.txt') as fi: 
    for line in fi: 
        spe = line.strip()

d = defaultdict(dict)
with open('/home/disk/pengying/data/formeta/'+spe+'.txt') as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if seq[0] == 'Source Name':
            continue
        dev = seq[5].replace(' ', '_')
        if dev in d[seq[10]]:
            d[seq[10]][dev].append(seq[29])
        else:
            d[seq[10]][dev] = [seq[29]]

order = []
with open('/home/disk/pengying/data/formeta/order/order.'+spe) as fi: 
    for line in fi: 
        order.append(spe+'.'+line.strip().replace(' ','_'))

o_dict = {}
for tissue, d_dev in d.items():
    print(tissue)
    d_AEI = {}
    for dev, samples in d_dev.items():
        l_AEI = []
        for sample in samples:
            with open(sample+'.fastq.sprint/aei.txt') as fi: 
                for line in fi: 
                    seq = line.strip()
                    l_AEI.append(float(seq))
        d_AEI[spe+'.'+dev] = round(mean(l_AEI), 3)
    y = []
    for x in order:
        if x in d_AEI:
            y.append(round(d_AEI[x], 3)) 
        else:
            y.append(0)
    print(y)
    o_dict[tissue] = y 

x_lab = order
plt.figure(figsize=(10, 18))
i = 1
for k in sorted(o_dict.keys()):
    plt.subplot(7,1,i)
    i += 1
    plt.bar(x_lab,o_dict[k])
    plt.xticks([])
    plt.ylabel('AEI')
    plt.title(k)
plt.xticks(x_lab, rotation='vertical');

plt.savefig('/home/disk/pengying/figure/stat_dev_AEI.'+spe+'.pdf', bbox_inches='tight')
plt.show()
plt.cla()
