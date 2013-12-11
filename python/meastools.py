#!/usr/bin/env python
import csv, re
import numpy
from itertools import product

###############################################################################
# readMeasures FUNCTION
# Accepts a file name and reads in measures
# Inputs  fileName - Name of file to read in
# Returns msrDict - dictionary containing all measurements
#         cornDict - Dictionary containing all corner iterations
#         cornList - Ordered list of corner names
#         modeDict - Dictionary containing all variable iterations
#         modeList - Ordered list of non-corner variables
#         specDict - Dictionary containing spec parameters scale, yaxLabel,
#                    and legLoc
#         specList - Ordered list of specifications
###############################################################################
def readMeasures(fileName):
    msrDict = {}
    cornDict = {}
    modeDict = {}
    specDict = {}
    cornList = []
    modeList = []
    specList = []
    with open(fileName,'rb') as f:
        reader = csv.reader(f)
        header = reader.next()
        for parameter in header:
            cell = re.search('(.*)_([MV])($|_)((.*)_(.*)_(.*))?',parameter)
            if cell == None:
                if parameter not in cornList:
                    cornList.append(parameter)
            elif cell.group(2) == 'V':
                if cell.group(1) not in modeList:
                    modeList.append(cell.group(1))
            elif cell.group(2) == 'M':
                if cell.group(1) not in specList:
                    specList.append(cell.group(1))
                specDict[cell.group(1),'scale']=float(cell.group(5))
                specDict[cell.group(1),'yaxLabel']=cell.group(6)
                specDict[cell.group(1),'legLoc']=int(cell.group(7))
            else:
                print 'Did not find anything. Error?'
        specStartIndx = len(cornList+modeList)
        modeStartIndx = len(cornList)
        rowLen = len(header)
        for row in reader:
            key = row[:specStartIndx]
            key.append('')
            for cornIndx,corn in enumerate(cornList):
                if corn not in cornDict.keys():
                    cornDict[corn] = [row[cornIndx]]
                elif row[cornIndx] not in cornDict[corn]:
                    cornDict[corn].append(row[cornIndx])
            for modeIndx,mode in enumerate(modeList):
                modeIndx+=modeStartIndx
                if mode not in modeDict.keys():
                    modeDict[mode] = [row[modeIndx]]
                elif row[modeIndx] not in modeDict[mode]:
                    modeDict[mode].append(row[modeIndx])
            for msrIndx in xrange(specStartIndx,rowLen,1):
                specIndx=msrIndx-specStartIndx
                key[specStartIndx] = specList[specIndx]
                msrDict[tuple(key)] = float(row[msrIndx])
    return msrDict,cornDict,cornList,modeDict,modeList,specDict,specList

###############################################################################
# calcMeasures FUNCTION
# Calculates sensitivity of measurement to independent variables
# Inputs  spec - specification to calc
#         modeKey - Key of current non-corner variable
#         msrDict - Dictionary containing all measurements
#         cornDict - Dictionary containing all corner iterations
#         cornList - Ordered list of corner names
# Returns deltaDict - Dictionary of sensitivities and std for each parameter
#         sortedDeltaList - List of parameters sorted by largest sensitivity
###############################################################################

def calcMeasures(spec, modeKey, msrDict, cornDict, cornList):
    deltasDict = {}
    deltaDict = {}
    sortedDeltaList = []
    msr1Key = list(cornList+modeKey)
    msr1Key.append(spec)
    msr2Key = list(cornList+modeKey)
    msr2Key.append(spec)
    for cornIndx,corn in enumerate(cornList):
        for otherCorn in product('01',repeat=len(cornList)-1):
            otherIndx=0
            for cornJndx,cornJ in enumerate(cornList):
                if corn == cornJ:
                    msr1Key[cornJndx] = cornDict[cornJ][0]
                    msr2Key[cornJndx] = cornDict[cornJ][1]
                else:
                    msr1Key[cornJndx] = cornDict[cornJ][int(otherCorn[otherIndx])]
                    msr2Key[cornJndx] = cornDict[cornJ][int(otherCorn[otherIndx])]
                    otherIndx += 1
            #print msr1Key, msr2Key
            if corn in deltasDict.keys():
                deltasDict[corn].append(msrDict[tuple(msr2Key)]-msrDict[tuple(msr1Key)])
            else:
                deltasDict[corn] = [msrDict[tuple(msr2Key)]-msrDict[tuple(msr1Key)]]
    
    for key in deltasDict.keys():
        deltaDict[key] = (abs(numpy.mean(deltasDict[key])), numpy.std(deltasDict[key]))
    
    sortedDeltaList = sorted(deltaDict, key=deltaDict.get, reverse=True)
    return deltaDict,sortedDeltaList
 
###############################################################################
# sortMeasures FUNCTION
# Sorts data for plotting. X axis is top 4 sensitive parameters. Remaining
#   variables used to generate family of curves
# Inputs  spec - specification to sort
#         sortedDeltaList - List of parameters sorted by largest sensitivity
#         modeKey - Key of current non-corner variable
#         msrDict - Dictionary containing all measurements
#         cornDict - Dictionary containing all corner iterations
#         cornList - Ordered list of corner names
# Returns meaure - List of 4xN measures to plot
#         msrTickLabels - x axis tick labesl
#         msrXaxLabels - x axis labels
#         msrLegText - curve family legend text
###############################################################################
def sortMeasures(spec, sortedDeltaList, modeKey, msrDict, cornDict, cornList):
    msrKeys = []
    msrTickLabels = []
    msrXaxLabels = []
    xaxMax = 4
    
    for cornIndx,cornBin in enumerate(product('01', repeat=min(len(sortedDeltaList),xaxMax))):
        msrKeys.append(list(cornList))
        tickLabel = []
        for sortCornIndx, sortCorn in enumerate(sortedDeltaList):
            corn = cornDict[sortCorn][int(cornBin[sortCornIndx])]
            msrKeys[cornIndx][cornList.index(sortCorn)] = corn
            tickLabel.append(corn)
            if sortCornIndx == xaxMax-1:
                break
        msrTickLabels.append('/'.join(key for key in tickLabel))
        msrKeys[cornIndx] += modeKey
        msrKeys[cornIndx].append(spec)
    
    xaxLabel = [c for i,c in enumerate(sortedDeltaList) if i < xaxMax]
    msrXaxLabels = ' / '.join(key for key in xaxLabel)
    
    measure = []
    msrLegText = []
    if len(sortedDeltaList) > xaxMax:
        familyDeltaList = [i for i in cornList if i in sortedDeltaList[xaxMax:]]
        for cornIndx,cornBin in enumerate(product('01', repeat=len(familyDeltaList))):
            measure.append([])
            legText = []
            for famCornIndx, famCorn in enumerate(familyDeltaList):
                corn = cornDict[famCorn][int(cornBin[famCornIndx])]
                for key in msrKeys:
                    key[cornList.index(famCorn)] = corn
                legText.append(''.join([famCorn, '=', corn])) 
            for key in msrKeys:
                measure[cornIndx].append(float(msrDict[tuple(key)]))
            msrLegText.append(', '.join(key for key in legText))
    else:
        measure.append([])
        for key in msrKeys:
            measure[0].append(float(msrDict[tuple(key)]))
    
    return measure,msrTickLabels,msrXaxLabels,msrLegText

