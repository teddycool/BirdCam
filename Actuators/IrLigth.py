__author__ = 'teddycool'
try:
    from config import birdcam
except:
    birdcam = {
                "IrLight": {"ControlPin": 12, "StartFreq": 50}
                }

class IrLigth(object):
    def __init__(self, GPIO, controlpin=12):
        self._gpio = GPIO
        self._pin = controlpin
        self._gpio.setup(self._pin,self._gpio.OUT)
        self._pin =  self._gpio.PWM(self._pin, 200)
        self._currrentFreq = birdcam["IrLight"]["StartFreq"]

    def initialize(self):
        self._pin.start(self._currrentFreq)


    def setFrequency(self, freq):
        self._currrentFreq = freq
        self._pin.ChangeDutyCycle(freq)

    def clean(self):
        self.setFrequency(0)
        self._pin.stop()
        print "PWM cleaned and stoped"


if __name__ == '__main__':
    print "Testcode for IrLigth"
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    ligth = IrLigth(GPIO, 12)
    ligth.initialize()
    ligth.setFrequency(90)
    print "PWM: " + str(ligth._currrentFreq)
    while(True):
        try:
           time.sleep(0.2)
        except:
            ligth.clean()
            GPIO.cleanup()
            break



