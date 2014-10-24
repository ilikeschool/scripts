#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def calcInvGain(Rf,Rs):
    return Rf/Rs

def calcNonInvGain(Rf,Rs):
    return 1 + Rf/Rs

def calcUnityGain(Rf,Rs):
    return 1

###############################################################################
# calcResNoise FUNCTION
# Calculates resistor noise over bandwidth
# Inputs  res   - Resistor value
#         bw    - bandwidth over which to integrate over
#         temp  - temperature at which to calculate noise
# Returns noise - Equivalent integrated resistor noise
###############################################################################
def calcResNoise(res,bw=20e3,temp=27):
    kT = (1.38e-23*(273+temp))
    return np.sqrt(4*kT*res*bw)

def calcPreampNoise(noiseList,noiseDict):
    compNoise = 0
    opCompNoise = 0
    resCompNoise = 0
    micCompNoise = 0 
    adcCompNoise = 0
    Rf = noiseDict['RF','input']
    Rs = noiseDict['RS','input']
    for noiseParam in noiseList:
        if noiseDict[noiseParam,'type'] is 'res':
            noise = calcResNoise(noiseDict[noiseParam,'input'])
        else:
            noise = noiseDict[noiseParam,'input']
        outGain = noiseDict[noiseParam,'scale']*noiseDict[noiseParam,'func'](Rf,Rs) 
        outNoise = noise*outGain
        inNoise = outNoise/noiseDict['gain']
        compNoise = np.sqrt(compNoise**2 + inNoise**2)
        if noiseDict[noiseParam,'type'] is 'op':
            opCompNoise = np.sqrt(opCompNoise**2 + inNoise**2)
        elif noiseDict[noiseParam,'type'] is 'res':
            resCompNoise = np.sqrt(resCompNoise**2 + inNoise**2)
        elif noiseDict[noiseParam,'type'] is 'adc':
            adcCompNoise = np.sqrt(adcCompNoise**2 + inNoise**2)
        elif noiseDict[noiseParam,'type'] is 'mic':
            micCompNoise = np.sqrt(micCompNoise**2 + inNoise**2)
    return compNoise,opCompNoise,resCompNoise,adcCompNoise,micCompNoise

def plotPreampNoise(xData,compNoiseArray,contrArray):
    colors = ['m','#3366cc','#dc3912','#ff9900','#109618']
    legText = ['Total','Opamp','Resistor','ADC','Microphone']
    ind = np.arange(0,len(xData))
    fig = plt.figure(figsize=(10.67, 7.13), dpi=100)
    ax = plt.subplot(211)
    box = ax.get_position()
    plt.grid()
    gcaFont = 8
    legFont = 6
    titleFont = 8 
    supTitleFont = 10
    msrYaxLabel = 'noise(uV)'
    #msrXaxLabel = 'gain(dB)'
    #ax.set_position([box.x0, box.y0, box.width*.65, box.height])
    for compPlot,colorPlot in zip(compNoiseArray,colors):
        plt.plot(ind,compPlot,color=colorPlot)
    plt.xlim(ind[0],ind[-1])
    plt.xticks(ind,xData)
    plt.ylabel(msrYaxLabel,fontsize=gcaFont)
    #plt.xlabel(msrXaxLabel,fontsize=gcaFont)
    #plt.title('Noise vs. gain',fontsize=titleFont)
    #plt.suptitle(supTitleC,fontsize=supTitleFont)
    ax = plt.subplot(212)
    box = ax.get_position()
    plt.grid()
    gcaFont = 8
    legFont = 6
    titleFont = 8 
    supTitleFont = 10
    width = 0.35
    msrYaxLabel = 'Contribution(%)'
    #msrXaxLabel = 'gain(dB)'
    #ax.set_position([box.x0, box.y0, box.width*.65, box.height])
    botLoc = np.array([0. for i in range(len(xData))])
    for contrPlot,colorPlot in zip(contrArray,colors[1:]):
        plt.bar(ind,contrPlot,width,bottom=botLoc,color=colorPlot)
        botLoc += contrPlot
    plt.xlim(ind[0],ind[-1])
    plt.ylim(0,100)
    plt.ylabel(msrYaxLabel,fontsize=gcaFont)
    #plt.xlabel(msrXaxLabel,fontsize=gcaFont)
    plt.xticks(ind+width/2.,xData)
    plt.yticks(np.arange(0,101,10))
    #plt.title('Noise vs. gain',fontsize=titleFont)
    #plt.suptitle(supTitleC,fontsize=supTitleFont)
    return fig


