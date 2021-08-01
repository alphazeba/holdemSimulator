# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:50:06 2021

@author: arnho
"""

import random
from card import buildHandFromCardNum

# deck

class Deck:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.cards = list(range(52))
        self.top = 0
        
    def setVisible(self,visibleCardNums):
        self.initialize()
        newCards = []
        for card in self.cards:
            if card not in visibleCardNums:
                newCards.append(card)
        self.cards = newCards
        
    def shuffle(self):
        random.shuffle(self.cards)
        self.top = 0
        
    def draw(self,num=1):
        assert self.getRemainingCards()-num >= 0
        output = []
        for i in range(self.top,self.top+num):
            output.append(self.cards[i])
        self.top += num
        return buildHandFromCardNum(output)
        
    def getRemainingCards(self):
        return len(self.cards) - self.top
        