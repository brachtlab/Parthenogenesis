#!/usr/bin/env python
import sys
from sys import argv

inHandle=open('%s'%argv[1],'r')
Dict={}
for line in inHandle:
	Dict[line]=1
keys=Dict.keys()
count=0
for k in keys:
	count+=1
print 'there were %s unique lines in file.'%count
inHandle.close()
