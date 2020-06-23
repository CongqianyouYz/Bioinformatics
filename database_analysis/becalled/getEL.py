import sys 

my_dir = sys.argv[1]

d = {}
with open(my_dir+"/ALL_A_to_I.depth") as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        d[seq[0]+':'+seq[1]] = seq[2]

fo = open(my_dir+"/ALL_A_to_I.el", "w")
with open(my_dir+"/ALL_A_to_I.alt") as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        fo.write(line.strip()+'\t'+d[seq[0]+':'+seq[1]]+'\n')
fo.close()
