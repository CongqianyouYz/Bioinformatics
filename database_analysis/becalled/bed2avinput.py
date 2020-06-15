import sys

fo = open(sys.argv[2], 'w')
with open(sys.argv[1]) as fi:
	for line in fi:
		seq = line.strip().split('\t')
		ref, alt = seq[3][0], seq[3][1]
		fo.write(seq[0].replace('chr','')+'\t'+seq[2]+'\t'+seq[2]+'\t'+ref+'\t'+alt+'\n')
fo.close()
