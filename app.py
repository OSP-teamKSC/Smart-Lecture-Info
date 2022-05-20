from flask import Flask, render_template, redirect, request, url_for
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/request', methods=['GET', 'POST'])
def test():
    if request.form.to_dict():
        data = request.form.to_dict()
        print(data['data'])
    a = {"1": "2"}
    return a

@app.route('/', methods=['GET', 'POST'])
def list():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)