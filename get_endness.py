#!/usr/bin/env python
import sys
from sys import argv
import Bio
from Bio import SeqIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#./get_endness.py <coordinates.txt> <assembly.fasta>

coordHandle=open('%s'%argv[1],'r')
fastaHandle=open('%s'%argv[2],'r')

lenDict={}
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	length=len(seq_record.seq)
	contig='%s'%seq_record.id
	lenDict[contig]=length
percents=[]
for line in coordHandle:
	contig=line.split()[0]
	start=int(line.split()[1])
	#stop=int(line.split()[2])
	seqlen=lenDict[contig]
	print 'ratio %s'%(float(start)/float(seqlen))
	percent=((float(start)/float(seqlen))*100)
	if percent>50:
		percent=100-percent
	print 'percent is %s'%percent
	percents.append(percent)


plt.hist(percents, bins=20)
plt.savefig('%s_percent_length.pdf'%argv[1],format='pdf')
plt.close()
coordHandle.close()
fastaHandle.close()
