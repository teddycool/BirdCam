__author__ = 'teddycool'
#motiondetector and statehandling

import time
import cv2
try:
    from config import birdcam
except:
    birdcam = { "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": False},
    "MotionDetector": {"MotionCount": 200, "History": 50}}


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
        self.bgSub = cv2.bgsegm.createBackgroundSubtractorMOG(history=birdcam["MotionDetector"]["History"])

    def update(self, frame):
        mask = self._prepareFrame(frame)
        if self._diffcount[1] > birdcam["MotionDetector"]["MotionCount"]:
            self._motionDetected = True
        else:
            self._motionDetected = False
        return self._motionDetected

    def draw(self, frame):
     #   if self._motionDetected:
     #       cv2.putText(frame, "VIDEO: Motion Detected " + " #" + str(self._diffcount[1]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
       # else:
       #     cv2.putText(frame, "VIDEO: No motion detected"+ " #" + str(self._diffcount[1]), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return frame

    def _prepareFrame(self,frame):
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = self.bgSub.apply(imgray)
        self._diffcount = (mask.size, len(mask[mask > 254]))
        return mask





if __name__ == '__main__':
    #Testcode for motiondetector
    #TODO: try with a videofile instead
    #vidcap = cv2.VideoCapture("C:\\Users\\psk\\Documents\\GitHub\\DartScore\\dartscore_20170326_185600.avi")
    cam = cv2.VideoCapture("C:\\Users\\psk\\Documents\\GitHub\\DartScore\\dartscore_20170326_185600.avi")
    img = cam.read()[1]
    print img

    winName = "Movement Indicator"
    cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
#    md = MotionDetector()
#    md.initialize()
    while True:
        cv2.imshow("test", cam.read()[1])

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyWindow(winName)
            break



