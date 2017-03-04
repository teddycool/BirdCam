__author__ = 'teddycool'
#Handling all configuration for birdcam
birdcam = { "Debug": True,
            "Cam": {"Res": (1024, 768), "Id": 1, "FrameRate": 20},
            "Streamer": {"StreamerImage": "/ram/stream/pic.jpg", "StreamerLib": "/ram/stream"},
            "RefreshRates": {"MainLoop": 10, "Streamer": 10, "Sensors": 0.01, "ServerSync": 0.0001}, #times per second #TODO: change to time between instead
            "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False, "PrintFrameRate": False},
            "MotionDetector": {"MotionCount": 200, "History":50},
            #"Recorder": {"VideoFileDir": "/ram/videos/", "VideoFile":"/home/pi/BirdCam/video.avi"},
            "Recorder": {"VideoFileDir": "/mnt/ubuntu/videos/", "VideoFile":"/home/pi/BirdCam/video.avi"},
            "Logger": {"LogFile": "/home/pi/BirdCam/Logger/log.txt"},
            "IrLigth": {"ControlPins":[26,19,13,6,4], "StartFreq": 100},
            "TempHum": {"Type": "2302","Pin": 2},
            "OcuLed" : {"Pin": 11},
            "PirSensor": {"Pin": 14},
            # sudo mount -t cifs //192.168.10.3/webhome /mnt/ubuntu -o user=psk,pass=elinsu,dom=EV39
            "Server" : {"Active": False, "ConnectionString": "sudo mount -t cifs //192.168.10.3/web /mnt/ubuntu -o user=psk,pass=elinsu,dom=EV39",
                        "MntPoint": "/mnt/ubuntu", "subdir": "/videos/"}
                }

