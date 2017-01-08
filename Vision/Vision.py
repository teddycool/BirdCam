__author__ = 'teddycool'
#Master class for the vision system, using other classes for each type of detection
#
#Webinfo used for this part of project:
# http://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android
import time
import sys
import os

import cv2

from picamera import PiCamera
#import picamera.array
from picamera.array import PiRGBArray
try:
    from config import birdcam
except:
    birdcam = {"Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
               "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.1},  # times per second
               "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False,
                          "VideoPath": "/home/pi/BirdCam/Videos/"},
               "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
               #            "IrLight": {"Pin": 12, "StartFreq": 50},
               "TempHum": {"Pin": 10},
               "OcuLed": {"Pin": 11},
               }
#from Logger import Logger
#import io


class Vision(object):

    def __init__(self, resolution):
        print "Vision object started..."
        self._seqno = 0
 #       self._log = Logger.Logger("Vision")
        self._cam = PiCamera()
        self._cam.resolution = resolution
        self._cam.framerate = 10
        self._rawCapture = PiRGBArray(self._cam, size=resolution)
        self._center = (resolution[0]/2, resolution[1]/2)
        #TODO: turn off cam led
        #TODO: check that streamer is running


    def initialize(self):
        print "Vision initialised"
        self._lastframetime = time.time()
        self._imagegenerator = self._cam.capture_continuous(self._rawCapture, format="bgr", use_video_port=True)

        print "Starting streamer..."
        print os.system('sudo mkdir /tmp/stream')
        print os.system('sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &')




    def update(self):
        print "Vision update"
#        self._log.info("Update started")
        frame = self._imagegenerator.next()
        self._rawCapture.truncate()
        self._rawCapture.seek(0)
        self._frame = frame.array

        if birdcam["Vision"]["WriteRawImageToFile"]:
            cv2.imwrite("/home/pi/BirdCam/Imgs/camseq"+str(self._seqno)+".jpg",self._frame )
        #TODO: deliver found obstacles back to main-loop or sensor-module
 #       self._log.info("Update finnished")
        #TODO: return detected obstacles etc

    def draw(self, frame):
 #       self._log.info("Draw started")
        framerate = 1/(time.time()-self._lastframetime)
        print "Vision framerate: " + str(framerate)
        self._lastframetime= time.time()

        #cv2.line(frame, self._laserfinder._point, self._center,(0,255,0),2)
        cv2.putText(frame,"Streamer: " + birdcam["Streamer"]["StreamerImage"] + " Current framerate: " + str(round(framerate, 2)), (5,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        #Draw to streamer lib to 'publish'
        cv2.imwrite(birdcam["Streamer"]["StreamerImage"],frame)
        if birdcam["Vision"]["WriteCvImageToFile"]:
            cv2.imwrite("/home/pi/BirdCam/Imgs/cvseq"+str(self._seqno)+".jpg",frame)
        self._seqno = self._seqno+1 #Used globally but set here        #TODO: set up a defined (max) framerate from config
 #       self._log.info("Draw finnished")


    def getCurrentFrame(self):
        return self._frame


    def __del__(self):
        print "Vision object deleted..."
        self._cam.close()




if __name__ == '__main__':
    print "Testcode for Vision"
    import RPi.GPIO as GPIO
 #   from Actuators import Laser

    GPIO.setmode(GPIO.BCM)

    vision= Vision( (640,480))
    vision.initialize()
    try:
        while 1:
            #print "Updating frame..."
            frame = vision.update()
            #print "Drawing frame..."
            vision.draw(frame)
            time.sleep(0.2)
    except:
        GPIO.cleanup()
        e = sys.exc_info()[0]
        print e