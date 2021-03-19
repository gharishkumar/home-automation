#!/bin/bash
sudo apt update
sudo apt install -y python3-opencv  cmake libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test 
sudo pip3 --no-cache-dir install face-recognition keyboard python-telegram-bot
sudo chmod +x $1/run.sh
cd $1
sudo crontab crontab.txt
