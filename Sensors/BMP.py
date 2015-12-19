__author__ = 'teddycool'

import Adafruit_BMP.BMP085 as BMP085


class BMP(object):

    def __init__(self):
        self._sensor = BMP085.BMP085()


    def readPressure(self):
        try:
            pre = float('{0:0.2f}'.format(self._sensor.read_pressure()/1000.0))
            return str(round(pre,1))
        except:
            return "N/A"

    def readTemperature(self):
        try:
            temp = float('{0:0.2f}'.format(self._sensor.read_temperature()))
            return str(round(temp,1))
        except:
            return "N/A"


if __name__ == '__main__':
    print "Testcode for BMP085 barometric"
    bmp = BMP()
    pres = bmp.readPressure()
    temp= bmp.readTemperature()
    print str(pres) + "hPa " + str(temp) + "C "