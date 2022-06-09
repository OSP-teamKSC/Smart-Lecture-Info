#!/bin/sh

# 1q2w3e4r@@
read -p "Enter the DataBase Password: " DBPW
#run flask
python flask-server/main.py $DBPW
