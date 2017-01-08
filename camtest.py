import picamera
cam = picamera.PiCamera()
try:
    while (1):
        cam.start_preview()
except:
    cam.stop_preview()