# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:22:40 2021

@author: arnho
"""

from categoryIntMapper import CategoryIntMapper

# test file

def arrayCompare(a,b):
    length = len(a)
    if length != len(b):
        return False;
    for i in range(length):
        if a[i] != b[i]:
            return False;
    return True;


categories = [
    ['heart','spade','club','diamonds'],
    [1,2,3,4,5,6,7,8,9,10,'j','q','k']
    ]
mapper = CategoryIntMapper(categories)

assert mapper.getTotalValues() == 52;


smallestValue = [categories[0][0],categories[1][0]]
largestValue = [categories[0][3],categories[1][12]]
assert arrayCompare(mapper.intToValue(0), smallestValue)
assert arrayCompare(mapper.intToValue(51), largestValue)
assert mapper.valueToInt(smallestValue) == 0
assert mapper.valueToInt(largestValue) == 51

for i in range(mapper.getTotalValues()):
    value = mapper.intToValue(i)
    assert i == mapper.valueToInt(value)
    
from card import Card, buildHandFromCardNum, handToString, _suit
num = 25
testCard = Card(num)
assert testCard.getCardNum() == num
assert testCard._isValidSuit(_suit['heart']) == True
assert testCard._isValidSuit('fake suit') == False

aCard = Card(0)
aCard.setFaceAndSuit(testCard.getFaceValue(), testCard.getSuit())
assert aCard.getCardNum() == testCard.getCardNum()

    
    
from handHasher import HandHasher
hh = HandHasher()

cardNums = [1, 4, 23, 0, 51]
ahand = [Card(x) for x in cardNums]
cardNums.sort()
bhand = [Card(x) for x in cardNums]
aHash = hh.hashHand(ahand)
bHash = hh.hashHand(bhand)
assert aHash == bHash
print("ahand   :  bhand");
for i in range(len(ahand)):
    print (ahand[i].toString() + " : " + bhand[i].toString())
print(str(aHash) + " : " + str(bHash))

flush,faceValues = hh.unhashHand(aHash)
assert flush == False
lastValue = faceValues[0]
for value in faceValues:
    assert value >= lastValue
    
    

from handPowerCalculator import HandPowerCalculator

hand = buildHandFromCardNum([1,3,2,4,5])
calc = HandPowerCalculator()
power = calc.calculateHand(hand)
handRank,_ = calc.powerToResult(power)
assert handRank == "straight flush"


hand = [Card(face=4,suit=_suit["heart"]), Card(face=4,suit=_suit['spade']), Card(face=4,suit=_suit['diamond']), Card(face=4,suit=_suit['club']), Card(face=6,suit=_suit['club'])]
power = calc.calculateHand(hand)
handRank,_ = calc.powerToResult(power)
assert handRank == 'four of a kind'



import random
baseDeck = list(range(52))
def sdh():
    random.shuffle(baseDeck)
    hand = []
    for i in range(5):
        hand.append(baseDeck[i])
    return buildHandFromCardNum(hand)

def testHand(hand):
    power = calc.calculateHand(hand)
    handRank, values = calc.powerToResult(power)
    print(power)
    print(handToString(hand))
    print(handRank, values)


from sets import getAllKLengthSubsets

testSet = [1,2,3,4,5]
result = getAllKLengthSubsets(testSet,2)
assert len(result) == 10


testSet = [1,2,3,4,5,6,7]
result = getAllKLengthSubsets(testSet,5)
assert len(result) == 21


testCards = buildHandFromCardNum([1,7,8,20,50,35,36])
handSets = getAllKLengthSubsets(testCards,5)
bestHandPower = -1
for hand in handSets:
    bestHandPower = max(bestHandPower, calc.calculateHand(hand))
handRank, _  = calc.powerToResult(bestHandPower)
assert handRank == 'straight'


from deck import Deck
testDeck = Deck()
hand = testDeck.draw(5)
power = calc.calculateHand(hand)
print(calc.powerToResult(power))
hand = testDeck.draw(5)
power = calc.calculateHand(hand)
print(calc.powerToResult(power))
hand = testDeck.draw(5)
power = calc.calculateHand(hand)
print(calc.powerToResult(power))
hand = testDeck.draw(5)
power = calc.calculateHand(hand)
print(calc.powerToResult(power))
print(testDeck.top)


from holdemSim import HoldemSim

sim = HoldemSim()
sim.setNumOpponents(4)
sim.setHand([12,25])
result = sim.simulateRound()
print(result)


print(sim.runNRounds(1000))


from userIO import UserIO

io = UserIO()
card = io.parseCard("ah")
confirmationCard = Card(face=14,suit=_suit["heart"])
assert card.getCardNum() == confirmationCard.getCardNum()


allCards = buildHandFromCardNum(list(range(52)))
for card in allCards:
    parsedCard = io.parseCard(card.toString())
    assert card.getCardNum() == parsedCard.getCardNum()


hand = io.parseCards("ah kh qh jh 10h")
power = calc.calculateHand(hand)
rank, _ = calc.powerToResult(power)
assert rank == "straight flush"


hand = io.parseCards("4h 4d 4s 4c 2c")
power = calc.calculateHand(hand)
rank, _ = calc.powerToResult(power)
assert rank == "four of a kind"

from main import Main
m = Main(["-o","1","-r","100","-h","7d 6d"])
m.run()