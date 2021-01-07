#!/usr/bin/env python
from Bio import SeqIO
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np

nRhHndle=open('all_normal.txt','r')
hRhHndle=open('all_hot.txt','r')
nHhHndle=open('hemiz_normal.txt','r')
hHhHndle=open('hemiz_hot.txt','r')
nR=[]
hR=[]
nH=[]
hH=[]
for line in nRhHndle:
	nR.append(float(line))
for line in hRhHndle:
	hR.append(float(line))
for line in nHhHndle:
	nH.append(float(line))
for line in hHhHndle:
	hH.append(float(line))	
normal=[]
normal.append(nR)
normal.append(nH)
hot=[]
hot.append(hR)
hot.append(hH)
box1=plt.boxplot(normal, positions=[1,3], whis=[15,85], showfliers=False, notch=True, patch_artist=True, labels=['all_normal','hemizy_normal'])
plt.setp(box1['boxes'], facecolor='lightblue')
box2=plt.boxplot(hot, positions=[2,4], whis=[15,85],showfliers=False, notch=True, patch_artist=True, labels=['all_hot','hemizy_hot'])
plt.setp(box2['boxes'], facecolor='pink')
plt.yscale('log')
plt.xticks([1,2,3,4],['normal','hot','normal','hot'])
plt.xlim(0.5,4.5)
#plt.ylim(1e-8,30)
plt.savefig('hemiz_boxplot_log_whis=15-85.pdf',format='pdf')
plt.show()
plt.close()

nRhHndle.close()
hRhHndle.close()
nHhHndle.close()
hHhHndle.close()
