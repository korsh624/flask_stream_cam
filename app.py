#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
#Initialize the Flask app
app = Flask(__name__)
import serial
import time
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
# print("connected arduino")
camera = cv2.VideoCapture(0)
print("connected camera")
def gen_frames():  
    while True:
        # data = arduino.readline()
        #prinnt("# read the port data")
        success, frame = camera.read()  # read the camera frame
        frame=cv2.resize(frame, (800, 600))
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, "data", (10, 50), font, 1, color=(0, 255, 255), thickness=2)
        # cv2.putText(frame, data, (10, 50), font, 1, color=(0, 255, 255), thickness=2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)
