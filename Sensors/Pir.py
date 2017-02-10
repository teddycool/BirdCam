__author__ = 'teddycool'
import cv2

class PirSensor(object):
    def __init__(self, GPIO, controlpin=14):
        self._gpio = GPIO
        self._pin = controlpin
        self._gpio.setup(self._pin,self._gpio.IN)
        self._pirmotion = False


    def update(self):
        if self._gpio.input(self._pin):
            self._pirmotion = True
            return True
        else:
            self._pirmotion = False
            return False

    def draw(self, frame):
        if self._pirmotion:
            cv2.putText(frame, "PIR: Motion Detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2)
            return frame
        else:
            cv2.putText(frame, "PIR: No motion detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            return frame



if __name__ == '__main__':
    print "Testcode for Pir"
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    pir = PirSensor(GPIO, 14)
    while(True):
        try:
           time.sleep(0.2)
           if pir.motion():
               print "Motion detected!"
           else:
               print "No motion detected!"
        except:
            break



