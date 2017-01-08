__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

#from Sensors import Sensors
from Vision import Vision
#from Actuators import IrLigth
from config import birdcam


#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._vision = Vision.Vision((640,480))
       # self._irlight = IrLigth.IrLigth(self._gpio,birdcam["IrLigth"]["ControlPin"])


    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
       # self._irlight.initialize()
        self._vision.initialize()
        print "BirdCam started at ", self.time

    def update(self):
        return
        #TODO: add vision update...
        #time.sleep(0.01)

    def draw(self):
        frame = self._vision.getCurrentFrame()
        self._vision.draw(frame)

    def __del__(self):
        print  "GPIO-cleanup..."
        GPIO.cleanup()
        print "MainLoop cleaned up"