import random
import card

class Deck:
    unused_cards = []
    def purge(self, amount):
        self.unused_cards.clear()
        for deck in range(amount):
            for suit in list(card.Suit):
                for value in card.card_values:
                    self.unused_cards.append(card.Card(value, suit))
    
    def shuffle(self, amount = 1):
        self.purge(amount)
        random.shuffle(self.unused_cards)

    def draw(self):
        return self.unused_cards.pop()
            
    def __init__(self, amount = 1):
        self.shuffle(amount)
