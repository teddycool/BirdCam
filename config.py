__author__ = 'teddycool'

#Handling all configuration for legorover
birdcam = { "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
               "RefreshRates": {"DriverLoop": 10, "Streamer": 2, "Sensors": 10}, #times per second
               "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False},
                "Logger": {"LogFile": "/home/pi/LegoRover/Logger/log.txt"},
                }

