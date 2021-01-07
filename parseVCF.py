#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
#./parseVCF <vcf file> <fasta assembly>
vcfHandle=open('%s'%argv[1],'r')
fastaHandle=open('%s'%argv[2],'r')
outHandle=open('%s_context_for_restriction_enzyme_search.txt'%argv[1],'w')
Dict={}
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	Dict['%s'%seq_record.id]=seq_record	
outHandle.write("contig\tposition\tREF\tALT\tsequence_context_ref\tsequence_context_alt\n")
for line in vcfHandle:
	if line[:1]!='#':
		contig=line.split()[0]
		position=int(line.split()[1])
		vcf_ref=line.split()[3]
		vcf_alt=line.split()[4]
		qual=float(line.split()[5])
		if qual>=100:
			if Dict.has_key(contig):
				sequence=Dict[contig].seq
				s=sequence[position-7:position+6]
				t=s[:6]+vcf_alt+s[7:]
				exact=sequence[position-1:position]
				#print 'pulled %s from sequence, %s predicted,%s is context'%(exact,vcf_ref,s)
				outHandle.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(contig,position,exact,vcf_alt,s,t))
			else:
				print 'found non-matching contig: %s'%contig

vcfHandle.close()
fastaHandle.close()
outHandle.close()
