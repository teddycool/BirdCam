__author__ = 'teddycool'
    #http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
    # Connected to pin 2...
import os
import time
import cv2

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class DS18B20(object):
    
    def __init__(self, serial):
        self._serial = serial
        self._sensorfile= "/sys/bus/w1/devices/" + self._serial + "/w1_slave"
        self._temp= "N/A"
        self._lastUpdate = 0

    def update(self):
        if time.time() - self._lastUpdate > 120:
            self.read_temp()
            self._lastUpdate = time.time()
            #Publish to MQTT

    def draw(self, frame, text, posx):

        cv2.putText(frame, text + self._temp + "C", (posx,50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame


    def temp_raw(self):    
        f = open(self._sensorfile, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp(self):
        try:
            lines = self.temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                #time.sleep(0.2)
                lines = self.temp_raw()

            temp_output = lines[1].find('t=')

            if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string) / 1000.0
                self._temp = str(round(temp_c,1))
        except:
            self._temp=  "N/A"



if __name__ == '__main__':
    print "Testcode for DS18B20"
    serials = ["28-0516a7c088ff", #outside
               "28-0317000161ff", #inside
               ]
    terms = []
    for serial in serials:
        print "DS18B20 with serial " + serial + " created"
        ts = DS18B20(serial)
        terms.append(ts)

    for ts in terms:
        print(ts.read_temp())
        print(ts.temp_raw())