from flask import Flask, jsonify
from controllers. mainController import *

app = Flask(__name__)


@app.route('/historical')
def getHistorical():
    return proccessData("historical")

@app.route('/monthly')
def getMonthly():
    return proccessData("monthly")


if __name__ == '__main__':
    app.run()
