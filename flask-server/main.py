from flask import (Flask, jsonify, render_template, request)
import json
from flask_cors import CORS
import knuBus
app = Flask("__main__")
CORS(app)

@app.route("/request", methods = ['GET', 'POST'])
def react_to_flask():
    if request.method == "POST":
        parsed_request = request.form.get('data')
        print(parsed_request)
        result = knuBus.accessDataBase()


    return result


@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html", flask_token="Hello world")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)