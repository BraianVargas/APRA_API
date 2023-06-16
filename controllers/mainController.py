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
    print(data[0])


    abnList = []
    [abnList.append(x) for x in abnRes if x not in abnList]

    proccessedData = {
        "__values__":[
            {
                "ABN" : abnList[i][0],
                "__data__" : [
                    { element } if element[2] == abnList[i][0] else "" for element in data 
                ]
            } for i in range(len(abnList))
        ]
    }

    return f"""
            abnList: {len(abnList)} \n
            result: {len(abnRes)} \n
            DATA: \n { proccessedData }
            """