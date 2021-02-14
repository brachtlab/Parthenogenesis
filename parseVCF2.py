#!/usr/bin/env python
import sys
from sys import argv
#./parseVCF2.py <vcf file> 
vcfHandle=open('%s'%argv[1],'r')
outHandle=open('%s_columns.txt'%argv[1],'w')

outHandle.write("contig1\tcontig2\tstart_contig1\tstop_contig2\tSV_size\tSV_coverage\ttotal_coverage\t#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ttransIndel_calls.txt")

for line in vcfHandle:
	if line[:1]!='#':
		contig=line.split()[0]
		position=int(line.split()[1])
		vcf_ref=line.split()[3]
		vcf_alt=line.split()[4]
		info=line.split()[7]
		ilist=info.split(';')
		ao='null'
		dp='null'
		chr2='null'
		end='null'
		svlen='null'
		for i in ilist:
			if 'AO' in i:
				ao=i.split('=')[1]
			if 'DP' in i:
				dp=i.split('=')[1]
			if 'CHR2' in i:
                                chr2=i.split('=')[1]
			if 'END' in i:
                                end=i.split('=')[1]
			if 'SVLEN' in i:
                                svlen=i.split('=')[1]
		outHandle.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(contig,chr2,position,end,svlen,ao,dp,line))

vcfHandle.close()
outHandle.close()
