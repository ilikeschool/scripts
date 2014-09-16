#!/usr/bin/env python
import sys
import re
import csv
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import meastools as m
from itertools import product


'''Notes:
Key structure for specsDict:
[specs,scales,yaxLabels,leglocs]
Key
'''

''' Used to debug memory
def memory():
    import os
    from wmi import WMI
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)/1024
'''

fileName = sys.argv[1] if len(sys.argv) >= 2 else raw_input("Enter name of file to parse: ")
fileName_noExt = re.search('(.+?)(\.[^.]*$|$)',fileName).group(1)

[msrDict,cornDict,cornList,modeDict,modeList,specDict,specList]=m.readMeasures(fileName)

modeKeys = map(list,product(*[modeDict[mode] for mode in modeList]))

fileName_sum_csv = fileName_noExt + '_stats_sum.csv'

with open(fileName_sum_csv,'wb') as fsum:
    writer_sum = csv.writer(fsum)
    header = ['SPEC', 'UNITS','MINIMUM','AVERAGE','MAXIMUM'] + cornList*3
    header_sum = modeList + header
    writer_sum.writerow(header_sum)
    for modeKey in modeKeys:
        modeTxtList = []
        for l,k in zip(modeList,modeKey):
            modeTxtList.append('_'.join([l,k]))
        modeTxt = '_'.join(modeTxtList)
        fileName_pdf = fileName_noExt + '_' + modeTxt + '_plots.pdf'
        fileName_csv = fileName_noExt + '_' + modeTxt + '_stats.csv'
        pp = PdfPages(fileName_pdf)
        with open(fileName_csv,'wb') as f:#, PdfPages(fileName_pdf) as pp:
            writer = csv.writer(f)
            writer.writerow(header)
            for spec in specList:
                [deltaDict,sortedDeltaList] = m.calcMeasures(spec,modeKey,msrDict,
                                                                cornDict,cornList)
                [measure,msrTickLabels,msrXaxLabels,msrLegText] = m.sortMeasures(
                            spec,sortedDeltaList,modeKey,msrDict,cornDict,cornList)
                #PRINT MEASURES
                fig = plt.figure(figsize=(10.67, 7.13), dpi=100)
                ax = plt.subplot(111)
                box = ax.get_position()
                plt.grid()
                gcaFont = 8
                legFont = 6
                titleFont = 10
                supTitleFont = 7
                msrScale = specDict[spec,'scale']
                msrYaxLabel = specDict[spec,'yaxLabel']
                msrLegLoc = specDict[spec,'legLoc']
                #ax.set_position([box.x0, box.y0, box.width*.65, box.height])
                if msrLegText == []:
                    msrLegText.append('')
                for msrplotIndx, msrplot in enumerate(measure):
                    xTickLoc = len(msrplot)
                    plt.plot(range(0,xTickLoc),[msrScale*x for x in msrplot], label = msrLegText[msrplotIndx])
                plt.xlim(0,xTickLoc-1)
                plt.xticks(range(0,xTickLoc),msrTickLabels,fontsize=gcaFont)
                plt.yticks(fontsize=gcaFont)
                plt.ylabel(msrYaxLabel,fontsize=gcaFont)
                plt.xlabel(msrXaxLabels,fontsize=gcaFont)
                plt.legend(loc=msrLegLoc,prop={'size':legFont})
                plt.title(spec,fontsize=titleFont)
                plt.suptitle(' / '.join(modeTxtList).replace('_','=') + ' ' + '(' + fileName_noExt + ')',fontsize=supTitleFont)
                pp.savefig()
                # Close figures to save memory
                plt.close('all')
                
                #PROCESS SENSITIVITIES
                modeStartIndx = len(cornList)
                specStartIndx = len(cornList+modeList)
                specKeys = [key for key in msrDict.keys() if (key[specStartIndx]==spec and 
                                                              list(key[modeStartIndx:specStartIndx]) == modeKey)]
                specVals = [msrDict.get(key) for key in msrDict.keys() if (key[specStartIndx]==spec and
                                                              list(key[modeStartIndx:specStartIndx]) == modeKey)]
                specLo,specHi = 9e9999,-9e9999
                for x,xkey in ((msrDict.get(key),key) for key in specKeys):
                    if x < specLo:
                        specLo = x
                        specLoKey = xkey
                    if x > specHi:
                        specHi = x
                        specHiKey = xkey
                specAvg = numpy.mean(specVals)
                maxDelta = max(data[0] for data in deltaDict.values())
                deltaVec = []
                for corn in cornList:
                    deltaVec.append(deltaDict[corn][0]/maxDelta)
                
                
                row = [spec, msrYaxLabel, msrScale*specLo, msrScale*specAvg, msrScale*specHi]
                row.extend(specLoKey[:modeStartIndx])
                row.extend(specHiKey[:modeStartIndx])
                row.extend(deltaVec)
                row_sum = modeKey + row
                writer.writerow(row)
                writer_sum.writerow(row_sum)
        
        pp.close()
