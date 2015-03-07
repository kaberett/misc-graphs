#!/usr/bin/python

import csv, math, sys, re, numpy, scipy, matplotlib
from pylab import *
from matplotlib import colors
from collections import OrderedDict # stackoverflow told me to do it

rc('text', usetex=True)
rcParams['text.latex.preamble'].append(r'\usepackage{tipa}')
#rcParams['figure.figsize'] = 10, 8

# There is surely a way to make this neater? /Surely/ four try-except
# blocks is excessive and I can parcel them up a bit more nicely?

# hello future self - line_in[0] is the island name.
# Chris reckons I can do something intelligent with .get and ?: maybe
# and subsequently suggests "if x in y" only with better var names
def dataHelper(dictname,first_line,line_in,posx,posxerr,posy,posyerr,poseps):
    dictname[line_in[0]]["type"]       = line_in[3]
    dictname[line_in[0]]["markersize"] = line_in[7]
    dictname[line_in[0]]["marker"]     = line_in[4]   
    dictname[line_in[0]]["mec"].append(line_in[5])  
    dictname[line_in[0]]["mfc"].append(line_in[6])    


    try:
        dictname[line_in[0]]["x"].append(float(line_in[posx]))
    except ValueError:
        dictname[line_in[0]]["x"].append("")
    try:
        dictname[line_in[0]]["xerr"].append(float(line_in[posxerr]))
    except (ValueError, TypeError) as e:
        dictname[line_in[0]]["xerr"].append("")
    try:
        dictname[line_in[0]]["y"].append(float(line_in[posy]))
    except ValueError:
        dictname[line_in[0]]["y"].append("")
    try:
        dictname[line_in[0]]["yerr"].append(float(line_in[posyerr]))
    except (ValueError, TypeError) as e:
        dictname[line_in[0]]["yerr"].append("") 
    try:
        dictname[line_in[0]]["EpsTl"].append(float(line_in[poseps]))
    except ValueError:
        dictname[line_in[0]]["EpsTl"].append("")

    return dictname

###
# read the input csv; turn it into something useful
###
def loadData(f,x,xerr,y,yerr):
    first_line = f.readline().split(',')
    print first_line
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
    poseps = first_line.index("EpsTl")

    # stick the data in the places
    for line in f:
        line_in = line.split(',')
        if line_in[0] not in islands and line_in[2] != '':
            islands[line_in[0]] = {"type": '', "x": [], "xerr": [], "y": [], "yerr": [], "marker": "", "mec": [], "mfc": [], "markersize": "", "EpsTl": []}
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr,poseps)
        elif line_in[0] in islands:
            dataHelper(islands,first_line,line_in,posx,posxerr,posy,posyerr,poseps)
        else:
            continue

    return islands

###
# make sure lists are same dimension & properly matched
###
def tidyData(dictionary):
    musteloidea = {}
    for key in dictionary:
        zipped = zip(dictionary[key]['x'], dictionary[key]['y'], dictionary[key]['xerr'], dictionary[key]['yerr'], dictionary[key]['EpsTl'],dictionary[key]['mec'], dictionary[key]['mfc'])
        zipped = [(x,y,xerr,yerr,EpsTl,mec,mfc) for (x,y,xerr,yerr,EpsTl,mec,mfc) in zipped if x!= '' and y!= '']
        mustelidae = [list(badger) for badger in zip(*zipped)]
        musteloidea[key] = dictionary[key]
        try:
            musteloidea[key]['x'] = mustelidae[0]
            musteloidea[key]['y'] = mustelidae[1]
            musteloidea[key]['xerr'] = mustelidae[2]
            musteloidea[key]['yerr'] = mustelidae[3]
            musteloidea[key]['EpsTl'] = mustelidae[4]
            musteloidea[key]['mec'] = mustelidae[5]
            musteloidea[key]['mfc'] = mustelidae[6]
        except IndexError:
            del musteloidea[key]
            print key + " had no values to unpack"
    return musteloidea

def generateSymbols(symbolType, dictionary):
    symbols = {}

#    markers = ['x','+','o','*','s','d','^','>','<','v','1','2','3','4','8']
#    colours = ['k','r','teal','silver','goldenrod','lightsteelblue','darkorchid','salmon','lightskyblue','chartreuse','saddlebrown','darkslateblue','orchid','indigo','turquoise']

    for key in dictionary:
        n = len(dictionary[key]['x'])
        print key,  " n = ", n
        if key not in symbols:
            symbols[key] = {'marker': dictionary[key]['marker'], 'mfc': dictionary[key]['mfc'], 'mec': dictionary[key]['mec'], 'markersize': int(dictionary[key]['markersize'])}
 
        if symbolType == "i":
            continue
        if symbolType == "c":
            if dictionary[key]['type'] == "HIMU":
                symbols[key]['mec'] = ['r'] * n
                symbols[key]['mfc'] = ['r'] * n
            elif dictionary[key]['type'] == "EMI" or dictionary[key]['type'] == "EMII":
                symbols[key]['mec'] = ['b'] * n
                symbols[key]['mfc'] = ['b'] * n
        if symbolType == "f":
            for i in range(len(dictionary[key]['EpsTl'])-1):
                if dictionary[key]['EpsTl'][i] <= -5:
                    symbols[key]['mec'][i] = '#0033CC'
                    symbols[key]['mfc'][i] = '#0033CC'
                if dictionary[key]['EpsTl'][i] >= -5 and dictionary[key]['EpsTl'][i] <= -3:
                    symbols[key]['mec'][i] = '#0099FF'
                    symbols[key]['mfc'][i] = '#0099FF'
                if dictionary[key]['EpsTl'][i] >= -3 and dictionary[key]['EpsTl'][i] <= -2:
                    symbols[key]['mec'][i] = '#66CC99'
                    symbols[key]['mfc'][i] = '#66CC99'
                if dictionary[key]['EpsTl'][i] >= -2 and dictionary[key]['EpsTl'][i] <= -1:
                    symbols[key]['mec'][i] = '#FFCC33'
                    symbols[key]['mfc'][i] = '#FFCC33'
                if dictionary[key]['EpsTl'][i] >= -1 and dictionary[key]['EpsTl'][i] <= 1:
                    symbols[key]['mec'][i] = '#FF6600'
                    symbols[key]['mfc'][i] = '#FF6600'
                if dictionary[key]['EpsTl'][i] >= 1 and dictionary[key]['EpsTl'][i] <= 3:
                    symbols[key]['mec'][i] = '#003300'
                    symbols[key]['mfc'][i] = '#003300'
                if dictionary[key]['EpsTl'][i] >=3:
                    symbols[key]['mec'][i] = '0.5' #'#003300'
                    symbols[key]['mfc'][i] = '0.5' #'#003300'

           # print symbols[key]

    return symbols   

def plotGraph(islands,symbols):
    # currently this is a dummy function; needs stuff breaking out into it
    return islands
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

    qLegend    = raw_input("Display legend? [y/n] ")
    symbolType = raw_input("Plot colours as islands, components or fractionation factors? [i/c/f] ")

    ###
    # crunch all the data
    ###
    with open(file_in, 'r') as f:
        islands = loadData(f,x,xerr,y,yerr)

    islands = tidyData(islands)
    symbols = generateSymbols(symbolType,islands)

    ###
    # TODO this should probably be broken out into its own function
    # plot a graaaaaaph
    ###
    fig = plt.figure()
    ax = plt.subplot(111)
    for key in islands:
        print key
        for i in range(len(islands[key]['x'])):
            ax.plot(islands[key]['x'][i], islands[key]['y'][i], symbols[key]['marker'], markersize=symbols[key]['markersize'], markeredgewidth=1, markerfacecolor = symbols[key]['mfc'][i], markeredgecolor = symbols[key]['mec'][i], label = key)
            try:
                errorbar(islands[key]['x'], islands[key]['y'], xerr = islands[key]['xerr'], fmt=None,ecolor=symbols[key]['mec'][i])
            except:
                # no fucks were given that day (this is probably a TODO)
                continue

            try:
                errorbar(islands[key]['x'], islands[key]['y'], islands[key]['yerr'], fmt=None,ecolor=symbols[key]['mec'][i])
            except:
                # no fucks were given that day (this is probably a TODO)
                continue


#    fill([25,25,0,0],[2,8,8,2], 'b', alpha=0.1) 

    xlabel(xAxisLabel, fontsize=18)
    ylabel(yAxisLabel, fontsize=18)

    if qLegend == "y":
        handles, labels = ax.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        ax.legend(by_label.values(), by_label.keys(), loc='center right', bbox_to_anchor=(1.35, 0.5), numpoints=1, markerscale=1,frameon=False, prop={'size':15})

savefig(figname)
