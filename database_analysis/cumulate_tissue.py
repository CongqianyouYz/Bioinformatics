from collections import defaultdict
import matplotlib.pyplot as plt
import subprocess as sub

with open('spe.txt') as fi:
	for line in fi:
		spe = line.strip()

def system_call(command):
	p = sub.Popen([command], stdout=sub.PIPE, shell=True)
	return p.stdout.read().decode("utf-8").strip()

d = defaultdict(list)
with open('/home/disk/pengying/data/formeta/'+spe+'.txt') as fi:
	for line in fi:
		seq = line.strip().split('\t')
		if seq[0] == 'Source Name':
			continue
		d[seq[10]].append(seq[29])

        
# -------------------------------------------------------------------
d_count = {}
d_percent = {}

for tissue, samples in d.items():
	print(tissue)
	d_tissue = {}
	for sample in samples:
		cnt, name = system_call('wc -l '+sample+'.fastq.sprint/A_to_I.res').split(' ')
		d_tissue[name] = int(cnt)
		d_tissue_sort = sorted(d_tissue.items(), key=lambda x: x[1], reverse=True)

	pool = set()
	o_cumu_lst = []
	diff = []
	count = []

	for i in d_tissue_sort:
		c_pool = set()
		with open(i[0]) as f1: 
			for line1 in f1: 
				seq1 = line1.strip().split('\t')
				pool.add(seq1[0]+':'+seq1[2]+':'+seq1[3])
				c_pool.add(seq1[0]+':'+seq1[2]+':'+seq1[3])
		o_cumu_lst.append(len(pool))
		count.append(len(c_pool))
	print(o_cumu_lst)

	diff.append(o_cumu_lst[0])
	for i in list(range(1,len(o_cumu_lst))):
		diff.append(o_cumu_lst[i]-o_cumu_lst[i-1])

	percent = []
	for i in list(range(len(diff))):
		percent.append(round(diff[i]/float(count[i]), 2)) 
	print(percent)
	print('---------------------------')
	
	d_count[tissue] = o_cumu_lst
	d_percent[tissue] = percent

	fo = open('pool_sites/cumulate.'+tissue+'.'+spe+'.txt', 'w')
	for site in sorted(list(pool)):
		fo.write(site+'\n')
	fo.close()

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
t_lst = []
for k in sorted(d_count.keys()):
	k, = plt.plot(d_count[k])
	t_lst.append(k,)
plt.title(spe+' RES')
l1 = plt.legend(t_lst, sorted(d_count.keys()), loc='best')
plt.gca().add_artist(l1);

plt.subplot(2,2,2)
t_lst = []
for k in sorted(d_percent.keys()):
	k, = plt.plot(d_percent[k])
	t_lst.append(k,)
plt.title(spe+' RES percent')
l1 = plt.legend(t_lst, sorted(d_percent.keys()), loc='best')
plt.gca().add_artist(l1);


# -------------------------------------------------------------------
for tissue, samples in d.items():
	print(tissue)
	d_tissue = {}
	for sample in samples:
		cnt, name = system_call('wc -l '+sample+'.fastq.sprint/A_to_I.res.gene').split(' ')
		d_tissue[name] = int(cnt)
		d_tissue_sort = sorted(d_tissue.items(), key=lambda x: x[1], reverse=True)

	pool = set()
	o_cumu_lst = []
	diff = []
	count = []

	for i in d_tissue_sort:
		c_pool = set()
		with open(i[0]) as f1: 
			for line1 in f1: 
				seq1 = line1.strip()
				pool.add(seq1)
				c_pool.add(seq1)
		o_cumu_lst.append(len(pool))
		count.append(len(c_pool))
	print(o_cumu_lst)

	diff.append(o_cumu_lst[0])
	for i in list(range(1,len(o_cumu_lst))):
		diff.append(o_cumu_lst[i]-o_cumu_lst[i-1])

	percent = []
	for i in list(range(len(diff))):
		percent.append(round(diff[i]/float(count[i]), 2)) 
	print(percent)
	print('---------------------------')

	d_count[tissue] = o_cumu_lst
	d_percent[tissue] = percent

	fo = open('pool_genes/cumulate.'+tissue+'.'+spe+'.txt', 'w')
	for gene in sorted(list(pool)):
		fo.write(gene+'\n')
	fo.close()

plt.subplot(2,2,3)
t_lst = []
for k in sorted(d_count.keys()):
	k, = plt.plot(d_count[k])
	t_lst.append(k,)
plt.title(spe+' gene')
l1 = plt.legend(t_lst, sorted(d_count.keys()), loc='best')
plt.gca().add_artist(l1);

plt.subplot(2,2,4)
t_lst = []
for k in sorted(d_percent.keys()):
	k, = plt.plot(d_percent[k])
	t_lst.append(k,)
plt.title(spe+' gene percent')
l1 = plt.legend(t_lst, sorted(d_percent.keys()), loc='best')
plt.gca().add_artist(l1);


plt.savefig('/home/disk/pengying/figure/cumulate_tissue.'+spe+'.pdf')
plt.show()
plt.cla()
