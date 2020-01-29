import numpy as np
from time import time
import json
import sys
from PIL import Image
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from networktables import NetworkTablesInstance
import cv2

#Define HSV Thresholds
lower_hsv = np.array([20,10,10])
upper_hsv = np.array([95,100,100])
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
    ta_entry= ntinst.getTable("FRcVisionpc").getEntry("pi_ta")

    print("Starting camera server")
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(WIDTH, HEIGHT)
    cvSink = cs.getVideo()
    img = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    output = cs.putVideo("MLOut", WIDTH, HEIGHT)
    
    while True: 
        _, frame = cvSink.grabFrame(img)
        #vision code
        lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        print(lab_frame[80,60])
        #Threshold HSV Colorspace (Only allow yellow ball color)
        lab_frame_origt = cv2.inRange(lab_frame, lower_lab, upper_lab)
        #Open to eliminate noise
        hsv_frame = cv2.erode(lab_frame_origt, anti_noise_kernel)
        hsv_frame = cv2.dilate(hsv_frame, anti_noise_kernel)
        #Close to fill in the logo
        hsv_frame = cv2.dilate(hsv_frame, anti_logo_kernel)
        hsv_frame = cv2.erode(hsv_frame, anti_logo_kernel)
        #EDT image segmentation
        #edt_frame = cv2.distanceTransform(hsv_frame, cv2.DIST_L2, 5)
        #edt_frame = cv2.inRange(edt_frame, 8, 255)
        #edt_frame = cv2.erode(edt_frame, edt_kernel)
        #edt_frame = cv2.dilate(edt_frame, circle_improvement_kernel)
        #Hough Circle Detection
        circles_out = cv2.HoughCircles(hsv_frame, cv2.HOUGH_GRADIENT, 1.2, 40)
        #Find largest circle if circles exist
        if circles_out is not None:
            circles = np.round(circles[0, :]).astype("int")
            largest_center = [0,0]
            largest_radius = 0
            for (x, y, r) in circles:
                if r >= largest_radius:
                    largest_center[0], largest_center[1], largest_radius = x, y, r
            print(str(largest_center))
            tx_entry.setDouble(largest_center[0])
            ty_entry.setDouble(largest_center[1])
            ta_entry.setDouble(largest_radius)
        else:
            print("No Power Cells in this galaxy!")
            tx_entry.setDouble(-1)
            ty_entry.setDouble(-1)
            ta_entry.setDouble(-1)
        try: 
            print("FPS: {:.1f}".format(1 / (time() - start)))
        except:
            print("Unable to fetch FPS. (But that was our only hope!)")
        start = time()
        output.putFrame(lab_frame_origt)


if __name__ == '__main__':
    config_file = "/boot/frc.json"
    main(config_file)
