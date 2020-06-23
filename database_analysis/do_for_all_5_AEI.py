import subprocess
import multiprocessing
import os

InstallPath = '/lustre/tianlab/tools/RNAEditingIndexer-master'

def Work(sprint_out_dir,a):
    print(sprint_out_dir)
    if os.path.exists(sprint_out_dir+'/AEI/EditingIndex.csv') == False:
        if os.path.exists(sprint_out_dir+'/AEI') == True:
            subprocess.Popen('rm -r '+sprint_out_dir+'/AEI', shell=True).wait()
        subprocess.Popen('mkdir '+sprint_out_dir+'/AEI', shell=True).wait()
        subprocess.Popen(InstallPath+'/RNAEditingIndex -d /lustre/tianlab/a_pengying/hg38/'+sprint_out_dir+' -f ll.bam -l /lustre/tianlab/a_pengying/hg38/'+sprint_out_dir+'/AEI -o /lustre/tianlab/a_pengying/hg38/'+sprint_out_dir+'/AEI -os /lustre/tianlab/a_pengying/hg38/'+sprint_out_dir+'/AEI --genome hg38 --stranded --keep_cmpileup', shell=True).wait()
        subprocess.Popen('rm '+sprint_out_dir+'/AEI/ucscHg38Genome.fa.GenomeIndex.jsd', shell=True).wait()
        subprocess.Popen('python3 /lustre/tianlab/a_pengying/scr/AEI_extract_AD.py '+sprint_out_dir+'/AEI/a/a_ucscHg38Alu.bed.gz_mpileup_strand_1.cmpileup '+sprint_out_dir+'/AEI/a/a_ucscHg38Alu.bed.gz_mpileup_strand_2.cmpileup '+sprint_out_dir+'/SPRINT_identified_regular.res '+sprint_out_dir+'/aei.txt', shell=True).wait()

fa = open('lst.txt')
PROC_LIMIT = 20
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
