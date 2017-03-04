__author__ = 'teddycool'
#PREREQ: https://learn.adafruit.com/downloads/pdf/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging.pdf

import os
import time
import Adafruit_DHT
import cv2


class DHT(object):

    def __init__(self, type, pin):
        self._pin = pin
        sensor_args = { '11': Adafruit_DHT.DHT11,
				        '22': Adafruit_DHT.DHT22,
				        '2302': Adafruit_DHT.AM2302 }
        self._sensor = sensor_args[type]
        self._hum="NA"
        self._temp="NA"
        self._lastUpdate = 0


    def update(self):
        if time.time() - self._lastUpdate > 120:
            try:
                #humidity, temperature
                humidity, temperature = Adafruit_DHT.read_retry(self._sensor, self._pin)
                humidity = round(float(humidity),1)
                temperature = round(float(temperature),1)
                self._hum  = str(humidity)
                self._temp = str(temperature)
            except:
                self._hum = "NA"
                self._temp = "NA"
            self._lastUpdate = time.time()

    def draw(self, frame):
        cv2.putText(frame, "Temp. " + self._temp + "C Hum. " + self._hum +  "%", (10,50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame



if __name__ == '__main__':
    print "Testcode for DHT humidity and temp sensors"
    type = '2302'
    sensor=DHT(type,2)
    while True:
        sensor.update()
        print "Type: " + type + "-> " + sensor._hum +  "%, " + sensor._temp + "C"
        time.sleep(1)