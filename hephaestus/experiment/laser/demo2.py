from flask import Flask, render_template, Response
import cv2
import numpy as np

spacing = 120
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (450, 650)

# fontScale
fontScale = 4

# Blue color in BGR
color = (0, 128, 0)

# Line thickness of 2 px
thickness = 16

app = Flask(__name__)
camera = cv2.VideoCapture(1)

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        frame[:, spacing:-1:spacing] = [0, 0, 255]  # red horizontal lines
        frame[spacing:-1:spacing, :] = [255, 0, 0]  # blue vertical lines
        frame = cv2.putText(frame, "Talos III", org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
