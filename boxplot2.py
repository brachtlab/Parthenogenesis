#!/usr/bin/env python
from Bio import SeqIO
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np

norm70handle=open('hsp70_normal.txt','r')
hot70handle=open('hsp70_hot.txt','r')
nRhandle=open('rest_normal.txt','r')
hRhandle=open('rest_hot.txt','r')
nAhandle=open('aig1_normal.txt','r')
hAhandle=open('aig1_hot.txt','r')
n70=[]
h70=[]
nR=[]
hR=[]
nA=[]
hA=[]
for line in norm70handle:
	n70.append(float(line))
for line in hot70handle:
	h70.append(float(line))
for line in nRhandle:
	nR.append(float(line))
for line in hRhandle:
	hR.append(float(line))
for line in nAhandle:
	nA.append(float(line))
for line in hAhandle:
	hA.append(float(line))	
normal=[]
normal.append(n70)
normal.append(nR)
normal.append(nA)
hot=[]
hot.append(h70)
hot.append(hR)
hot.append(hA)
box1=plt.boxplot(normal, positions=[1,3,5], whis=[15,85], showfliers=False, notch=True, patch_artist=True, labels=['Hsp70_normal','Rest_normal','AIG1_normal'])
plt.setp(box1['boxes'], facecolor='lightblue')
box2=plt.boxplot(hot, positions=[2,4,6], whis=[15,85],showfliers=False, notch=True, patch_artist=True, labels=['Hsp70_hot','Rest_hot','AIG1_hot'])
plt.setp(box2['boxes'], facecolor='pink')
plt.yscale('log')
plt.xticks([1,2,3,4,5,6],['normal','hot','normal','hot','normal','hot'])
plt.xlim(0.5,6.5)
#plt.ylim(1e-8,30)
#plt.show()
plt.savefig('boxplot_log_whis=15-85.pdf',format='pdf')
plt.close()

norm70handle.close()
hot70handle.close()
nRhandle.close()
hRhandle.close()
nAhandle.close()
hAhandle.close()
