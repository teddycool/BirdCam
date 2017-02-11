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
        self._firstFrame = None
        self._nextFrame = None
        self._states=["IDLE", "START", "RECORDING", "STOP"]
        self._state= self._states[0]
        self._prepFrameQueue = []  #Put & pop from this array
        self._videow = None
        self._diff = None

    def initialize(self, first, current, next):
        #Fill queue with copies of first frame?
        self._firstFrame = self._prepareFrame(first)
        self._currentFrame = self._prepareFrame(current)
        self._currentNext = self._prepareFrame(next)
        self.bgSub = cv2.bgsegm.createBackgroundSubtractorMOG()


    def update(self, nframe):
        self._nextFrame = self._prepareFrame(nframe)

        self._diff = self._diffImg(self._firstFrame, self._currentFrame, self._nextFrame)
        self._firstFrame= self._currentFrame
        self._currentFrame = self._nextFrame
        self._diffcount = cv2.countNonZero(self._diff)
        if self._diffcount > 10000:
            self._motionDetected = True
        else:
            self._motionDetected = False
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
        #return self._motionDetected

    def draw(self, frame):
        #frame = self._diff
        frame = self.bgSub.apply(frame)
        if self._motionDetected:
            cv2.putText(frame, "VIDEO: Motion Detected " + " #" + str(self._diffcount), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "VIDEO: No motion detected", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return frame



    def _prepareFrame(self,frame):
        frame = self.bgSub.apply(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)
        return gray

    def _diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        self._diff = cv2.bitwise_and(d1, d2)
        return self._diff




if __name__ == '__main__':
    #Testcode for motiondetector
    #TODO: try with a videofile instead
    cam = cv2.VideoCapture(0)
    winName = "Movement Indicator"
    cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
    md = MotionDetector()
    md.initialize(cam.read()[1])
    while True:
        md.update(cam.read()[1])
        cv2.imshow(winName, md._diff)
        print md._motionDetected

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyWindow(winName)
            break



