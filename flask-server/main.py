from flask import (Flask, render_template, request)
from flask_cors import CORS
import json
import knuBus

app = Flask("__main__")
CORS(app)
@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html" )

# request
@app.route('/request', methods=['GET', 'POST'])
def test():
    # 요청이 오면
    if request.json:
        search = request.json
        # search = json.dump(search)
        print(search)
        data = knuBus.accessDataBase(search)
        json_data = json.dumps(data)
    # return
    return json_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)