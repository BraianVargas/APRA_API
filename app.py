from flask import Flask, jsonify
from controllers. mainController import *

app = Flask(__name__)
app.config.from_pyfile("./data/config.py")

@app.route('/historical')
def getHistorical():
    return proccessData("historical")

@app.route('/monthly')
def getMonthly():
    return proccessData("monthly")

@app.route('/etl')
def loadEtl():
    return loadDatabase()


if __name__ == '__main__':
    app.run()
