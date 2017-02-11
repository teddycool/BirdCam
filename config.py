__author__ = 'teddycool'
#Handling all configuration for birdcam
birdcam = { "Cam": {"Res": (1024, 768), "Id": 1, "FrameRate": 20},
            "Streamer": {"StreamerImage": "/ram/stream/pic.jpg", "StreamerLib": "/ram/stream"},
            "RefreshRates": {"MainLoop": 10, "Streamer": 2, "Sensors": 0.01}, #times per second
            "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": False,
                       "VideoFileDir": "/ram/videos/", "VideoFile":"/ram/videos/video.avi"},
            "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
            "IrLigth": {"ControlPins":[26,19,13,6,4], "StartFreq": 100},
            "TempHum": {"Type": "2302","Pin": 2},
            "OcuLed" : {"Pin": 11},
            "PirSensor": {"Pin": 14},
            "Server" : {"Active": False, "Url": "//192.168.0.4/videos", "User": "pi", "PassWord": "raspberry", "Domain": "EV39", "MntPoint": "/mnt/ubuntu"}
                }

