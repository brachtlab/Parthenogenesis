#!/usr/bin/env python
import sys
from sys import argv

inHandle=open('%s'%argv[1],'r')
outHandle=open('%s_renamed.txt'%argv[1],'w')
x=0
for line in inHandle:
	x+=1
	items=line.split('\t')[1:]
	ident=line.split()[0]
	outHandle.write('%s'%x)
	for item in items:
		outHandle.write('\t%s'%item)
	#outHandle.write('\n')	

inHandle.close()
outHandle.close()
