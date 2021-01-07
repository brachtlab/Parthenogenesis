#!/usr/bin/env python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
from sys import argv

inHandle=open("halicephalobus_mephisto.PRJNA528747.WBPS15.annotations.gff3",'r')
genomeHandle=open("mephisto_omega.fasta",'r')
coordHandle=open('mephisto_omega_mv_no_indels_noheader.vcf_interval_coverage.txt_hemizygous_intervals.txt','r')
outHandle=open('hemizgous_genes_overlapping_CDS_found.txt','w')
geneCoordHandle=open('genes_hemizygous_coordinates.txt','w')
noGeneHandle=open('hemizygous_no_genes.txt','w')
contigDict={}
for item in SeqIO.parse(genomeHandle,'fasta'):
	contigDict[item.id]=item.seq
hemizDict={}
subtractDict={}
x=0
for line in coordHandle:
	x+=1
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	tuple=(start,stop)
	triple='%s_%s_%s'%(contig,start,stop)
	subtractDict[triple]=1
	if hemizDict.has_key(contig):
		oldlist=hemizDict[contig]
		oldlist.append(tuple)
		hemizDict[contig]=oldlist
	else:
		newlist=[]
		newlist.append(tuple)
		hemizDict[contig]=newlist
geneNumber=len(hemizDict.keys())
print "the coordinate input file has %s contigs and %s hemizygous regions."%(geneNumber,x)
e=0
c=[]#cds coordinate list
for line in inHandle:
	if line!='#\n' and line[:3]!='##g' and line[:3]!='##s'and line !=' \n':
		#print line
		if line[:3]=='###':
			if c:#resolves to false if empty:
				c.sort()
				#print 'c is %s'%c
				begin=int(c[0])
				c.sort(reverse=True)
				end=int(c[0])
			else:
				begin=-1
				end=-1
			#print 'begin %s and end %s'%(begin,end)
			c=[]#reset cds list
			if hemizDict.has_key(contig):
				intervals=hemizDict[contig]
				for i in intervals:
					start=i[0]
					stop=i[1]
					tr='%s_%s_%s'%(contig,start,stop)
					if start<begin<stop or start<end<stop:#indicates an overlapping transcript
						#print 'line is %s'%line.split()
						#items=line.split()[8]
						#print 'items are %s'%items
						g=items.split(';')[1]
						t=items.split(';')[0]
						#print 'gene %s'%g
						#print 'transcript %s'%t
						transcript=t.split(':')[1]
						gene=g.split(':')[1]
						outHandle.write('%s\t%s\n'%(gene,transcript))
						geneCoordHandle.write('%s\t%s\t%s\t%s\t%s\n'%(gene,transcript,contig,start,stop))
						e+=1
						#print tr
						if subtractDict.has_key(tr):
							#print 'found match %s'%t
							del subtractDict[tr]
		elif line.split()[2]=='CDS':
			first=int(line.split()[3])
			last=int(line.split()[4])
			c.append(first)
			c.append(last)
			contig=line.split()[0]
		elif line.split()[2]=='mRNA':
			 items=line.split()[8]

print '%s genes found and written to file.'%e

print '%s hemizygous with no genes are %s'%(len(subtractDict),subtractDict)
keys=subtractDict.keys()
#print keys
for k in keys:
	#print subtractDict[k]
	noGeneHandle.write('%s\n'%k)
outHandle.close()
coordHandle.close()
inHandle.close()
genomeHandle.close()
noGeneHandle.close()
geneCoordHandle.close()
