#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#parse-dfam.py <pfam_tblout.txt> <fasta_of_dfam_query>
pfamHandle=open('%s'%argv[1],'r')
outHandle_contigs=open('%s_contig_summary_statistics.txt'%argv[1],'w')
outHandle_elements=open('%s_element_summary_statistics.txt'%argv[1],'w')
fastaHandle=open('%s'%argv[2],'r')
contigDict={}
elementDict={}
contigs={}
x=0
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	contig='%s'%seq_record.id
	contigs[contig]=1

for line in pfamHandle:
	if line[:1]!='#':
		x+=1
		contig=line.split()[0]
		n=line.split()[2]
		id=line.split()[3]
		name=n+'_'+id
		evalue=line.split()[12]
		tuple=(name,evalue)
		tuple2=(contig,evalue)
		if contigDict.has_key(contig):
			l=contigDict[contig]
			l.append(tuple)
		else:
			new_l=[]
			new_l.append(tuple)
			contigDict[contig]=new_l
		if elementDict.has_key(name):
			m=elementDict[name]
			m.append(tuple2)
		else:
			new_m=[]
			new_m.append(tuple2)
			elementDict[name]=new_m

cs=contigDict.keys()
outHandle_contigs.write('contig\tnumber_elements\telement_names\n')
for c in cs:
	x=0
	elist=contigDict[c]
	string=''
	for e in elist:
		x+=1
		string=string+' ; '+e[0]+'_'+e[1]
	outHandle_contigs.write('%s\t%s\t%s\n'%(c,x,string))
	if contigs.has_key(c):
		del contigs[c]#remove
nr=contigs.keys()
for n in nr:
	outHandle_contigs.write('%s\t0\tnone\n'%n)

outHandle_elements.write('element\tnumber_contigs_nr\tnumber_hits\tcontigs\n')
elements=elementDict.keys()
for e in elements:
	x=0
	j=0
	clist=elementDict[e]
	print clist
	string=''
	Dict={}
	for c in clist:
		j+=1
		string=string+' ; '+c[0]+'_'+c[1]
		Dict[c[0]]=1
	nrcs=Dict.keys()
	s=''
	for nrc in nrcs:#get_nonredundant contigs
		x+=1
		s=s+' ; '+nrc	
	outHandle_elements.write('%s\t%s\t%s\t%s\n'%(e,x,j,s))		
		


pfamHandle.close()
outHandle_contigs.close()
outHandle_elements.close()
fastaHandle.close()
