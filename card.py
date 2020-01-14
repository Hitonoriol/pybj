from enum import Enum

class Suit(Enum):
    Diamonds = "♦"
    Clubs = "♣"
    Hearts = "♥"
    Spades = "♠"

    def random():
        return random.choice(card_suits)

card_suits = list(Suit)

class Values(Enum):
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"
    Six = "6"
    Seven = "7"
    Eight = "8"
    Nine = "9"
    Ten = "10"
    Jack = "J"
    Queen = "Q"
    King = "K"
    Ace = "A"

    def random():
        return random.choice(card_values)

card_values = list(Values)

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_score(self):
        if (self.value not in ten_cards and self.value != Values.Ace):
            return int(self.value.value)
        elif (self.value in ten_cards):
            return 10
        else:
            return 11

    def card_str(self):
        return self.value.value + " " + self.suit.value
    
ten_cards = [Values.Jack, Values.Queen, Values.King, Values.Ten]
