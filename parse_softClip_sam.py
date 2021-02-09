#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
from Bio.Align.Applications import MuscleCommandline
from Bio.Align import AlignInfo
from Bio import AlignIO
muscle_exe='/usr/local/muscle3.8.31_i86darwin64'
#./parse_softClip_sam.py <sam_file_only_soft_clip_reads.sam> 
#note, produce sam file using retain_softClip_reads.py

inHandle=open('%s'%argv[1],'r')
#first step = get list of sites with structural aberrations
outHandle=open('%s_over5_over2kb_sameContig_soft-clippped-sequence-matches.txt'%argv[1],'w')
S3Dict={}
rDict={}
j=0
for line in inHandle:
	if line[:1]!='@':
		j+=1
		if j%10000==0:
			print 'processed %s thousand reads on first read-through of file.'%(j/1000)
		position=int(line.split()[3])
		read=line.split()[0]
		contig=line.split()[2]
		cigar=line.split()[5]
		revcigar=cigar[::-1]
		length=len(line.split()[9])
		sequence=line.split()[9]
		if cigar[-1:]=='S':#then softclip at 3' end
			revoffset=revcigar.split('M')[0].lstrip('S')
			offset=int(revoffset[::-1])#reverse back
			delta=length-offset
			realposition=position+delta
			combo=contig+'^'+'%s'%realposition
			soft_clipped=sequence[delta:]
			if S3Dict.has_key(combo):
				S3Dict[combo]+=1
				rlist=rDict[combo]
				rlist.append(soft_clipped)
				rDict[combo]=rlist
			else:
				S3Dict[combo]=1
				newlist=[]
				newlist.append(soft_clipped)
				rDict[combo]=newlist
S3keys=S3Dict.keys()
consensusDict={}
FiveSeqDict={}
for c in S3keys:
	num_reads=S3Dict[c]
	soft_clipped_list=rDict[c]
	contig=c.split('^')[0]
	pos=c.split('^')[1]
	x=0
	if num_reads > 5:
		temp_handle=open('temp.fasta','w')
		for s in soft_clipped_list:
			x+=1
			temp_handle.write('>%s\n%s\n'%(x,s))
		temp_handle.close()
		muscle_cline=MuscleCommandline(muscle_exe,input='temp.fasta',out='%s^%s_aligned.fasta'%(contig,pos),diags=True,maxiters=1,log='.align_log.txt')
		muscle_cline()
		alignment=AlignIO.read(open('%s^%s_aligned.fasta'%(contig,pos)),'fasta')#read in the alignment
		summary_align=AlignInfo.SummaryInfo(alignment)
		consensus='%s'%summary_align.dumb_consensus(threshold=0.9,require_multiple=1, ambiguous='')#don't show ambiguous and require more than 1 sequence to include.
		if len(consensus) > 60:
			shortconsensus=consensus[:60]
			consensusDict[shortconsensus]='%s^%s'%(contig,pos)
			FiveSeqDict['%s^%s'%(contig,pos)]=shortconsensus	
#print consensusDict
inHandle.close()
j=0
inHandle=open('%s'%argv[1],'r')
matchDict={}
crossDict={}
ThreeSeqDict={}
for line in inHandle:
	if line[:1]!='@':
		j+=1
                if j%10000==0:
                        print 'processed %s thousand reads on second read-through of file.'%(j/1000)
	        position=int(line.split()[3])
        	contig=line.split()[2]
		sequence=line.split()[9]
		cigar=line.split()[5]
		if cigar[-1:]=='M':#then want to check for consensus
			clip=int(cigar.split('S')[0])
			scan=sequence[clip:]#look at matching portion of read
			consensi=consensusDict.keys()
			for c in consensi:
				if c in scan:
					ThreeSeqDict['%s^%s'%(contig,position)]=scan
					crossDict['%s^%s'%(contig,position)]=consensusDict[c]#store position of 5' end of match
					if matchDict.has_key('%s^%s'%(contig,position)):
						matchDict['%s^%s'%(contig,position)]+=1
					else:
						matchDict['%s^%s'%(contig,position)]=1
outHandle.write('upstream contig\tupstream position\tupstream readcount\tdownstream contig\tdownstream position\tdownstream readcount\n')
matches=matchDict.keys()
allHandle=open('%s_all_matches.txt'%argv[1],'w')
allHandle.write('upstream contig\tupstream position\tupstream readcount\tupstream sequence\tdownstream contig\tdownstream position\tdownstream readcount\tdownstream sequence\n')
for m in matches:
	upstream=crossDict[m]
	upcontig=upstream.split('^')[0]
	uppos=int(upstream.split('^')[1])
	upnum=S3Dict['%s^%s'%(upcontig,uppos)]
	upseq=FiveSeqDict[upstream]
	downstream=m
	downcontig=downstream.split('^')[0]
	downpos=int(downstream.split('^')[1])
	downseq=ThreeSeqDict[downstream]
	allHandle.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(upcontig,uppos,upnum,upseq,downcontig,downpos,matchDict[m],downseq))
	if upcontig==downcontig:
		size=downpos-uppos
		if size>2000:#require 2kb
			if matchDict[m]>5: #high confidence
				outHandle.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(upcontig,uppos,upnum,upseq,downcontig,downpos,matchDict[m],downseq))

inHandle.close()
outHandle.close()
allHandle.close()
