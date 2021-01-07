#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
from operator import xor
#./get_differential_restriction_sites.py <input context file> <enzyme recognition site>
recognition_sequence='%s'%argv[2]
inHandle=open('%s'%argv[1],'r')
inHandle.next()#skip header
outHandle=open('%s_restriction_sites_%s.txt'%(argv[1],recognition_sequence),'w')
for line in inHandle:
	string1=line.split()[4]
	string2=line.split()[5]
	if xor(recognition_sequence in string1, recognition_sequence in string2):
		outHandle.write(line)

inHandle.close()
outHandle.close()


