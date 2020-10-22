# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:14:34 2018

@author: sl4516
"""
import numpy as np
import matplotlib.pyplot as plt

def f(x):                                   #Define given top hat function
    if 3<=x<=5:
        return 4
    else:
        return 0

def g(x):                                   #Define given gaussian function
    if abs(x)<3:
        return np.exp((-1*x**2)/2.)/(np.sqrt(2*np.pi))
    else:
        return 0                            #Padding of Gaussian function to prevent high frequency overspillage

rng=np.arange(-12.8,12.8,0.1)               #Have 256 samples to optimize, FFT uses 2^N samples 
fx=[f(rang) for rang in rng]                #Sample given functions
gx=[g(rang) for rang in rng]
fftf=np.fft.fft(fx)                         #Fast fourier transform functions
fftg=np.fft.fft(gx)
conv=np.fft.ifft(fftf*np.conj(fftg)*(1./(2*np.pi)))  #Convolve functions using convolution theorem, use conjugate of fft(g) to alias

rng1=np.fft.fftfreq(len(rng),0.1)           #Frequency domain for fourier transforms 
rng2=np.fft.fftshift(rng)                   #Frequency domain shifted for convolution


plt.plot(rng,fx, label="Function f")                         #Plot given functions in real space in sensible range
plt.plot(rng,gx, label="Function g")
plt.title("Functions f and g")
plt.legend(loc='upper right',prop={'size': 9})
plt.xlabel("t")
plt.xlim(-4,8)

fig1, ax1 = plt.subplots()
plt.plot(rng1,fftf, label="FT of f")                         #Plot transforms of given functions in frequency space in sensible range
plt.plot(rng1,fftg, label="FT of g")
plt.xlim(-2,2)
plt.title("Fourier transforms of functions f and g")
plt.legend(loc='upper right',prop={'size': 9})
plt.xlabel("frequency")

fig1, ax1 = plt.subplots()
plt.plot(rng2,np.abs(conv))                                  #Plot convolution in real space in sensible range
plt.title("Convolution of functions f and g")
plt.legend(loc='upper right',prop={'size': 9})
plt.xlabel("t")
plt.ylabel("f convolved with g as a function of t")
plt.xlim(-1,11)