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
camera = cv2.VideoCapture(0)

# # open reference image for computer vision
# laser_reference = cv2.imread("laser_reference.jpg")
#
# # get grayscale version and RGB version of reference
# laser_reference_gray = cv2.cvtColor(laser_reference, cv2.COLOR_BGR2GRAY)
# laser_reference_rgb = cv2.cvtColor(laser_reference, cv2.COLOR_BGR2RGB)

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
pixel = (42.0, 94.0, 122.0, 139.0, 150.0, 157.0, 163.0, 168.0, 171.0)  # /**< Measured values of pixels. */
cm = (20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0)

cam_number = 1  # /**< The number of the camera, the 0 is the built in my computer. */
cam_width = 640  # /**< Width of the video's resolution. */
cam_height = 480  # /**< Height of the video's resolution. */
threshold_min = 245  # /**< Minimum value of the binary threshold. */
threshold_max = 255  # /**< Maximum value of the binary threshold. */


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        # frame[:, spacing:-1:spacing] = [0, 0, 255]  # red horizontal lines
        # frame[spacing:-1:spacing, :] = [255, 0, 0]  # blue vertical lines
        # frame = cv2.putText(frame, "Talos III", org, font,
        #                     fontScale, color, thickness, cv2.LINE_AA)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(frame, 200, 255)

        ret, thresh = cv2.threshold(frame, threshold_min, threshold_max, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            m = cv2.moments(contours[0])
            if m["m00"] > 0.0:
                coord_x = int(m["m10"] / m["m00"])
                coord_y = int(m["m01"] / m["m00"])

                # if (coord_y > pixel[0]) and (coord_y < pixel[-1]):
                if True:
                    i = 0
                    # while coord_y > pixel[i + 1]:
                    #     i += 1
                    # distance = cm[i] + ((coord_y - pixel[i]) * (cm[i + 1] - cm[i]) / (pixel[i + 1] - pixel[i]))
                    #

                    cv2.circle(frame, (coord_x, coord_y), 20, (0, 255, 0), 3)
                    # cv2.putText(frame, "{} {}")
                    # frame = cv2.putText(frame, "{} ", (coord_x, coord_y), font,
                    #                     fontScale, color, thickness, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)

        cv2.imshow('mask', mask)

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
