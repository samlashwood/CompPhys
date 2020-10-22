# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 11:02:26 2018

@author: sl4516
"""

import numpy as np
import matplotlib.pyplot as plt
import timeit

np.random.seed(1)                                   #Seed for random numbers

rands=np.random.uniform(0,1,1400000)                #Generate a list of random numbers using seed (above)
unirands=rands[:1000000]
plt.hist(unirands,50)                               #Histogram with 50 bins of 10^5 numbers        
plt.title("Uniform random numbers between 0 and 1") 

randspi=[np.pi*x for x in rands]                    #List of uniform random numbers between 0 and pi

                                                    
def randstranspdf(a=rands,b=2):                     #Transformation method for given function to get weighted numbers
    m=[np.arccos(1-b*k) for k in a]
    return m 
randspdf1=randstranspdf()[:1000000]

fig1, ax1 = plt.subplots()
plt.hist(randspdf1,50)                              #Histogram with 50 bins for transformation method of 10^5 numbers 
plt.title("sin(x)/2 distributed random numbers between 0 and pi (transformation method)")
 
rands4pi=[(4/np.pi)*x for x in rands]               #4/pi to cover domain of transformation function
randspdf2=randstranspdf(a=rands4pi,b=np.pi/2.)      #Transformation method used again to get comparison function for rejection method

np.random.seed(14)                                  #Seed for random numbers
randsnew=np.random.uniform(0,1,1400000)             #Generate a new list of random numbers so there is no correlation for the rejection method

def P2(x):                                          #Desired given function for rejection method
    return (2.0/np.pi)*(np.sin(x))**2
                                        
def rejection_const(a=randspi):                     #Rejection method for second given function to get weighted numbers using constant comparison function
    accepts=[a[k] for k in range(1400000) if P2(a[k])>=randsnew[k]]
    return accepts                                  #Comparison function y=1

def rejection_sin(a=randspdf2):                     #Rejection method for second given function to get weighted numbers using 2/pi*sin(x) comparison function
    accepts=[a[k] for k in range(1400000) if P2(a[k])>=randsnew[k]*(2./np.pi)*np.sin(a[k])]      #Comaprative list comprehension used to increase efficiency
    return accepts

randsrej=rejection_const()[:1000000]                #Weighted randoms using constant comp. fn.
fig1, ax1 = plt.subplots()
plt.hist(randsrej,50)                               #Histogram with 50 bins of 10^5 numbers 
plt.title("2sin^2(x)/pi distributed random numbers between 0 and pi using constant comparison (rejection method)")

randsrej1=rejection_sin()[:1000000]                 #Weighted randoms using given sinusoid comp. fn.
fig1, ax1 = plt.subplots()
plt.hist(randsrej1,50)                              #Histogram with 50 bins of 10^5 numbers  
plt.title("2sin^2(x)/pi distributed random numbers between 0 and pi using 2sin(x)/pi comparison (rejection method)")

print("rejection/transformation ratio is ", timeit.timeit(rejection_sin,number=10)/timeit.timeit(randstranspdf,number=10))      #Time method and print time ratio rejetcion/transformation method  

#Note: rejection method and transformation methods written as functions so that the 'timeit' module could be easily used to time the processes    
            