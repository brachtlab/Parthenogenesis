#!/usr/bin/python
from Bio import SeqIO
from Bio import Seq
import sys
from sys import argv
import random
inHandle_left=open("%s"%argv[1],"r")
outHandle_left=open("%s_%s_RANDOM.fastq"%(argv[1],argv[2]),"w")
x=0
left_sequences=[]
numitems=int(argv[2])#items we want
totalnum=int(argv[3])#items in file
m=0
z=0
for seq_record in SeqIO.parse(inHandle_left,"fastq"):
	x+=1
	z+=1
	if x%10000==0:
		print "processed %s thousand reads and %s thousand written"%(x/1000, m/1000)
	readname="%s"%seq_record.id
	randomnum=random.uniform(0,totalnum)
	if randomnum < numitems:
			if z < 1000:#store no more than 1000 items in list at a time
				left_sequences.append(seq_record)
			else:
				SeqIO.write(left_sequences,outHandle_left,"fastq")
				z=0 #reset
				left_sequences=[]#reset
			m+=1
if left_sequences:#check for empty, if not, write the remaining data
	SeqIO.write(left_sequences,outHandle_left,"fastq")
inHandle_left.close()
outHandle_left.close()	

