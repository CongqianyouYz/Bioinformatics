import os
import pandas as pd
from collections import defaultdict

with open('spe.txt') as fi: 
    for line in fi: 
        spe = line.strip()
    
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


# ---------------------------------------------------------------
for tissue, d_dev in d.items():
    if os.path.exists('pool_sites/elMat.'+tissue+'.'+spe+'.txt') == True:
        continue
    print(tissue)
    dirs = []
    for dev, samples in d_dev.items():
        dirs.extend(samples)
    df_raw = pd.read_csv(dirs[0]+'.fastq.sprint/ALL_A_to_I.el', sep='\t', header=None, names=['chr','pos','type','ad','dp'])
    df_raw['key'] = df_raw['chr']+':'+df_raw['pos'].map(str)+':'+df_raw['type']
    df_raw[dirs[0]] = df_raw['ad'] / df_raw['dp']
    df = df_raw[['key', dirs[0]]]

    for i in range(1, len(dirs)):
        df_add = pd.read_csv(dirs[i]+'.fastq.sprint/ALL_A_to_I.el', sep='\t', header=None, names=['chr','pos','type','ad','dp'])
        df_add['key'] = df_add['chr']+':'+df_add['pos'].map(str)+':'+df_add['type']
        df_add[dirs[i]] = df_add['ad'] / df_add['dp']
        df_add_final = df_add[['key', dirs[i]]]
        df = df.merge(df_add_final, how='outer').fillna(0)
    df.round(6).to_csv('pool_sites/elMat.'+tissue+'.'+spe+'.txt', index=False, sep='\t')


# ---------------------------------------------------------------
for tissue, d_dev in d.items():
    if os.path.exists('pool_sites/addpMat.'+tissue+'.'+spe+'.txt') == True:
        continue
    print(tissue)
    dirs = []
    for dev, samples in d_dev.items():
        dirs.extend(samples)
    df_raw = pd.read_csv(dirs[0]+'.fastq.sprint/ALL_A_to_I.el', sep='\t', header=None, names=['chr','pos','type','ad','dp'])
    df_raw['key'] = df_raw['chr']+':'+df_raw['pos'].map(str)+':'+df_raw['type']
    df_raw[dirs[0]] = df_raw['ad'].map(str)+':'+df_raw['dp'].map(str)
    df = df_raw[['key', dirs[0]]]

    for i in range(1, len(dirs)):
        df_add = pd.read_csv(dirs[i]+'.fastq.sprint/ALL_A_to_I.el', sep='\t', header=None, names=['chr','pos','type','ad','dp'])
        df_add['key'] = df_add['chr']+':'+df_add['pos'].map(str)+':'+df_add['type']
        df_add[dirs[i]] = df_add['ad'].map(str)+':'+df_add['dp'].map(str)
        df_add_final = df_add[['key', dirs[i]]]
        df = df.merge(df_add_final, how='outer').fillna(0)
    df.round(6).to_csv('pool_sites/addpMat.'+tissue+'.'+spe+'.txt', index=False, sep='\t')


# ---------------------------------------------------------------
# 2/3 cutoff and data formation
# ---------------------------------------------------------------
for tissue, d_dev in d.items():
    filename = 'pool_sites/addpMat.'+tissue+'.'+spe+'.txt'  # addpMat.ovary.hg38.txt
    if os.path.exists(filename+'.sub2.3') == True:
        continue
    print(tissue)
    df_sub = pd.read_csv(filename, sep='\t', low_memory=False)
    df_sub = df_sub.applymap(str)
    res = (df_sub == '0').astype(int).sum(axis=1)
    res1 = res[res <= ((df_sub.shape[1] - 1) / float(3))]
    pos = res1.index
    df_sub_cutoff = df_sub.loc[pos]
    df_sub_cutoff.to_csv(filename+'.sub2.3', sep='\t', index=False)

    f_ad = open(filename+'.sub2.3.ad', 'w')
    f_dp = open(filename+'.sub2.3.dp', 'w')
    with open(filename+'.sub2.3') as fi:
        for line in fi:
            seq = line.strip().split('\t')
            if seq[0] == 'key':
                sample_order = seq[1:]
                f_ad.write(line)
                f_dp.write(line)
            else:
                f_ad.write(seq[0])
                f_dp.write(seq[0])
                for ele in seq[1:]:
                    if ele == '0':
                        f_ad.write('\t0')
                        f_dp.write('\t0')
                    else:
                        ad, dp = ele.split(':')
                        f_ad.write('\t'+ad)
                        f_dp.write('\t'+dp)
                f_ad.write('\n')
                f_dp.write('\n')
    f_ad.close()
    f_dp.close()


# ---------------------------------------------------------------
# dev header
# ---------------------------------------------------------------
order = {}
i = 1
with open('/home/disk/pengying/data/formeta/order/order.'+spe) as fi:
    for line in fi:
        order[line.strip().replace(' ','_')] = str(i)
        i += 1

for tissue, d_dev in d.items():
    print(tissue)
    fo = open('pool_sites/header.'+tissue, 'w')
    d_header = {}
    for dev, samples in d_dev.items():
        for sample in samples:
            d_header[sample] = dev
    for k in sorted(d_header.keys()):
        fo.write(order[d_header[k]]+'\n')
    fo.close()
