

import sys
from holdemSim import HoldemSim
from userIO import UserIO
from card import handToCardNum

class Main:
    def __init__(self, arguments):
        self.arguments = arguments
        self.io = UserIO()
        self.sim = HoldemSim()

    def getFlag(self, flag):
        flagIndex = -1
        toMatch = "-"+flag
        for i, arg in enumerate(self.arguments):
            if arg == toMatch:
                flagIndex = i
                break
        if flagIndex == -1:
            return None
        argumentIndex = flagIndex + 1
        if len(self.arguments) <= argumentIndex:
            return None
        return self.arguments[argumentIndex]

    def spacer(self):
        print("---------")

    def run(self):
        handInput = self.getFlag('h')
        boardInput = self.getFlag('b')
        opponentsInput = self.getFlag("o")
        roundsInput = self.getFlag('r')
        rounds = 1000

        if(handInput != None):
            self.sim.setHand( cards=self.io.parseCards(handInput))
        if(boardInput != None):
            self.sim.setBoard( cards=self.io.parseCards(boardInput))
        if(opponentsInput != None):
            self.sim.setNumOpponents( int(opponentsInput) )
        if(roundsInput != None):
            rounds = int(roundsInput)

        print("Hold'em Simulator")
        self.spacer()
        print(self.sim.toString())
        self.spacer()
        result = self.sim.runNRounds(rounds)

        win,loss,push = result
        print("W: " + str(win))
        print("L: " + str(loss))
        print("P: " + str(push))
        self.spacer()
        print(self.sim.drawGraph())

if __name__ == "__main__":
    arguments = sys.argv[1:]
    main = Main(arguments)
    main.run()