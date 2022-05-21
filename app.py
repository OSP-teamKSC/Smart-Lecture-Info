from flask import Flask, render_template, redirect, request, url_for
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# request
@app.route('/request', methods=['GET', 'POST'])
def test():
    # 요청이 오면
    if request.form.to_dict():
        data = request.form.to_dict()
        print(data['data'])
    a = {"1": "2"}
    # a를 json으로 return
    return a

# main page
@app.route('/', methods=['GET', 'POST'])
def list():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)