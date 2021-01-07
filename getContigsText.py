#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#getContigs.py <assemblyfile> <textfile_delimited_by_\n>
scafHandle=open('%s'%argv[2],'r')
outHandle=open("%s.fasta"%argv[2],'w')
nc_outHandle=open('%s_potential_noncoding.txt'%argv[2],'w')
genome_handle=open("%s"%argv[1],"r")
scafDict={}
x=0
y=0
for line in scafHandle:
	x+=1
	name=line.split('.p')[0]
	scafDict[name]=1
print scafDict
for seq_record in SeqIO.parse(genome_handle,"fasta"):
	seqlength=len(seq_record.seq)
	i="%s"%seq_record.id
	#ident=i.split('.p')[0]
	#print ident
	if scafDict.has_key(i):
		y+=1
		last=seq_record.seq[-1:]
		#print last
		if last=='*':
			sequence=seq_record.seq[:-1]
			print 'pre-trim %s'%seq_record.seq
			print 'post-trim %s'%sequence
		else:
			sequence=seq_record.seq
		outHandle.write(">%s\n%s\n"%(i,sequence))
		print "found it!"
		del scafDict[i]
print '%s sequences found and written out of %s total'%(y,x)
print 'not found:'
#print scafDict
for key in scafDict.keys():
	nc_outHandle.write('%s\n'%key)
		
genome_handle.close()
outHandle.close()
nc_outHandle.close()
