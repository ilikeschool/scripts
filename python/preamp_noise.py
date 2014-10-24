#!/usr/bin/env python
import numpy as np
import preamp_noise_funcs as nf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

Rtot = 20e3
gainSteps = np.arange(0,21)
opNoiseScale = np.logspace(0,5,num=6,base=2)
noiseList = ['OP1','RS','RF','OP2','RNS','RNF','RNBIAS','RAAP','RAAN','ADC','MIC']
noiseTypes = ['op','res','res','op','res','res','res','res','res','adc','mic']
noiseFuncs = [nf.calcNonInvGain,   ## OP1
        nf.calcInvGain,            ## RS
        nf.calcUnityGain,          ## RF
        nf.calcUnityGain,          ## OP2
        nf.calcUnityGain,          ## RNS
        nf.calcUnityGain,          ## RNF
        nf.calcUnityGain,          ## RNBIAS
        nf.calcUnityGain,          ## RAAP
        nf.calcUnityGain,          ## RAAN
        nf.calcUnityGain,          ## ADC
        nf.calcNonInvGain]         ## MIC
noiseScales = [2,               ## OP1
        2,                      ## RS
        2,                      ## RF
        2,                      ## OP2
        1,                      ## RNS
        1,                      ## RNF
        0,                      ## RNBIAS
        1,                      ## RAAP
        1,                      ## RAAN
        1/np.sqrt(4),                      ## ADC
        0]                      ## MIC
noiseInps = [3e-6,              ## OP1
        Rtot,                   ## RS
        0,                      ## RF
        3e-6,                   ## OP2
        2e3,                    ## RNS
        2e3,                    ## RNF
        10e3,                   ## RNBIAS
        2e3,                    ## RAAP
        2e3,                    ## RAAN
        3.53e-6,                ## ADC
        2.5e-6]                 ## MIC

noiseDict = {}
for noiseParam,noiseType,noiseFunc,noiseScale,noiseInp in zip(noiseList,noiseTypes,noiseFuncs,noiseScales,noiseInps):
    noiseDict[noiseParam,'type'] = noiseType
    noiseDict[noiseParam,'func'] = noiseFunc
    noiseDict[noiseParam,'scale'] = noiseScale
    noiseDict[noiseParam,'input'] = noiseInp

noiseDict['gain'] = 2*nf.calcNonInvGain(noiseDict['RF','input'],noiseDict['RS','input'])

'''
gain = []
compNoise = []
opCompNoise = []
resCompNoise = []
adcCompNoise = []
micCompNoise = []
opContr = []
resContr = []
adcContr = []
micContr = []


for gainStep in gainSteps:
    Rstep = (1-10**(-gainStep/20.0))*Rtot
    noiseDict['RF','input'] = Rstep
    noiseDict['RS','input'] = Rtot-Rstep
    noiseDict['gain'] = 2*nf.calcNonInvGain(noiseDict['RF','input'],noiseDict['RS','input'])
    cNoise,oNoise,rNoise,aNoise,mNoise = nf.calcPreampNoise(noiseList,noiseDict)
    gain.append(noiseDict['gain'])
    compNoise.append(cNoise*1e6)
    opCompNoise.append(oNoise*1e6)
    opContr.append(oNoise**2/cNoise**2*100)
    resCompNoise.append(rNoise*1e6)
    resContr.append(rNoise**2/cNoise**2*100)
    adcCompNoise.append(aNoise*1e6)
    adcContr.append(aNoise**2/cNoise**2*100)
    micCompNoise.append(mNoise*1e6)
    micContr.append(mNoise**2/cNoise**2*100)

compNoiseArray = [np.array(compNoise),np.array(opCompNoise),np.array(resCompNoise),np.array(adcCompNoise),np.array(micCompNoise)]
contrArray = [np.array(opContr),np.array(resContr),np.array(adcContr),np.array(micContr)]
legText = ['Total','Opamp','Resistor','ADC','Microphone']
plotDict = {}

with PdfPages('gain_sweep.pdf') as pp:
    fig = nf.plotPreampNoise(gainSteps,compNoiseArray,contrArray)
    pp.savefig()
    plt.close('all')
'''
compNoise = []
opCompNoise = []
resCompNoise = []
adcCompNoise = []
micCompNoise = []
opContr = []
resContr = []
adcContr = []
micContr = []

opNoise = noiseDict['OP1','input']
for opStep in opNoiseScale:
    noiseDict['OP1','input'] = opNoise/np.sqrt(opStep)
    noiseDict['OP2','input'] = opNoise/np.sqrt(opStep)
    cNoise,oNoise,rNoise,aNoise,mNoise = nf.calcPreampNoise(noiseList,noiseDict)
    compNoise.append(cNoise*1e6)
    opCompNoise.append(oNoise*1e6)
    opContr.append(oNoise**2/cNoise**2*100)
    resCompNoise.append(rNoise*1e6)
    resContr.append(rNoise**2/cNoise**2*100)
    adcCompNoise.append(aNoise*1e6)
    adcContr.append(aNoise**2/cNoise**2*100)
    micCompNoise.append(mNoise*1e6)
    micContr.append(mNoise**2/cNoise**2*100)


compNoiseArray = [np.array(compNoise),np.array(opCompNoise),np.array(resCompNoise),np.array(adcCompNoise),np.array(micCompNoise)]
contrArray = [np.array(opContr),np.array(resContr),np.array(adcContr),np.array(micContr)]
legText = ['Total','Opamp','Resistor','ADC','Microphone']
plotDict = {}

with PdfPages('opNoise_sweep_adc_4x.pdf') as pp:
    fig = nf.plotPreampNoise(opNoiseScale,compNoiseArray,contrArray)
    pp.savefig()
    plt.close('all')



