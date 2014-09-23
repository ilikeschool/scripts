#!/usr/bin/env python
import sys
import re
import csv
import numpy as np
import mathfunc as mf
from itertools import product
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


dacBits = 7
thermBits = 4 

#fileName = "20140822_tb_hp_dac_linearity_mc_ideal_bias.csv"

fileName = sys.argv[1] if len(sys.argv) >= 2 else raw_input("Enter name of file to parse: ")
fileName_noExt = re.search('(.+?)(\.[^.]*$|$)',fileName).group(1)
fileName_match_csv = fileName_noExt + '_match_sum.csv'
fileName_stats_csv = fileName_noExt + '_stats_sum.csv'
fileName_pdf = fileName_noExt + '_plots.pdf'

indexList = []
dataList  = []
with open(fileName,'rb') as f:
    reader = csv.reader(f)
    header = reader.next()
    indexList = [int(float(i)) for i in header[1:dacBits+2**thermBits-1-thermBits+4]]
    for row in reader:
        dirList=[]
        dirList.append([float(i) for i in row[1:dacBits+2**thermBits-1-thermBits+4]])
        dirList.append([float(i) for i in row[dacBits+2**thermBits-1-thermBits+4:]])
        dataList.append(dirList)

indexArray = np.array(indexList)
dataArray = np.array(dataList)

histArray = np.concatenate((dataArray.T[::-1,1,:],dataArray.T[:,0,:]))
fullIndexArray = np.concatenate((indexArray[::-1].astype(float)/2,-indexArray.astype(float)/2))

stat = []
for bitHist,bitIndex in zip(histArray,fullIndexArray):
    bitStat = (bitIndex,np.mean(bitHist),np.std(bitHist),np.std(bitHist)/np.mean(bitHist)*100)
    stat.append(bitStat)    

statArray = np.array(stat)

bits = []
for bit in product('01',repeat=dacBits):
    bits.append(bit)

bitsArray = np.fliplr(np.array(bits)).astype(int)

if thermBits > 0:
    newBitsArray = []
    thermWeights = np.logspace(0,thermBits-1,num=thermBits,base=2)
    for i,bit in enumerate(bitsArray):
        bitSum = np.multiply(bit[dacBits-thermBits:dacBits],thermWeights).sum()
        thermCode = [1 if bitSum>=j else 0 for j in range(1,2**thermBits)]
        newBit = np.append(np.delete(bit,np.s_[dacBits-thermBits:dacBits]),thermCode)
        newBitsArray.append(newBit)
    bitsArray = np.array(newBitsArray)

         
isum = []
inl_best=[]
dnl_best=[]
inl_end=[]
dnl_end=[]
inl_ideal=[]
dnl_ideal=[]
max_inl_best=[]
max_dnl_best=[]
max_inl_end=[]
max_dnl_end=[]
max_inl_ideal=[]
max_dnl_ideal=[]
lsbIdeal = 500e-9
xData = np.arange(-2**dacBits,2**dacBits)+0.5
for data in dataArray:
    isumBip = []
    for dataDir in data:
        isumDir=[]
        dataOffset = dataDir[1:-1]-dataDir[0]
        for bit in bitsArray:
            isumDir.append(np.multiply(dataOffset[1:],bit).sum()+dataOffset[0]+dataDir[0])
        isumBip.append(np.array(isumDir))
    isum.append(np.concatenate((isumBip[1][::-1],isumBip[0])))
    inl,dnl = mf.calcInlDnl_bestfit(xData,isum[-1])
    inl_best.append(inl)
    dnl_best.append(np.insert(dnl,0,0))
    max_inl_best.append((inl.min(),inl.max()))
    max_dnl_best.append((dnl.min(),dnl.max()))
    inl,dnl = mf.calcInlDnl_endpoint(xData,isum[-1])
    inl_end.append(inl)
    dnl_end.append(np.insert(dnl,0,0))
    max_inl_end.append((inl.min(),inl.max()))
    max_dnl_end.append((dnl.min(),dnl.max()))
    inl,dnl = mf.calcInlDnl_ideal(xData,isum[-1],lsbIdeal)
    inl_ideal.append(inl)
    dnl_ideal.append(np.insert(dnl,0,0))
    max_inl_ideal.append((inl.min(),inl.max()))
    max_dnl_ideal.append((dnl.min(),dnl.max()))

with open(fileName_match_csv,'wb') as fmatch:
    writer_match = csv.writer(fmatch)
    header = ['CODE','MEAN','STD','MISMATCH']
    writer_match.writerow(header)
    for stat in statArray:
        writer_match.writerow(stat)

with open(fileName_stats_csv,'wb') as fsum:
    writer_sum = csv.writer(fsum)
    header = ['MIN_INL_BEST','MAX_INL_BEST','MIN_DNL_BEST','MAX_DNL_BEST','MIN_INL_END','MAX_INL_END','MIN_DNL_END','MAX_DNL_END','MIN_INL_IDEAL','MAX_INL_IDEAL','MIN_DNL_IDEAL','MAX_DNL_IDEAL']
    writer_sum.writerow(header)
    for a,b,c,d,e,f in zip(max_inl_best,max_dnl_best,max_inl_end,max_dnl_end,max_inl_ideal,max_dnl_ideal):
        writer_sum.writerow(list(a+b+c+d+e+f))

supTitle = ['Best Fit','Endpoint Fit','Ideal Fit(LSB=500nA)']

with PdfPages(fileName_pdf) as pp:
    for inlc,dnlc,supTitleC in zip([inl_best,inl_end,inl_ideal],[dnl_best,dnl_end,dnl_ideal],supTitle):
        fig = plt.figure(figsize=(10.67, 7.13), dpi=100)
        ax = plt.subplot(211)
        box = ax.get_position()
        plt.grid()
        gcaFont = 8
        legFont = 6
        titleFont = 8 
        supTitleFont = 10
        msrYaxLabel = 'INL(LSB)'
        msrXaxLabel = 'intput code'
        #ax.set_position([box.x0, box.y0, box.width*.65, box.height])
        for inlb in inlc:
            plt.plot(xData,inlb)
        plt.xlim(xData[0],xData[-1])
        plt.ylabel(msrYaxLabel,fontsize=gcaFont)
        plt.xlabel(msrXaxLabel,fontsize=gcaFont)
        #plt.title('INL',fontsize=titleFont)
        ax = plt.subplot(212)
        box = ax.get_position()
        plt.grid()
        msrYaxLabel = 'DNL(LSB)'
        for dnlb in dnlc:
            plt.plot(xData,dnlb)
        plt.xlim(xData[0],xData[-1])
        plt.ylabel(msrYaxLabel,fontsize=gcaFont)
        plt.xlabel(msrXaxLabel,fontsize=gcaFont)
        #plt.title('DNL',fontsize=titleFont)
        plt.suptitle(supTitleC,fontsize=supTitleFont)
        pp.savefig()
        plt.close('all')
