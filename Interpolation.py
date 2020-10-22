# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 12:49:28 2018

@author: samla
"""
import numpy as np
import matplotlib.pyplot as plt
from Matrix_Solving import LUsolve


def linearint(a,value):                                 #a is 2-array of coordinates, value is x-value required to interpolate for
    comp=0
    while comp==0:                                      #Sorting elements of data, so that interval that value falls into can be found
        comp1=0
        for m in range(len(a)-1):
            if a[m][0]>a[m+1][0]:
                a[m],a[m+1]=a[m+1],a[m]                 #Swap values if one is larger than t'other
                comp1+=1
        if comp1==0:
            comp+=1

    index=-1
    for m in range(len(a)-1):                           #Find index of lower bound of the interval that value falls into
        if value>=a[m][0] and value<a[m+1][0]:
            index=m
            break
    if index==-1:
        return None                                     #(below) return interpolated value from standard formula
    return ((a[index+1][0]-value)*a[index][1]+(value-a[index][0])*a[index+1][1])/(a[index+1][0]-a[index][0])
    

    
def cubicspline(a,value):                               #a is 2-array of coordinates, value is x-value required to interpolate for
    mat=np.zeros((len(a),len(a)))
    mat1=np.zeros((len(a),1))                           #To encode linear equations
    
    comp=0
    while comp==0:                                      #Sorting elements of data, so that interval that value falls into can be found
        comp1=0
        for m in range(len(a)-1):
            if a[m][0]>a[m+1][0]:
                a[m],a[m+1]=a[m+1],a[m]                 #Swap values if one is larger than t'other
                comp1+=1
        if comp1==0:
            comp+=1                                     #If no swaps made down the list, exit loop

    
    def fna(x,xi,xip):                                  #Implementation of the given A/B/C/D functions as functions of required x, and the upper and lower bounds of its interval 
        return (xip-x)/(xip-xi)
    def fnb(x,xi,xip):
        return 1-fna(x,xi,xip)
    def fnc(x,xi,xip):
        return ((fna(x,xi,xip)**3-fna(x,xi,xip))*((xip-xi)**2))/6
    def fnd(x,xi,xip):
        return ((fnb(x,xi,xip)**3-fnb(x,xi,xip))*((xip-xi)**2))/6
    
    mat[0][0]=1                                         #Natural spline BCs
    mat[len(a)-1][len(a)-1]=1
    for i in range(1,len(a)-1):                         #Construct matrix encoding linear equations 
        mat[i][i-1]=(a[i][0]-a[i-1][0])/6
        mat[i][i]=(a[i+1][0]-a[i-1][0])/3
        mat[i][i+1]=(a[i+1][0]-a[i][0])/6
        mat1[i][0]=((a[i+1][1]-a[i][1])/(a[i+1][0]-a[i][0]))-((a[i][1]-a[i-1][1])/(a[i][0]-a[i-1][0]))
    
    solvedf=LUsolve(mat,mat1)                           #Solve matrix equation

    index=-1                                            #Find index of lower bound of the interval that value falls into
    for m in range(len(a)-1):
        if value>=a[m][0] and value<a[m+1][0]:
            index=m
            break
    if index==-1:
        return None                                     #(below) return interpolated value from standard formula
    fx=(fna(value,a[index][0],a[index+1][0])*a[index][1])+(fnb(value,a[index][0],a[index+1][0])*a[index+1][1])+(fnc(value,a[index][0],a[index+1][0])*solvedf[index][0])+(fnd(value,a[index][0],a[index+1][0])*solvedf[index+1][0])
    return fx
    

lists=[[-2.1, 0.012155],[-1.45, 0.122151],[-1.3, 0.184520],[-0.2, 0.960789],[0.1, 0.990050],[0.15, 0.977751],[0.8, 0.527292],[1.1, 0.298197],[1.5, 0.105399],[2.8, 3.936690e-4],[3.8, 5.355348e-7]]
 

xval=np.arange(-10,10,0.1)
yvalspline=[cubicspline(lists,x) for x in  xval]        #Generating the x-values and related interpolated function values
yvallin=[linearint(lists,x) for x in  xval]
xval1=[lists[m][0] for m in range(len(lists))]
yval=[lists[m][1] for m in range(len(lists))]

for i in range(len(lists)):                             #Add origonal data to linear interpolated data
    np.append(xval,lists[i][0])
    np.append(yvallin,lists[i][1])
    
plt.plot(xval1,yval,'g+', label='Given data')                              #PLotting linear (black) and spline (red) graphs
plt.plot(xval,yvallin,'k-', label='Linearly interpolated data')
plt.plot(xval,yvalspline,'r-', label='Cubic spline interpolated data')
plt.title("Interpolation of given data using linear and cubic spline methods")
plt.legend(loc='upper right',prop={'size': 9})
plt.xlabel("x")
plt.ylabel("y")
        