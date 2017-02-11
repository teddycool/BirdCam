import MainLoop
import time
import os
import sys

class Main(object):

    #TODO: add debug mode and get rid of all printouts when not in debug...

    def __init__(self):
        print "Init Main object for CamDevice..."
        self._mainLoop=MainLoop.MainLoop()

        self._mainLoop.initialize()


    def run(self):
        running = True
        while running:
            start = time.time()
            try:
                frame = self._mainLoop.update()
                end = time.time()
                fr = round(1/(end-start),1)
                self._mainLoop.draw(frame, fr)
                start = time.time()
            except:
                running = False
            # except:
            #     e = sys.exc_info()
            #     t = time
            #     n = time.ctime()[11:13] + time.ctime()[14:16]
            #     s = str(n).rjust(4)
            #     f = file(time.asctime() + ".log", 'w')
            #     for l in e:
            #         f.write(str(l))
            #     #TODO: add reboot counter to avoid restarting over and over again...
            #     print "Waiting to reboot..."
            #     time.sleep(2)
            #     os.system('sudo reboot')


#Testcode to run module. Standard Python way of testing modules.
#Put in  /etc/rc.local for autostart at boot:
# cd /home/pi/BirdCam
# sudo python Main.py &
#Put in  /etc/rc.local to create the nedded ramdisk:
#sudo mkdir -p /ram
#sudo mount -t tmpfs -o size=100m tmpfs /ram

# sudo mount -t cifs //192.168.0.4/videos /mnt/ubuntu -o user=pi,pass=raspberry,dom=EV39


if __name__ == "__main__":
    cd=Main()
    cd.run()
