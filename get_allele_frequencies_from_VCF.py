#!/usr/bin/env python
import sys
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

inHandle=open('%s'%argv[1],'r')
frequencies=[]
unfolded_frequencies=[]
coverage=[]
for line in inHandle:
	if line[:1]!='#': #skip headers
		quality=float(line.split()[5])
		if quality>10:
			info=line.split()[7]
			items=info.split(';')
			for i in items:
				if i.split('=')[0]=='DP4':
					numberstring=i.split('=')[1]
					nums=numberstring.split(',')
					f_ref=int(nums[0])
					r_ref=int(nums[1])
					f_alt=int(nums[2])
					r_alt=int(nums[3])
					ref_cov=f_ref+r_ref
					alt_cov=f_alt+r_alt
					total_cov=ref_cov+alt_cov
					alt_freq=(float(alt_cov)/float(total_cov))
					unfolded_alt_freq=(float(alt_cov)/float(total_cov))
					if alt_freq>0.50:
						alt_freq=1-alt_freq#get minor allele freq
					if 120>total_cov>=60: 
						frequencies.append(alt_freq)
						unfolded_frequencies.append(unfolded_alt_freq)
						coverage.append(total_cov)
							
plt.hist(frequencies, bins=50)
plt.savefig("MAF_%s.pdf"%argv[1], dpi=300, format='pdf')
plt.close()
plt.hist(unfolded_frequencies, bins=50)
plt.savefig("unfolded_allele_freqs_%s.pdf"%argv[1], dpi=300, format='pdf')
plt.close()
plt.hist(coverage, bins=50)
plt.savefig("coverage_%s.pdf"%argv[1], dpi=300, format='pdf')
plt.close()
inHandle.close()
