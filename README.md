# frc2020-raspberry-sees-lemon

Detect Power Cells using a Raspberry Pi for the 2020 FRC game. Uses the FRCVision image for the Pi.
Tested on Pi 4B, may work on older models but might not run fast enough.

***RASPBERRY SEES LEMON WAS DEVELOPED BY FRC TEAM 117***

For the FRCVision RPi image, please use the forFRCVision<version number>.py file. Currently forFRCVision6.py

*FRCVision is available at wpilibsuite/FRCVision-pi-gen*

# Installation Instructions:

**1** Connect to Pi install libraries:

Connect everything over ethernet as shown below:

SWITCH-------POWER

|

|-------INTERNET (ETHERNET ON ROUTER)

|

|-------RASPBERRY PI

|

|-------COMPUTER

**2** SSH into Raspberry Pi:

**Windows:**

1. Download PuTTY
2. SSH into the Pi, the default hostname is FRCVision.local
3. Default log is username `pi` password is `raspberry`

**UNIX (Mac/Linux):**
1. Open Terminal
2. `ssh pi@frcvision.local`
3. Default log is username `pi` password is `raspberry`

**3** Install Libraries:

1. Copy the contents of **setup_rpi_libs.sh**
2. Paste (right-click) this into the CLI and press enter
3. Type `Y` when prompted

**4** Test libraries:

1. type `python3` and press enter
2. paste or retype the contents of **imports_test.py**
3. type `exit()` or press CTRL+D
4. If any errors occured, open an issue on this repo
   
**5** Shutdown Raspberry Pi:

1. type `sudo shutdown -h now` and press enter
2. *wait for the green light on the back of the pi to stop blinking (~7 secs)*

**6** Reconnect Pi to upload code:

Unplug everything and reconnect everything as shown below:

COMPUTER<-------------->RPI<------------->USB WEBCAM
            ETHERNET             USB

**7** Upload code to the Pi:

1. Power on the pi. 
2. Now, open a new tab in Firefox at **http://frcvision.local**
3. Upload the **forFRCVision6.py** file in the applications tab after clicking writeable and selecting *uploaded python file*
4. Navigate to **http://frcvision.local:1182** to see vision


# ADDITIONAL NOTES

DATA IS SENT OVER **NETWORKTABLES**; IT IS ABOUT THE *LARGEST DETECTED POWER CELL*:

* pi_tx = x-coord (/160)
* pi_ty = y-coord (/120)
* pi_ta = corresponds to area of target

The table is called *FRCVisionpc*
