import cv2, io, imutils, numpy
from imutils.video import VideoStream
#Initiate capture
cap = cv2.VideoCapture(0)
cap.start()
#Define HSV Thresholds
lower_hsv = numpy.array([])
upper_hsv = numpy.array([])
#Define morphological operation kernels
anti_noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
anti_logo_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19,19))
#Continuosly
while True:
	_, img = cap.read() #Read the capture
	#Convert to HSV Colorspace
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#Threshold HSV Colorspace (Only allow yellow ball color)
	hsv_frame = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
	#Open to eliminate noise
	hsv_frame = cv2.erode(hsv_frame, anti_noise_kernel, iterations = 2)
	hsv_frame = cv2.dilate(hsv_frame, anti_noise_kernel, iterations = 2)
	#Close to fill in the logo
	hsv_frame = cv2.dilate(hsv_frame, anti_logo_kernel)
	hsv_frame = cv2.erode(hsv_frame, anti_logo_kernel)
	#Watershed image segmentation
