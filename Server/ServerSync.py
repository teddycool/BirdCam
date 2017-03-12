__author__ = 'teddycool'
#syncing files to server

import time
import sys
from config import birdcam
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
        if  os.system('sudo mkdir /ram/videos') == 0:
            print "Created /ram/videos directory for tempfiles"
        self._connect()

    def update(self, recstate):
        if recstate == "STOP":
            if self._init:
                # get all files in temp video directory and copy them to server if bigger then x
                onlyfiles = [f for f in listdir("/ram/videos/") if isfile(join("/ram/videos/", f))]
                for f in onlyfiles:
                    fh = join("/ram/videos/", f)
                    print "File to handle: " + fh
                    size = os.path.getsize(fh)
                    print "filesize = " + str(size)
                    if  size > birdcam["Server"]["MinSizeToCopy"]:
                        try:
                            shutil.copy2(fh, join(birdcam["Server"]["MntPoint"] + birdcam["Server"]["subdir"], f))
                            print "Copied file to webserver: " + join(
                                birdcam["Server"]["MntPoint"] + birdcam["Server"]["subdir"], f)
                        except:
                            print "I/O error"
                            return
                    os.remove(fh)
                    print "Removed file from ramdisk: " + fh
        return

    def draw(self,frame):
 #       if self._init:
 #           cv2.putText(frame, "Server sync available", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
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
            os.system('sudo umount /mnt/ubuntu')
            print "Server filesystem unmounted"
        except:
            print "Server filesystemen not unmouted!"



if __name__ == '__main__':
    print "Testcode for ServerSync"

    ss= ServerSync()
    ss.initialize()
    ss.update("IDLE")
    time.sleep(2)
    ss.update("STOP")
