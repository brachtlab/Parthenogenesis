#!/usr/bin/env python
import sys
from sys import argv

inHandle=open('hemizgous_genes_overlapping_CDS_found.txt','r')
pantherHandle=open('mephisto_pantherScore.out','r')
outHandle=open('hemizygous_overlappingCDS_pantherScore_subset','w')

dict={}
for line in pantherHandle:
	transcript=line.split()[0]
	if dict.has_key(transcript):
		print 'redundancy found'
	else:
		dict[transcript]=line

for line in inHandle:
	t=line.split()[1]
	if dict.has_key(t):
		outHandle.write(dict[t])
	else:
		print 'missing entry found!'

inHandle.close()
outHandle.close()
pantherHandle.close()
