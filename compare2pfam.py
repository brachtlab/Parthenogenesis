#!/usr/bin/python
from Bio import SeqIO
from Bio import Seq
from Bio.Seq import Seq
import sys
from sys import argv
#./compare2pfam.py <x-pfam_output> <y-pfam_output>
xHandle=open("%s"%argv[1],"r")
yHandle=open("%s"%argv[2],"r")
outHandle=open("X_%s_Y_%s.txt"%(argv[1],argv[2]),'w')
xDict={}
yDict={}
#pfam domtblout files have 3 header lines that start with #
for line in xHandle:
	if line[:1]!='#':
		part1=line.split()[3]
		part2=line.split()[4]
		pfid=part1+'_'+part2
		if xDict.has_key(pfid):
			xDict[pfid]+=1
		else:
			xDict[pfid]=1
for line in yHandle:
        if line[:1]!='#':
                part1=line.split()[3]
                part2=line.split()[4]
                pfid=part1+'_'+part2
                if yDict.has_key(pfid):
                        yDict[pfid]+=1
                else:
                        yDict[pfid]=1
outHandle.write('Pfam\t%s\t%s\n'%(argv[1],argv[2]))
xkeys=xDict.keys()
for x in xkeys:
	if yDict.has_key(x):
		outHandle.write('%s\t%s\t%s\n'%(x,xDict[x],yDict[x]))
		del xDict[x]#now remove this element from both dictionaries
		del yDict[x]
xunique=xDict.keys()
if xunique:#check if empty
	for xu in xunique:
		outHandle.write('%s\t%s\t0\n'%(xu,xDict[xu]))
yunique=yDict.keys()
if yunique:#check if empty
        for yu in yunique:
                outHandle.write('%s\t0\t%s\n'%(yu,yDict[yu]))
xHandle.close()
yHandle.close()
outHandle.close()
