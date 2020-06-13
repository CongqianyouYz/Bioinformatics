import subprocess
import multiprocessing
import os

ref = '/home/genomewide/refgenome/rheMac8/rheMac8'
gtf = '/home/genomewide/annotation/rheMac8/Macaca_mulatta.Mmul_8.0.1.92.chr.gtf'

def Work(sprint_out_dir,a):
	print(sprint_out_dir)
	sample = sprint_out_dir.replace('.fastq.gz','')
	if os.path.exists(sample+'.tophat')==False or os.path.exists(sample+'.tophat/accepted_hits.bam')==False:
		subprocess.Popen('tophat2 -p 6 --library-type fr-firststrand -o '+sample+'.tophat '+ref+' '+sprint_out_dir, shell=True).wait()
		subprocess.Popen('cufflinks -G '+gtf+' --library-type fr-firststrand -q --no-update-check -p 10 -u -o '+sample+'.tophat/cufflinks '+sample+'.tophat/accepted_hits.bam', shell=True).wait()

fa = open('lst.txt')
PROC_LIMIT = 5
jobs = []
i = 1

for line in fa: 
	sprint_out_dir = line.strip()
	print(str(i)+'-----'+sprint_out_dir)
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
