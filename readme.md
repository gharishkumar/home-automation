# Home Automation
This project is on PIR detection, capturing and sending a photo via mail and face authentication included. Initially decided to include telegram but it turned out to be not that good. So, ~telegram~. Follow the below instructions to install.

## Installation
 - [Install RaspberryPi OS](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
 - Make sure the internet is connected
 - Clone git repository
```bash
gh repo clone gharishkumar/home-automation
```
   **or**
 - Download the zip from the repository and unzip
```bash
wget https://github.com/gharishkumar/home-automation/archive/min.zip
unzip min.zip
cd home-automation-min
```
 - Install required packages by
```bash
 sudo sh install.sh
```

## Setup
 - Capture clear image of 3 persons
```bash
 python3 capture_image.py
```
**or**
 - Add images of 3 persons as `Person1_IMG.jpg` `Person2_IMG.jpg` `Person3_IMG.jpg` to `home-automation-min` folder
 - Open `homeautomation_final.py`
```bash
 nano homeautomation_final.py
```
**or**
 - Open and edit in [Thonny python IDE](https://thonny.org/)
 - Change the `names` accordingly

 - Change the `mail adderss`
 Make sure to turn on [Less secure app access](https://myaccount.google.com/u/0/lesssecureapps) in case of [gmail](https://mail.google.com/mail/u/0/)
 You may need to dissable [2-Step Verification](https://myaccount.google.com/u/0/signinoptions/two-step-verification)

 - Connect the `circuit` as shown
![Image](https://github.com/gharishkumar/home-automation/raw/main/homeautomation_bb.png)
 - Run `homeautomation_final.py`
```bash
 python3 homeautomation_final.py
```
## Run at startup
 - ~~Add `homeautomation_final.py` to [*startup*](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)~~
 - Included with the `install.sh` script

