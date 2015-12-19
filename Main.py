__author__ = 'teddycool'

import os, sys
from MainLoop import MainLoop
from Logger import Logger

class Main(object):

    def __init__(self):
        print "Init Main object..."
        self._mainloop =  MainLoop()
        self._log = Logger.Logger('main')


    def run(self):
        self._mainloop.initialize()
        running=True
        frames = 0
        while running:
            try:
                self._mainloop.update()
                self._mainloop.draw()
                print "End of Main..."
            except Exception as e:
                running = False
                print str(e)


if __name__ == "__main__":
    print 'Started from: Main.py,  if __name__ == "__main__" '
    gl=Main()
    gl.run()

