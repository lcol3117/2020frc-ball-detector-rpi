import cv2, io, imutils, numpy
from imutils.video import VideoStream
#Initiate capture
cap = cv2.VideoCapture(0)
cap.start()
#Continuosly
while True:
	_, img = cap.read() #Read the capture
	#Convert to HSV Colorspace
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
