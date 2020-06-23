from collections import defaultdict
from numpy import mean
import matplotlib.pyplot as plt 
import subprocess as sub 
import os

with open('spe.txt') as fi: 
    for line in fi: 
        spe = line.strip()

def system_call(command):
    p = sub.Popen([command], stdout=sub.PIPE, shell=True)
    return p.stdout.read().decode("utf-8").strip()

d = defaultdict(dict)
with open('/home/disk/pengying/data/formeta/'+spe+'.txt') as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if seq[0] == 'Source Name':
            continue
        if spe == 'hg38':
            dev = seq[5].replace(' ', '_')
            if dev in d[seq[10]]:
                d[seq[10]][dev].append(seq[29])
            else:
                d[seq[10]][dev] = [seq[29]]
        elif spe in ['galGal5', 'oryCun2']:
            dev = seq[44].replace(' ', '_')
            if dev in d[seq[10]]:
                d[seq[10]][dev].append(seq[29])
            else:
                d[seq[10]][dev] = [seq[29]]
        elif spe == 'mm10':
            dev = seq[44].replace(' ', '_')
            if dev in d[seq[6]]:
                d[seq[6]][dev].append(seq[29])
            else:
                d[seq[6]][dev] = [seq[29]]
        elif spe == 'rheMac8':
            dev = seq[42].replace(' ', '_')
            if dev in d[seq[8]]:
                d[seq[8]][dev].append(seq[28])
            else:
                d[seq[8]][dev] = [seq[28]]
        elif spe == 'rn6':
            dev = seq[43].replace(' ', '_')
            if dev in d[seq[10]]:
                d[seq[10]][dev].append(seq[29])
            else:
                d[seq[10]][dev] = [seq[29]]
        elif spe == 'monDom5':
            dev = seq[41].replace(' ', '_')
            if dev in d[seq[8]]:
                d[seq[8]][dev].append(seq[27])
            else:
                d[seq[8]][dev] = [seq[27]]

order = []
with open('/home/disk/pengying/data/formeta/order/order.'+spe) as fi:
    for line in fi:
        order.append(spe+'.'+line.strip().replace(' ','_'))

o_dict = {}
for tissue, d_dev in d.items():
    print(tissue)
    d_count = {}
    for dev, samples in d_dev.items():
        l_count = []
        for sample in samples:
            sample_cnt, sample_name = system_call('wc -l '+sample+'.fastq.sprint/A_to_I.res').split(' ')
            _, sample_reads = system_call('grep ^SN '+sample+'.fastq.sprint/snvBAMdir/all_combined.zz.sorted.bam.stats | cut -f 2- | grep -w "reads mapped:"').split('\t')
            l_count.append(1000000 * int(sample_cnt) / float(sample_reads))
        d_count[spe+'.'+dev] = mean(l_count)
    y = []
    for x in order:
        if x in d_count:
            y.append(round(d_count[x],2))
        else:
            y.append(0)
    print(y)
    o_dict[tissue] = y

x_lab = order
plt.figure(figsize=(10, 18))
i = 1
for k in sorted(o_dict.keys()):
    plt.subplot(len(o_dict),1,i)
    i += 1
    plt.bar(x_lab,o_dict[k])
    plt.xticks([])
    plt.ylabel('RES number')
    plt.title(k)
plt.xticks(x_lab, rotation='vertical');

plt.savefig('/home/disk/pengying/figure/stat_dev_site.'+spe+'.pdf', bbox_inches='tight')
plt.show()
plt.cla()
