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

### Card Holder ###
- Designed a modular 3D model in TinkerCAD.
- Printed and assembled the 3D-printed parts.
- Secured white LED beside the camera module for consistent lighting conditions.

### Card Dispenser/Roller ###
- Secured 3D printed rods (wrapped in sticky tack for increased friction) to continuous servos.
- Utilized the “AngularServo” module from “gpiozero” library to program the servos’ direction and speed.
- Fine-tuned servo active times to dispense exactly one card at a time.
- Wrote roller class in the main game for improved readability.
- Wrote a Python script automating the image collection process of cards (including a blank card).

### Image Recognition ###
- Pillow (Python Imaging Library) is used to perform various image processes to get clean edges on the card’s value (A, 2, ... Q, K). 
  - The contrast is increased and the image is converted to grayscale. This is necessary for red cards that are very close to white (the background colour) on the grayscale.
  - Image subtraction: An image of a white card taken beforehand is subtracted from the image to normalize lighting effects (e.g. glare from LED).
- NumPy is used to convert the image to binary (black or white) by carefully choosing a threshold value (all pixels under the threshold become black, all above become white).
- A bounding rectangle around the largest shape is extracted, resized, and compared to a set of 13 [templateImages](/templates) using bitwise-XOR and counting white pixels to find the closest matching shape.
  - A breadth-first search algorithm is applied to “edges” in the image to get the minimal and maximal x and y coordinates of every “shape”. 
  - Edges are pixels that are adjacent to pixels of the opposite colour. 
  - A bounding rectangle is created with these minimal and maximal coordinates. The largest rectangle bounding a valid shape (completely enclosed, no holes) is considered.
  - By carefully cropping the image beforehand,  this largest shape is consistently the card’s value in all our cases. In the case of “10”, this shape is the “0”.
- Template Images were manually generated with this same algorithm on a handpicked set of cards.- 
- Wrote a Python class to modularize the process.

### Buttons ###
- Created two pull-up circuits containing simple push buttons on the breadboard, connecting the RPi’s GPIO and GND pins.
- Wrote button class and function that pauses the program until a button input is registered and returns the ID of the button pressed.
- Registers exactly one button press at a time.

### Main Game ###
- Prompt the player by displaying text messages on an LCD using the “rpi_lcd” library.
- Updates the player on the state of the game throughout the game (displays both the dealer and player hands).
- Player class keeps track of player and dealer hands as well as the player’s balance throughout multiple games.
- Dynamic calculation of “hard” and “soft” hands (i.e. update the value of an ace)
- Takes input on bets, allowing users to increase or confirm their bets.
- Double down option is also included
- Hit/stand phase of the game is skipped if there is a player/dealer blackjack
- Captures photos from the camera using the camera module from “picamera” library.
- Determines if the player wins or loses, adds to/subtracts from player balance accordingly, displays appropriate winning/losing screen

#### For more details, please see our [final report](/Final_Report.pdf)
