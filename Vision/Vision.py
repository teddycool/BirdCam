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
import MotionDetector
try:
    from config import birdcam
except:
    birdcam =    {"Cam": {"Res": (1024, 768), "Id": 1, "FrameRate": 20},
                  "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
     "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.1},  # times per second
     "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": True, "VideoPath": "/home/pi/BirdCam/Videos/"},
     }

class Vision(object):

    def __init__(self):
        print "Vision object started..."
        self._seqno = 0
        self._md = MotionDetector.MotionDetector()
        self._recording= False


    def initialize(self):
        print "Vision initialised"
        print "Starting streamer..."

        print os.system('sudo mkdir /ram/stream')
        print os.system('sudo mkdir /ram/videos')
        print os.system('sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer  /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /ram/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &')

        print "CAM init..."

        self._resolution = birdcam["Cam"]["Res"]
        self._cam = picamera.PiCamera()
        self._cam.resolution =  self._resolution
        self._center = ( self._resolution[0]/2,  self._resolution[1]/2)
        #TODO: add flips to config for easier handling
        self._cam.hflip = False
        self._cam.vflip = False
        self._cam.framerate = birdcam["Cam"]["FrameRate"]
        print "Wait for the automatic gain control to settle"
        time.sleep(2)
        print "Setting cam fix values"
        # Now fix the values
        self._cam.shutter_speed = self._cam.exposure_speed
        self._cam.exposure_mode = 'off'
        g = self._cam.awb_gains
        self._cam.awb_mode = 'off'
        self._cam.awb_gains = g
        print "Starting image-generator..."
        self._lastframetime = time.time()
        self._rawCapture = PiRGBArray(self._cam, size= self._resolution)
        self._imagegenerator = self._cam.capture_continuous(self._rawCapture, format="bgr", use_video_port=True)

        first = self._frameUpdate()
        current = self._frameUpdate()
        next = self._frameUpdate()

        self._md.initialize(first, current ,next)
        #TODO: move videoformat to config?
        #TODO: Move to motion detector...
        #self._videow = cv2.VideoWriter(birdcam["Vision"]["VideoFile"], cv2.VideoWriter_fourcc(*'XVID'), 5,  self._resolution, True)
        frame = self._frameUpdate()
        return frame

    def _frameUpdate(self):
        rawframe = self._imagegenerator.next()
        self._rawCapture.truncate()
        self._rawCapture.seek(0)
        frame = rawframe.array
        return frame

    def update(self, saveToFile = False):
        #TODO: add logic for frame changed...
        #TODO: fix VideoWriter to open/close files when needed
        frame = self._frameUpdate()
        self._md.update(frame)
        #self._recording = self._md.update(frame)
        return frame

    def draw(self, frame, framerate=0):
        cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        frame = self._md.draw(frame)
        if birdcam["Vision"]["PrintFrameRate"] and framerate!=0:
            cv2.putText(frame, "Framerate: " + str(framerate), (10, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        #Note in stream when recording...
        if self._recording and (int(time.ctime()[18:19]) % 2 == 0):
            cv2.putText(frame, "<--Recording-->" , (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)

        #Write to actual frame for MJPG streamer
        #cv2.VideoWriter.open(birdcam["Vision"]["VideoFile"], cv2.VideoWriter_fourcc(*'XVID'), 5,  self._resolution, True )
        cv2.imwrite(birdcam["Streamer"]["StreamerImage"], frame)
        #TODO: add logic to record video when framess are changed and a number of frames/seconds after...
        #if self._md.
        #self._videow.write(frame)
        return frame


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