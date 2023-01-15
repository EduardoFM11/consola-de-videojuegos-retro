#! /bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install mednafen wmctrl xdotool mplayer qjoypad xserver-xorg-input-joystick -y
pip install pyudev
pip install tk
