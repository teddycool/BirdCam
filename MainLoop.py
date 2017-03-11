__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import DHT
from Vision import Vision
from Vision import MotionDetector
from Recorder import Recorder
from Actuators import IrLigth
from config import birdcam
from Sensors import Pir
from Server import ServerSync


#Global GPIO used by all...
import RPi.GPIO as GPIO
import os
import cv2

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
        #self._pir = Pir.PirSensor(self._gpio, birdcam["PirSensor"]["Pin"])
        self._md = MotionDetector.MotionDetector()
        self._rec = Recorder.Recorder()
        self._sync = ServerSync.ServerSync()
        #self._pirMotion = False
        self._mdMotion = False



    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
        for index in range(0, len(birdcam["IrLigth"]["ControlPins"])):
            self._irlight[index].initialize()
        self._vision.initialize()
        self._md.initialize()
        self._rec.initialize()
        self._sync.initialize()
        print "BirdCam started at ", self.time

    def update(self):
        #get next frame
        frame = self._vision.update()
        self._dht.update()
        #self._pirMotion = self._pir.update()
        self._mdMotion = self._md.update(frame)
        recstate = self._rec.update(frame,self._mdMotion)
        self._sync.update(recstate)
        return frame

    def draw(self, frame, fr):
        #print " MainLoop draw started"
        frame = self._dht.draw(frame)

        #frame = self._pir.draw(frame)
        frame = self._md.draw(frame)
        frame = self._rec.draw(frame, fr)
        frame = self._sync.draw(frame)
        self._vision.draw(frame, fr)

    def __del__(self):
        print "BirdCam stopped at ", self.time
        print  "GPIO-cleanup..."
        GPIO.cleanup()
        print "MainLoop cleaned up"