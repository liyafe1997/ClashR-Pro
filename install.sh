#!/bin/bash

mkdir -p ~/.config/clash

sudo mkdir -p /opt/ClashR_Pro/clashr

sudo cp ./clashr.png /opt/ClashR_Pro/logo.png
sudo cp ./clashr-linux-amd64 /opt/ClashR_Pro/clashr/clashr-linux-amd64
sudo cp ./main.py /opt/ClashR_Pro/ClashrPro
sudo cp -r ./zenipy /opt/ClashR_Pro/zenipy
sudo cp ./config.py /opt/ClashR_Pro/config.py
sudo cp ./ClashR\ Pro.desktop /usr/share/applications/ClashR\ Pro.desktop

sudo chmod +x /opt/ClashR_Pro/ClashrPro
sudo chmod +x /opt/ClashR_Pro/clashr/clashr-linux-amd64

echo "success"
