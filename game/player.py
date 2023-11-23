class Player:
    def __init__(self, balance, hand=0):
        self.balance = balance
        self.hand = hand

    def addBalance(self, amount):
        self.balance += amount

    def loseBalance(self, amount):
        self.balance -= amount

    def changeHand(self, cardNum):
        if (cardNum == 'Ace'):
            if (self.hand <= 10):
                self.hand += 11
            else:
                self.hand += 1
        elif (cardNum == 'Jack' or cardNum == 'Queen' or cardNum == 'King'):
            self.hand += 10
        else:
            self.hand += int(cardNum)
        