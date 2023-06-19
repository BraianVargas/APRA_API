import mysql.connector
import json
from flask import jsonify, current_app, g

def getDB():
    if 'db' not in g:
        g.db = mysql.connector.connect( 
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


def proccessData(his_mont):
    db, g= getDB()

    cursor = db.cursor()
    sql = f"SELECT * FROM datos_{str(his_mont)}"
    abnReq = f"SELECT ABN FROM datos_{str(his_mont)}"
    
    cursor.execute(abnReq)
    abnRes = cursor.fetchall()

    cursor.execute(sql)
    data = cursor.fetchall()
    
    def addElement(i):
        elements = []
        for element in data:
            if element[2] == abnList[i][0]:
                elements.append(element)
            else:
                pass
        return elements
    abnList = []
    [abnList.append(x) for x in abnRes if x not in abnList]

    proccessedData = {
        "__values__":[
            {
                "ABN" : abnList[i][0],
                "__data__" : addElement(i) 
            } for i in range(len(abnList))
        ]
    }

    return proccessedData
