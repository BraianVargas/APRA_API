from flask import Flask, jsonify
from controllers.mainController import *
from controllers.etlController import *

app = Flask(__name__)
app.config.from_pyfile("./data/config.py")

@app.route('/historical')
def getHistorical():
    return process_data("historicos")

@app.route('/monthly')
def getMonthly():
    return process_data("mensuales")

@app.route('/etl')
def loadEtl():
    engine = create_engine('mysql+mysqlconnector://root@localhost/apra_etl', connect_args={'connect_timeout': 120})
    return loadDatabase(engine)

# PRODUCTION
# @app.route('/etl')
# def loadEtl():
#     engine = create_engine('mysql+mysqlconnector://Flowkai@Flowkai.mysql.pythonanywhere-services.com/apra_etl', connect_args={'connect_timeout': 120})
#     return loadDatabase(engine)


if __name__ == '__main__':
    app.run()
