sudo mkdir /tmp/stream
sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &
