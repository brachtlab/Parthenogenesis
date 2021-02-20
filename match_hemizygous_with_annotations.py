#!/usr/bin/env python
import sys
from sys import argv

handle1=open('The16.txt_genes_overlapping_CDS_found.txt_genes_pfam_domains_E_0.0001.txt','r')
handle2=open('genes_hemizygous_coordinates.txt','r')
outHandle=open('The16_annotations_by_region.txt','w')
hDict={}
subDict={}
for line in handle2:
	t1=line.split()[0]
	t2=line.split()[1]
	if hDict.has_key(t2):
                print 'duplicate found in coord file. %s'%line
        else:
                hDict[t2]=line
		subDict[t2]=1
for line in handle1:
	gene=line.split()[0]
	if hDict.has_key(gene):
		outHandle.write('%s\t%s'%(hDict[gene].rstrip('\n'),line))
		subDict[gene]=2

no_annotations=subDict.keys()
for n in no_annotations:
	if subDict[n]==1:
		outHandle.write('%s\tno_annotation_found\n'%hDict[n].rstrip('\n'))
		


handle1.close()
handle2.close()
outHandle.close()
