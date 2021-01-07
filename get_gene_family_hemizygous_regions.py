#!/usr/bin/env python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
from sys import argv
#NOTE: use a text file of gene names with only gene names delimited by \n
#./get_gene_family_hemizygous_regions.py <text file of gene names only>

hsp70_handle=open('%s'%argv[1],'r')
outHandle=open('%s_hemizygous_regions.txt'%argv[1],'w')
hemizygous_gene_handle=open('genes_hemizygous_coordinates.txt','r')

Dict={}
x=0
for line in hsp70_handle:
	Dict[line.rstrip('\n')]=1
for line in hemizygous_gene_handle:
	transcript=line.split()[1]
	gene=line.split()[0]
	contig=line.split()[2]
	start=int(line.split()[3])
	stop=int(line.split()[4])
	if Dict.has_key(gene) or Dict.has_key(transcript):
		x+=1
		outHandle.write('%s\t%s\t%s\n'%(contig,start,stop))
	if Dict.has_key(gene):
		del Dict[gene]
	if Dict.has_key(transcript):
		del Dict[transcript]

print 'found %s'%x
print 'not found: %s'%Dict
hsp70_handle.close()
hemizygous_gene_handle.close()
outHandle.close()
