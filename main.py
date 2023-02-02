#!/usr/bin/env python
# -*- coding: utf-8 -*

# sudo apt-get install python3-flask
# pip3 install opencv-python

from flask import Flask, render_template, Response
import cv2
import ffmpeg_streaming
from ffmpeg_streaming import Formats


app = Flask(__name__)


# app.config["CACHE_TYPE"] = "null"

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/stream')
def stream():
    # First we stream the video file
    stream_feed()

    """Video streaming home page."""
    return render_template('stream.html')


def gen():
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    while True:
        ret, frame = vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    vs.release()
    cv2.destroyAllWindows()



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Transcode la video en fichiers streamable via la techno HLS
# https://developer.apple.com/streaming/
def stream_feed():
    video = ffmpeg_streaming.input('videos/video.mp4')

    hls = video.hls(Formats.h264())
    hls.auto_generate_representations()
    hls.output('static/output/hls.m3u8')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)