import MainLoop
import time
import os
import sys

class Main(object):

    def __init__(self):
        print "Init Main object for CamDevice..."
        self._mainLoop=MainLoop.MainLoop()

        self._mainLoop.initialize()
        running = True
        while running:
            try:
                self._mainLoop.update()
            except:
                running = False
                del (self._mainLoop)
                e = sys.exc_info()
                t = time
                n = time.ctime()[11:13] + time.ctime()[14:16]
                s = str(n).rjust(4)
                f = file(time.asctime() + ".log", 'w')
                for l in e:
                    f.write(str(l))
                #TODO: add reboot counter to avoid restarting over and over again...
                os.system('sudo reboot')


#Testcode to run module. Standard Python way of testing modules.
#Put in  /etc/rc.local for autostart at boot:
# cd /home/pi/NetBridgLogger
# sudo python Main.py &

if __name__ == "__main__":
    cd=Main()
    cd.run()
