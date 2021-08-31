from flask import Flask, render_template, Response
import cv2
import pyautogui
import numpy as np
import time
import mss
import imutils
import simplejpeg

app = Flask(__name__)

#camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

new_frame_time = 0
prev_frame_time = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
font = cv2.FONT_HERSHEY_SIMPLEX

def gen_frames():  # generate frame by frame from camera
    global new_frame_time
    global prev_frame_time

    while True:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            # Capture frame-by-frame
            #success, frame = camera.read()  # read the camera frame
            #if not success:
            #    break
            #else:
                #ret, buffer = cv2.imencode('.jpg', frame)

            #scale = 1/16

            # PYAUTOGUI
            #img = pyautogui.screenshot()
            img = np.array(sct.grab(monitor))
            #img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
            #img = cv2.resize(img, ((int(2560*scale),int(1440*scale))))

            # HIGH RES BUT SLOW?
            img = imutils.resize(img, 240, 180, inter=cv2.INTER_LINEAR)
            #img = imutils.resize(img, 240, 180, inter=cv2.INTER_LANCZOS4)
            #img = cv2.resize(img, ((240,180)), interpolation=cv2.INTER_LINEAR)
            #img = cv2.resize(img, ((480,320)), interpolation=cv2.INTER_LINEAR)
            """
            new_frame_time = time.time()

            # fps will be number of frame processed in given time frame
            # since their will be most of time error of 0.001 second
            # we will be subtracting it to get more accurate result
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
        
            # converting the fps into integer
            fps = int(fps)
        
            # converting the fps to string so that we can display it on frame
            # by using putText function
            fps = str(fps)
        
            # putting the FPS count on the frame
            cv2.putText(img, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            """

            ret, buffer = cv2.imencode('.jpg', img, encode_param)
            #frame = simplejpeg.encode_jpeg(img)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type:image/jpeg\r\n'
                    b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
                    b'\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video')
def video():
    page = """
    <html>
        <head>
            <title>Video Streaming Demonstration</title>
        </head>
        <body style="background-color:black;">
            <img id="stream" heigth="100%" width="100%" src="http://192.168.253.69:5000/video_feed" onerror="javascript: alert('failure')"/>
        </body>
    
    <script>
        let stateCheck = setInterval(() => {
        if (document.readyState === 'complete') {
            clearInterval(stateCheck);
            // document ready
        }
        console.log(document.readyState);
        }, 100);
    
    </script>
    
    </html>
    """

    return page


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
