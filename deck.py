#Foreign imports
from random import randint

HEART = '♥'
DIAMOND = '♦'
CLUB = '♣'
SPADE = '♠'

ACE = 'A'
JACK = 'J'
QUEEN = 'Q'
KING = 'K'

VALUES = [ACE, '2', '3', '4', '5', '6', '7', '8', '9', '10', JACK, QUEEN, KING]
SUITS = [HEART, DIAMOND, CLUB, SPADE]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def to_int_runs(self):
        if(self.value == ACE):
            return 1
        elif(self.value == JACK):
            return 11
        elif(self.value == QUEEN):
            return 12
        elif(self.value == KING):
            return 13
        else:
            return int(self.value)
        
    def to_int_15s(self):
        if(self.value == ACE):
            return 1
        elif(self.value in [JACK, QUEEN, KING]):
            return 10
        else:
            return int(self.value)
        
    def display(self):
        return f'{self.value} {self.suit}'

class Deck:
    def __init__(self):
        self.reset_deck()
        
    def reset_deck(self):
        self.flipped = None #Card that gets flipped after throwing cards away
        self.hands = [] #List of lists with Card()s that represent player hands
        self.extra = [] #List of cards that were removed with get_card() for crib

        for suit in SUITS:
            for value in VALUES:
                self.deck.append(Card(value, suit))

    def get_hands(self, num_hands, num_cards):
        if(len(self.hands) == 0):
            #Check that values are within bounds
            if(num_hands * num_cards <= len(self.deck)):
                for h in range(num_hands):
                    hand = []
                    for c in range(num_cards):
                        card = randint(0, len(self.deck)-1)
                        hand.append(self.deck[card])
                        del self.deck[card]
                    self.hands.append(hand)
        
        return self.hands
    
    def get_flipped(self):
        if(self.flipped == None and len(self.deck) >= 1):
            card = randint(0, len(self.deck)-1)
            self.flipped = self.deck[card]
            del self.deck[card]

        return self.flipped
    
    def get_card(self):
        if(len(self.deck) >= 1):
            card = randint(0, len(self.deck)-1)
            self.extra.append(self.deck[card])
            del self.deck[card]

            return self.extra[-1]
        return None