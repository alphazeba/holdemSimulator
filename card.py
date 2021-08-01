# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:14:20 2021

@author: arnho
"""

from categoryIntMapper import CategoryIntMapper

# card
_cardFaceValues = list(range(2,13+2))
def getCardFaceValues():
    return _cardFaceValues.copy()


_suit = {
    "heart": "♡",
    "spade": "♠",
    "club": "♣",
    "diamond": "♢"
}
_cardSuits = [_suit["heart"],_suit["spade"],_suit["club"],_suit["diamond"]]
def getCardSuits():
    return _cardSuits.copy()

def buildCardMapper():
    categories = [
    getCardSuits(), # suits
    getCardFaceValues() # faceValues
    ]
    mapper = CategoryIntMapper(categories)
    return mapper

def buildHandFromCardNum(cardNums):
    return [Card(cardNum) for cardNum in cardNums]

def handToCardNum(hand):
    return [card.getCardNum() for card in hand]

def handToString(hand):
    result = ""
    for card in hand:
        result += card.toString() + ", "
    return result

class Card:
    face = 0
    suit = 0
    cardNum = 0
    
    def __init__(self, cardNum=None, face=None, suit=None, mapper= buildCardMapper()):
        self.mapper = mapper
        if cardNum != None:
            self.setCardNum(cardNum)
        else:
            self.setFaceAndSuit(face,suit)
        
    def setFaceAndSuit(self,face,suit):
        assert self._isValidFace(face)
        assert self._isValidSuit(suit)
        self.suit = suit
        self.face = face
        self.cardNum = self.mapper.valueToInt([suit,face])
        
    def _isValidSuit(self, suit):
        return suit in _cardSuits
    
    def _isValidFace(self, face):
        return face in _cardFaceValues
        
    def getSuit(self):
        return self.suit
    
    def getFaceValue(self):
        return self.face
    
    def setCardNum(self,cardNum):
        self.cardNum = cardNum
        self.suit,self.face = self.mapper.intToValue(cardNum)
        
    def getCardNum(self):
        return self.cardNum
    
    def getFancyFace(self):
        face = self.face
        if face == 11:
            return "J"
        elif face == 12:
            return "Q"
        elif face == 13:
            return "K"
        elif face == 14:
            return "A"
        else:
            return str(face)

    def toString(self):
        return "" + self.getFancyFace() + self.suit