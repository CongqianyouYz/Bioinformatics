import sys, os
import subprocess as sub
import matplotlib.pyplot as plt

if os.path.exists('log_size.txt') == False:
	handle = sub.Popen("wc -l *sprint/A_to_I.res | sort -nr | sed 's/.*ERR/ERR/' > log_size.txt", shell=True).wait()
if os.path.exists('log_size.gene.txt') == False:
	handle = sub.Popen("wc -l *sprint/A_to_I.res.gene | sort -nr | sed 's/.*ERR/ERR/' > log_size.gene.txt", shell=True).wait()
if os.path.exists('pool_genes') == False:
	handle = sub.Popen('mkdir pool_genes', shell=True).wait()
if os.path.exists('pool_sites') == False:
	handle = sub.Popen('mkdir pool_sites', shell=True).wait()
with open('spe.txt') as fi:
	for line in fi:
		spe = line.strip()

pool = set()
o_cumu_lst = []
diff = []
count = []

with open('log_size.txt') as fi:
	for line in fi:
		c_pool = set()
		seq = line.strip()
		if 'total' in seq:
			continue
		with open(seq) as f1:
			for line1 in f1:
				seq1 = line1.strip().split('\t')
				pool.add(seq1[0]+':'+seq1[2]+':'+seq1[3])
				c_pool.add(seq1[0]+':'+seq1[2]+':'+seq1[3])
		o_cumu_lst.append(len(pool))
		count.append(len(c_pool))
print(o_cumu_lst)

diff.append(o_cumu_lst[0])
for i in list(range(1, len(o_cumu_lst))):
	diff.append(o_cumu_lst[i]-o_cumu_lst[i-1])

percent = []
for i in list(range(len(diff))):
	percent.append(round(diff[i]/float(count[i]), 2))
print(percent)
fo = open('pool_sites/cumulate_spe.'+spe+'.txt', 'w')
for site in sorted(list(pool)):
	fo.write(site+'\n')
fo.close()


# --------------------------------------------------------------
pool_gene = set()
o_cumu_lst_gene = []
diff = []
count = []

with open('log_size.gene.txt') as fi:
	for line in fi:
		c_pool = set()
		seq = line.strip()
		if 'total' in seq:
			continue
		with open(seq) as f1:
			for line1 in f1:
				seq1 = line1.strip()
				pool_gene.add(seq1)
				c_pool.add(seq1)
		o_cumu_lst_gene.append(len(pool_gene))
		count.append(len(c_pool))
print(o_cumu_lst_gene)

diff.append(o_cumu_lst_gene[0])
for i in list(range(1, len(o_cumu_lst_gene))):
	diff.append(o_cumu_lst_gene[i]-o_cumu_lst_gene[i-1])

percent_gene = []
for i in list(range(len(diff))):
	percent_gene.append(round(diff[i]/float(count[i]), 2))
print(percent_gene)
fo = open('pool_genes/cumulate_spe.'+spe+'.txt', 'w')
for gene in sorted(list(pool_gene)):
	fo.write(gene+'\n')
fo.close()


# --------------------------------------------------------------
plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
plt.plot(o_cumu_lst)
plt.title(spe+' RES')
plt.subplot(2,2,2)
plt.plot(percent)
plt.title(spe+' RES percent')
plt.subplot(2,2,3)
plt.plot(o_cumu_lst_gene)
plt.title(spe+' gene')
plt.subplot(2,2,4)
plt.plot(percent_gene)
plt.title(spe+' gene percent');

plt.savefig('/home/disk/pengying/figure/cumulate_spe.'+spe+'.pdf')
plt.show()
plt.cla()
