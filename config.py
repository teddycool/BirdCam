__author__ = 'teddycool'

#Handling all configuration for birdcam
birdcam = { "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
            "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 10}, #times per second
            "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "VideoPath": "/home/pi/BirdCam/Videos/"},
            "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
            "IrLight": {"Pin": 12, "StartFreq": 50},
            "TempHum": {"Pin": 14},
            "OcuLed" : {"Pin": 10},
                }

