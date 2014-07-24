#!/usr/bin/python

import csv, math, sys, re

###
# load data up
###
def loadData(f):
    # define a new array to read stuff into
    data = [["Measurement", "Value (V)", "Internal precision (1se)"]]

    # I only actually want data from the second block of running totals
    # TODO: does this need to be flexible for other element runs?
    i = 0
    for line in f:
        if i < 2:
            if "Running total results" in line:
                i += 1
            continue
        else:
            if not line.strip(): continue
            try:
                if line[8] != ' ':
                    data.append( [ line[8:37], line[37:52], line[52:64] ])
            except:
                continue
    return data

# I want to automatically stick the sample name in, too.
def identifySample(f):
    for line in f:
        if "Sample   :" in line:
            temp = re.split(r':', line)
            sampleName = str(re.search(r'\b..*\b', temp[1]).group(0))
    return sampleName

###
# transpose the table
###
def transposeData(runNo, data, sampleName):
    transposed = []
    # this ultimately wants to be user-controlled - scrape off the row titles,
    # present as a drop-down list, and let the user choose which to include in
    # the reduced data table, with tickyboxes for whether to include internal
    # precision.
    headers = ['file', 'sample']
    data_out = [runNo, sampleName]
    for data_index in [
        1,
        2,
        7,
        12,
        13,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        25,
        26,
    ]:
        try:
            headers.append(data[data_index][0])
            headers.append('internal precision')
            data_out.append(float(data[data_index][1]))
            data_out.append(float(data[data_index][2]))
        except:
            continue
    return [headers, data_out] # our two rows

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: %s file.csv [file2.csv ...]" % sys.argv[0]
        sys.exit(1)

    files = sys.argv[1:]

    ###
    # actually do the thing (damn, I'm good at comments)
    ###
    for filename in files:
        # pull run number out of filename
        runNo = re.search(r'[0-9][0-9]*', filename).group(0)

        # do I seriously have to do this in a separate operation because magic?
        with open(filename, 'r') as f:
            sampleName = identifySample(f)

        # dump final running totals for the file into a table
        with open(filename, 'r') as f:
            data = loadData(f)


        transposed = transposeData(runNo, data, sampleName)
        # transpose 'em
        with open('transposeddata.csv', 'a') as f:
            csvwriter = csv.writer(f)
            for row in transposed[1:] :
                csvwriter.writerow(row)
