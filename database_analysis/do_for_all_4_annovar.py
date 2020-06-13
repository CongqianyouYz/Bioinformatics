import subprocess
import multiprocessing
import os

with open('spe.txt') as fi:
	for line in fi:
		spe = line.strip()

d = {}
with open('ALL_A_to_I.'+spe+'_multianno.txt') as fi:
	for line in fi:
		seq = line.strip().split('\t')
		d['chr'+seq[0]+':'+seq[1]+':'+seq[3]+seq[4]] = seq[5:7]

def Work(sprint_out_dir,a):
	print(sprint_out_dir)
	s_gene = set()
	fo = open(sprint_out_dir+'/A_to_I.res.anno', 'w')
	with open(sprint_out_dir+'/A_to_I.res') as fi:
		for line in fi:
			seq = line.strip().split('\t')
			key = seq[0]+':'+seq[2]+':'+seq[3]
			fo.write(key+'\t'+'\t'.join(d[key])+'\n')
			if d[key][0] != 'intergenic':
				if d[key][1] != 'NONE':
					s_gene.add(d[key][1])
	fo.close()
	f_gene = open(sprint_out_dir+'/A_to_I.res.gene', 'w')
	for gene in sorted(list(s_gene)):
		f_gene.write(gene+'\n')
	f_gene.close()

fa = open('lst.txt')
PROC_LIMIT = 10
jobs = []
i = 1

for line in fa: 
	sprint_out_dir = line.strip()
	print(str(i), sprint_out_dir)
	i += 1
	if 1==1:
		p = multiprocessing.Process(target=Work, args=(sprint_out_dir,1))
		p.start()
		jobs.append(p)
		if len(jobs) >= PROC_LIMIT:
			for p in jobs:
				p.join()
			jobs=[]
for p in jobs:
	p.join()

