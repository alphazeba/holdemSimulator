# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 00:15:11 2021

@author: arnho
"""

from deck import Deck
from card import Card, buildHandFromCardNum, handToString, handToCardNum
from handPowerCalculator import HandPowerCalculator
from sets import getAllKLengthSubsets


class HoldemSim:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.deck = Deck()
        self.calc = HandPowerCalculator()
        self.numOpponents = 1
        self.finalNumBoardCards = 5
        self.finalNumHand = 2
        self.boardCards = []
        self.hand = []
        self.visibleCardsChanged = False
        self._initGraph()

    def toString(self):
        output = ""
        output += "Hand:  " + handToString(self.hand) + "\n"
        output += "Board: " + handToString(self.boardCards) + "\n"
        output += "Opponents: " + str(self.numOpponents)
        return output
        
    def _dirtyVisibleCards(self):
        self.visibleCardsChanged = True
        
    def _cleanVisibleCards(self):
        visibleCards = self.hand + self.boardCards
        self.deck.setVisible( handToCardNum(visibleCards) )
        self.visibleCardsChanged = False
        
    def _visibleCardsHaveChanged(self):
        return self.visibleCardsChanged
        
    def setNumOpponents(self, num):
        self.numOpponents = num
        
    def setHand(self, cardNums=None, cards=None):
        self._dirtyVisibleCards()
        if cardNums != None:
            self.hand = buildHandFromCardNum(cardNums)
        else:
            self.hand = cards
        
    def setBoard(self, cardNums=None, cards=None):
        self._dirtyVisibleCards()
        if(cardNums != None):
            self.boardCards = buildHandFromCardNum(cardNums)
        else:
            self.boardCards = cards
        
    def getBestHand(self,playerHand,boardCards):
        availableCards = playerHand + boardCards
        possibleHands = getAllKLengthSubsets(availableCards, 5)
        bestPower = -1
        for hand in possibleHands:
            bestPower = max(bestPower, self.calc.calculateHand(hand))
        return bestPower
        
    def simulateRound(self):
        if(self._visibleCardsHaveChanged()):
            self._cleanVisibleCards()
        self.deck.shuffle()
        roundHands = [self.hand + self.deck.draw(self.finalNumHand-len(self.hand))]
        for i in range(self.numOpponents):
            roundHands.append(self.deck.draw(self.finalNumHand))
        roundBoard = self.boardCards + self.deck.draw(self.finalNumBoardCards-len(self.boardCards))
        handPowers = [ self.getBestHand(hand, roundBoard) for hand in roundHands ]
        bestPower = -1
        bestIndices = []
        for i in range(len(handPowers)):
            if handPowers[i] > bestPower:
                bestPower = handPowers[i]
                bestIndices = [i]
            elif handPowers[i] == bestPower:
                bestIndices.append(i)
        return (handPowers, bestIndices,  [handToCardNum(hand) for hand in roundHands], handToCardNum(roundBoard))
    
    def runNRounds(self,n):
        win = 0
        loss = 0
        push = 0
        
        for i in range(n):
            handPowers, winners, _ , _ = self.simulateRound()
            playerPower = handPowers[0]
            self._trackPower(playerPower)
            if 0 in winners:
                if len(winners) == 1:
                    win += 1
                else:
                    push += 1
            else:
                loss += 1
        return (win/n, loss/n, push/n)

    def _initGraph(self):
        self.graph = {}

    def _trackPower(self,power):
        if power in self.graph:
            self.graph[power] += 1
        else: 
            self.graph[power] = 1

    def drawGraph(self, numBuckets=100,height=25): # TODO use numpy instead.
        minPower = None
        maxPower = None
        maxBucket = 0
        for power in self.graph:
            if maxPower == None or power > maxPower:
                maxPower = power
            if minPower == None or power < minPower:
                minPower = power
        buckets = [0] * numBuckets
        powerRange = maxPower - minPower
        for power in self.graph:
            bucketIndex =  int((power-minPower)/powerRange*numBuckets)-1
            buckets[bucketIndex] += 1
            if buckets[bucketIndex] > maxBucket:
                maxBucket = buckets[bucketIndex]
        for bucket in buckets:
            if bucket > 0:
                bucket = int(bucket / maxBucket * height)-1
        
        output = ""
        for h in reversed(list(range(height))):
            for bucket in buckets:
                if bucket > h:
                    output += '#'
                else:
                    output += ' '
            output += '\n'
        minPowerString = str(minPower)
        maxPowerString = str(maxPower)
        bottomSpace = " " * (numBuckets - len(minPowerString) - len(maxPowerString))
        output += minPowerString + bottomSpace + maxPowerString + '\n'
        return output

    
    def printRound(self, roundResults):
        handPowers, winners, hands, board = roundResults
        print("board: " + handToString(buildHandFromCardNum(board)))
        print('-----')
        for i in range(len(hands)):
            winText = ""
            if i in winners:
                winText = " Winner"
            print("Player " + str(i) + winText)
            print("cards: " + handToString(buildHandFromCardNum(hands[i])))
            rank, cards = self.calc.powerToResult(handPowers[i])
            print("best hand: " + rank)
            print(cards)
            print('-----')
        
        