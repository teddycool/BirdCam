__author__ = 'teddycool'
#syncing files to server

import time
import sys
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
            #print os.system('sudo mount -t cifs //192.168.10.3/webhome /mnt/ubuntu -o user=psk,pass=elinsu,dom=EV39')
            res = os.system(birdcam["Server"]["ConnectionString"])
            if res==0:
                print "Webserver filesystem mounted successfully"
                self._init = True
            else:
                self._init = False

        except:
            e = sys.exc_info()
            for l in e:
                print l
            self._init = False

    def update(self):
        #Do serversync here...
        return

    def draw(self,frame):
 #       if self._init:
 #           cv2.putText(frame, "Server sync available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 #       else:
 #           cv2.putText(frame, "Server sync not available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame


    def __del__(self):
        try:
            os.system('sudo umount /mnt/ubuntu')
            print "Server filesystem unmounted"
        except:
            print "Server filesystemen not unmouted!"

