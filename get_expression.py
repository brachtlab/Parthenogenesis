#!/usr/bin/env python
from Bio import SeqIO
from Bio import Seq
from Bio.Seq import Seq
import sys
from sys import argv

expHandle=open('filtered_labled_used_in_volcano_plot_2.csv','r')
fastaHandle=open('%s'%argv[1],'r') 
outHandle=open('%s_expression_data.csv'%argv[1],'w')
eDict={}
outHandle.write(expHandle.next())
for line in expHandle:
	#print line
	name=line.split(',')[1].strip('"')
	eDict[name]=line
u=0
j=0
x=0
uj=0
k=0
ke=0
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	x+=1
	tname=seq_record.id.split('.p')[0]
	if eDict.has_key(tname):
		j+=1
		outHandle.write(eDict[tname])
	else:
		print 'no expresssion data for %s'%tname


expHandle.close()
fastaHandle.close() 
outHandle.close()
