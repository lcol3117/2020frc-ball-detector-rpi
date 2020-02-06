# frc2020-raspberry-sees-lemon
detect power cells on raspberry pi 4

***RASPBERRY SEES LEMON***

For the FRCVision RPi image, please use the forFRCVision%.py
such that % is the version number

*FRCVision is available at wpilibsuite/FRCVision-pi-gen*

**NOTE OF WARNING:
The non-frcvision versions may not be up-to-date USE THEM WITH CAUTION**

# Instalation Instructions:

**1** Connect to install libs

Connect everything over ethernet as shown below:

( SWITCH )<---POWER

^^^

| | |----INTERNET (ETHERNET ON ROUTER)

| |

| |--------RASPBERRY PI 4

|

|------------COMPUTER

**2** SSH into Pi

-Windows: Download PuTTY, Open PuTTY, *frcvision.local* ENTER, log in as *pi*, password is *raspberry*
-UNIX (Mac/Linux): Open Terminal, *ssh pi@frcvision.local* ENTER, password is *raspberry*

**3** Install Libs

-right-click to paste the contents of **setup_rpi_libs.sh** into the CLI and press enter

NOTE: Type Y when prompted

**4** Test libs

-test the libs by:

* typing *python3* and pressing enter
* pasting or retyping the contents of **imports_test.py**
- typing *exit()*
- If any errors occured, open an issue on this repo
   
**5** Shutdown Pi

-type *sudo shutdown -h now* and press enter

-*wait for the green light on the back of the pi to stop blinking (~7 secs)*

**6** Reconnect to upload code

Unplug everything and reconnect everything as shown below:

COMPUTER<-------------->RPI<------------->MS LIFECAM HD-3000
            ETHERNET             USB

**7** Upload code

Power on the pi. 
Now, open a new tab in Firefox at **http://frcvision.local**
Upload the **forFRCVision6.py** file in the applications tab after clicking writeable and selecting *uploaded python file*
Navigate to **http://frcvision.local:1182** to see vision


# ADDITIONAL NOTES

DATA IS SENT OVER NETWORKTABLES; IT IS ABOUT THE LARGEST DETECTED POWER CELL:

pi_tx = x-coord (/160)
pi_ty = y-coord (/120)
pi_ta = corresponds to area of target

The table is called *FRCVisionpc*
