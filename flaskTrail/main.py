from flask import Flask, render_template, Response, request, jsonify
import cv2
from matplotlib.style.core import available
# from torchvision.transforms.v2.functional import adjust_brightness
from ultralytics import YOLO
# import numpy as np
app = Flask(__name__)

model = YOLO('yolo11n.pt')
model2 = YOLO('yolo11n.pt')

threshold = 0.01
brightness = 0
cam = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global threshold
    data = request.get_json()
    threshold = float(data['threshold']) / 100
    print(threshold)
    print(jsonify({"status": "success", "threshold": threshold}))
    return jsonify({"status": "success", "threshold": threshold})

@app.route('/update_brightness', methods=['POST'])
def update_brightness():
    global brightness
    data = request.get_json()
    brightness = float(data['brightness'])
    brightness *= 5.1
    brightness = brightness - 255
    return jsonify({"status": "success", "brigtness": brightness})

def setBrightness(image):
    global brightness
    h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    v = brightness = brightness * 5.1 - 255


@app.route('/update_cam', methods=['POST'])
def update_cam():
    global cam
    data = request.get_json()
    cam = int(data['camera'].replace("cam", "")) - 1
    return jsonify({"status": "success", "cam": cam})



def generate_frames():
    global threshold
    global brightness
    global cam
    availableCams = []
    for i in range(10):
        cap = cv2.VideoCapture()
        if cap.isOpened():
            availableCams.append(i)
            cap.release()
    print("Available cameras: ", availableCams)
    cap = cv2.VideoCapture(cam)
    # cap = cv2.VideoCapture(0)
    # cap2 = cv2.VideoCapture(1)
    while True:
        success, frame = cap.read()
        # _, frame2 = cap2.read()
        if not success:
            break
        else:
            # for i in availableCams:
                cap = cv2.VideoCapture(cam)
                # cap2 = cv2.VideoCapture(1)
                # frame = setBrightness()
                frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness)
                # results = model.predict(source=frame, conf=threshold)
                results = model.track(source=frame, conf=threshold)
                for r in results:
                    frame = r.plot()

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
