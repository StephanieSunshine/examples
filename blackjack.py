#!/usr/bin/env python3

import random
import sys
from time import sleep

class Card:
    cardName = {
        "Ace": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
        "Six": 6,
        "Seven": 7,
        "Eight": 8,
        "Nine": 9,
        "Ten": 10,
        "Jack": 10,
        "Queen": 10,
        "King": 10
    }

    cardSuit = [ "clubs", "hearts", "spades", "diamonds" ]

    # constructor
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit

    # string value of card instance
    def __str__(self):
        # return human readable string of card
        return self.name + " of " + self.suit

    # integer value of card instance
    def __call__(self):
        # return value of card
        return self.cardName[self.name]

class Game:
    endTime = 1 # seconds

    def __init__(self):
        self.scores = {"computer": 0, "human": 0}
        self.hands = {"computer": [], "human": []}
        # human result
        self.res = 0
        # computer result
        self.cRes = 0

    # build deck
    def buildDeck(self):
        self.deck = []
        # build deck
        for n in Card.cardName:
            for s in Card.cardSuit:
                self.deck.append(Card(n, s))

    # shuffle deck
    def shuffle(self, times):
        for i in range(times):
            random.shuffle(self.deck)

    # deal
    def deal(self):
        self.hands["human"].append(self.deck.pop())
        self.hands["computer"].append(self.deck.pop())

        self.hands["human"].append(self.deck.pop())
        self.hands["computer"].append(self.deck.pop())

    # game loop
    def begin(self):
        # clear screen
        sys.stdout.write("\x1b[2J\x1b[H")

        while True:
            self.buildDeck()
            self.shuffle(6)
            self.hands = {"computer": [], "human": []}
            self.playRound()

    # play round
    def playRound(self):
        print("Blackjack!\n")
        self.deal()
        gameOver = self.playHuman()
        if not gameOver:
            gameOver = self.playComputer()
        if not gameOver:   
            print("Round result: human: %s computer %s\n" % (self.res, self.cRes))
            if self.res > self.cRes:
                print("Human wins!\n")
                self.scores["human"] += 1
            elif self.cRes > self.res:
                print("Computer wins!\n")
                self.scores["computer"] += 1
            else:
                print("Computer pushes!\n")

    # play human
    def playHuman(self):
        # human turn
        while True:
            print("computer: %s human: %s\n" % (self.scores["computer"], self.scores["human"]))
            print("Computer is showing: %s\n" % self.hands["computer"][-1])
            print("You have:")
            
            # do we have aces?
            ace = False
            # does the computer have blackjack?
            compBJack = False
            # does the human have blackjack?
            humanBJack = False
            # how many aces does the human have?
            aceCount = 0
            # what is the value of everything else we have?
            value = 0
            # what is our highest valid card combo
            self.res = 0

            # prepping for blackjack test
            for c in self.hands["human"]:
                print(c)
                if c() == 1:
                    ace = True
                    aceCount += 1
                else:
                    value += c()

            # edge case of more than one ace makes me have to check this
            if ace and aceCount == 1 and value == 10 and len(self.hands["human"]) == 2:
                humanBJack = True
                print("\nValue: 21")
            elif ace:
                # first ace is 11, all following are 1, aceCount + 10 makes for the first one @ 11 and all following 1
                # if it is under 22 with the first ace at 11, then show the option
                if (aceCount + 10 + value) < 22:
                    print("\nValue: %s or %s" % (aceCount + value, aceCount + 10 + value))
                    # take the higher of the two
                    self.res = aceCount + 10 + value
                else:
                    print("\nValue: %s" % (aceCount + value))
                    self.res = aceCount + value
            else:
                print("\nValue: %s" % value)
                self.res = value

            # check for blackjacks
            if len(self.hands["computer"]) == 2 and len(self.hands["human"]) == 2:
                if self.hands["computer"][0]() + self.hands["computer"][1]() == 11 and (self.hands["computer"][0]() == 1 or self.hands["computer"][1]() == 1):
                    # computer has blackjack
                    compBJack = True
                if compBJack and humanBJack:
                    print("Both have blackjack, dealer pushes")
                    sleep(self.endTime)
                    # games over, return true so computer doesn't try to run
                    return(True)
                elif compBJack:
                    print("Computer has blackjack!")
                    self.scores["computer"] += 1
                    sleep(self.endTime)
                    return(True)
                elif humanBJack:
                    print("Human has blackjack!")
                    self.scores["human"] += 1
                    sleep(self.endTime)
                    return(True)

            # check for bust
            if aceCount + value > 21:
                print("Human busted!")
                self.scores["computer"] += 1
                sleep(self.endTime)
                return(True)

            # human moves
            userInput = input("(H)it, (S)tand, or (Q)uit: ").upper()
            if userInput == "Q":
                # quit the game
                print("Final score computer: %s human: %s" % (self.scores["computer"], self.scores["human"]))
                sys.exit()
            elif userInput == "S":
                # computers turn
                print("Human stands")
                sleep(self.endTime)
                break
            elif userInput == "H":
                self.hands["human"].append(self.deck.pop())
                print("Human hits")
                sleep(self.endTime)
                continue
            else:
                print("something else was pressed, trying again")
                sleep(self.endTime)
                continue
        # games not over, let the computer play
        return(False)

    # play computer
    def playComputer(self):
        # computers turn
        print("\nComputers turn")
        while True:
            # display hand
            # hit if under 17
            cAce = False
            cAceCount = 0
            cValue = 0
            self.cRes = 0
            print("Computer is showing: ")
            for card in self.hands["computer"]:
                print(card)
                if card() == 1:
                    cAce = True
                    cAceCount += 1 
                else:
                    cValue += card()
            if cAce:
                if (cAceCount + 10 + cValue) < 22:
                    print("\nValue: %s or %s\n" % ( cAceCount + cValue, cAceCount + 10 + cValue))
                    self.cRes = cAceCount + 10 + cValue
                else:
                    print("\nValue: %s\n" % (cAceCount + cValue))
                    self.cRes = cAceCount + cValue
            else:
                print("\nValue: %s\n" % (cValue))
                self.cRes = cValue

            # if under 17 hit
            if self.cRes < 17:
                print("Computer hits\n")
                self.hands["computer"].append(self.deck.pop())
                # next
                continue
            elif self.cRes > 21:
                # bust
                print("Computer busted!\n")
                self.scores["human"] += 1
                return(True)
            else:
                # stand
                print("Computer stands\n")
                return(False)
 
# main
Game().begin()
