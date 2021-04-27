from flask import Flask, render_template, Response
import cv2
import pyautogui
import numpy as np

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            #ret, buffer = cv2.imencode('.jpg', frame)

            scale = 1/16

            # PYAUTOGUI
            img = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            #img = cv2.resize(img, ((int(2560*scale),int(1440*scale))))

            # HIGH RES BUT SLOW?
            #img = cv2.resize(img, ((480,320)), interpolation=cv2.INTER_LANCZOS4)
            img = cv2.resize(img, ((240,180)), interpolation=cv2.INTER_LANCZOS4)

            ret, buffer = cv2.imencode('.jpg', img)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    page = """
    <html>
        <head>
            <title>Video Streaming Demonstration</title>
        </head>
        <body style="background-color:black;">
            <img id="stream" heigth="100%" width="100%" src="http://0.0.0.0:5000/video_feed" onerror="javascript: alert('failure')"/>
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
