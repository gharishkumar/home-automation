#!/bin/bash
sudo apt update
sudo apt install -y python3-opencv  cmake libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test 
sudo pip3 --no-cache-dir install face-recognition keyboard python-telegram-bot
cd $1
sudo chmod +x run.sh
sudo crontab crontab.txt
