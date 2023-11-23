import random

class Deck:
    def __init__(
            self,
            card_categories=['Hearts', 'Diamonds', 'Clubs', 'Spades'],
            cards_list=['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
            ):
        self.card_categories = card_categories
        self.cards_list = cards_list
        self.deck = [(card, category) for category in card_categories for card in cards_list]
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        temp = self.deck[0]
        self.deck.pop(0)
        return temp
    
    def resetDeck(self):
        self.deck = [(card, category) for category in self.card_categories for card in self.cards_list]