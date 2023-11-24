import math
import random

from player import Player
from deck import Deck

newDeck = Deck()
newDeck.shuffle()

play_again = 1

while play_again:
    player1 = Player(100, 0)

    bet = int(input("What would you like to bet? "))
    while (bet > player1.balance or bet < 0):
        bet = int(input("Bet is not accepted. Please try again: "))

    dealer_hand = [newDeck.deal(), newDeck.deal()]
    player_hand = [newDeck.deal(), newDeck.deal()]

    newDeck.changeHand(dealer_hand[0][0])
    newDeck.changeHand(dealer_hand[1][0])

    player1.changeHand(player_hand[0][0])
    player1.changeHand(player_hand[1][0])


    print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and an unknown card in his hand!")
    print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
    print("You are currently at " + str(player1.hand))
    print("\n")

    while (player1.hand < 21 and input("Hit or stand? (h / s)") == "h"):
        player_hand.append(newDeck.deal())
        player1.changeHand(player_hand[-1][0])
        print("You received a " + player_hand[-1][0] + " of " + player_hand[-1][1] + ". You are currently at " + str(player1.hand))
        print("\n")

    if (player1.hand <= 21): # only do dealer stuff if player hasn't busted
        print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and a " + dealer_hand[1][0] + " of " + dealer_hand[1][1] + "!")
        print("The dealer is at " + str(newDeck.dealer_hand))

        # make dealer keep hitting until they reach 17
        while (newDeck.dealer_hand < 17):
            dealer_hand.append(newDeck.deal())
            newDeck.changeHand(dealer_hand[-1][0])
            print("The dealer received a " + dealer_hand[-1][0] + " of " + dealer_hand[-1][1] + ". The dealer is currently at " + str(newDeck.dealer_hand))
            print("\n")


    # TODO make a bunch of functions

    # check if player won
    if (player1.hand > 21): # you busted
        print("You busted!")
        player1.loseBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    elif (newDeck.dealer_hand > 21): # the dealer busted
        print("The dealer busted!")
        player1.addBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand == 21): # blackjack!
        print("Blackjack!")
        player1.addBalance(bet * 3)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand < newDeck.dealer_hand): # the dealer had the better hand
        print("The dealer beat you!")
        player1.loseBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand > newDeck.dealer_hand): # you had the better hand
        print("You beat the dealer!")
        player1.addBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand == newDeck.dealer_hand): # push
        print("Push!")
        print("Your balance is still at " + str(player1.balance))
    
    play_again = int(input("Do you want to play again? (0 / 1)"))
    while (play_again != 0 and play_again != 1):
        play_again = int(input("Input not accepted. Please try again: "))
    
    if (play_again):
        newDeck.resetDeck()
        player1.hand = 0
    
    print("\n")
    
print("Thanks for playing!")