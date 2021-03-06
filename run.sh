#!/bin/sh

# 1q2w3e4r@@
sudo apt-get -y update

if which python3 > /dev/null;then
        echo "python3 already installed"
    else
        sudo apt install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

sudo apt-get install mysql-server

#run flask
python3 flask-server/main.py
