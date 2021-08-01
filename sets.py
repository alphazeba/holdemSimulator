# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:25:06 2021

@author: arnho
"""

def appendToAll(value, array):
    for item in array:
        item.append(value)
    return array

def getAllKLengthSubsets(array,k, startIndex=0):
    if k == 0: return [[]]
    m = len(array)-startIndex-(k-1)
    output = []
    for i in range(m):
        index = startIndex+i
        value = array[index]
        output = output + appendToAll(value,getAllKLengthSubsets(array,k-1,index+1))   
    return output
    
    
    
