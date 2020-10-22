# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:11:17 2018

@author: sl4516
"""
import numpy as np

def LUdecomp(a,b=None):                 #Function to decompose matix a, where a and b are matrices. b included if part of a matrix equation for pivoting reasons
    L=np.zeros(a.shape)
    U=np.zeros(a.shape)                 #Generate L and U matrices of the correct size
    for m in range(L.shape[1]):
        L[m][m]=1                       #Generate '1's on trace of L
  
    comp=0
    while comp==0:                      #Assuming it is possible to pivot matrix:
        comp1=0
        for row in range(a.shape[0]):       #Implement pivoting so that a 0 is never in the trace
            if a[row][row]==0:              #If there is a 0 on the diagonal AND if there is a row without 0 in same column
                for rows in range(a.shape[0]):
                    if a[rows][row]!=0:
                        comp1+=1
                        a[[row,rows]]=a[[rows,row]]  #Swap rows 
                        if b:
                            b[[row,rows]]=b[[rows,row]]  #Also swap rows in RHS matrix

                        break    
        if comp1==0:                    #Repeat this process until no swaps are made on a pass
            comp+=1

    for i in range(U.shape[0]):         #Implementation of Crout's Algorithm to decompose matrix
        for j in range(U.shape[1]):
            if i<=j:                    #Building U matrix
                tempsum=0   
                for k in range(i):
                    tempsum+=L[i][k]*U[k][j]
                U[i][j]=a[i][j]-tempsum
            if i>j:                     #Building L matrix with '1's on the leading diagonal
                tempsum=0
                for k in range(j):
                    tempsum+=L[i][k]*U[k][j]
                L[i][j]=(a[i][j]-tempsum)/U[j][j]
    
    comb=L+U                            #Compute combination matrix of L and U
    for m in range(comb.shape[1]):
        comb[m][m]-=1
    return L,U,comb,b


def deter(a):                           #Function to compute determinant of matrix a
    up=LUdecomp(a)[1]                   #Get upper triangular matrix of decomposition of a 
    determinant=1
    for i in range(up.shape[0]):        #Multiply upper matrix's diagonals to get Trace
        determinant*=up[i][i]
    return determinant


def LUsolve(a,b1):                      #Function to solve equation of form ax=b, where a and b are matrices
    
    LUde=LUdecomp(a,b1)                 #Decompose matrix into triangluar matrices 
    L=LUde[0]                           #L matrix
    U=LUde[1]                           #U matrix
    b=LUde[3]                           #Pivoted b1
    
    i=L.shape[1]
    X=np.zeros(b.shape)                 #Generate X and Y matrices to do Back/forward substitution
    Y=np.zeros(b.shape)
    
    Y[0]=b[0]                           #Forward substitution to solve for solution matrix (X) by first obtaning Y
    for k in range(1,b.shape[0]):       #Formula from lectures used
        tempsum1=0
        for j in range(i):
            tempsum1+=L[k][j]*Y[j]      
        Y[k]=b[k]-tempsum1  

    X[b.shape[0]-1]=Y[b.shape[0]-1]/U[b.shape[0]-1][b.shape[0]-1]      #Use Y to obtain X      
    
    reversedlist=list(range(b.shape[0]))[::-1]                         #Work backwards along indices to Build X (solution) 
    for k in reversedlist:                                             #Back substitution
            tempsum1=0
            for j in range(k+1,b.shape[0]):
                tempsum1+=U[k][j]*X[j]      
            X[k]=(Y[k]-tempsum1)/U[k][k]              
    return X                            #Return solution X


def inverse(A):                         #Function to compute inverse by solving LU(inverse)=(identity)
    iden=np.zeros(A.shape)
    for m in range(A.shape[0]):
        iden[m][m]=1
    return LUsolve(A,iden)
            
a1=np.array([[3,1,0,0,0],[3,9,4,0,0],[0,9,20,10,0],[0,0,-22,31,-25],[0,0,0,-55,60]])
a2=np.array([[2],[5],[-4],[8],[9]])     #Implementation of given matrix equation


print("The combination LU matrix is: ", LUdecomp(a1)[2])                        #LU combination matrix
print("The determinant of the given matrix is: ", deter(a1))                    #Determinant
print("The solution of the given matrix equation is : ", LUsolve(a1,a2))        #Solution to matrix equation
print("The inverse of the given matrix is: ", inverse(a1))                      #Inverse of given matrix


"""
a=np.array([[0,1,0],[0,0,1],[1,0,0]])       #Validate pivoting
print(LUdecomp(a)[2])

print(np.linalg.det(a1))
print(np.matmul(a1,LUsolve(a1,a2)))         #Validate results by checking against numpy results
print(np.matmul(a1,inverse(a1)))
"""