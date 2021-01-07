#!/usr/bin/env python
import sys
from sys import argv

#./get_interSNPcoverage.py <vcf file> <depth file>

vcfHandle=open('%s'%argv[1],'r')
depthHandle=open('%s'%argv[2],'r')
outHandle=open('%s_interval_coverage.txt'%argv[1],'w')
outHandle.write('contig\tinterval_start\tinterval_stop\tinterval_length\tinterval_coverage\n')
depth=[]
intervalDict={}
oldpos=-1
for line in vcfHandle:
	if line[:1]!='#':
		c=line.split()[0]
		pos=int(line.split()[1])
		if oldpos!=-1:
			interval=(oldpos,pos)
			if intervalDict.has_key(c):
				intervalDict[c].append(interval)
			else:
				newlist=[]
				newlist.append(interval)
				intervalDict[c]=newlist
		oldpos=pos
#print intervalDict
start=0
stop=0
length=1
running_coverage=0
valid='False'
for line in depthHandle:
#	print line
#	print 'start %s'%start
#	print 'stop %s'%stop
#	print 'running length %s'%length
#	print valid
	contig=line.split()[0]
	position=int(line.split()[1])
#	print 'current position %s'%position
	coverage=int(line.split()[2])
	if start<=position<=stop:
		running_coverage+=coverage
		length+=1
	else:#new interval
		interval_coverage=running_coverage/length
		if valid=='True':
			#print 'interval %s	%s	%s is %s long and has coverage %s'%(contig,start,stop,length,interval_coverage)
			#print 'final position %s'%(position-1)
			outHandle.write('%s	%s	%s	%s	%s\n'%(contig,start,stop,length,interval_coverage))
		length=1 #must account for the current value
		running_coverage=coverage#must account for current value
		if intervalDict.has_key(contig):
			intlist=intervalDict[contig]
		else:
			intlist=[(1,0)]
		valid='False'
		for i in intlist:#get new start/stop
			if i[0]<=position<=i[1]:
				start=i[0]
				stop=i[1]
				valid='True'
			
	
vcfHandle.close()
depthHandle.close()
outHandle.close()
