from flask import Flask, redirect, url_for, request
from chat import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return "WElcome to Chaat"


@app.route("/getresponse", methods=["POST"])
def getResponse():
    msg = request.form['msg']
    return get_response(msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

##".\flasktest.py"cls
