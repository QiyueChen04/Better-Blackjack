import math
import random
from time import sleep

from rpi_lcd import LCD
from player import Player
from deck import Deck
from button import Button
from roller import Roller
from cardDetector import CardDetector

lcd = LCD()
cd = CardDetector()

newDeck = Deck()
newDeck.shuffle()
player = Player(1000, 0)
playerHand = []
dealerHand = []
cards_list=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

red = Button(22)
blue = Button(27)
roller = Roller()

def waiting(): # Default Waiting Screen
    lcd.clear()
    lcd.text("Push any button", 1, "center")
    lcd.text("to continue", 2, "center")
    if (Button.waitForBtn):
        lcd.clear()
        return

def displayHand(name, hand, line): # Display cards on LCD screen
    temp = name + ":"
    for x in hand:
        temp = temp + " " + str(cards_list[x])
    lcd.text(temp, line)

lcd.text("   Welcome to   ", 1)
lcd.text("BetterBlackjack!", 2)
sleep(3)
waiting()

lcd.text("Current Balance:", 1)
lcd.text(str(player.balance), 2)
sleep(3)

play_again = 1
while play_again:

    lcd.text(" How much would ", 1)
    lcd.text("you like to bet?", 2)
    sleep(2)

    bet = 100
    lcd.text("B: Done  R: +100", 1)
    lcd.text("100", 2, "center")
    while (1): # continue to allow user to add 100 to bet until user clicks blue or bet exceeds balance
        if (Button.waitForBtn == 22):
            bet += 100
            if (bet >= player.balance):
                bet = player.balance
                break
            lcd.text(str(bet), 2, "center")
        else:
            break

    lcd.text("  Bet Recieved  ", 1) # promp to let user know game is commencing
    lcd.text("   Good Luck!   ", 2)
    # currentCard = camera.detect()
    sleep(2)
    playerHand = []
    dealerHand = []

    lcd.text("  PLAYER CARD   ", 1) # Dealing Player Card 1
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    # player.changehand(cards_list[currentCard])
    # playerHand.append(currentCard)
    # currentCard = camera.detect()
    sleep()
    waiting()

    lcd.text("  PLAYER CARD   ", 1) # Dealing Player Card 2
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    # player.changehand(cards_list[currentCard])
    # playerHand.append(currentCard)
    # currentCard = camera.detect()
    lcd.sleep(1)
    waiting()

    lcd.text("  DEALER CARD   ", 1) # Dealing Dealer Card 1
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    # newDeck.changehand(cards_list[currentCard])
    # dealerHand.append(currentCard)
    # currentCard = camera.detect()
    lcd.sleep(1)
    waiting()

    lcd.text("  DEALER CARD   ", 1) # Dealing Dealer Card 2
    lcd.text("  DO NOT FLIP   ", 2)
    roller.pushCard()
    # newDeck.changehand(cards_list[currentCard])
    # dealerHand.append(currentCard)
    # currentCard = camera.detect()
    lcd.sleep(1)
    waiting()
    
    if (player.hand == 21 and player.hand > newDeck.dealer_hand): # player blackjack!
        lcd.text("We're so Barack!", 1)
        lcd.text("Player Blackjack", 2)
        lcd.sleep(3)

        player.addBalance(bet * 1.5)
    elif (player.hand == 21 and player.hand == newDeck.dealer_hand): # Push with 2 blackjacks
        lcd.text("lol you thought ", 1)
        lcd.text("      Push      ", 2)
        lcd.sleep(3)
    elif (newDeck.dealer_hand == 21 and player.hand < newDeck.dealer_hand): # dealer blackjack
        lcd.text(" It's so Joever ", 1)
        lcd.text("Dealer Blackjack", 2)
        lcd.sleep(3)

        player.loseBalance(bet)
    else: # "regular" game
        displayHand("Player", playerHand, 1)


        if (2 * bet <= player.balance): # if they can double ask for double down
                lcd("Double Down?", 1, "center")
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
    
    lcd.text("Current Balance:", 1)
    lcd.text(str(player.balance), 2, "center")
    sleep(3)
    
    play_again = int(input("Do you want to play again? (0 / 1)"))
    while (play_again != 0 and play_again != 1):
        play_again = int(input("Input not accepted. Please try again: "))
    
    if (play_again):
        newDeck.resetDeck()
        player.hand = 0
    
    print("\n")
    
print("Thanks for playing!")
