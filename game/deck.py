import random

class Deck:
    def __init__(
            self,
            dealer_hand=0,
            card_categories=['Hearts', 'Diamonds', 'Clubs', 'Spades'],
            cards_list=['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],
            ):
        self.dealer_hand = dealer_hand
        self.card_categories = card_categories
        self.cards_list = cards_list
        self.deck = [(card, category) for category in card_categories for card in cards_list]
    
    def shuffle(self):
        random.shuffle(self.deck)

    def changeHand(self, cardNum):
        if (cardNum == 'Ace'):
            if (self.dealer_hand <= 10):
                self.dealer_hand += 11
            else:
                self.dealer_hand += 1
        elif (cardNum == 'Jack' or cardNum == 'Queen' or cardNum == 'King'):
            self.dealer_hand += 10
        else:
            self.dealer_hand += int(cardNum)

    def deal(self):
        temp = self.deck[0]
        self.deck.pop(0)
        return temp
    
    def resetDeck(self):
        self.deck = [(card, category) for category in self.card_categories for card in self.cards_list]
        random.shuffle(self.deck)
        self.dealer_hand = 0