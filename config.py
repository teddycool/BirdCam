__author__ = 'teddycool'
#Handling all configuration for birdcam
birdcam = { "cam": {"res": (640, 480), "id": 1, "framerate": 20},
            "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
            "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.1}, #times per second
            "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": True,
                       "VideoPath": "/home/pi/BirdCam/Videos/"},
            "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
#            "IrLight": {"Pin": 12, "StartFreq": 50},
            "TempHum": {"Pin": 10},
            "OcuLed" : {"Pin": 11},
                }

