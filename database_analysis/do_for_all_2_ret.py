import subprocess
import multiprocessing
import os

def Work(sprint_out_dir,a):
	print(sprint_out_dir)
	if os.path.exists(sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.bam')==False and os.path.exists(sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted')==True:
			subprocess.Popen('samtools view -H '+sprint_out_dir+'/snvBAMdir/all.bam > '+sprint_out_dir+'/snvBAMdir/SAMheader.txt',shell=True).wait()
			subprocess.Popen('python ~/scr/zz2sam.py '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted ',shell=True).wait()
			subprocess.Popen('cat '+sprint_out_dir+'/snvBAMdir/SAMheader.txt '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.sam > '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.sam.header',shell=True).wait()
			subprocess.Popen('samtools view -bS '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.sam.header > '+sprint_out_dir+'/snvBAMdir/all_combined.zz.bam',shell=True).wait()
			subprocess.Popen('samtools sort '+sprint_out_dir+'/snvBAMdir/all_combined.zz.bam -f '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.bam',shell=True ).wait()

			subprocess.Popen('rm -rf '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.sam',shell=True).wait()
			subprocess.Popen('rm -rf '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.sam.header',shell=True).wait()
			subprocess.Popen('rm -rf '+sprint_out_dir+'/snvBAMdir/all_combined.zz.bam',shell=True).wait()
			subprocess.Popen('samtools stats '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.bam > '+sprint_out_dir+'/snvBAMdir/all_combined.zz.sorted.bam.stats',shell=True).wait()

fa = open('lst.txt')
PROC_LIMIT = 5
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
