import sys
import json
from flask import (Flask, render_template, request)
from flask_cors import CORS

import getUniv
import knuBus
import Init

DBPW = "1q2w3e4r@@"

app = Flask("__main__")
CORS(app)

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/UnivList', methods=['GET', 'POST'])
def getuniv():
    # 요청이 오면
    if request.json:
        search = request.json
        year = 2022
        season = search['season']
        json_data = getUniv.getMajor(year, season)
        json_data = json.dumps(json_data)
    # return
    return json_data

# request
@app.route('/request', methods=['GET', 'POST'])
def test():
    # 요청이 오면
    if request.json:
        search = request.json
        # search = json.dump(search)
        print(search)
        data = knuBus.accessDataBase(search, DBPW)
        json_data = json.dumps(data)
    # return
    return json_data


if __name__ == "__main__":
    Init.init(DBPW)
    app.run(host="0.0.0.0")