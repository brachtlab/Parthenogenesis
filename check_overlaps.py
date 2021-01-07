#!/usr/bin/env python
import sys
from sys import argv
#./check_overlaps.py <mephisto hemizygous_coordinates.txt> <gene_of_interest_coordinates.txt>

hemizHandle=open('%s'%argv[1],'r')
geneHandle=open('%s'%argv[2],'r')
hemizDict={}
for line in hemizHandle:
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	tuple=(start,stop)
	if hemizDict.has_key(contig):
		old_l=hemizDict[contig]
		old_l.append(tuple)
		hemizDict[contig]=old_l
	else:
		list=[]
		list.append(tuple)
		hemizDict[contig]=list
o=0
g=0
gDict={}
for line in geneHandle:
	g+=1
	contig=line.split()[0]
	begin=int(line.split()[1])
	end=int(line.split()[2])
	if hemizDict.has_key(contig):
		intervals=hemizDict[contig]
		for i in intervals:
			start=i[0]
			stop=i[1]
			if start<begin<stop or start<end<stop:
				gene=line.split()[3]
				print 'found an overlap. hemizygous interval = %s, gene = %s'%(i,line)
				#o+=1
				gDict[gene]=1
gs=gDict.keys()
for gn in gs:
	o+=1
print '%s genes processed and %s non-redundant overlap with hemizygous intervals.'%(g,o)
hemizHandle.close()
geneHandle.close()
