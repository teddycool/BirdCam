__author__ = 'teddycool'
#syncing files to server

import time
from config import birdcam
import cv2
import os


class ServerSync(object):
    def __init__(self):
        self._lastSync = 0
        self._state = "IDLE" #IDLE, CHECK, COPY
        self._init = False

    def initialize(self):
        try:
            print os.system('sudo mount -t cifs //192.168.10.3/bcvideos /mnt/ubuntu -o user=pi,pass=raspberry,dom=EV39')
            print "Server filesystem mounted"
            self._init = True
        except:
            self._init = False

    def update(self):
        return

    def draw(self,frame):
        if self._init:
            cv2.putText(frame, "Server sync available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Server sync not available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame


    def __del__(self):
        try:
            os.system('sudo umount /mnt/ubuntu')
            print "Server filesystem unmounted"
        except:
            print "Server filesystemen not unmouted!"

