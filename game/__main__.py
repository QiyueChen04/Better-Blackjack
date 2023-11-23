import math
import random

from player import Player
from deck import Deck

newDeck = Deck()
newDeck.shuffle()

while True:
    player1 = Player(100, 0)

    bet = int(input("What would you like to bet? "))
    while (bet > player1.balance or bet < 0):
        bet = int(input("Bet is not accepted. Please try again: "))

    dealer_hand = [newDeck.deal(), newDeck.deal()]
    player_hand = [newDeck.deal(), newDeck.deal()]

    player1.changeHand(player_hand[0][0])
    player1.changeHand(player_hand[1][0])

    print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and an unknown card in his hand!")
    print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
    print("You are currently at " + str(player1.hand))

    while (player1.hand < 21 and input("Hit or stand? (h / s)") == "h"):
        player_hand.append(newDeck.deal())
        player1.changeHand(player_hand[-1][0])
        print("You received a " + player_hand[-1][0] + " of " + player_hand[-1][1] + ". You are currently at " + str(player1.hand))

    if (player1.hand > 21):
        print("You busted!")
        player1.loseBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand == 21):
        print("Blackjack!")
        player1.addBalance(bet * 3)
        print("Your balance is now at " + str(player1.balance))
    else:
        print("You beat the dealer!")
        player1.addBalance(bet * 2)
        print("Your balance is now at " + str(player1.balance))

    break