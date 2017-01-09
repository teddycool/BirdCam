__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import DHT
from Vision import Vision2
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
        self._vision = Vision2.Vision()
       # self._irlight = IrLigth.IrLigth(self._gpio,birdcam["IrLigth"]["ControlPin"])
        self._dht = DHT.DHT(birdcam["TempHum"]["Type"], birdcam["TempHum"]["Pin"])


    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
       # self._irlight.initialize()
        self._vision.initialize()
        print "BirdCam started at ", self.time

    def update(self):
        print " MainLoop update started"
        self._dht.update()
        frame = self._vision.update()
        #TODO: add sync/copy mechanism to netstorage at certain intervals
        return frame

    def draw(self, frame, fr):
        print " MainLoop draw started"
        frame = self._dht.draw(frame)
        self._vision.draw(frame, fr)

    def __del__(self):
        print  "GPIO-cleanup..."
        GPIO.cleanup()
        print "MainLoop cleaned up"