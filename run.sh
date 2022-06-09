#!/bin/sh

# 1q2w3e4r@@
sudo apt-get -y update

sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

sudo apt-get install mysql-server

read -p "Enter the DataBase Password: " DBPW
#run flask
python3 flask-server/main.py $DBPW
