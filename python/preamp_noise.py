#!/usr/bin/env python
import numpy as np
import mathfunc as mathf

Rtot = 20
gainSteps = np.arange(0,21)
noiseDict = {'OP1','RS','RF','OP2','RNS','RNF','RNBIAS','ADC','MIC'}
Rf = []
Rs = []
gain = []
for gainStep in gainSteps:
    Rstep = (1-10**(-gainStep/20.0))*Rtot
    Rf.append(Rstep)
    Rs.append(Rtot-Rstep)
    gain.append(20*np.log10(2*(1+Rstep/(Rtot-Rstep))))
    MICgain = 2*(1+Rstep/(Rtot-Rstep))
    OP1gain = 2*(1+Rstep/(Rtot-Rstep))
    RSgain = 2*(Rstep/(Rtot-Rstep))
    RFgain = 2
    OP2gain = 2
    RNSgain = 1
    RNFgain = 1
    RNBIASgain = 0 #2
    ADCgain = 1

