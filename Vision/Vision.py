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
import os
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
        self._recording= False


    def initialize(self):
        print "Vision initialised"
        print "Starting streamer..."

        print os.system('sudo mkdir /ram/stream')
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
        #Rotate the camera-view
        self._cam.rotation = 270
        print "Wait for the automatic gain control to settle"
        time.sleep(2)
      #  print "Setting cam fix values"
        # Now fix the values
        #self._cam.shutter_speed = self._cam.exposure_speed
        self._cam.exposure_mode = 'sports'
       # g = self._cam.awb_gains
        self._cam.awb_mode = 'auto'
        self._cam.sharpness = 10
      # self._cam.awb_gains = g
        print "Starting image-generator..."
        self._lastframetime = time.time()
        self._rawCapture = PiRGBArray(self._cam, size= self._resolution)
        self._imagegenerator = self._cam.capture_continuous(self._rawCapture, format="bgr", use_video_port=True)
        print "getting first frame"
        frame = self.update()

    def update(self):
        rawframe = self._imagegenerator.next()
        self._rawCapture.truncate()
        self._rawCapture.seek(0)
        frame = rawframe.array
        return frame


    #Final draw and actually drawing to stream
    def draw(self, frame, framerate=0):
        if birdcam["Vision"]["PrintFrameRate"] and framerate!=0:
            cv2.putText(frame, "Framerate: " + str(framerate), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.imwrite(birdcam["Streamer"]["StreamerImage"], frame)
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