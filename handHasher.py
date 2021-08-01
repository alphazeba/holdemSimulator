# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 15:35:07 2021

@author: arnho
"""

from categoryIntMapper import CategoryIntMapper
from card import getCardFaceValues, Card

# hand hasher

class HandHasher:
    def __init__(self):
        self.mapper = self._buildHandMapper()
        
    def hashHand(self,hand):
        assert len(hand) == 5
        flush = self._isFlush(hand)
        faceValues = self._handToSortedFaceValueList(hand)
        handValue = [flush] + faceValues
        return self.mapper.valueToInt( handValue )
    
    def unhashHand(self,handHash):
        flush, c1,c2,c3,c4,c5 = self.mapper.intToValue(handHash)
        handValues = [c1,c2,c3,c4,c5]
        return (flush, handValues)
        
        
    def _buildHandMapper(self):
        faceValues = getCardFaceValues()
        mapperCategories = [
            [False, True] # flush states.
        ]
        for i in range(5):
            mapperCategories.append(faceValues.copy())
        return CategoryIntMapper(mapperCategories)
        
    def _isFlush(self,hand):
        suit = hand[0].getSuit()
        for i in range(1,len(hand)):
            if suit != hand[i].getSuit():
                return False
        return True
    
    def _handToSortedFaceValueList(self,hand):
        # values are sorted smallest to largest so that the resulting hashvalues tend smaller.
        faceValueList = []
        for card in hand:
            faceValueList.append(card.getFaceValue())
        faceValueList.sort()
        return faceValueList