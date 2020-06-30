import subprocess
import multiprocessing
import os

ref = '/lustre/tianlab/a_pengying/anno/mm10/mm10'
gtf = '/lustre/tianlab/a_pengying/anno/mm10/Mus_musculus.GRCm38.87.chr.gtf'
thr = '9' 

def Work(sprint_out_dir,a):
    print(sprint_out_dir)
    sample = sprint_out_dir.replace('.fastq.gz','')
    if os.path.exists(sample+'.tophat')==False or os.path.exists(sample+'.tophat/accepted_hits.bam')==False:
        subprocess.Popen('/lustre/tianlab/tools/tophat-2.1.1.Linux_x86_64/tophat2 -p '+thr+' --library-type fr-firststrand -o '+sample+'.tophat '+ref+' '+sprint_out_dir, shell=True).wait()
        subprocess.Popen('/lustre/tianlab/tools/cufflinks-2.2.1.Linux_x86_64/cufflinks -G '+gtf+' --library-type fr-firststrand -q --no-update-check -p '+thr+' -u -o '+sample+'.tophat/cufflinks '+sample+'.tophat/accepted_hits.bam', shell=True).wait()
    subprocess.Popen('/lustre/tianlab/tools/cufflinks-2.2.1.Linux_x86_64/cuffquant -p '+thr+' --library-type fr-firststrand --no-update-check -q -u -o '+sample+'.tophat/cuffquant/ merged_asm/merged.gtf '+sample+'.tophat/accepted_hits.bam', shell=True).wait()

fa = open('for_exp.txt')
PROC_LIMIT = 4
jobs = []
i = 1 

for line in fa:
    sprint_out_dir = line.strip()
    print('>>>>> '+str(i)+': '+sprint_out_dir)
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

# cuffmerge -g Gallus_gallus.Gallus_gallus-5.0.88.chr.gtf -s galGal5.fa -p 40 assembly_list.txt
