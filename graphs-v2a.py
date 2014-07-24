#!/usr/bin/python

import csv, math, sys, re, numpy, scipy, matplotlib
from pylab import *
rc('text', usetex=True)
rcParams['text.latex.preamble'].append(r'\usepackage{tipa}')
rcParams['figure.figsize'] = 8, 3.8

def loadData(f,x,xerr,y,yerr):
    islands = {}

# Sample structure:
# datadict = {"St. Helena": { x: [x1,...], xerr: [xerr1,...] y: [y1,...], yerr: [yerr1,...]}, 
#              "Gough": ...}
#
#

    first_line = f.readline().split(',')

# TODO this is gross: sort it out!

    posx    = None
    posxerr = None
    posy    = None
    posyerr = None

# TODO work out how to make it skip a datatype I don't actually want - poss. the gross hack of a column of 0s in the input? There's got to be a nicer way.

    for i in range(len(first_line)):
        if first_line[i] == x:
            posx = i
        if first_line[i] == xerr:
            posxerr = i
        if first_line[i] == y:
            posy = i
        if first_line[i] == yerr:
            posyerr = i

 
# TODO refactor so I'm not repeating lumps of code!
# TODO tell the thing how to handle me asking it to float #DIV/0
   
    for line in f:
        line_in = line.split(',')
        if line_in[0] not in islands and line_in[2] != '':
            islands[line_in[0]] = {x: [], xerr: [], y: [], yerr: []}

            islands[line_in[0]][x].append(line_in[posx])
            islands[line_in[0]][xerr].append(line_in[posxerr])
            islands[line_in[0]][y].append(line_in[posy])
            islands[line_in[0]][yerr].append(line_in[posyerr])
        elif line_in[0] in islands:
            islands[line_in[0]][x].append(line_in[posx])
            islands[line_in[0]][xerr].append(line_in[posxerr])
            islands[line_in[0]][y].append(line_in[posy])
            islands[line_in[0]][yerr].append(line_in[posyerr])
        else:
            continue

    return islands



if __name__ == '__main__':

    # if I'm doing things this way I need to define all of x,y,etc!
    file_in = sys.argv[1]
    x = sys.argv[2]
    xerr = sys.argv[3]
    y = sys.argv[4]
    yerr = sys.argv[5]

    ###
    # actually do the thing (damn, I'm good at comments)
    ###
    with open(file_in, 'r') as f:
        islands = loadData(f,x,xerr,y,yerr)
        print islands

#    symbols = ['bo','g+','rx','k^','k>','k<','kv','m2', '1','3','4']
#    colours = ['b','g','r','k','k','k','k','m','0.75','0.75','0.75']
#           
#    fig = plt.figure()
#    ax = plt.subplot(111)
# 
#    # plot a graaaaaaaaphs
#    for i in range(len(islands)):
#       #print islands[i][0],islands[i][1],islands[i][2]
#       try:
#           ax.plot(islands[i][0], islands[i][1], symbols[i], markersize=5,
#		markeredgewidth=1, markeredgecolor=colours[i], 
#                label=islands[i][3][0])
#           errorbar(islands[i][0], islands[i][1], islands[i][2],
#	            fmt=None,ecolor=colours[i])
#       except:
#           continue
#
#    ylabel("\\textepsilon\,$^{205}$Tl")
#    xlabel("[Tl] (ppb)")
#
#    box = ax.get_position()
#    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])

#    ax.legend(loc='center right', bbox_to_anchor=(1.31, 0.5), numpoints=1, markerscale=1.2,frameon=False, prop={'size':10})

#    savefig('../../../writing/graphs/epstl-tl.pdf')
