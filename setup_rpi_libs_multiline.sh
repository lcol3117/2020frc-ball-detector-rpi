#!/bin/bash
sudo mount -o remount, rw /
sudo apt-get uninstall python
sudo apt-get uninstall python3
sudo apt-get uninstall python-numpy
sudo apt-get uninstall python3-numpy
sudo apt-get uninstall python-pip
sudo apt-get uninstall python3-pip
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install scikit-image
sudo pip3 install opencv
sudo pip3 install imutils
sudo pip3 install pillow
