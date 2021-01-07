#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#nhmer-to-gff.py <pfam_tblout.txt>
pfamHandle=open('%s'%argv[1],'r')
outHandle=open('%s.gff'%argv[1],'w')

outHandle.write("##gff-version 3\n")
x=0
for line in pfamHandle:
	if line[:1]!='#':
		x+=1
		contig=line.split()[0]
		n=line.split()[2]
		id=line.split()[3]
		name=n+'_'+id
		start=int(line.split()[6])
		stop=int(line.split()[7])
		evalue=line.split()[12]
		strand=line.split()[11]
		outHandle.write("%s\t%s\t%s_%s\t%s\t%s\t.\t%s\t.\tID=test;Name=%s_%s\n"%(contig,name,name,evalue,start,stop,strand,name,evalue))
		
pfamHandle.close()
outHandle.close()
