__author__ = 'teddycool'
#syncing files to server

import time
import sys
try:
    from config import birdcam
except:
    birdcam = {
                "Recorder": {"VideoFileDir": "/mnt/ubuntu/videos/", "VideoFile": "/home/pi/BirdCam/video.avi",
                     "tempfile": "/ram/videos/", "MinSize": 100000},
                "Server": {"Active": False,
                          "ConnectionString": "sudo mount -t cifs //192.168.10.3/web /mnt/ubuntu -o user=psk,pass=elinsu,dom=EV39",
                          "MntPoint": "/mnt/ubuntu", "subdir": "/videos/"}
               }
import cv2
import os
import shutil

from os import listdir
from os.path import isfile, join


class ServerSync(object):
    def __init__(self):
        self._lastSync = 0
        self._state = "IDLE" #IDLE, CHECK, COPY
        self._init = False

    def initialize(self):
        #Create temp video dir on ramdisk
        try:
            print os.system('sudo mkdir /ram/videos')
        except:
            pass
        self._connect()



    def update(self, recstate):
        if recstate == "STOP":
            if self._init:
                # get all files in temp video directory and copy them to server if bigger then x
                onlyfiles = [f for f in listdir("/ram/videos/") if isfile(join("/ram/videos/", f))]
                for f in onlyfiles:
                    fh = join("/ram/videos/", f)
                    print "File to copy to handle: " + fh
                    if os.path.getsize(fh) > birdcam["Recorder"]["MinSize"]:
                        try:
                            shutil.copy2(fh, join(birdcam["Server"]["MntPoint"] + birdcam["Server"]["subdir"], f))
                            print "Copied file to webserver: " + join(birdcam["Server"]["MntPoint"] + birdcam["Server"]["subdir"], f)
                        except:
                            print "I/O error"
                            return
                    os.remove(fh)
                    print "Removed file from ramdisk: " + fh
        return

    def draw(self,frame):
 #       if self._init:
 #           cv2.putText(frame, "Server sync ongoing", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 #       else:
 #           cv2.putText(frame, "Server sync not available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame


    def _connect(self):
        try:
            # connect to webserver via connectionstring
            res = os.system(birdcam["Server"]["ConnectionString"])
            if res == 0:
                print "Webserver filesystem mounted successfully"
                self._init = True
            else:
                self._init = False

        except:
            e = sys.exc_info()
            for l in e:
                print l
            self._init = False


    def __del__(self):
        try:
 #           os.system('sudo umount /mnt/ubuntu')
            print "Server filesystem not unmounted"
        except:
            print "Server filesystemen not unmouted!"



if __name__ == '__main__':
    print "Testcode for ServerSync"
    #Create the testfile
    filename = join("/ram/videos/", "bc2_" + time.strftime("%Y%m%d_%H%M%S") + ".txt")
    f = file(filename, "w")
    f.write("Testing-" * 100000)
    print os.path.getsize(filename)
    while (os.path.getsize(filename) < birdcam["Recorder"]["MinSize"]):
        f = file(filename, "w")
        f.write("Testing-" * 100)
        f.close()
        print "adding data to file    " + str(os.path.getsize(filename))


    ss= ServerSync()
    ss._init = True
    #Do nothing
    ss.update("IDLE")
    time.sleep(2)
    #Copy and erase testfile
    ss.update("STOP")
