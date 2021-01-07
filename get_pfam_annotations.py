#!/usr/bin/env python
import sys
from sys import argv

pfamHandle=open('h_mephisto_NR_PfamA_results_E_0.0001.txt','r')
namesHandle=open('hemizgous_genes_found.txt','r')
outHandle=open('hemizygous_genes_pfam_domains_E_0.0001.txt','w')

nameDict={}
for line in namesHandle:
	name=line.split()[1]
	if nameDict.has_key(name):
		print 'duplicate found %s'%name
	else:
		nameDict[name]=1
for line in pfamHandle:
	if line[:1]!='#':
		gene=line.split(' ')[0]
		if nameDict.has_key(gene):
			outHandle.write(line)

pfamHandle.close()
namesHandle.close()
outHandle.close()
	
