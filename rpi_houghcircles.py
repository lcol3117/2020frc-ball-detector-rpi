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
edt_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
circle_improvement_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
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
	#EDT image segmentation
	edt_frame = cv2.distanceTransform(hsv_frame, cv2.DIST_L2, 5)
	edt_frame = cv2.erode(edt_frame, edt_kernel)
	edt_frame = cv2.dilate(edt_frame, circle_improvement_kernel)
	#Hough Circle Detection
	circles_out = cv2.HoughCircles(edt_frame, cv2.HOUGH_GRADIENT, 1.2, 40)
	#Find largest circle if circles exist
	if circles_out is not None:
		circles = np.round(circles[0, :]).astype("int")
		largest_center = [0,0]
		largest_radius = 0
		for (x, y, r) in circles:
			if r >= largest_radius:
				largest_center[0], largest_center[1], largest_radius = x, y, r
	try:
		print(str(largest_center))
	except:
		pass
