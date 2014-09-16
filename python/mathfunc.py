#!/usr/bin/env python
import numpy

###############################################################################
# calcInlDnl FUNCTION
# Calculates INL and DNL for dataset
# Inputs  xDataIn - x coordinates of dataset
#         yDataIn - dataset to operate on
# Returns inl - Normalized INL data
#         dnl - Normalized DNL data
###############################################################################
def calcInlDnl_bestfit(xDataIn,yDataIn):
    dnl = []
    midX = len(xDataIn)/2
    coeffs = numpy.polyfit(xDataIn,yDataIn,1)
    bestFit = [coeffs[0]*x + coeffs[1] for x in xDataIn]
    lsb = numpy.float64(bestFit[midX]-bestFit[midX-1])
    inl = numpy.subtract(yDataIn,bestFit)/lsb
    for x in range(1,len(yDataIn)):
        dnl.append((yDataIn[x]-yDataIn[x-1])/lsb-1)
    return inl,numpy.array(dnl)

def calcInlDnl_endpoint(xDataIn,yDataIn):
    dnl = []
    lsb = (yDataIn[-1] - yDataIn[0])/(xDataIn[-1] - xDataIn[0])
    offset = yDataIn[0]-xDataIn[0]*lsb
    endpoint = [x*lsb + offset for x in xDataIn]
    inl = numpy.subtract(yDataIn,endpoint)/lsb
    for x in range(1,len(yDataIn)):
        dnl.append((yDataIn[x]-yDataIn[x-1])/lsb-1)
    return inl,numpy.array(dnl)

def calcInlDnl_ideal(xDataIn,yDataIn,lsb):
    dnl = []
    ideal = [x*lsb for x in xDataIn]
    inl = numpy.subtract(yDataIn,ideal)/lsb
    for x in range(1,len(yDataIn)):
        dnl.append((yDataIn[x]-yDataIn[x-1])/lsb-1)
    return inl,numpy.array(dnl)

