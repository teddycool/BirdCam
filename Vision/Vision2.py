__author__ = 'teddycool'
#Master class for the vision system, using other classes for each type of detection
#
#Webinfo used for this part of project:
# http://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android
import time
import picamera
#import picamera.array
from picamera.array import PiRGBArray
import cv2
import sys
import numpy as np
import os
import pickle
try:
    from config import birdcam
except:
    birdcam =    {"cam": {"res": (1024, 768), "id": 1, "framerate": 20},
                  "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
     "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.1},  # times per second
     "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": True, "VideoPath": "/home/pi/BirdCam/Videos/"},
     }

class Vision(object):

    def __init__(self):
        print "Vision object started..."
        self._seqno = 0
        #TODO: check that streamer is running


    def initialize(self):
        print "Vision initialised"
        print "Starting streamer..."

        print os.system('sudo mkdir /tmp/stream')
        print os.system('sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer  /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &')

        print "CAM init..."

        resolution = birdcam["cam"]["res"]
        self._cam = picamera.PiCamera()
        self._cam.resolution = resolution
        self._center = (resolution[0]/2, resolution[1]/2)
        # TODO: Read accelerometer and adjust flipping depending om camera rotation
        self._cam.hflip = False
        self._cam.vflip = True
        #self._cam.framerate = deviceconfig["cam"]["framerate"]
        #print "Wait for the automatic gain control to settle"
        #time.sleep(2)
        #print "Setting cam fix values"
        # Now fix the values
        #self._cam.shutter_speed = self._cam.exposure_speed
        #self._cam.exposure_mode = 'off'
        #g = self._cam.awb_gains
        #self._cam.awb_mode = 'off'
        #self._cam.awb_gains = g
        print "Starting image-generator..."
        self._lastframetime = time.time()
        self._rawCapture = PiRGBArray(self._cam, size=resolution)
        self._imagegenerator = self._cam.capture_continuous(self._rawCapture, format="bgr", use_video_port=True)
        #self._contourFinder.initialize()
        frame =  self.update()
       # self._videow = cv2.VideoWriter(deviceconfig["Streamer"]["VideoFile"], cv2.cv.CV_FOURCC('P','I','M','1'), 20, resolution )
        return frame

    def update(self, saveToFile = False):
        #TODO: make threaded in exception catcher
        rawframe = self._imagegenerator.next()
        self._rawCapture.truncate()
        self._rawCapture.seek(0)
        frame = rawframe.array
        #self._contourFinder.update(frame)
        return frame

    def draw(self, frame, framerate=0, text = ""):
        #self._contourFinder.draw(frame)
        if birdcam["Vision"]["PrintFrameRate"] and framerate!=0:
            cv2.putText(frame, "Framerate: " + str(framerate), (10, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        if text != "":
            cv2.putText(frame, text , (5, self._cam.resolution[1]/2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2)
        #Write to actual frame for MJPG streamer
        cv2.imwrite(birdcam["Streamer"]["StreamerImage"], frame)


    def setRotation(self, rot):
        if rot in [0,90,180,270]:
            self._cam.rotation = rot


    def __del__(self):
        print "Vision object deleted..."
        self._cam.close()


if __name__ == '__main__':
    print "Testcode for Vision"

    vision= Vision()
    frame = vision.initialize()
    print "Running...... waiting for ctrl-c...."
    print vision._imagegenerator
    print "Start of try"
    frames = 0
    rotation = 0
    framer = 0
    while 1:
        print "Vision update"
        start = time.time()
        frame = vision.update()
        "Vision draw"
        vision.draw(frame, framerate=framer )
        #time.sleep(0.1)
        end = time.time()
        framer = 1/(end-start)