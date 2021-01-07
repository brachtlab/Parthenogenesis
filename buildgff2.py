#!/usr/bin/env python
from Bio import SeqIO
from Bio import Seq
import sys
from sys import argv
out=open("%s.gff"%argv[1],"w")
out.write("##gff-version 3\n")
out.write('##date Wed Aug 21 15:51:21 2013\n')
out.write('##source gbrowse gbgff gff3 dumper\n')
out.write('##sequence-region Contig7580.0:1..66022\n')
blastHandle=open('%s'%argv[1],'r')
j=0
for line in blastHandle:
	j+=1
	evalue=float(line.split()[10])
	query=line.split()[0]
	subj=line.split()[1]
	start=int(line.split()[8])
	stop=int(line.split()[9])
	matchlen=int(line.split()[3])
	matchpercent=float(line.split()[2])
	lenpercent='%s, %s aa %s percent'%(subj,matchlen,matchpercent)
	if stop < start:
		orientation = '-'
	else:
		orientation = '+'
	q_start=int(line.split()[6])
	q_stop=int(line.split()[7])
	out.write("%s\t%s\t%s\t%s\t%s\t.\t%s\t.\tID=test\n"%(query,subj,lenpercent,q_start,q_stop,orientation))
out.close()
blastHandle.close()
