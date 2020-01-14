from enum import Enum
import random
import os.path

import deck
import screen_utils
import save_utils
import xor

savefile = "pybj.dat"

class Result(Enum):
    bust = "Bust"
    blackjack = "Blackjack"
    push = "Push"
    win = "You win"
    dealer_win = "Dealer wins"

result_win = [Result.blackjack, Result.win]

class BlackJack:
    decks = 1
    deck = deck.Deck(decks)

    money = 0
    bet = 0
    losses = 0
    wins = 0
    
    result = ""
    
    player_hand = []
    dealer_hand = []

    dealer_limit = 17
    
    player_score = 0
    dealer_score = 0
    
    turn = 1
    
    game_end = False
    stand = False
    skip = False

    save_attrs = ["money", "losses", "wins"]
    save_key = 1337
    line_delim = "---------------------"
    
    def __init__(self, money = 1000):
        screen_utils.cls()
        self.money = money
        print(self.line_delim)
        print("Welcome to BlackJack!", "\nDealer draws to 17.")
        print(self.line_delim)
        self.load_game()
        self.restart()
    
    def load_game(self):
        if (not os.path.exists(savefile)):
            return
        load = save_utils.load_dict(savefile)
        for attr in self.save_attrs:
            setattr(self, attr, float(xor.decode(load[xor.encode(attr, self.save_key)], self.save_key)))
    
    def save_game(self):
        save = {}
        for attr in self.save_attrs:
            save[xor.encode(attr, self.save_key)] = xor.encode(str(getattr(self, attr)), self.save_key)
        save_utils.save_dict(save, savefile)

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
        screen_utils.cls()
        lim = -1
        if (len(self.dealer_hand) == 2):
            lim = 1
            
        print(self.line_delim)
        print("[Turn #", self.turn, " | Bet: ", self.bet, "]", sep = "")
        print(self.line_delim)
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
        print(self.line_delim, "\n")
        
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
        elif (self.dealer_score >= self.dealer_limit and self.stand):
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
            screen_utils.cls()
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
                if (self.dealer_score < self.dealer_limit):
                    self.deal_to_dealer()
                    self.check_score()
            self.print_state()
            self.turn += 1
        self.end_game()
