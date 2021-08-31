import cv2
import time

cap = cv2.VideoCapture('http://10.0.0.64:5000/video_feed')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while True:
  ret, frame = cap.read()
  if ret:
    cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video', frame)
  else:
    cap = cv2.VideoCapture('http://10.0.0.64:5000/video_feed')
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    time.sleep(2)
    
  if cv2.waitKey(1) == 27:
    exit(0)
