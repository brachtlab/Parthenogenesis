#!/usr/bin/env python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
from sys import argv

coordHandle=open('mephisto_omega_mv_no_indels_noheader.vcf_interval_coverage.txt_hemizygous_intervals.txt','r')
#coordHandle=open('ts.txt','r')
outHandle=open('hemizgous.gff','w')
hsp70Handle=open('hemiz_genes_Hsp70_hmmer_out_eval_1e-6.txt','r')
aig1Handle=open('hemiz_genes_AIG1_hmmer_out_eval_1e-6.txt','r')
x=0
hDict={}
aDict={}
for line in hsp70Handle:
	if line[:1]!='#':
		gene=line.split()[0]
		hDict[gene]=1
for line in aig1Handle:
 	if line[:1]!='#':
		gene=line.split()[0]
		aDict[gene]=1

for line in coordHandle:
	x+=1
	j=0
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	gffHandle=open("halicephalobus_mephisto.PRJNA528747.WBPS15.annotations.gff3",'r')
	for line in gffHandle:
		j+=1
		if line[:1]!='#':
			begin=int(line.split()[3])
			end=int(line.split()[4])
			gff_contig=line.split()[0]
			new_contig=gff_contig+'_'+'%s'%start+'-'+'%s'%stop
			if gff_contig==contig:
				if begin>stop+100000:
					break
				#print 'interval is %s from %s to %s and line is %s'%(contig,start,stop,line)
				if start<=begin<=stop or start<=end<=stop:
					#print 'within interval!\n %s'%line
					if start<begin:
						new_begin=begin-start
					else:
						new_begin=0
					if stop<end:
						new_end=stop
					else:
						new_end=end-start
					items=line.split('\t')
					items[3]='%s'%new_begin
					items[4]='%s'%new_end
					items[0]=new_contig
					separator='\t'
					if len(line.split())>=9:
						tems=line.split()[8]
						its=tems.split(':')
						for i in its:
							id=i.split(';')[0]
							#print id
							if hDict.has_key(id):
								print 'found Hsp70, %s'%id
								newtems=tems+';Alias=Hsp70 family'
								items[8]=newtems
								#print items[8]
								#print gff_contig
							elif aDict.has_key(id):
								print 'found aig1, %s'%id
								newtems=tems+';Alias=AIG1 family'
								items[8]=newtems
					newline=separator.join(items)					
					outHandle.write(newline+'\n')
				#else:
				#	print 'NOT found to be within interval. %s'%line

	gffHandle.close()
	print 'processed line %s from input coordinate file and %s lines from gff file.'%(x,j)

outHandle.close()
coordHandle.close()
hsp70Handle.close()
aig1Handle.close()
