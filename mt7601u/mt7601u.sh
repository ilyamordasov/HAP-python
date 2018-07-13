#!/bin/bash
# Root-Check
if [ "$UID" != "0" ]
then
echo "Please execute Script with Root-Rights!"
exit
else
# Go to the USER-Directory
cd ~
# Download the Tarball for your Kernel from the Dropbox!
#wget $(echo "https://dl.dropboxusercontent.com/u/80256631/mt7601-"`uname -r | awk '{sub(/\+/,"")}{print}'`"-"`uname -v | awk '{sub (/#/,"")} {print $1}'`).tar.gz
# Extract the Tarball
#tar -xzf $(echo mt7601-`uname -r | awk '{sub(/\+/,"")}{print}'`"-"`uname -v | awk '{sub (/#/,"")}{print $1}'`).tar.gz
# Start Install-Script
#./install.sh
# Disable Power-Safe-Mode for the Wifi-Chip(Create Config-File)
echo "options rt2870 rtw_power_mgnt=0 rtw_enusbss=0" #> /etc/modprobe.d/rt2870.conf
# Write WLAN Config
echo "WRITE WLAN-CONFIGURATION!"
read -p "Insert SSID(WLAN-Network Name)! " ssid
read -p "Insert WLAN-Password! " password
echo -e "auto lo\niface lo inet loopback\n\nauto eth0\nallow-hotplug eth0\niface eth0 inet manual\n\nauto wlan0\nallow-hotplug wlan0\niface wlan0 inet manual\nwpa-ap-scan 1\nwpa-scan-ssid 1\nwpa-ssid \"$ssid\"\nwpa-psk \"$password\"" #> /etc/network/interfaces
fi
exit