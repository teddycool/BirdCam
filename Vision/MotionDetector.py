__author__ = 'teddycool'
#motiondetector and statehandling

import time
import cv2
from config import birdcam

#Min number of changed pixels for motion detected
#Number of frames before motion true
#Number of frames before motion false
#Max number of frames before stopping?
#Min number of idle frames


class MotionDetector(object):
    def __init__(self):
        self._motionDetected = False
        self._currentFrame=None
        self._previousFrame = None
        self._states=["IDLE", "START", "RECORDING", "STOP"]
        self._state= self._states[0]
        self._prepFrameQueue = []  #Put & pop from this array
        self._videow = None

    def initialize(self, firstframe):
        #Fill queue with copies of first frame?
        self._currentFrame = firstframe


    def update(self, cframe):

        #detect motion
        #handle states..

        #Statemachine IDLE


        #Statemachine START
        # Create writer and Start recording
       # videofile = file(birdcam["Vision"]["VideoFileDir"] + time.asctime() + ".avi", 'w')
       # self._videow = cv2.VideoWriter(videofile, cv2.VideoWriter_fourcc(*'XVID'), 5, self._resolution, True)

        # Statemachine RECORDING

        # detect no motion..
        # Statemachine STOP
        #Empty frame queue
        #Stop recording
        #copy videofile to network-resource if server active
        #Remove file from ramdisk

        #True if motion detected = recording
        return False




    def _prepareFrame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)
        return gray



if __name__ == '__main__':
    #Testcode for motiondetector
    #TODO: try with a videofile instead

    md = MotionDetector()
    frame = None
    cam = cv2.VideoCapture("C:\\Users\\psk\\Documents\\GitHub\\BirdCam\\Vision\\video.avi")
    (grabbed, frame) = cam. read()
    if not grabbed:
        print "Didn't read frame from videofile"
    else:
        md.initialize(frame)
        while True:
            (grabbed, frame) = cam.read()
            if not grabbed:
                break
            cv2.imshow("MotionDetector", frame)
        cam.release()
        cv2.destroyAllWindows()




