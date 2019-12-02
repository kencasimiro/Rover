#!/bin/sh
#uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --width 384 --height 216 --framerate 20 --server-option '--port=9090' --server-option '--max-queued-connections=30' --server-option '--max-streams=25' --server-option '--max-threads=29'
python3 /home/pi/workspace/Rover-Pi/listener.py

