from flask import (Flask, render_template)

app = Flask("__main__")

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html", flask_token="Hello world")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)