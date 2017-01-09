__author__ = 'teddycool'
#Handling all configuration for birdcam
birdcam = { "Cam": {"Res": (1024, 768), "Id": 1, "FrameRate": 20},
            "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
            "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.01}, #times per second
            "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": True,
                       "VideoFile": "/home/pi/BirdCam/Videos/test.avi"},
            "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
            "IrLight": {"Pin": 12, "StartFreq": 50},
            "TempHum": {"Type": "2302","Pin": 2},
            "OcuLed" : {"Pin": 11},
                }

