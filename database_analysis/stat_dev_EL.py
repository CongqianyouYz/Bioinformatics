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
	d_EL = {}
	for dev, samples in d_dev.items():
		l_ad = []
		l_dp = []
		for sample in samples:
			with open(sample+'.fastq.sprint/A_to_I.res') as fi:
				for line in fi:
					seq = line.strip().split('\t')
					ad, dp = seq[6].split(':')
					l_ad.append(int(ad))
					l_dp.append(int(dp))
		d_EL[spe+'.'+dev] = round(sum(l_ad) / float(sum(l_dp)), 2)
	y = []
	for x in order:
		if x in d_EL:
			y.append(round(d_EL[x],2))
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
	plt.ylabel('AEI')
	plt.title(k)
plt.xticks(x_lab, rotation='vertical');

plt.savefig('/home/disk/pengying/figure/stat_dev_EL.'+spe+'.pdf', bbox_inches='tight')
plt.show()
plt.cla()

