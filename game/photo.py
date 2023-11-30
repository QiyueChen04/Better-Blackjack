from picamera import PiCamera
from time import sleep

def takePhoto():
    camera = PiCamera()
    camera.resolution = (400, 300)
    camera.start_preview()
    sleep(0.5)
    camera.capture(f'../pics/scan.jpg')
    camera.stop_preview()

