# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 12:02:06 2018

@author: sl4516
"""
import numpy as np
from mpmath import mp
mp.prec=112                      #Specify precision of floats from external module


#machine accuracy is smallest number meaningfully subracted from 1

print(np.finfo(np.longdouble))  #Machine specs

def macac(a,b,c):
    floats=[]                   #List of floats that can be meaningfull subtracted from 1
    while c-a<c:                #While '1-number' is still meaningful
        floats.append(a)        #Add number to list of meaningful floats
        a=a/b                   #Divide by 2 and repeat- 2 must be a float of correct form 
    return floats[-1]           #Final list value is machine accuracy


print("Machine accuracy:", macac(0.5,2,1))

print("float 16:", "%.100s" % macac(np.float16(0.5),np.float16(2),np.float16(1)))
print("float 32:", "%.100s" % macac(np.float32(0.5),np.float32(2),np.float32(1)))
print("float 64:", "%.100s" % macac(np.float64(0.5),np.float64(2),np.float64(1)))           #note problems and overcome-machine limitations
print("float 128:", "%.200s" % macac(mp.mpf(0.5),mp.mpf(2),mp.mpf(1)))                      #'np.float128' not supported on windows

