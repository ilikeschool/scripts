#!/usr/bin/env python
import numpy as np
import preamp_noise_funcs as nf
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_pdf import PdfPages

fileName_sum_csv = "preamp_noise_summary.csv"
fileName_scat_csv = "preamp_noise_scatter.csv"

Rtot = 12e3
gainSteps = np.arange(0,21)
op1NoiseScales = np.linspace(1,4,4) 
op2NoiseScales = np.linspace(1,4,4) 
adcNoiseScales = np.linspace(1,3,3)
micNoiseScales = np.linspace(0,1,2)
opNoise = 2.12e-6
adcNoise = 9.162e-6
micNoise = 2.5e-6
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
        1,                      ## ADC
        0]                      ## MIC
noiseInps = [opNoise,           ## OP1
        Rtot,                   ## RS
        0,                      ## RF
        opNoise,                ## OP2
        2e3,                    ## RNS
        2e3,                    ## RNF
        10e3,                   ## RNBIAS
        2e3,                    ## RAAP
        2e3,                    ## RAAN
        adcNoise,               ## ADC
        micNoise]               ## MIC

noiseDict = {}
for noiseParam,noiseType,noiseFunc,noiseScale,noiseInp in zip(noiseList,noiseTypes,noiseFuncs,noiseScales,noiseInps):
    noiseDict[noiseParam,'type'] = noiseType
    noiseDict[noiseParam,'func'] = noiseFunc
    noiseDict[noiseParam,'scale'] = noiseScale
    noiseDict[noiseParam,'input'] = noiseInp

noiseDict['gain'] = 2*nf.calcNonInvGain(noiseDict['RF','input'],noiseDict['RS','input'])


compNoise = []
opCompNoise = []
resCompNoise = []
adcCompNoise = []
micCompNoise = []
opContr = []
resContr = []
adcContr = []
micContr = []
dataArray = []
dataDictList = [dict() for x in gainSteps]

for micNoiseScale in micNoiseScales:
    for adcNoiseScale in adcNoiseScales:
        for op1NoiseScale in op1NoiseScales:
            for op2NoiseScale in op2NoiseScales:
                for gainStep in gainSteps:
                    Rstep = (1-10**(-gainStep/20.0))*Rtot
                    noiseDict['RF','input'] = Rstep
                    noiseDict['RS','input'] = Rtot-Rstep
                    noiseDict['gain'] = 2*nf.calcNonInvGain(noiseDict['RF','input'],noiseDict['RS','input'])
                    noiseDict['OP1','input'] = opNoise/np.sqrt(op1NoiseScale)
                    noiseDict['OP2','input'] = opNoise/np.sqrt(op2NoiseScale)
                    noiseDict['ADC','input'] = adcNoise/np.sqrt(2**(adcNoiseScale-1))
                    noiseDict['MIC','scale'] = micNoiseScale*2
                    cNoise,oNoise,rNoise,aNoise,mNoise = nf.calcPreampNoise(noiseList,noiseDict)
                    compNoise = cNoise*1e6
                    opCompNoise = oNoise*1e6
                    resCompNoise = rNoise*1e6
                    adcCompNoise = aNoise*1e6
                    micCompNoise = mNoise*1e6
                    opFilt = 1 if op1NoiseScale >= op2NoiseScale else 0
                    fullScale = 10**(-gainStep/20.0)*1.0/np.sqrt(2)/2*1000
                    snr = 20*np.log10(fullScale/compNoise*1000)
                    snr_1vrms = 20*np.log10(1/cNoise)
                    current = 50+20*(op1NoiseScale+op2NoiseScale)+75*2**(adcNoiseScale-1)
                    fom = snr+10*np.log10(1/(3*current*1e-6))
                    dataLabel = str(int(adcNoiseScale)) + "ADC/" + str(int(op1NoiseScale)) + "OP1/" + str(int(op2NoiseScale)) + "OP2"
                    dataArray.append([micNoiseScale,adcNoiseScale,op1NoiseScale,op2NoiseScale,opFilt,gainStep,fullScale,compNoise,opCompNoise,resCompNoise,adcCompNoise,micCompNoise,snr,snr_1vrms,current,fom,dataLabel])
                    if micNoiseScale == 0 and opFilt:
                        key = (current)
                        if key not in dataDictList[gainStep].keys():
                            dataDictList[gainStep][key] = [compNoise,dataLabel]
                        elif compNoise < dataDictList[gainStep][key][0]:
                            dataDictList[gainStep][key] = [compNoise,dataLabel]

with open(fileName_sum_csv,'wb') as f:
    writer= csv.writer(f)
    header = ['MIC','ADC','OP1','OP2','OPFILT','GAIN','FS','COMPN','OPN','RESN','ADCN','MICN','SNR','SNR_1Vrms','CURRENT','FOM','LABEL']
    writer.writerow(header)
    for data in dataArray:
        writer.writerow(data)

minNoise = [float("inf") for x in gainSteps]
with open(fileName_scat_csv,'wb') as f:
    writer= csv.writer(f)
    header = np.concatenate((['current'],gainSteps,gainSteps))
    writer.writerow(header)
    dataKeys = sorted(dataDictList[0])
    for key in dataKeys:
        rowNoise = []
        rowLabel = []
        for gainStep in gainSteps:
            if dataDictList[gainStep][key][0] < minNoise[gainStep]:
                minNoise[gainStep] =  dataDictList[gainStep][key][0]
                rowNoise = rowNoise + [dataDictList[gainStep][key][0]]
                rowLabel = rowLabel + [dataDictList[gainStep][key][1]]
            else:
                rowNoise = rowNoise + [''] 
                rowLabel = rowLabel + ['']
                
        row = [key] + rowNoise + rowLabel
        writer.writerow(row)

#compNoise = []
#opCompNoise = []
#resCompNoise = []
#adcCompNoise = []
#micCompNoise = []
#opContr = []
#resContr = []
#adcContr = []
#micContr = []
#
#opNoise = noiseDict['OP1','input']
#for opStep in opNoiseScale:
#    noiseDict['OP1','input'] = opNoise/np.sqrt(opStep)
#    noiseDict['OP2','input'] = opNoise/np.sqrt(opStep)
#    cNoise,oNoise,rNoise,aNoise,mNoise = nf.calcPreampNoise(noiseList,noiseDict)
#    compNoise.append(cNoise*1e6)
#    opCompNoise.append(oNoise*1e6)
#    opContr.append(oNoise**2/cNoise**2*100)
#    resCompNoise.append(rNoise*1e6)
#    resContr.append(rNoise**2/cNoise**2*100)
#    adcCompNoise.append(aNoise*1e6)
#    adcContr.append(aNoise**2/cNoise**2*100)
#    micCompNoise.append(mNoise*1e6)
#    micContr.append(mNoise**2/cNoise**2*100)
#
#
#compNoiseArray = [np.array(compNoise),np.array(opCompNoise),np.array(resCompNoise),np.array(adcCompNoise),np.array(micCompNoise)]
#contrArray = [np.array(opContr),np.array(resContr),np.array(adcContr),np.array(micContr)]
#legText = ['Total','Opamp','Resistor','ADC','Microphone']
#plotDict = {}
#
#with PdfPages('opNoise_sweep_adc_4x.pdf') as pp:
#    fig = nf.plotPreampNoise(opNoiseScale,compNoiseArray,contrArray)
#    pp.savefig()
#    plt.close('all')
