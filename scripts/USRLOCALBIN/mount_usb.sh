#! /bin/bash

ACTION=$1
DEVBASE=$2
DEVICE="/dev/${DEVBASE}"

echo '${DEVICE}'

sudo mkdir /media/pi/6061-6154
sudo mount ${DEVICE} /media/pi/6061-6154
