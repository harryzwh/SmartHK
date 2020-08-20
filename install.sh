#!/bin/bash

Add_Env_Var()
{
  if [[ ! $(cat /home/$USER/.profile) =~ $1 ]]; then
    echo "export $1=$2" | tee -a /home/$USER/.profile
  else
    echo "$1 already exists!"
  fi
}

SCRIPT_PATH=$(dirname $(readlink -f "$0"))

Add_Env_Var DB_NAME smart

source /home/$USER/.profile

rm -rf /home/$USER/nodered
mkdir /home/$USER/nodered
cp "$SCRIPT_PATH/flows.json" /home/$USER/nodered

docker-compose up -d

sleep 30

python3 "$SCRIPT_PATH/init.py"

source "$SCRIPT_PATH/esp8266_install.sh"
