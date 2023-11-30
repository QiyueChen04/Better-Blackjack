import math
import random
from time import sleep

from rpi_lcd import LCD
from player import Player
from button import Button
from roller import Roller
from cardDetector import CardDetector
from subprocess import call
from PIL import Image

lcd = LCD()
cd = CardDetector()

dealer = Player(0, 0)
player = Player(1000, 0)
playerHand = []
dealerHand = []
cards_list=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

red = Button(22)
blue = Button(27)
roller = Roller()

currentCard = 0

def waiting(): # Default Waiting Screen
    lcd.clear()
    lcd.text("Push any button", 1, "center")
    lcd.text("to continue", 2, "center")
    if (Button.waitForBtn()):
        lcd.clear()
        return

def displayHand(name, hand, line): # Essentially displays cards of either the dealer or player in the format of lcd.text("name: X X X X", line)
    temp = name + ":"
    for x in hand:
        temp = temp + " " + str(cards_list[x])
    lcd.text(temp, line)

def fullDisplay(): # Function for displaying the entirety of the player and dealer's hand
    displayHand("You", playerHand, 1)  
    displayHand("Dealer", dealerHand, 2)
    sleep(3)

def getCard():
    print("Taking Image!\n")
    call(['raspistill', '-o', '../pics/scan.jpg', '-w', '400', '-h', '300'])
    img = Image.open(r'../pics/scan.jpg')
    currentCard = cd.determineRank(img)

lcd.text("   Welcome to   ", 1)
lcd.text("BetterBlackjack!", 2)
sleep(3)
waiting()

lcd.text("Current Balance:", 1)
lcd.text(str(player.balance), 2)
sleep(3)

while (1): # keep looping until the user says no to playing again which breaks this while loop

    lcd.text(" How much would ", 1)
    lcd.text("you like to bet?", 2)
    sleep(2)

    bet = 100 # TODO change bet adjusting options
    lcd.text("B: Done  R: +100", 1)
    lcd.text("100", 2, "center")
    while (1): # continue to allow user to add 100 to bet until user clicks blue or bet exceeds balance
        if (Button.waitForBtn() == 22):
            bet += 100
            if (bet >= player.balance):
                bet = player.balance
                break
            lcd.text(str(bet), 2, "center")
        else:
            break

    lcd.text("  Bet Recieved  ", 1) # promp to let user know game is commencing
    lcd.text("   Good Luck!   ", 2)
    getCard()

    lcd.text("   YOUR CARD    ", 1) # Dealing Player Card 1
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    player.changeHand(cards_list[currentCard])
    playerHand.append(currentCard)
    getCard()
    waiting()

    lcd.text("   YOUR CARD    ", 1) # Dealing Player Card 2
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    player.changeHand(cards_list[currentCard])
    playerHand.append(currentCard)
    getCard()
    waiting()

    lcd.text("  DEALER CARD   ", 1) # Dealing Dealer Card 1
    lcd.text(" Flip this card ", 2)
    roller.pushCard()
    dealer.changeHand(cards_list[currentCard])
    dealerHand.append(currentCard)
    getCard()
    waiting()

    lcd.text("  DEALER CARD   ", 1) # Dealing Dealer Card 2
    lcd.text("  DO NOT FLIP   ", 2)
    roller.pushCard()
    dealer.changeHand(cards_list[currentCard])
    dealerHand.append(currentCard)
    getCard()
    waiting()
    
    if (player.hand == 21 and player.hand > dealer.hand): # player blackjack!
        fullDisplay()
        lcd.text("We're so Barack!", 1)
        lcd.text("Blackjack", 2)
        player.addBalance(bet * 1.5)
    elif (player.hand == 21 and player.hand == dealer.hand): # Push with 2 blackjacks
        fullDisplay()
        lcd.text("lol you thought ", 1)
        lcd.text("      Push      ", 2)
    elif (dealer.hand == 21 and player.hand < dealer.hand): # dealer blackjack
        fullDisplay()
        lcd.text(" It's so Joever ", 1)
        lcd.text("Dealer Blackjack", 2)
        player.loseBalance(bet)
    else: # "regular" game
        dealerStarter = "Dealer: " + str(cards_list[dealerHand[0]]) + " ?"

        hitStand = True
        if (2 * bet <= player.balance): # if they can double ask for double down
                displayHand("You", playerHand, 1)
                lcd.text(dealerStarter, 2)
                sleep(3)

                lcd.text("Double Down?", 1, "center")
                lcd.text("B-No       R-Yes", 2)
                if (Button.waitForBtn() == 22):
                    hitStand = False
                    bet *= 2
                    lcd.text("   YOUR CARD    ", 1) # Dealing Player Card 3
                    lcd.text(" Flip this card ", 2)
                    roller.pushCard()
                    player.changeHand(cards_list[currentCard])
                    playerHand.append(currentCard)
                    getCard()
                    waiting()
        
        if (hitStand): #if they cannot double or say no, proceed to hit/stand phase
            while (player.hand <= 21):
                displayHand("You", playerHand, 1) # every time they hit redisplay their hand
                lcd.text(dealerStarter, 2)
                sleep(3)
                
                lcd.text("Hit or Stand?", 1, "center")
                lcd.text("B-Stand    R-Hit", 2)
                if (Button.waitForBtn() == 22):
                    lcd.text("   YOUR CARD    ", 1) # Dealing Player Card 3
                    lcd.text(" Flip this card ", 2)
                    roller.pushCard()
                    player.changeHand(cards_list[currentCard])
                    playerHand.append(currentCard)
                    getCard()
                    waiting()
                else: # if they ever hit the blue button break out of while look
                    lcd.clear()
                    break

        if (player.hand <= 21): # only do dealer stuff if player hasn't busted
            lcd.text("Please flip", 1, "center")
            lcd.text("dealer card #2", 2, "center")
            sleep(3)

            # make dealer keep hitting until they reach 17
            while (dealer.hand < 17):
                fullDisplay()

                lcd.text("  DEALER CARD   ", 1) # Dealing Dealer Card 1
                lcd.text(" Flip this card ", 2)
                roller.pushCard()
                dealer.changeHand(cards_list[currentCard])
                dealerHand.append(currentCard)
                getCard()
                lcd.sleep(1)
                waiting()


        fullDisplay() # right before winning/losing messages display entirety of both hands regardless of hit/stand/double down decisions

        # check if player won
        if (player.hand > 21): # you busted
            lcd.text("You Bust!", 1, "center")
            player.loseBalance(bet)
        elif (dealer.hand > 21): # the dealer busted
            lcd.text("Dealer Bust!", 1, "center")
            player.addBalance(bet)
        elif (player.hand < dealer.hand): # the dealer had the better hand
            lcd.text("Dealer Wins!", 1, "center")
            player.loseBalance(bet)
        elif (player.hand > dealer.hand): # you had the better hand
            print("You Win!", 1, "center")
            player.addBalance(bet)
        elif (player.hand == dealer.hand): # push
            print("Push!")
    sleep(3)
    waiting()

    lcd.text("Current Balance:", 1)
    lcd.text(str(player.balance), 2, "center")
    sleep(5)
    
    lcd.text("Play Again?", 1, "center")
    lcd.text("B-No       R-Yes", 2)
    
    
    if (Button.waitForBtn() == 22):
        dealer.reset()
        player.reset()
        playerHand = []
        dealerHand = [] # remember to reset the playerHand and dealerHand arrays as well as the objects
        lcd.text("Please Reshuffle", 1, "center")
        lcd.text("The Deck", 2, "center")
        sleep(10)

        waiting()
    else:
        break

lcd.clear()
lcd.text("Thank You For", 1, "center")
lcd.text("Playing!", 2, "center")
