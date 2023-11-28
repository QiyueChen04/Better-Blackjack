import math
import random
from time import sleep

from rip_lcd import LCD
from player import Player
from deck import Deck
from button import Button

lcd = LCD()

newDeck = Deck()
newDeck.shuffle()
player1 = Player(1000, 0)

red = Button(22)
blue = Button(27)

def centreNum(n, line):
    digits = math.floor(math.log(n, 10)) + 1
    for x in range(math.floor((16 - digits) / 2)):
        lcd.text(" ", line)
    num = str(n)
    lcd.text(num, line)


lcd.text("   Welcome to   ", 1)
lcd.text("BetterBlackjack!")
sleep(3)
lcd.clear()


play_again = 1

while play_again:

    lcd.text("Current Balance:", 1)
    centreNum(player1.balance, 2)
    sleep(3)
    lcd.clear()

    lcd.text(" How much would ", 1)
    lcd.text("you like to bet?", 2)
    sleep(2)
    lcd.clear()

    bet = 100
    lcd.text("B: Done  R: +100", 1)
    centreNum(100, 2)
    while (1):
        if (Button.waitForBtn == 22):
            bet += 100
            if (bet >= player1.balance):
                bet = player1.balance
                break
            centreNum(bet, 2)
        else:
            break
    lcd.clear()
    
    lcd.text("  Bet Recieved  ", 1)
    lcd.text("   Good Luck!   ", 2)
    sleep(2)

    dealer_hand = [newDeck.deal(), newDeck.deal()]
    player_hand = [newDeck.deal(), newDeck.deal()]

    newDeck.changeHand(dealer_hand[0][0])
    newDeck.changeHand(dealer_hand[1][0])

    player1.changeHand(player_hand[0][0])
    player1.changeHand(player_hand[1][0])

    
    if (player1.hand == 21 and player1.hand > newDeck.dealer_hand): # player blackjack!
        print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
        print("\n")
        print("Blackjack!")
        player1.addBalance(bet * 1.5)
        print("Your balance is now at " + str(player1.balance))
    elif (player1.hand == 21 and player1.hand == newDeck.dealer_hand): # Push with 2 blackjacks
        print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
        print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and a " + dealer_hand[1][0] + " of " + dealer_hand[1][1])
        print("\n")
        print("Push!")
        print("Your balance is still at " + str(player1.balance))
    elif (newDeck.dealer_hand == 21 and player1.hand < newDeck.dealer_hand): # dealer blackjack
        print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
        print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and a " + dealer_hand[1][0] + " of " + dealer_hand[1][1])
        print("\n")
        print("Dealer Blackjack!")
        player1.loseBalance(bet)
        print("Your balance is now at " + str(player1.balance))
    else: # "regular" game
        print("You received a " + player_hand[0][0] + " of " + player_hand[0][1] + " and a " + player_hand[1][0] + " of " + player_hand[1][1])
        print("The dealer has a " + dealer_hand[0][0] + " of " + dealer_hand[0][1] + " and an unknown card in his hand!")
        print("You are currently at " + str(player1.hand))
        print("\n")

        if (2 * bet <= player1.balance and input("Double Down? (y / n)") == "y"): # if they can double ask for double down
                bet *= 2
                player_hand.append(newDeck.deal())
                player1.changeHand(player_hand[-1][0])
                print("You received a " + player_hand[-1][0] + " of " + player_hand[-1][1] + ". You are currently at " + str(player1.hand))
                print("\n")
        else: #if they cannot double or say no, proceed to hit/stand phase
            while (player1.hand <= 21 and input("hit or stand? (h / s)") == "h"):
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
