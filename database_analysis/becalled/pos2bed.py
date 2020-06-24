import os
import subprocess as sub 

files = os.listdir('.')
for f in files:
    if f.endswith('.txt'):
        o_file = f.replace('.txt', '.bed')
        fo = open(o_file, 'w')
        with open(f) as fi: 
            for line in fi: 
                seq = line.strip().split(':')
                start = str(int(seq[1])-1)
                fo.write(seq[0]+'\t'+start+'\t'+seq[1]+'\t'+seq[2]+'\n')
        fo.close()
        sub.Popen('sortBed -i '+o_file+' > '+o_file.replace('.bed', '.sort.bed'), shell=True).wait()
        sub.Popen('rm '+o_file, shell=True).wait()
