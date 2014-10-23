#!/usr/bin/python

import csv, math, sys, re, numpy, scipy, matplotlib
from pylab import *
rc('text', usetex=True)
rcParams['text.latex.preamble'].append(r'\usepackage{tipa}')
#rcParams['figure.figsize'] = 8, 3.8

def dataHelper(dictname,first_line, line_in,posx,posxerr,posy,posyerr):
    try:
        dictname[line_in[0]]["x"].append(float(line_in[posx]))
        if posxerr is not None:
             dictname[line_in[0]]["xerr"].append(float(line_in[posxerr]))
        dictname[line_in[0]]["y"].append(float(line_in[posy]))
        if posyerr is not None:
            dictname[line_in[0]]["yerr"].append(float(line_in[posyerr]))
    except ValueError:
        print "No value was present"

    return dictname

def loadData(f,x,xerr,y,yerr):
    first_line = f.readline().split(',')

    # datadict = {"St. Helena": { "x": [x1,...], "xerr": [xerr1,...] "y": [y1,...], 
    #                             "yerr" [yerr1,...]}, 
    #             "Gough": ...}
    islands = {}

    # determine positions of the stuff I care about
    posx    = first_line.index(x)
    if xerr is not None:
        posxerr = first_line.index(xerr)
    else:
        posxerr = None
    posy    = first_line.index(y)
    if yerr is not None:
        posyerr = first_line.index(yerr)
    else:
        posyerr = None

    # stick the data in the places
    for line in f:
        line_in = line.split(',')
        if line_in[0] not in islands and line_in[2] != '':
            islands[line_in[0]] = {"x": [], "xerr": [], "y": [], "yerr": []}
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr)
        elif line_in[0] in islands:
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr)
        else:
            continue

    return islands

def tidyData(dictionary):
    for key in dictionary:
        if len(dictionary[key]['x']) != len(dictionary[key]['y']):
            if len(dictionary[key]['x']) < len(dictionary[key]['y']):
                dictionary[key]['y'] = dictionary[key]['y'][:len(dictionary[key]['x'])]
            elif len(dictionary[key]['y']) < len(dictionary[key]['x']):
                dictionary[key]['x'] = dictionary[key]['x'][:len(dictionary[key]['y'])]
    return dictionary

if __name__ == '__main__':

    if len(sys.argv) < 3:
	    print >> sys.stderr, "Usage: %s file_in x y (xerr) (yerr)" % sys.argv[0]
	    sys.exit(1)

    file_in = sys.argv[1]
    x = sys.argv[2]
    y = sys.argv[3]
    try:
        xerr = sys.argv[4]
    except IndexError: 
        xerr = None
    try:
        yerr = sys.argv[5]
    except IndexError:
        yerr = None

    figname    = raw_input("Path to save file? ")
    xAxisLabel = raw_input("X axis? Use TeX formatting. ")
    yAxisLabel = raw_input("Y axis? ")


    ###
    # actually do the thing (damn, I'm good at comments)
    ###
    with open(file_in, 'r') as f:
        islands = loadData(f,x,xerr,y,yerr)

    islands = tidyData(islands)

    symbols = ['bo','g+','rx','k^','k>','k<','kv','m2', '1','3','4']
    colours = ['b','g','r','k','k','k','k','m','0.75','0.75','0.75']
           
    fig = plt.figure()
    ax = plt.subplot(111)

    # plot a graaaaaaaaphs (TODO deal with the not-error-handling!)
    i = 0
    for key in islands:
#       print key,islands[key]['x'],islands[key]['y'],islands[key]['xerr'],islands[key]['yerr']
       if islands[key]['x'] != []:
           ax.plot(islands[key]['x'], islands[key]['y'], symbols[i], markersize=5,
                   markeredgewidth=1, markeredgecolor=colours[i], label=key)
#          errorbar(islands[key]['x'], islands[key]['y'], islands[key]['yerr'],
#	            fmt=None,ecolor=colours[i])
       if i < len(symbols)-1:
            i += 1
       else:
            i = 0

    xlabel(xAxisLabel)
    ylabel(yAxisLabel)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])

    ax.legend(loc='center right', bbox_to_anchor=(1.31, 0.5), numpoints=1, markerscale=1.2,frameon=False, prop={'size':10})

    savefig(figname)
