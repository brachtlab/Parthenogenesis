#!/usr/bin/env python
import sys
from sys import argv

pfamHandle=open('h_mephisto_NR_PfamA_results_E_0.0001.txt','r')
namesHandle=open('%s'%argv[1],'r')
outHandle=open('%s_genes_pfam_domains_E_0.0001.txt'%argv[1],'w')

nameDict={}
for line in namesHandle:
	name1=line.split()[0]
	name2=line.split()[1]
	if nameDict.has_key(name1):
		print 'duplicate found %s'%name1
	else:
		nameDict[name1]=1
	if nameDict.has_key(name2):
                print 'duplicate found %s'%name2
        else:
                nameDict[name2]=2

for line in pfamHandle:
	if line[:1]!='#':
		gene=line.split(' ')[0]
		if nameDict.has_key(gene):
			outHandle.write(line)

pfamHandle.close()
namesHandle.close()
outHandle.close()
	
