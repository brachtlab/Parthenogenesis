#!/usr/bin/env python
import sys
import Bio
from Bio import SeqIO
from sys import argv
#./extract.py <coordinate file> <fasta>
inHandle=open('%s'%argv[1],'r')
sequenceHandle=open('%s'%argv[2],'r')
outHandle=open('%s_sequences.fasta'%argv[1],'w')
seqDict={}
for seq_record in SeqIO.parse(sequenceHandle,'fasta'):
	name=seq_record.id
	seqDict[name]=seq_record
for line in inHandle:
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	if seqDict.has_key(contig):
		sequence=seqDict[contig].seq[start:stop]
		outHandle.write('>%s_%s-%s\n%s\n'%(contig,start,stop,sequence))
inHandle.close()
outHandle.close()
sequenceHandle.close()
