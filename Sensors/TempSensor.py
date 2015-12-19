
#http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
import os
import time
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class TempSensor(object):
    
    def __init__(self, serial="28-03146af27cff"):
        self._serial = serial
        self._sensorfile= "/sys/bus/w1/devices/" + self._serial + "/w1_slave"

    def temp_raw(self):    
        f = open(self._sensorfile, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp(self):
        lines = self.temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.temp_raw()
            
        temp_output = lines[1].find('t=')
        
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

if __name__ == '__main__':
    print "Testcode for TempSensor"
    ts=TempSensor()
    while True:
            print(ts.read_temp())
            time.sleep(1)