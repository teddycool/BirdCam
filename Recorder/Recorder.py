__author__ = 'teddycool'

import time
import cv2
import os
from config import birdcam

class Recorder(object):

    def __init__(self):
        print "Recorder object started..."
        self._seqno = 0
        self._recording= False
        #self._states["IDLE","START", "REC"]
        self._state = "IDLE"
        self._videow = None


    def initialize(self):
        print "Recorder initialised with state " + self._state


    def update(self,frame, pirmotion, mdmotion):
        #TODO: move recording to draw function
        if pirmotion or mdmotion:
            if self._state == "IDLE":
                self._state = "START"
            elif self._state == "START":
                self._state = "REC"

        if not pirmotion and not mdmotion:
            self._state = "IDLE"

        return self._state

    def draw(self, frame,fr):
        #Write recorder string to frame
        cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

        if self._state == "START":
            filename = "bc2_" + time.strftime("%Y%m%d_%H%M%S") + ".avi"
            self._videow = cv2.VideoWriter(birdcam["Recorder"]["VideoFileDir"] + filename,
                                           cv2.VideoWriter_fourcc(*'XVID'), int(fr),
                                           birdcam["Cam"]["Res"], True)
            self._videow.write(frame)
            cv2.putText(frame, "<--Recording-->", (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif self._state == "IDLE":
            if self._videow is not None:
                #self._videow.close()
                self._videow = None

        elif self._state == "REC":
            self._videow.write(frame)
            cv2.putText(frame, "<--Recording-->", (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0, 0, 255), 2)
        return frame

