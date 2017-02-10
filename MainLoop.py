__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import DHT
from Vision import Vision
from Actuators import IrLigth
from config import birdcam
from Sensors import Pir



#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._vision = Vision.Vision()
        self._irlight = []
        for index in range(0,len(birdcam["IrLigth"]["ControlPins"])):
            self._irlight.append(IrLigth.IrLigth(self._gpio,birdcam["IrLigth"]["ControlPins"][index]))
        self._dht = DHT.DHT(birdcam["TempHum"]["Type"], birdcam["TempHum"]["Pin"])
        self._pir = Pir.PirSensor(self._gpio, birdcam["PirSensor"]["Pin"])


    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
        for index in range(0, len(birdcam["IrLigth"]["ControlPins"])):
            self._irlight[index].initialize()
        self._vision.initialize()
        print "BirdCam started at ", self.time

    def update(self):
        #print " MainLoop update started"
        self._dht.update()
        self._pir.update()
        frame = self._vision.update()
        #TODO: add sync/copy mechanism to netstorage at certain intervals
        return frame

    def draw(self, frame, fr):
        #print " MainLoop draw started"
        frame = self._dht.draw(frame)
        frame = self._pir.draw(frame)
        self._vision.draw(frame, fr)

    def __del__(self):
        print "BirdCam stopped at ", self.time
        print  "GPIO-cleanup..."
        GPIO.cleanup()
        print "MainLoop cleaned up"