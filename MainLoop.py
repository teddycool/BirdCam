__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import Sensors
from Driver import Driver
from Vision import Vision
from Actuators import Laser


#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._driver = Driver.Driver(self._gpio)
        self._sensors = Sensors.Sensors(self._gpio)
        self._vision = Vision.Vision((640,480))


    def initialize(self):
        print "MainLoop init..."
        print "Starting streamer..."
        print os.system('sudo mkdir /tmp/stream')
        print os.system('sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &')
        print "Starting timers..."
        self.time=time.time()
        self._vision.initialize()
        print "BirdCam started at ", self.time

    def update(self):
        self._sensors.update()
        #TODO: add vision update...
        #self._driver.update(self._sensors.sensorvaluesdict)
        #time.sleep(0.01)

    def draw(self):
        frame = self._vision.getCurrentFrame()
        self._sensors.draw(frame)
        self._driver.draw(frame)
        self._vision.draw(frame)

    def __del__(self):
        GPIO.cleanup()
        print "MainLoop cleaned up"