class Player:
    def __init__(self, balance, hand=0, soft=False):
        self.balance = balance
        self.hand = hand
        self.soft = soft

    def addBalance(self, amount):
        self.balance += amount

    def loseBalance(self, amount):
        self.balance -= amount

    def changeHand(self, cardNum):
        if (cardNum == 'A'):
            if (self.hand <= 10):
                self.hand += 11
                self.soft = True
            else:
                self.hand += 1
        elif (cardNum == 'J' or cardNum == 'Q' or cardNum == 'K'):
            self.hand += 10
        else:
            self.hand += int(cardNum)
        if (self.hand > 21 and self.soft == True):
            self.hand -= 10
            self.soft = False