#Also Known As:
#Raspberry sees a Lemon

import numpy as np
from time import time
import math
import json
import sys
from PIL import Image
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from networktables import NetworkTablesInstance
import cv2
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import imutils

#Define HSV Thresholds
lower_hsv = np.array([15,60,80])
upper_hsv = np.array([30,255,130])
#Define RGB Thresholds
lower_rgb = np.array([68,154,0])
upper_rgb = np.array([255,255,166])
#Define LAB Thresholds
labt = (55, 100, -128, 13, 22, 127) #LAB BAD
lower_lab = np.array([150,100,170])
upper_lab = np.array([250,150,200])
#Define morphological operation kernels
anti_noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
anti_logo_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
anti_lighting_anomaly_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
marker_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#circle_improvement_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

def parseError(str, config_file):
    print("config error in '" + config_file + "': " + str, file=sys.stderr)


def read_config(config_file):
    team = -1

    # parse file
    try:
        with open(config_file, "rt", encoding="utf-8") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(config_file, err), file=sys.stderr)
        return team

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object", config_file)
        return team

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number", config_file)

    # cameras
    try:
        cameras = j["cameras"]
    except KeyError:
        parseError("could not read cameras", config_file)

    return team


class PBTXTParser:
    def __init__(self, path):
        self.path = path
        self.file = None

    def parse(self):
        with open(self.path, 'r') as f:
            self.file = ''.join([i.replace('item', '') for i in f.readlines()])
            blocks = []
            obj = ""
            for i in self.file:
                if i == '}':
                    obj += i
                    blocks.append(obj)
                    obj = ""
                else:
                    obj += i
            self.file = blocks
            label_map = {}
            for obj in self.file:
                obj = [i for i in obj.split('\n') if i]
                i = int(obj[1].split()[1]) - 1
                name = obj[2].split()[1][1:-1]
                label_map.update({i: name})
            self.file = label_map

    def get_labels(self):
        return self.file


def main(config):
    team = read_config(config)
    WIDTH, HEIGHT = 160, 120

    print("Connecting to Network Tables")
    ntinst = NetworkTablesInstance.getDefault()
    ntinst.startClientTeam(team)

    """Format of these entries found in WPILib documentation."""
    tx_entry= ntinst.getTable("FRCvisionpc").getEntry("pi_tx")
    ty_entry= ntinst.getTable("FRCvisionpc").getEntry("pi_ty")
    ta_entry= ntinst.getTable("FRCVisionpc").getEntry("pi_ta")

    print("Starting camera server")
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(WIDTH, HEIGHT)
    cvSink = cs.getVideo()
    img = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    output = cs.putVideo("MLOut", WIDTH, HEIGHT)
    
    while True: 
        _, frame = cvSink.grabFrame(img)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print(hsv_frame[80,60])
        #Threshold HSV Colorspace (Only allow yellow ball color)
        hsv_frame_origt = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
        #Open to eliminate noise
        hsv_frame = cv2.erode(hsv_frame_origt, anti_noise_kernel)
        hsv_frame = cv2.dilate(hsv_frame, anti_noise_kernel)
        #Close to fill in the logo
        hsv_frame = cv2.dilate(hsv_frame, anti_logo_kernel)
        hsv_frame = cv2.erode(hsv_frame, anti_logo_kernel)
        #Close to fill in shadows/highlights to improve watershed (lighting anomalies segment true units)
        hsv_frame = cv2.dilate(hsv_frame, anti_lighting_anomaly_kernel, iterations = 3)
        imageog = cv2.erode(hsv_frame, anti_lighting_anomaly_kernel, iterations = 3)
        #Erode marker proto image to allow watershed
        imagefm = cv2.erode(imageog, marker_kernel)
        #Convert Colorspace for watershed
        imageo = cv2.cvtColor(imageog, cv2.COLOR_GRAY2BGR)
        #Watershed image segmentation
        shifted = cv2.pyrMeanShiftFiltering(imageo, 21, 51)
        # compute the exact Euclidean distance from every binary
        # pixel to the nearest zero pixel, then find peaks in this
        # distance map
        D = ndimage.distance_transform_edt(imageog)
        Dfm = ndimage.distance_transform_edt(imagefm)
        #calculate mindist
        if cv2.countNonZero(imagefm)>=(120*160)/4:
            idealmindist=40
        else:
            idealmindist=20
        localMax = peak_local_max(Dfm, indices=False, min_distance=idealmindist,
            labels=imagefm)

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
            
            #Get contour area
            area = cv2.contourArea(c)
            #Get enclosing circle
            ((x,y),r) = cv2.minEnclosingCircle(c)
            
            #Only allow circles
            ca_ideally_pi = area/(r**2)
            ca_err = abs(ca_ideally_pi-math.pi)
            print(ca_err)
            if (ca_err > 1.25):
                pass
            else: 
                x, y, r = 0, 0, -1
            #Select the new largest circle
            if r>lgtr:
                lgtx, lgty, lgtr = x, y, r

            cv2.drawMarker(imageo, (int(x), int(y)), (0, 255, 0), markerType=cv2.MARKER_CROSS)
        #Find largest circle if circles exist
        if lgtr != -1:
            print(str([lgtx,lgty,lgtr]))
            tx_entry.setDouble(lgtx)
            ty_entry.setDouble(lgty)
            ta_entry.setDouble(lgtr)
            cv2.drawMarker(imageo, (int(lgtx),int(lgty)), (255, 0, 0), markerType=cv2.MARKER_CROSS)
        else:
            print("No Lemons in this galaxy!")
            tx_entry.setDouble(-1)
            ty_entry.setDouble(-1)
            ta_entry.setDouble(-1)
        try: 
            print("FPS: {:.1f}".format(1 / (time() - start)))
        except:
            print("Unable to fetch FPS. (But that was our only hope!)")
        start = time()
        output.putFrame(imageo)


if __name__ == '__main__':
    config_file = "/boot/frc.json"
    main(config_file)
