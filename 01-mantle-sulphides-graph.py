#!/usr/bin/python

import csv, math, sys, re, numpy, scipy, matplotlib
from pylab import *
rc('text', usetex=True)
rc('text.latex', preamble=r'\usepackage{cmbright}')
rcParams['text.latex.preamble'].append(r'\usepackage{tipa}')

x = [0,0.57,0.73,0.54,0.63,0.78,0.49,0.645,0.55,0.69,0.6,1.5,0.75,0.885,0]
xerr = [None,0.0855,0.1095,0.081,0.0945,0.117,0.0735,0.09675,0.0825,0.1035,0.09,None,None,None,None]
y = [14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
ytext = ["","","Tl$^{3+}$ (VI)","Tl$^{3+}$ (IV)","Tl$^+$ (VI)","Ni$^{3+}$ (VI)","Ni$^{2+}$ (VI)","Ni$^{2+}$ (IV)","Fe$^{3+}$ (VI)","Fe$^{3+}$ (IV)","Fe$^{2+}$ (VI)","Fe$^{2+}$ (IV)","Cu$^{3+}$ (VI)","Cu$^{2+}$ (VI)","Cu$^{2+}$ (IV)",""]


# set up the substitution field
placeholder = 0
for i in x:
    placeholder += i
xmean = placeholder/len(x)
minx = 0.49 - 0.49*0.15 
maxx = 0.78 + 0.78*0.15

# set up the plot environment
fig = plt.figure()
loc = matplotlib.ticker.MultipleLocator(base=1)
ax = plt.subplot(111)
ax.yaxis.set_major_locator(loc)
ax.set_yticklabels(ytext)
 
# plot a graaaaaaaaphs
for i in range(len(x)):
    ax.plot(x[i], y[i], 'kx', markersize=6, markeredgewidth=1, zorder=5)
    errorbar(x[i], y[i], xerr = xerr[i], fmt=None,ecolor='k')

ax.axvline(xmean,color='gray',lw=1.5,alpha=0.5)
ax.axvspan(minx,maxx, alpha=0.1, color='gray')

ylabel("Ion (coordination number)")
xlabel("Ionic radius (\\AA)")

ax.set_ylim([0,14])

savefig('Dropbox/PhD/writing/Exercises/ionic-radii.png')
