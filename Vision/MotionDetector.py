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
        self._diff = None
        self._diffcount=0

    def initialize(self):
        self.bgSub = cv2.bgsegm.createBackgroundSubtractorMOG(history=50)

    def update(self, frame):
        mask = self._prepareFrame(frame)
        if self._diffcount[1] > birdcam["Vision"]["MotionCount"]:
            self._motionDetected = True
        else:
            self._motionDetected = False
        return frame

    def draw(self, frame):
        if self._motionDetected:
            cv2.putText(frame, "VIDEO: Motion Detected " + " #" + str(self._diffcount[1]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "VIDEO: No motion detected"+ " #" + str(self._diffcount[1]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return frame

    def _prepareFrame(self,frame):
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = self.bgSub.apply(imgray)
        self._diffcount = (mask.size, len(mask[mask > 254]))
        return mask





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



