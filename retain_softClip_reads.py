#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

#./retain_softClip_reads.py <sam file input>
#NOTE: will generate a sam file with only soft-clipped, mapped reads retained.
x=0
inHandle=open("%s"%argv[1],"r")
outHandle=open("%s_mapped_softClipped_reads_only.sam"%argv[1],"w")
for line in inHandle:
	x+=1
	if x%100000==0:
		print "processed %s lines from file"%x
	if line[:1] != "@":
                readflag=line.split()[1]
		colons=readflag.count(':')
		if colons==0:
	                binstring=bin(int(readflag))
	                reversebinstring=binstring[::-1]
	                bpos=reversebinstring.find("b")
	                binstringclip=reversebinstring[:bpos]
	                length=len(binstringclip)
	                flag=binstringclip.ljust(11,'0')
	                unmapped=int(flag[2])
		else:
			unmapped=1
                if unmapped==1:
			pass
		else:
			cigar=line.split()[5]
			if 'S' in cigar:			
				outHandle.write(line)
	else:
		outHandle.write(line)	
inHandle.close()
outHandle.close()

