from enum import Enum
from os import system, name
import os.path
from time import sleep
from shutil import get_terminal_size
import json
import random
import base64
import re

savefile = "pybj.dat"

def base64_fix_padding(data, altchars=b'+/'):
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def xor(data, key = 1337, decode = False):
    if (decode):
        data = base64_fix_padding(data.encode()).decode("utf-8")
    length = len(data);
    for i in range(length): 
        data = (data[:i] + chr(ord(data[i]) ^ (key)) + data[i + 1:])
    if (not decode):
        data = base64.b64encode(data.encode()).decode("utf-8")
    return data

def save_dict(dic, file):
    dump = json.dumps(dic)
    f = open(file,"w")
    f.write(dump)
    f.close()

def load_dict(file):
    f = open(file, "r")
    dic = json.loads(f.readline())
    return dic

def cls(): 
    if name == 'nt': 
        _ = system('cls') 
    elif (name == 'posix'): 
        _ = system('clear')
    else:
        print("\n" * get_terminal_size().lines * 2, end='')

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

class Deck:
    unused_cards = []
    def purge(self, amount):
        self.unused_cards.clear()
        for deck in range(amount):
            for suit in list(Suit):
                for value in card_values:
                    self.unused_cards.append(Card(value, suit))
    
    def shuffle(self, amount = 1):
        self.purge(amount)
        random.shuffle(self.unused_cards)

    def draw(self):
        return self.unused_cards.pop()
            
    def __init__(self, amount = 1):
        self.shuffle(amount)

ten_cards = [Values.Jack, Values.Queen, Values.King, Values.Ten]
ldelim = "---------------------"
dealer_limit = 17

class Result(Enum):
    bust = "Bust"
    blackjack = "Blackjack"
    push = "Push"
    win = "You win"
    dealer_win = "Dealer wins"

result_win = [Result.blackjack, Result.win]

class BlackJack:
    decks = 1

    losses = 0
    wins = 0
    result = ""
    deck = Deck(decks)
    money = 0
    bet = 0
    player_hand = []
    dealer_hand = []
    player_score = 0
    dealer_score = 0
    turn = 1
    game_end = False
    stand = False
    skip = False
    def __init__(self, money = 1000):
        cls()
        self.money = money
        print(ldelim)
        print("Welcome to BlackJack!", "\nDealer draws to 17.")
        print(ldelim)
        self.load_game()
        self.restart()

    save_attrs = ["money", "losses", "wins"]
    def load_game(self):
        if (not os.path.exists(savefile)):
            return
        load = load_dict(savefile)
        for attr in self.save_attrs:
            setattr(self, attr, float(xor(load[xor(attr)], decode = True)))
    
    def save_game(self):
        save = {}
        for attr in self.save_attrs:
            save[xor(attr)] = xor(str(getattr(self, attr)))
        save_dict(save, savefile)

    def view_hand(self, hand, lim = -1):
        i = 1
        card_str = ""
        for card in hand:
            if (lim != -1):
                if (i > lim):
                    card_str = "*"
                else:
                    card_str = card.card_str()
            else:
                card_str = card.card_str()
            print("[" + card_str + "]", end = " ", sep = "")
            i += 1

    def place_bet(self):
        self.bet = (input("Place your bet: "))
        if (self.bet.isdigit()):
            self.bet = int(self.bet)
        else:
            self.place_bet()
        if (self.bet < 1 or self.bet > self.money):
            self.place_bet()
        else:
            self.money -= self.bet

    def deal_to_dealer(self):
        self.dealer_hand.append(self.deck.draw())
        newcard = Card.get_score(self.dealer_hand[-1])
        if (newcard == 11 and newcard + self.dealer_score > 21):
            self.dealer_score += 1
        else:
            self.dealer_score += newcard

    def deal_to_player(self):
        self.player_hand.append(self.deck.draw())
        newcard = Card.get_score(self.player_hand[-1])
        if (newcard == 11 and newcard + self.player_score > 21):
            self.player_score += 1
        else:
            self.player_score += newcard

    def print_state(self):
        cls()
        lim = -1
        if (len(self.dealer_hand) == 2):
            lim = 1
        print(ldelim)
        print("[Turn #", self.turn, " | Bet: ", self.bet, "]", sep = "")
        print(ldelim)
        print("Dealer's hand:")
        if (self.stand):
            lim = -1
        self.view_hand(self.dealer_hand, lim)
        if (lim == 1 and not self.stand):
            d_score = self.dealer_hand[0].get_score()
        else:
            d_score = self.dealer_score
        print("\n", "Score: ", d_score, sep = "")
        print("Player's hand:")
        self.view_hand(self.player_hand)
        print("\n", "Score: ", self.player_score, sep = "")
        print(ldelim, "\n")
        if (self.stand):
            sleep(1)

    def player_turn(self):
        action = input("[ (0) Hit | (1) Stand ]: ")
        if (action != "0" and action != "1"):
            self.player_turn()
        if (action == "1"):
            self.skip = True
            self.stand = True
        else:
            self.deal_to_player()
        self.check_score()
        
    def check_score(self):
        if (self.player_score > 21):
            self.result = Result.bust
            self.game_end = True
        elif (self.player_score == 21):
            self.money += self.bet * 2.5
            self.result = Result.blackjack
            self.game_end = True
        elif (self.dealer_score > 21):
            self.money += self.bet * 2
            self.result = Result.win
            self.game_end = True
            return
        elif (self.dealer_score >= dealer_limit and self.stand):
            if (self.dealer_score == self.player_score):
                self.money += self.bet
                self.result = Result.push
                self.game_end = True
                return
            if (self.player_score > self.dealer_score):
                self.money += self.bet * 2
                self.result = Result.win
                self.game_end = True
            else:
                self.game_end = True
                self.result = Result.dealer_win

    def retry(self):
        retry = input("Play again [<enter>] or Exit [n]: ").lower()
        if (retry != "n"):
            cls()
            self.restart()

    def end_game(self):
        ratio = 0
        print("Game over:", self.result.value, "\nYour cash:", int(self.money))
        if (self.result in result_win):
            self.wins += 1
        elif (self.result != Result.push):
            self.losses += 1
        if (self.losses > 0):
            ratio = self.wins / self.losses
        print("Win/Loss ratio:", self.wins, "/", self.losses, "(", ratio, ")")
        self.save_game()
        self.retry()
        
    def restart(self):
        if (self.money == 0):
            print(" *You sold your kidney for $300 to play some poker")
            self.money = 300
        self.turn = 1
        self.game_end = False
        self.stand = False
        self.dealer_score = 0
        self.player_score = 0
        self.dealer_hand.clear()
        self.player_hand.clear()
        self.deck.shuffle(self.decks)
        print("Your balance: ", int(self.money), sep = "")
        self.place_bet()
        self.deal_to_dealer()
        self.deal_to_dealer()
        self.deal_to_player()
        self.deal_to_player()
        self.print_state()
        while (not self.game_end):
            self.check_score()
            if (self.game_end):
                break
            if (not self.stand):
                self.player_turn()
            else:
                if (self.dealer_score < dealer_limit):
                    self.deal_to_dealer()
                    self.check_score()
            self.print_state()
            self.turn += 1
        self.end_game()

game = BlackJack()
