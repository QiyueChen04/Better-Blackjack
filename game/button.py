import RPi.GPIO as GPIO
from time import sleep

class Button:
    
    GPIO.setmode(GPIO.BCM)
    btns = []
    
    def __init__(self, pin):
        self.pin = pin
        Button.btns.append(self)
    
    def input(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        return(not(GPIO.input(self.pin)))
    
    def waitForBtn():
        while True:
            for b in Button.btns:
                if b.input():
                    sleep(0.1)
                    return b.pin
            sleep(0.1)
            
        

