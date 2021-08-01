# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:18:19 2021

@author: arnho
"""


# categoryIntConverter

class CategoryIntMapper:
    def __init__(self,categories):
        self.setCategories(categories)
            
    def setCategories(self,categories):
        self.levels = categories
        self.totalValues = 1
        for level in categories:
            self.totalValues *= len(level)
            
    def getTotalValues(self):
        return self.totalValuesF
    
    def valueToInt(self,value):
        n = 0
        for li,level in enumerate(self.levels):
            n *= len(level)
            for ci,category in enumerate(level):
                if value[li] == category:
                    n += ci
                    break
                elif ci == len(level)-1:
                    invalidCategoryName = 1
                    print("could not find")
                    print(value[li])
                    print("in")
                    print(level)
                    assert invalidCategoryName == 0
        return n
        
    def intToValue(self,n):
        assert n >= 0
        assert n < self.totalValues
        value = []
        curn = n
        for li,level in enumerate( reversed(self.levels) ):
            remainder = curn%len(level)
            value.append(level[remainder])
            curn = curn // len(level)
        return list(reversed(value))
            