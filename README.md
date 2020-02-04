# frc2020-raspberry-sees-lemon
detect power cells on raspberry pi 4

RASPBERRY SEES A LEMON

For the FRCVision RPi image, please use the forFRCVision%.py
such that % is the version number

FRCVision is available at wpilibsuite/FRCVision-pi-gen

NOTE OF WARNING:
The non-frcvision versions may not be up-to-date USE THEM WITH CAUTION

Instalation Instructions
Connect everything over ethernet as shown below:

( SWITCH )<---POWER

^   ^   ^

|...|...|----INTERNET (ETHERNET ON ROUTER)

|...|

|...|--------RASPBERRY PI 4

|

|------------COMPUTER*

-Windows: Download PuTTY, Open PuTTY, *frcvision.local* ENTER, log in as *pi*, password is *raspberry*
-UNIX (Mac/Linux): Open Terminal, *ssh pi@frcvision.local* ENTER, password is *raspberry*

-right-click to paste the contents of **setup_rpi_libs.sh** into the CLI and press enter
-test the libs by
   -typing *python3* and pressing enter
   -pasting or retyping the contents of **imports_test.py**
   -typing *exit()*
   -If any errors occured, open an issue on this repo
-type *sudo shutdown -h now* and press enter
-wait for the green light on the back of the pi to stop blinking (~7 secs)

Unplug everything and reconnect everything as shown below:

COMPUTER<-------------->RPI<------------->MS LIFECAM HD-3000
            ETHERNET             USB

Power on the pi. 
Now, open a new tab in Firefox at **http://frcvision.local**
Upload the **forFRCVision6.py** file in the applications tab after clicking writeable and selecting *uploaded python file*
Navigate to **http://frcvision.local:1182** to see vision
