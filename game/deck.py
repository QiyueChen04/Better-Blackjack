import random

class Deck:
    def __init__(
            self,
            dealer_hand=0,
            card_categories=['Hearts', 'Diamonds', 'Clubs', 'Spades'],
            cards_list=['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],
            soft = False
            ):
        self.dealer_hand = dealer_hand
        self.card_categories = card_categories
        self.cards_list = cards_list
        self.deck = [(card, category) for category in card_categories for card in cards_list]
        self.soft = soft
    
    def shuffle(self):
        random.shuffle(self.deck)

    def changeHand(self, cardNum): 
        if (cardNum == 'A'):
            if (self.dealer_hand <= 10):
                self.dealer_hand += 11
                self.soft = True
            else:
                self.dealer_hand += 1
        elif (cardNum == 'J' or cardNum == 'Q' or cardNum == 'K'):
            self.dealer_hand += 10
        else:
            self.dealer_hand += int(cardNum)
        if (self.dealer_hand > 21 and self.soft == True):
            self.dealer_hand -= 10
            self.soft = False

    def deal(self):
        temp = self.deck[0]
        self.deck.pop(0)
        return temp
    
    def resetDeck(self):
        self.deck = [(card, category) for category in self.card_categories for card in self.cards_list]
        random.shuffle(self.deck)
        self.dealer_hand = 0