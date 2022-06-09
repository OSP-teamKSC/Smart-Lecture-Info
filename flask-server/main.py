import sys
import json
from flask import (Flask, render_template, request)
from flask_cors import CORS

import getUniv
import knuBus
import Init
# from crawler import crawlAndInsert

DBPW = sys.argv[1]

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
        isGE = True if search['Gubun'] == 'GE' else False
        print(search)
        data = knuBus.accessDataBase(search, DBPW)
        json_data = json.dumps(data)
    # return
    return json_data


if __name__ == "__main__":
    Init.init()
    # for season in range(0,4):
        # crawlAndInsert(2022, search['Season'], True, DBPW)
        # crawlAndInsert(2022, search['Season'], False, DBPW)
    app.run(host="0.0.0.0", port="8080", debug=True)