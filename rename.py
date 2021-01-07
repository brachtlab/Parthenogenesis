#!/usr/bin/env python
import sys
from sys import argv

inHandle=open('%s'%argv[1],'r')
outHandle=open('%s_renamed.txt'%argv[1],'w')
x=0
identDict={}
for line in inHandle:
	x+=1
	items=line.split('\t')[1:]
	ident=line.split()[0]
	if identDict.has_key(ident):
		print 'redundant protein found %s, assigned number %s'%(ident,identDict[ident])
		outHandle.write('%s'%identDict[ident])
                for item in items:
                        outHandle.write('\t%s'%item)
	else:
		identDict[ident]=x#the number is the first time it's encountered
		outHandle.write('%s'%x)
		for item in items:
			outHandle.write('\t%s'%item)
	#outHandle.write('\n')	

inHandle.close()
outHandle.close()
