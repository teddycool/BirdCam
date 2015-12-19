__author__ = 'teddycool'

class Buzzer(object):
    def __init__(self, GPIO, controlpin=20):
        self._gpio = GPIO
        self._pin = controlpin
        self._gpio.setup(self._pin,self._gpio.OUT)
        self._pin =  self._gpio.PWM(self._pin, 200)

        self._speedGpio = self._gpio.setup(26,self._gpio.OUT )
        self._speedGpio =  self._gpio.PWM(26, 200) #Pin 26 for speed control and using 200 hz
        self._currrentFreq = 0
        self._pin.start(self._currrentFreq)


    def setFrequency(self, freq):
        self._currrentFreq = freq
        self._speedGpio.ChangeDutyCycle(freq)


if __name__ == '__main__':
    print "Testcode for Buzzer"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import time
    buzzer = Buzzer(GPIO, 20)
    buzzer.setFrequency(20)
    time.sleep(2)
    buzzer.setFrequency(0)
    GPIO.cleanup()



