#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
#./find_clip-cliffs.py <sam_file_only_soft_clip_reads.sam> <text_file_of_hemizygous_coordinates.txt> #note, coord file is contig,start,stop, tab-delimited, other stuff doesn't matter 
#note, produce sam file using retain_softClip_reads.py
inHandle=open('%s'%argv[1],'r')
outHandle=open('%s_no-SV-detected.txt'%argv[1],'w')
outHandle2=open('%s_SV-detected.txt'%argv[1],'w')
S3Dict={}
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
			if S3Dict.has_key(combo):
				S3Dict[combo]+=1
			else:
				S3Dict[combo]=1
S3keys=S3Dict.keys()
mc_positionDict={}
for c in S3keys:
	num_reads=S3Dict[c]
	contig=c.split('^')[0]
	pos=int(c.split('^')[1])
	if num_reads > 50:
		if mc_positionDict.has_key(contig):
			positions=mc_positionDict[contig]
			positions.append(pos)
			mc_positionDict[contig]=positions
		else:
			newlist=[]
			newlist.append(pos)
			mc_positionDict[contig]=newlist

inHandle.close()
j=0
S5Dict={}
inHandle=open('%s'%argv[1],'r')
for line in inHandle:
	if line[:1]!='@':
		j+=1
                if j%10000==0:
                        print 'processed %s thousand reads on second read-through of file.'%(j/1000)
	        position=int(line.split()[3])
        	contig=line.split()[2]
		sequence=line.split()[9]
		cigar=line.split()[5]
		if cigar[-1:]=='M':#then is a clip-match
			combo=contig+'^'+'%s'%position
			if S5Dict.has_key(combo):
				S5Dict[combo]+=1
			else:
				S5Dict[combo]=1

cm_positionDict={}
S5keys=S5Dict.keys()
for c in S5keys:
        num_reads=S5Dict[c]
        contig=c.split('^')[0]
        pos=int(c.split('^')[1])
        if num_reads > 50:
                if cm_positionDict.has_key(contig):
                        positions=cm_positionDict[contig]
                        positions.append(pos)
                        cm_positionDict[contig]=positions
                else:
                        newlist=[]
                        newlist.append(pos)
                        cm_positionDict[contig]=newlist
mcstartlist=[]
mcstoplist=[]
cmstartlist=[]
cmstoplist=[]
hemiHandle=open('%s'%argv[2],'r')
for line in hemiHandle:
	sv=0
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	if mc_positionDict.has_key(contig):
		mc_list=mc_positionDict[contig]
		start_closest=min(mc_list, key=lambda x:abs(x-start))
		distance=abs(start-start_closest)
		if distance<200:
			sv=1
		mcstartlist.append(distance)
		#mc_list.sort()
		#outHandle.write('%s\t%s\t%s\t%s\n'%(contig,start,distance,mc_list))
		stop_closest=min(mc_list, key=lambda x:abs(x-stop))
		distance=abs(stop-stop_closest)
		mcstoplist.append(distance)
	if cm_positionDict.has_key(contig):
                cm_list=cm_positionDict[contig]
                start_closest=min(cm_list, key=lambda x:abs(x-start))
                distance=abs(start-start_closest)
                cmstartlist.append(distance)
                stop_closest=min(cm_list, key=lambda x:abs(x-stop))
                distance=abs(stop-stop_closest)
		if distance<200:
			sv=1
		cmstoplist.append(distance)
	if sv==0:
		outHandle.write(line)
	else:
		outHandle2.write(line)

plt.hist(mcstartlist,bins=20, range=[0,1000])
#plt.xlim([0,3000])
plt.savefig("nearest_match_clip_50_reads_START-hemizygous-region.pdf", format='pdf')
plt.close()		
plt.hist(mcstoplist,bins=20, range=[0,1000])
#plt.xlim([0,3000])
plt.savefig("nearest_match_clip_50_reads_STOP-hemizygous-region-control.pdf", format='pdf')
plt.close()
plt.hist(cmstartlist,bins=20,range=[0,1000])
#plt.xlim([0,3000])
plt.savefig("nearest_clip_match_50_reads_START-hemizygous-region-control.pdf", format='pdf')
plt.close()             
plt.hist(cmstoplist,bins=20,range=[0,1000])
#plt.xlim([0,3000])
plt.savefig("nearest_clip_match_50_reads_STOP-hemizygous-region.pdf", format='pdf')
plt.close()
inHandle.close()
outHandle.close()
hemiHandle.close()
outHandle2.close()
