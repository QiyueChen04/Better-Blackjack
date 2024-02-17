# Better Blackjack

### Group Members: Andrew Shen, Bryan Cui, David Li, Edison Du, Qiyue Chen ###

## Minimum Viable Prototype: ## 
1. Be a functional card dealer capable of scanning and recording dealt cards
2. Have a working version of Blackjack, with the human player playing with an AI dealer
3. Accept user input via buttons (hit/stand, changing bets, etc)

## What We Achieved: ## 
1. Card dealer scans and correctly identifies Victoria Playing Cards reliably, but may not be as accurate for other decks of cards. The camera works but can be sluggish (5 seconds to deal a card). The card dealing rollers need to be maintained consistently (e.g. re-apply sticky tack for grip) but work well otherwise.
2. A single-player version of Blackjack and Blackjack Dealer was implemented successfully.
3. The buttons and LCD screen for user interaction work consistently and allow for complete gameplay, but the betting feature can be unforgiving (only allowing players to increase their bet) due to the limited buttons available.

## Technical Details on Achievements: ##
### Raspberry Pi ### 
- Soldered 40 header pins.
- Wired servos, camera, breadboard, LEDs, LCD, buttons to GPIO pins of RPi.
- Created a bash script to run the main game program on boot.
