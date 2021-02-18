#!/usr/bin/env python
import sys
from sys import argv
import Bio
from Bio import SeqIO

#the goal of this script is to implement a series of filters for structural problems with assembly. 

#Filter for:
# 1.  sequences with zero coverage region (over 20bp)
# 2.  or too close to contig ends (less than 2kb from either end)
# 3.  or with low coverage left or right flanks (flanking 2kb), overall <85x or 20bp with zero coverage.
#./meta_filter.py <depth file> <coordinates.txt> <assembly.fasta> note, coordinates have contig,start,stop with tab delimiting. Depthfile is produced by samtools depth command.

coordHandle=open('%s'%argv[2],'r')
fastaHandle=open('%s'%argv[3],'r')
outHandle1=open('%s_passed_meta.txt'%argv[2],'w')
outHandle2=open('%s_failed_meta.txt'%argv[2],'w')
testhandle=open('testOut.txt','w')
lenDict={}
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	length=len(seq_record.seq)
	contig='%s'%seq_record.id
	lenDict[contig]=length

#intervalDict={}
x=0
for line in coordHandle:
	x+=1
	print 'processed %s line from coordHandle'%x
	meta_flag=0
	#h_length=1
	reason='null'
	contig=line.split()[0]
	print 'contig is %s'%contig
	start=int(line.split()[1])
	stop=int(line.split()[2])
	contig_length=lenDict[contig]
	if stop+2000>contig_length:#not enough room on right flank
		meta_flag=1
		reason='right_too_short'
	if start<2000:#not enough room on left flank
		meta_flag=1
		reason='left_too_short'
	if meta_flag==0:
	        h_running_coverage=0
	        l_running_coverage=0
	        r_running_coverage=0
		l_under5=0
		h_under5=0
		r_under5=0
		depthHandle=open('%s'%argv[1],'r')
		for l in depthHandle:
			c=l.split()[0]
			position=int(l.split()[1])
			coverage=int(l.split()[2])
			if c==contig:
				#print l
				#print 'reason is %s'%reason
				if (start-2000)<=position<=start:#left flank
					l_running_coverage+=coverage
					#print 'left flank %s'%l
	                                #print 'reason is %s'%reason
					#testhandle.write(l)
					if coverage<5:
						l_under5+=1
						#reason='left_flank_coverage_<5'
				if start<=position<=stop:#in hemizygous region
					if coverage<5:
						h_under5+=1
						#meta_flag=1
						#reason='hemizygous_coverage_<5'
				if stop<=position<=stop+2000:#right flank
					#print 'right flank %s'%l
                                	#print 'reason is %s'%reason
					r_running_coverage+=coverage
					if coverage<5:
						r_under5+=1
						#meta_flag=1
						#reason='right_flank_coverage_<5'
				if position>=stop+2000:
					break#done with depth file
		depthHandle.close()
		left_coverage=l_running_coverage/2000
		right_coverage=r_running_coverage/2000
		print 'for line %s'%line
		print 'left flank coverage is %s'%left_coverage
		print 'right flank coverage is %s'%right_coverage
		if left_coverage<85:
			meta_flag=1
			reason='left_coverage_low'
		if right_coverage<85:
			meta_flag=1
                        reason='right_coverage_low'
		if l_under5>20:
			meta_flag=1
			reason='left_flank_coverage_>20bp <5 reads'
		if h_under5>20:
			meta_flag=1
			reason='heterozygous_coverage_>20bp <5 reads'
		if r_under5>20:
			meta_flag=1
			reason='right_flank_coverage_>20bp <5 reads'
		print 'reason is %s'%reason
		print 'meta_flag is %s'%meta_flag

	if meta_flag==1:
		outHandle2.write('%s\t%s'%(reason,line))
	else:
		outHandle1.write(line)			
	
coordHandle.close()
fastaHandle.close()
outHandle1.close()
outHandle2.close()
testhandle.close()
