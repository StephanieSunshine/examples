# card.py -- simple class to simulate a deck of cards and their values

# for pytest
class TestClass:
    def test_one(self):
        # test if Card.cardName is a dictionary
        print("tested if Card.cardName is a dictionary\n")
        assert type(Card.cardName) is dict 

    def test_two(self):
        # test if self.cardSuit is a list
        print("tested if Card.cardSuit is a list\n")
        assert type(Card.cardSuit) is list

    def test_three(self):
        # test if we have 13 card names
        print("tested if Card.cardName has 13 cards\n")
        assert len(Card.cardName) == 13

    def test_four(self):
        # test that we have 4 card suits
        print("tested if Card.cardSuit has 4 suits\n")
        len(Card.cardSuit) == 4

    def test_five(self):
        # test that __str__ returns a valid string
        print("tested if Card.__str__ returns a valid string\n")
        assert str(Card("Ace", "hearts")) == "Ace of hearts"

    def test_six(self):
        # test that __call__ returns an integer
        print("tested if Card.__call__ returns a valid integer\n")
        assert Card("Ace", "hearts")() == 1 

# real class
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


