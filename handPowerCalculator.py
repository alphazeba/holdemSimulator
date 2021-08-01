# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 15:30:10 2021

@author: arnho
"""

from handHasher import HandHasher
from categoryIntMapper import CategoryIntMapper
from card import getCardFaceValues


_highCard = "high card"
_pair = "pair"
_twoPair = "two pair"
_threeOfAKind = "three of a kind"
_straight = "straight"
_flush = "flush"
_fullHouse = "full house"
_fourOfAKind = "four of a kind"
_straightFlush = "straight flush"
_handRanking = [_highCard, _pair, _twoPair, _threeOfAKind, _straight, _flush, _fullHouse, _fourOfAKind, _straightFlush]

class HandPowerCalculator:
    def __init__(self):
        self.powerMemo = {}
        self.handHasher = HandHasher()
        self.powerMapper = self._buildPowerMapper()
        self.runs = 0
        self.usedMemo = 0
        
    def calculateHand(self,hand):
        self.runs += 1
        handHash = self._hashHand(hand)
        if handHash in self.powerMemo:
            self.usedMemo += 1
            return self.powerMemo[handHash]
        handPower = self._calculateHand(handHash)
        self.powerMemo[handHash] = handPower
        return handPower
    
    def powerToResult(self,power):
        handRank, c1,c2,c3,c4,c5 = self.powerMapper.intToValue(power)
        return (handRank,[c1,c2,c3,c4,c5])
        
    def getEffortSavedRatio(self):
        return self.usedMemo/self.runs
    
    def _buildPowerMapper(self):
        handTypes = _handRanking.copy()
        faceValues = getCardFaceValues()
        categories = [handTypes]
        for i in range(5):
            categories.append(faceValues)
        return CategoryIntMapper(categories)
        
    def _hashHand(self,hand):
        return self.handHasher.hashHand(hand)
    
    def _unhashHand(self,handHash):
        flush, handValues = self.handHasher.unhashHand(handHash)
        return flush, handValues
    
    def _calculateHand(self,handHash):
        flush, handValues = self._unhashHand(handHash)
        handValues = list(reversed(handValues)) # handHashes store faceValues in increasing sorted order.
        straight,lowStraight = self._isStraight(handValues)
        if(straight and flush):
            if lowStraight:
                handValues = self._getLowStraightHandValues()
            return self._powerMap(_straightFlush,handValues)
        matches = self._findMatches(handValues)
        match = self._isFourOfAKind(matches)
        if(match != None):
            return self._powerMap(_fourOfAKind, self._moveValuesToFront(handValues,match))
        match = self._isFullHouse(matches)
        if(match != None):
            threeOfAKind, twoOfAKind = match
            return self._powerMap(_fullHouse, self._moveValuesToFront( self._moveValuesToFront(handValues,twoOfAKind), threeOfAKind))
        if(flush):
            return self._powerMap(_flush, handValues)
        if(straight):
            if lowStraight:
                handValues = self._getLowStraightHandValues()
            return self._powerMap(_straight, handValues)
        match = self._isThreeOfAKind(matches)
        if(match != None):
            return self._powerMap(_threeOfAKind, self._moveValuesToFront(handValues, match))
        match = self._isTwoPair(matches)
        if(match != None):
            largePair,smallPair = match
            return self._powerMap(_twoPair, self._moveValuesToFront( self._moveValuesToFront(handValues,smallPair), largePair))
        match = self._isPair(matches)
        if(match != None):
            return self._powerMap(_pair, self._moveValuesToFront(handValues, match))
        return self._powerMap(_highCard, handValues)
    
    def _powerMap(self, handRank, handValues):
        return self.powerMapper.valueToInt([handRank] + handValues)
    
    def _getLowStraightHandValues(self):
        return [5,4,3,2,14]
    
    def _isStraight(self,handValues):
        lowStraightPattern = [14,5,4,3,2]
        lastValue = handValues[0]
        straight = True
        lowStraight = (lastValue == lowStraightPattern[0])
        for i in range(1,len(handValues)):
            value = handValues[i]
            if value != lastValue-1:
                straight = False
            if value != lowStraightPattern[i]:
                lowStraight = False
            lastValue = value
        straight = straight or lowStraight
        return (straight, lowStraight)
    
    def _isFourOfAKind(self,matches):
        if len(matches) == 1:
            numMatches, value = matches[0]
            if numMatches == 4:
                return value
        return None
    
    def _isFullHouse(self,matches):
        if len(matches) == 2:
            threeOfAKind = None
            twoOfAKind = None
            for match in matches:
                numMatches, value = match
                if numMatches == 3:
                    threeOfAKind = value
                elif numMatches == 2:
                    twoOfAKind = value
            if threeOfAKind != None:
                return (threeOfAKind, twoOfAKind)
        return None
    
    def _isThreeOfAKind(self,matches):
        if len(matches) == 1:
            numMatches, value = matches[0]
            if(numMatches == 3):
                return value
        return None
    
    def _isPair(self,matches):
        if len(matches) == 1:
            numMatches, value = matches[0]
            if(numMatches == 2):
                return value
        return None
    
    def _isTwoPair(self,matches):
        if len(matches) == 2:
            aMatches, aValue = matches[0]
            bMatches, bValue = matches[1]
            if(aMatches == 2 and bMatches == 2):
                if aValue > bValue:
                    return (aValue,bValue)
                else:
                    return (bValue,aValue)
        return None
    
    def _findMatches(self,handValues):
        matches = {}
        for value in handValues:
            if value in matches:
                matches[value] += 1
            else:
                matches[value] = 1
        matchList = []
        for valueKey in matches:
            numMatches = matches[valueKey]
            if numMatches > 1:
                matchList.append([numMatches,valueKey])
        return matchList
    
    def _moveValuesToFront(self, handValues, moveValue):
        prefill = []
        body = []
        for value in handValues:
            if value == moveValue:
                prefill.append(value)
            else:
                body.append(value)
        return prefill + body
    
