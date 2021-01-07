#!/usr/bin/env python
import sys
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
from scipy import stats
np.random.seed(30301)
hemiz=[]
homoz=[]
h=0
o=0
x=0
inHandle=open('%s'%argv[1],'r')
hemizHandle=open('%s_hemizygous_intervals.txt'%argv[1],'w')
homozHandle=open('%s_gene_conversion_intervals.txt'%argv[1],'w')
inHandle.next()#skip header
for line in inHandle:
	length=int(line.split()[3])
	coverage=int(line.split()[4])
	if coverage<500:
		if length>=2000:
			x+=1
			hemiz.append(coverage)
			if coverage<65:
				hemizHandle.write(line)
				h+=1
			elif coverage>80:
				homozHandle.write(line)
				o+=1
		elif length < 500:
			x+=1
			homoz.append(coverage)
data=[]
data.append(homoz)
data.append(hemiz)
plt.violinplot(data, showmedians=True, showextrema=False)
plt.ylim(0,200)
plt.xticks([1,2],['under 500 bp','over 2000 bp'])
statistic,pvalue=stats.ttest_ind(homoz,hemiz,equal_var=False)
plt.savefig('under500_over2000_violinplot_p-value%s.png'%pvalue,format='png')
plt.close()
print 't-test p-value is %s'%pvalue
print 'written %s candidate hemizygous regions to file.'%h
print 'written %s canddiate gene conversion regions to file.'%o
print 'there were %s intervals <65 or >2000bp.'%x
inHandle.close()
hemizHandle.close()
homozHandle.close()
