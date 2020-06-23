import sys 

res1 = set()
res2 = set()
with open(sys.argv[3]) as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if seq[5] == '+' and seq[3] == 'AG':
            res1.add(seq[0]+':'+seq[2])
        elif seq[5] == '-' and seq[3] == 'TC':
            res2.add(seq[0]+':'+seq[2])
sum_ad = 0 
sum_dp = 0 

with open(sys.argv[1]) as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if seq[4] in ['A','a']:
            sum_dp = sum_dp + int(seq[6]) + int(seq[8])
            pos = seq[0]+':'+seq[3]
            if pos in res1:
                sum_ad += int(seq[8])
    
with open(sys.argv[2]) as fi: 
    for line in fi: 
        seq = line.strip().split('\t')
        if seq[4] in ['T','t']:
            sum_dp = sum_dp + int(seq[7]) + int(seq[9])
            pos = seq[0]+':'+seq[3]
            if pos in res2:
                sum_ad += int(seq[7])

fo = open(sys.argv[4], 'w')
fo.write(str(sum_ad/float(sum_dp)*100)+'\n')
fo.close()
