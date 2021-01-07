#!/usr/bin/env python
import sys
from sys import argv
#./back_name.py <orthologous blocks file> <HMEP name mapping.txt> <HNKZ name mapping.txt>
inHandle=open('%s'%argv[1],'r')
outHandle=open('%s_back-mapped-names.txt'%argv[1],'w')
mepHandle=open('%s'%argv[2],'r')
nkzHandle=open('%s'%argv[3],'r')

mepDict={}
nkzDict={}

for line in mepHandle:
	original=line.split()[0]
	n=int(line.split()[1])
	new=n-1
	mepDict[new]=original

for line in nkzHandle:
	original=line.split()[0]
        n=int(line.split()[1])
        new=n-1
        nkzDict[new]=original
for line in inHandle:
	hnum=int(line.split()[0])
	nkznum=int(line.split()[1])
	if mepDict.has_key(hnum):
		meph=mepDict[hnum]
	else:
		meph='unknown'
	if nkzDict.has_key(nkznum):
		nkz=nkzDict[nkznum]
	else:
		nkz='unknown'
	outHandle.write('%s\t%s\t%s'%(meph,nkz,line))

inHandle.close()
outHandle.close()
mepHandle.close()
nkzHandle.close()
