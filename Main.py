import MainLoop
import time
import os
import sys

class Main(object):

    #TODO: add debug mode and get rid of all printouts when not in debug...

    def __init__(self):
        print "Init Main object for CamDevice..."
        self._mainLoop=MainLoop.MainLoop()
        print "Staring mainloop initialize"
        self._mainLoop.initialize()
        f = file("bc2_restarts.txt", 'a')
        f.write(time.asctime() + "\n")
        f.close()


    def run(self):
        running = True
        print "Starting mainloop update"
        while running:
            start = time.time()
            try:
                frame = self._mainLoop.update()
                end = time.time()
                fr = round(1/(end-start),1)
                self._mainLoop.draw(frame, fr)
                start = time.time()
            except (KeyboardInterrupt):
                running = False
            except:
                running = False
                e = sys.exc_info()
                f = file(time.asctime() + ".log", 'w')
                for l in e:
                    print l
                    f.write(str(l))
                print "Execution ended..."
            #     #TODO: add reboot counter to avoid restarting over and over again...
                print "Waiting to reboot..."
                time.sleep(2)
                os.system('sudo reboot')


#Testcode to run module. Standard Python way of testing modules.
#Put in  /etc/rc.local for autostart at boot:
# cd /home/pi/BirdCam
# sudo python Main.py &
#Put in  /etc/rc.local to create the nedded ramdisk:
#sudo mkdir -p /ram
#sudo mount -t tmpfs -o size=100m tmpfs /ram
 
# sudo mount -t cifs //192.168.10.6/bcvideos /mnt/ubuntu -o user=pi,pass=raspberry,dom=EV39


if __name__ == "__main__":
    cd=Main()
    cd.run()
