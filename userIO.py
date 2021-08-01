
from card import Card, _suit

class UserIO:
    def parseCard(self,cardText):
        cardText = cardText.strip().lower()
        assert len(cardText) == 2 or len(cardText) == 3
        lastPlace = len(cardText)-1
        faceText = cardText[0:lastPlace]
        suitText = cardText[lastPlace]
        return Card(face=self.parseFace(faceText),suit=self.parseSuit(suitText))

    faceMap = {
       "2": 2, "3": 3,
       "4": 4, "5": 5,
       "6": 6, "7": 7,
       "8": 8, "9": 9,
       "10":10,"j": 11,
       "q": 12,"k": 13,
       "a": 14
   }
    def parseFace(self, faceText):
        return self.faceMap[faceText]

    suitSynonyms = {
        _suit["heart"]: [_suit["heart"], "h"],
        _suit["club"]: [_suit["club"], "c"],
        _suit["spade"]: [_suit["spade"], "s"],
        _suit["diamond"]: [_suit["diamond"], "d"]
    }
    def parseSuit(self,suitText):
        for key in self.suitSynonyms:
            if suitText in self.suitSynonyms[key]:
                return key
        assert 1==2

    def parseCards(self, cardsText):
        cardTextArray = cardsText.split(' ')
        return [ self.parseCard(cardText) for cardText in cardTextArray]