import numpy as np
from time import time
import json
import sys
from PIL import Image
import cv2
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import imutils

#Define HSV Thresholds
lower_hsv = np.array([20,56,63])
upper_hsv = np.array([75,255,255])
#Define RGB Thresholds
lower_rgb = np.array([68,154,0])
upper_rgb = np.array([255,255,166])
#Define LAB Thresholds
labt = (55, 100, -128, 13, 22, 127) #LAB BAD
lower_lab = np.array([150,100,170])
upper_lab = np.array([250,150,200])
#Define morphological operation kernels
anti_noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
anti_logo_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19,19))
edt_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
circle_improvement_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
from imutils.video import VideoStream
#Initiate capture
cap = cv2.VideoCapture(0)
while True:
        #vision code
        _, frame = cap.read() #Read the capture
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print(hsv_frame[80,60])
        #Threshold HSV Colorspace (Only allow yellow ball color)
        hsv_frame_origt = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
        #Open to eliminate noise
        hsv_frame = cv2.erode(hsv_frame_origt, anti_noise_kernel, iterations = 5)
        hsv_frame = cv2.dilate(hsv_frame, anti_noise_kernel, iterations = 5)
        #Close to fill in the logo
        hsv_frame = cv2.dilate(hsv_frame, anti_logo_kernel)
        imageog = cv2.erode(hsv_frame, anti_logo_kernel)
        cv2.imshow("Thresh",imageog)
        imageo = cv2.cvtColor(imageog, cv2.COLOR_GRAY2BGR)
        #Watershed image segmentation
        shifted = cv2.pyrMeanShiftFiltering(imageo, 21, 51)
        # compute the exact Euclidean distance from every binary
        # pixel to the nearest zero pixel, then find peaks in this
        # distance map
        D = ndimage.distance_transform_edt(imageog)
        localMax = peak_local_max(D, indices=False, min_distance=20,
            labels=imageog)

        # perform a connected component analysis on the local peaks,
        # using 8-connectivity, then appy the Watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=imageog)
        print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
        
        # allocate ram for the largest circle values
        lgtx, lgty, lgtr = -1, -1, -1

        # loop over the unique labels returned by the Watershed
        # algorithm
        for label in np.unique(labels):
            # if the label is zero, we are examining the 'background'
            # so simply ignore it
            if label == 0:
                continue

            # otherwise, allocate memory for the label region and draw
            # it on the mask
            mask = np.zeros(imageog.shape, dtype="uint8")
            mask[labels == label] = 255

            # detect contours in the mask and grab the largest one
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            c = max(cnts, key=cv2.contourArea)

            # draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            #Select the new largest circle
            if r>lgtr:
                lgtx, lgty, lgtr = x, y, r

            cv2.circle(imageo, (int(x), int(y)), int(r), (0, 255, 0), 2)
            cv2.putText(imageo, "#{}".format(label), (int(x) - 10, int(y)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            #Find largest circle if circles exist
            if lgtr != -1:
                print(str([lgtx,lgty,lgtr]))
            else:
                print("No Power Cells in this galaxy!")
            try: 
                print("FPS: {:.1f}".format(1 / (time() - start)))
            except:
                print("Unable to fetch FPS. (But that was our only hope!)")
            start = time()


