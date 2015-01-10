#!/usr/bin/python

import csv, math, sys, re, numpy, scipy, matplotlib
from pylab import *
from matplotlib import colors
from collections import OrderedDict # stackoverflow told me to do it

rc('text', usetex=True)
rcParams['text.latex.preamble'].append(r'\usepackage{tipa}')
#rcParams['figure.figsize'] = 8, 3.8

# There is surely a way to make this neater? /Surely/ four try-except
# blocks is excessive and I can parcel them up a bit more nicely?

# hello future self - line_in[0] is the island name.
# Chris reckons I can do something intelligent with .get and ?: maybe
# and subsequently suggests "if x in y" only with better var names
def dataHelper(dictname,first_line,line_in,posx,posxerr,posy,posyerr):
    dictname[line_in[0]]["type"] = line_in[3]
    try:
        dictname[line_in[0]]["x"].append(float(line_in[posx]))
    except ValueError:
        dictname[line_in[0]]["x"].append("")
    try:
        if posxerr is not None:
             dictname[line_in[0]]["xerr"].append(float(line_in[posxerr]))
    except ValueError:
        dictname[line_in[0]]["xerr"].append("")
    try:
        dictname[line_in[0]]["y"].append(float(line_in[posy]))
    except ValueError:
        dictname[line_in[0]]["y"].append("")
    try:
        if posyerr is not None:
            dictname[line_in[0]]["yerr"].append(float(line_in[posyerr]))
    except ValueError:
        dictname[line_in[0]]["yerr"].append("") 

    return dictname

###
# read the input csv; turn it into something useful
###
def loadData(f,x,xerr,y,yerr):
    first_line = f.readline().split(',')

    # datadict = {"St. Helena": { "type": '',  "x": [x1,...], "xerr": [xerr1,...] "y": [y1,...], 
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
            islands[line_in[0]] = {"type": '', "x": [], "xerr": [], "y": [], "yerr": []}
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr)
        elif line_in[0] in islands:
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr)
        else:
            continue

    return islands

###
# make sure lists are same dimension & properly matched
###
def tidyData(dictionary):
    musteloidea = {}
    for key in dictionary:
        zipped = zip(dictionary[key]['x'], dictionary[key]['y'])
        zipped = [(x,y) for (x,y) in zipped if x!= '' and y!= '']
        mustelidae = [list(badger) for badger in zip(*zipped)]
        musteloidea[key] = dictionary[key]
        try:
            musteloidea[key]['x'] = mustelidae[0]
            musteloidea[key]['y'] = mustelidae[1]
        except IndexError:
            del musteloidea[key]
            print key + " had no values to unpack"
    return musteloidea

###
# put together a semi-replicable list of symbol types
# NB there are data structures for actual replicability
###
def generateSymbols(symbolType, dictionary):
    symbols = {}
    i = 0

    markers = ['x','+','o','*','s','d','^','>','<','v','1','2','3','4','8']
    colours = ['k','r','teal','silver','goldenrod','lightsteelblue','darkorchid','salmon','lightskyblue','chartreuse','saddlebrown','darkslateblue','orchid','indigo','turquoise']

    if symbolType == "i":
        for key in dictionary:
            print key
            if key not in symbols:
                symbols[key] = {'marker': '', 'mfc': '', 'mec': '', 'markersize': 10}
            if key == "Jenner":
                symbols[key]['marker'] = "o"
                symbols[key]['mec'] = "0.75"
                symbols[key]['mfc'] = "0"
                symbols[key]['markersize'] = 5
            elif key == "Hawai'i":
                symbols[key]['marker'] = 'x'
                symbols[key]['mec'] = '0.75'
                symbols[key]['mfc'] = '0.75'
                symbols[key]['markersize'] = 5
            elif key == "Azores":
                symbols[key]['marker'] = '+'
                symbols[key]['mec'] = '0.75'
                symbols[key]['mfc'] = '0.75'
                symbols[key]['markersize'] = 5
            elif key == "Iceland":
                symbols[key]['marker'] = '^'
                symbols[key]['mec'] = '0.75'
                symbols[key]['mfc'] = '0.75'    
                symbols[key]['markersize'] = 5
            elif key =="Mantle":
                symbols[key]['marker'] = '*'
                symbols[key]['mec'] = 'w'
                symbols[key]['mfc'] = 'k'
            else:
                symbols[key]['marker'] = markers[i]
                symbols[key]['mfc'] = colours[i]
                symbols[key]['mec'] = colours[i]
                i += 1
    elif symbolType == "c":
        for key in dictionary:
            if key not in symbols:
                symbols[key] = {'marker': '', 'mfc': '', 'mec': '', 'markersize': 10}

            # select symbol colours by type
            if dictionary[key]['type'] == "HIMU":
                symbols[key]['mec'] = 'r'
                symbols[key]['mfc'] = 'r'
            elif dictionary[key]['type'] == "EMI" or dictionary[key]['type'] == "EMII":
                symbols[key]['mec'] = 'b'
                symbols[key]['mfc'] = 'b'
            elif dictionary[key]['type'] == "mantle" or dictionary[key]['type'] == "AOC" or dictionary[key]['type'] == "FeMn":
                symbols[key]['mec'] = 'k'
                symbols[key]['mfc'] = 'k'
            
            # select symbol colours for literature data (... set type to "lit" yeah)
            elif key == "Jenner" or key == "Hawai'i" or key == "Azores" or key == "Iceland":
                symbols[key]['mec'] = "k"
                symbols[key]['mfc'] = "0.75"
                symbols[key]['markersize'] = 5
            else:
                symbols[key]['mfc'] = colours[i]
                symbols[key]['mec'] = colours[i]
 
            if key != "Jenner" and key != "Hawai'i" and key != "Azores" and key != "Iceland":
                symbols[key]['marker'] = markers[i]
                i += 1
            elif key == "Jenner":
                symbols[key]['marker'] = 'o'
            elif key == "Hawai'i":
                symbols[key]['marker'] = 'x'
            elif key == "Iceland":
                symbols[key]['marker'] = '^'
            elif key == "Azores":
                symbols[key]['marker'] = '+'
            elif key == "Mantle":
                symbols[key]['marker'] = '*'

    return symbols

###
# do the thing!
###
if __name__ == '__main__':

    if len(sys.argv) < 3:
	    print >> sys.stderr, "Usage: %s file_in x y (xerr) (yerr)" % sys.argv[0]
	    sys.exit(1)

    # get filename and key args
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

    # prompt user for relevant input
    figname    = raw_input("Path to save file? ")
    xAxisLabel = raw_input("X axis? Use TeX formatting. ")
    yAxisLabel = raw_input("Y axis? ")

    qLegend    = raw_input("Display legend? y/n ")
    symbolType = raw_input("Plot as islands or components? [i/c] ")

    ###
    # crunch all the data
    ###
    with open(file_in, 'r') as f:
        islands = loadData(f,x,xerr,y,yerr)

    islands = tidyData(islands)
    print islands   
    symbols = generateSymbols(symbolType,islands)
    
    ###
    # TODO this should probably be broken out into its own function
    # plot a graaaaaaph
    ###
    fig = plt.figure()
    ax = plt.subplot(111)
    for key in islands:
       ax.plot(islands[key]['x'], islands[key]['y'], symbols[key]['marker'], markersize=symbols[key]['markersize'], markeredgewidth=1,markerfacecolor = symbols[key]['mfc'], markeredgecolor = symbols[key]['mec'], label = key)
       # TODO actually have an option on /both/ types of error bar
       try:
           errorbar(islands[key]['x'], islands[key]['y'], xerr = islands[key]['xerr'], fmt=None,ecolor=symbols[key]['mec'])
       except:
           # no fucks were given that day (this is probably a TODO)
           print "No x error-bar values provided."
           continue

#       try:
#           errorbar(islands[key]['x'], islands[key]['y'], islands[key]['yerr'], fmt=None,ecolor=symbols[key]['mec'])
#       except:
           # no fucks were given that day (this is probably a TODO)
#           print "No y error-bar values provided."
#           continue


#    fill([25,25,0,0],[2,8,8,2], 'b', alpha=0.1) 

    xlabel(xAxisLabel)
    ylabel(yAxisLabel)

    if qLegend == "y":
        handles, labels = ax.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        ax.legend(by_label.values(), by_label.keys(), loc='center right', bbox_to_anchor=(1.31, 0.5), numpoints=1, markerscale=1.2,frameon=False, prop={'size':10})

savefig(figname)
