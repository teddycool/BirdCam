

# BirdCam generation 3
A raspberry pi 3 with an ir-cam mounted in a bird-house connected by WLAN to our network.
Video-files will be stored on the pi but also synchronized to a network-disc and web-server.
Videos will be recorded as soon something moves in the birdhouse.
Sensors will detect temperature and humidity. 
This information will also be put as text in the video-stream.

Live videostream:
http://sundback.ddns.net/

YouTube playlist with selected videos:
https://www.youtube.com/playlist?list=PLV_h32w58P6RqVj_bv-gp7MivZIyKaHpq

Project webpage (currently in swedish):
http://www.sundback.com/wp/projekt/holkcam/holkcam3/


sudo apt-get update
sudo apt-get upgrade
wget http://lilnetwork.com/download/raspberrypi/mjpg-streamer.tar.gz
tar xvzf mjpg-streamer.tar.gz
sudo apt-get install libjpeg8-dev
sudo apt-get install imagemagick
cd mjpg-streamer/mjpg-streamer
make
./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www"
