from picamera import PiCamera
from time import sleep

def takePhoto():
    camera = PiCamera()
    camera.start_preview()
    sleep(0.5)
    camera.capture(f'../pics/blank.jpg')
    camera.stop_preview()
