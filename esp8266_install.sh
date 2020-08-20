#!/bin/bash

sudo apt install -y build-essential cmake libncurses-dev flex bison gperf python python-serial python-pip

wget https://github.com/harryzwh/xtensa-lx106-elf-RPi/releases/download/v1.22.0-97/xtensa-lx106-elf-arm64-1.22.0-97-gca13a260-5.2.0.tar.gz -O ~/xtensa-lx106-elf.tar.gz
sudo tar -zxvf ~/xtensa-lx106-elf.tar.gz -C /usr/local/
echo 'export PATH="$PATH:/usr/local/xtensa-lx106-elf/bin"' | tee -a /home/$USER/.profile

sudo usermod -a -G dialout $USER

cd ~
#git clone --depth=1  --recursive https://github.com/espressif/ESP8266_RTOS_SDK.git
wget https://github.com/espressif/ESP8266_RTOS_SDK/releases/download/v3.3/ESP8266_RTOS_SDK-v3.3.zip -O ~/ESP8266_RTOS_SDK.zip
unzip ~/ESP8266_RTOS_SDK.zip
echo "export IDF_PATH=\"/home/$USER/ESP8266_RTOS_SDK\"" | tee -a /home/$USER/.profile
source /home/$USER/.profile

python -m pip install --user -r $IDF_PATH/requirements.txt
