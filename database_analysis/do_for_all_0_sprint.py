import subprocess
import multiprocessing
import os

def Work(sprint_out_dir,a):
	print(sprint_out_dir)
	d_res = sprint_out_dir+'.fastq.sprint'
	subprocess.Popen('gunzip /home/disk/pengying/data/fatsq/galGal5/'+sprint_out_dir+'.fastq.gz', shell=True).wait()
	subprocess.Popen('/home/disk/pengying/tools/sprint-0.1.8/bin/sprint main -rp /home/genomewide/annotation/galGal5/galGal5_repeat.bed -c 0 -p 6 -1 /home/disk/pengying/data/fatsq/galGal5/'+sprint_out_dir+'.fastq /home/genomewide/refgenome/galGal5/galGal5.fa ./'+sprint_out_dir+'.fastq.sprint /home/zhangfeng/tools/bwa-0.7.12/bwa /home/zhangfeng/tools/samtools-1.2/samtools', shell=True).wait()
	subprocess.Popen('mkdir '+d_res+'/snvBAMdir', shell=True).wait()
	subprocess.Popen('mv '+d_res+'/tmp/all_combined.zz.sorted '+d_res+'/snvBAMdir', shell=True).wait()
	subprocess.Popen('mv '+d_res+'/tmp/genome/all.bam '+d_res+'/snvBAMdir', shell=True).wait()
	subprocess.Popen('mv '+d_res+'/tmp/*snv* '+d_res+'/snvBAMdir', shell=True).wait()
	subprocess.Popen('rm -r '+d_res+'/tmp', shell=True).wait()
	subprocess.Popen('gzip /home/disk/pengying/data/fatsq/galGal5/'+sprint_out_dir+'.fastq', shell=True).wait()

fa = open('for_sprint.txt')
PROC_LIMIT = 5
jobs = []
i = 1

for line in fa: 
	sprint_out_dir = line.strip()
	print(str(i)+'-------------------'+sprint_out_dir)
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
