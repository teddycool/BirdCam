__author__ = 'teddycool'
#PREREQ: https://learn.adafruit.com/downloads/pdf/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging.pdf

import os
import time
import Adafruit_DHT
class DHT(object):

    def __init__(self, type, pin):
        self._pin = pin
        sensor_args = { '11': Adafruit_DHT.DHT11,
				'22': Adafruit_DHT.DHT22,
				'2302': Adafruit_DHT.AM2302 }
        self._sensor = sensor_args[type]


    def read(self):
        try:
            #humidity, temperature
            humidity, temperature = Adafruit_DHT.read_retry(self._sensor, self._pin)
            humidity = round(float(humidity),1)
            temperature = round(float(temperature),1)
            return str(humidity), str(temperature)
        except:
            return "N/A", "N/A"




if __name__ == '__main__':
    print "Testcode for DHT humidity and temp sensors"
    dht11=DHT('11',21)
    while True:
        print "DHT11-> " + str(dht11.read())
        time.sleep(1)