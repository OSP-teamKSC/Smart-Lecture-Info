#!/bin/sh

# 1q2w3e4r@@
sudo apt-get update

sudo apt install python3
sudo apt install build-essential python3-pip libffi-dev python3-dev python3-setuptools libssl-dev -y
sudo apt install python3-venv -y

python3 -m venv venv
source venv/bin/activate

sudo apt-get install mysql-server

pip install -r requirements.txt

read -p "Enter the DataBase Password: " DBPW
#run flask
python3 flask-server/main.py $DBPW
