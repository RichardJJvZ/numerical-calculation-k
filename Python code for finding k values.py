# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:02:51 2024

@author: richa
"""
from __future__ import division
import scipy.integrate as integrate
import scipy.special as special
from scipy.integrate import quad
import math

import numpy as np
from scipy import optimize
from mpmath import mpf, mp, qfrom, ellipk, ellipe, ellipf, ellipfun, jtheta
import matplotlib.pyplot as mpl

"""
The first part gives solutions when varkappa * n is big enough for this to give solutions
because the complete elliptic integral does not go to infinity extremely fast we need 
several algorithms depending on the expected k we find
"""
def solving_alg(n,accuracy,varkappa):
    high_k = 1
    low_k = 0
    mogelijke_k=[]
    beste_schatters_k = []
    for j in range(accuracy):
        m=100000
        stepsize = (high_k-low_k)/m
        for i in range(m):
            test = low_k + i*stepsize
            if abs(special.ellipk(test**2) * test * 2 * varkappa * n -math.pi) < 0.1**(j+1):
                mogelijke_k.append(test)
        if mogelijke_k == []:
            break
        low_k = mogelijke_k[0]
        high_k = mogelijke_k[-1]
        if low_k == high_k:
            if m < 1000 * 2**10:
                m = 2 * m
            else:
                beste_schatters_k.append(low_k)
            best_k = low_k
        else:
            best_k = (high_k+low_k)/2
            mogelijke_k = []
        beste_schatters_k.append(best_k)
    return beste_schatters_k[-1]
"""
When varkappa * n is between 0.28 and 0.15 this gives the fastest approximation
"""
def solving_alg_smallvarkappa(n,accuracy,varkappa):
    high_k = 1
    low_k = 0.9999
    mogelijke_k=[]
    beste_schatters_k = []
    for j in range(accuracy):
        m=100000
        stepsize = (high_k-low_k)/m
        for i in range(m):
            test = low_k + i*stepsize
            if abs(special.ellipk(test**2) * test * 2 * varkappa * n -math.pi) < 0.1**(j+1):
                mogelijke_k.append(test)
        if mogelijke_k == []:
            break
        low_k = mogelijke_k[0]
        high_k = mogelijke_k[-1]
        if low_k == high_k:
            if m < 1000 * 2**10:
                m = 2 * m
            else:
                beste_schatters_k.append(low_k)
            best_k = low_k
        else:
            best_k = (high_k+low_k)/2
            mogelijke_k = []
        beste_schatters_k.append(best_k)
    return beste_schatters_k[-1]
"""
When varkappa *n is between 0.09 and 0.15 this gives the fastest approximation
when it is even smaller python is unable to compute it as the answer would be
all 9's and when this no lnonger gives a good enough approximation python cannot
go to another step between this and 1
"""
def solving_alg_very_smallvarkappa(n,accuracy,varkappa):
    high_k = 1
    low_k = 0.99999999
    mogelijke_k=[]
    beste_schatters_k = []
    for j in range(accuracy):
        m=1000000
        stepsize = (high_k-low_k)/m
        for i in range(m):
            test = low_k + i*stepsize
            if abs(special.ellipk(test**2) * test * 2 * varkappa * n -math.pi) < 0.1**(j+1):
                mogelijke_k.append(test)
        if mogelijke_k == []:
            break
        low_k = mogelijke_k[0]
        high_k = mogelijke_k[-1]
        if low_k == high_k:
            if m < 1000 * 2**10:
                m = 2 * m
            else:
                beste_schatters_k.append(low_k)
            best_k = low_k
        else:
            best_k = (high_k+low_k)/2
            mogelijke_k = []
        beste_schatters_k.append(best_k)
    return beste_schatters_k[-1]
varkappalist = []
k_list = []

#This function combines the abo
def Total_solve(n, accuracy, varkappa):
    if varkappa * n >= 0.28:
        return solving_alg(n, accuracy, varkappa)
    elif varkappa * n >= 0.15:
        return solving_alg_smallvarkappa(n, accuracy, varkappa)
    else:
        return solving_alg_very_smallvarkappa(n, accuracy, varkappa)

def make_range_givenvarkappa(varkappa):
    var_k_list = []
    for a in range(10):
        ans = 0
        ans = Total_solve(a+1,10,varkappa)
        var_k_list.append(ans)
        print((a+1)/10)
    return var_k_list, varkappa
def make_range_givenwinding(n):
    winding_k_list = []
    for b in range(10):
        ans = Total_solve(n,10,1-0.1 * b)
        winding_k_list.append(ans)
        print(b/10)
    return winding_k_list,n
def make_range_given_lowvarkappa(varkappa):
    var_k_list = []
    for a in range(5):
        ans = 0
        ans = Total_solve(a+6,10,varkappa)
        var_k_list.append(ans)
        print((a+1)/10)
    return var_k_list, varkappa

#for a in {0.09,0.08,0.07,0.06,0.05,0.04,0.03,0.02}:
#    print(make_range_given_lowvarkappa(a))
    