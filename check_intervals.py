#!/usr/bin/env python
import sys
from sys import argv
#./check_intervals.py <back-mapped synteny file> <mephisto hemizygous> <NKZ hemizygous>

synHandle=open('%s'%argv[1],'r')
mepHandle=open('%s'%argv[2],'r')
nkzHandle=open('%s'%argv[3],'r')
meph_out=open('%s_within_syntenic.txt'%argv[2],'w')
nkz_out=open('%s_within_syntenic.txt'%argv[3],'w')
meph_synDict={}
nkz_synDict={}
mncrossDict={}
nmcrossDict={}
for line in synHandle:
	mephContig=line.split()[0]
	nkzContig=line.split()[1]
	meph_start=int(line.split()[7])
	meph_stop=int(line.split()[11])
	nkz_start=int(line.split()[16])
	nkz_stop=int(line.split()[20])
	if meph_stop<meph_start:
		print 'reversed interval found for meph!'
	if nkz_stop<nkz_start:
		print 'reversed interval for nkz'
	mcombo='%s\t%s\t%s'%(mephContig,meph_start,meph_stop)
	ncombo='%s\t%s\t%s'%(nkzContig,nkz_start,nkz_stop)
	mncrossDict[mcombo]=ncombo
	nmcrossDict[ncombo]=mcombo
	mep_interval=(meph_start,meph_stop)
	nkz_interval=(nkz_start,nkz_stop)
	if meph_synDict.has_key(mephContig):
		list=meph_synDict[mephContig]
		list.append(mep_interval)
		meph_synDict[mephContig]=list
	else:
		new_list=[]
		new_list.append(mep_interval)
		meph_synDict[mephContig]=new_list

	if nkz_synDict.has_key(nkzContig):
                list=nkz_synDict[nkzContig]
                list.append(nkz_interval)
                nkz_synDict[nkzContig]=list
        else:
                new_list=[]
                new_list.append(nkz_interval)
                nkz_synDict[nkzContig]=new_list
m=0
meph_out.write('contig\themiz_start\themiz_stop\themiz_len\tcoverage\tsyntenic_start\tsyntenic_stop\tsyntenic_contig\tsyntenic_star\tsyntenic_stop\n')
hDict={}
for line in mepHandle:
	contig=line.split()[0]
	begin=int(line.split()[1])
	end=int(line.split()[2])
	if meph_synDict.has_key(contig):
		syntenic_regions=meph_synDict[contig]
		for s in syntenic_regions:
			start=s[0]
			stop=s[1]
			if start<begin<stop and start<end<stop:#fully within syntenic region
				ncombo=mncrossDict['%s\t%s\t%s'%(contig,start,stop)]
				meph_out.write('%s\t%s\t%s\t%s\n'%(line.rstrip('\n'),start,stop,ncombo))
				m+=1
				hDict[ncombo]=1 #track regions
				
n=0
h=0
nkz_out.write('contig\themiz_start\themiz_stop\themiz_len\tcoverage\tsyntenic_start\tsyntenic_stop\tsyntenic_contig\tsyntenic_star\tsyntenic_stop\tcorresponding_hetero_homozyg_region?\n')
for line in nkzHandle:
	flag='NO'
        contig=line.split()[0]
        begin=int(line.split()[1])
        end=int(line.split()[2])
        if nkz_synDict.has_key(contig):
                syntenic_regions=nkz_synDict[contig]
                for s in syntenic_regions:
                        start=s[0]
                        stop=s[1]
                        if start<begin<stop and start<end<stop:#fully within syntenic region
				mcombo=nmcrossDict['%s\t%s\t%s'%(contig,start,stop)]
				if hDict.has_key('%s\t%s\t%s'%(contig,start,stop)):
					flag='YES'
					h+=1
                                nkz_out.write('%s\t%s\t%s\t%s\t%s\n'%(line.rstrip('\n'),start,stop,mcombo,flag))
                                n+=1
print 'for mephisto, %s syntenic hemizygous found and for NKZ332, %s. There were %s coincident homo/heterozygous syntenic regions.'%(m,n,h)
synHandle.close()
mepHandle.close()
nkzHandle.close()
meph_out.close()
nkz_out.close()
