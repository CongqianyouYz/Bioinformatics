import sys, os
import subprocess as sub
import matplotlib.pyplot as plt

if os.path.exists('log_size.txt') == False:
	handle = sub.Popen("wc -l *sprint/A_to_I.res | sort -nr | sed 's/.*ERR/ERR/' > log_size.txt", shell=True).wait()
if os.path.exists('log_size.gene.txt') == False:
	andle = sub.Popen("wc -l *sprint/A_to_I.res.gene | sort -nr | sed 's/.*ERR/ERR/' > log_size.gene.txt", shell=True).wait()

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


# --------------------------------------------------------------
with open('spe.txt') as fi:
	for line in fi:
		spe = line.strip()

plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)
plt.plot(o_cumu_lst)
plt.title('galGal5 RES')
plt.subplot(2,2,2)
plt.plot(percent)
plt.title('galGal5 RES percent')
plt.subplot(2,2,3)
plt.plot(o_cumu_lst_gene)
plt.title('galGal5 gene')
plt.subplot(2,2,4)
plt.plot(percent_gene)
plt.title('galGal5 gene percent');

plt.savefig('/home/disk/pengying/figure/cumulate_spe.'+spe+'.pdf')
plt.show()
plt.cla()

