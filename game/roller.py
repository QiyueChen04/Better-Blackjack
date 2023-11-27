from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from subprocess import call


class Roller:
    
    call(['sudo', 'pigpiod'])
    
    def stop(self):
        self.innerServo.detach()
        self.outerServo.detach()
    
    def __init__(self, inner_pin, outer_pin):
        factory = PiGPIOFactory()
        self.innerServo = AngularServo(inner_pin, min_angle=-100, max_angle=100, pin_factory=factory)
        self.outerServo = AngularServo(outer_pin, min_angle=-100, max_angle=100, pin_factory=factory)
        self.stop()
    
    def pushCard(self):
        self.innerServo.angle = 80
        self.outerServo.angle = 80
        sleep(1.2)
                
        self.innerServo.angle = 50
        sleep(0.2)
                
        self.innerServo.angle = 0
        sleep(0.7)
                
        self.innerServo.angle = -35
        sleep(0.5)
                
        self.outerServo.angle = 0
        sleep(0.2)
                
        self.innerServo.angle = 0
        
        self.stop()
        sleep(0.3)
        

#call(['raspistill', '-o', '..\pics\'+str(i)+'.jpg', '-w', '400', '-h', '300'])





