import subprocess
import multiprocessing
import os

def Work(sprint_out_dir,a):
	print(sprint_out_dir)
	if os.path.exists(sprint_out_dir+'/A_to_I.res') == False:
		subprocess.Popen('python2 ~/scr/getA2I.py 1 '+sprint_out_dir+'/ '+sprint_out_dir+'/A_to_I.res', shell=True).wait()

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
