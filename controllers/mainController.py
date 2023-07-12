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
import json

def process_data(his_mont):
    db, g = getDB()

    cursor = db.cursor()

    abn = f"SELECT * FROM datos_{str(his_mont)} "
    abn_req = f"SELECT DISTINCT ABN FROM datos_{str(his_mont)} "
    sql_col_names = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'datos_{his_mont}'"
    
    cursor.execute(abn)
    data = cursor.fetchall()
    
    cursor.execute(abn_req)
    abns = cursor.fetchall()

    cursor.execute(sql_col_names)
    columns = [col[0] for col in cursor.fetchall()]

    def addElement(abn):
        elements = []
        for x in data:
            if abn in x:
                elements.append(
                    {
                        columns[i] : x[i] for i in range(len(columns))
                    } 
                )
        return elements

    processed_data = {
        "__values__" : [
            {
                "ABN": abn[0],
                "__data__" : addElement(abn[0])
            } for abn in abns
        ]
    }

    return processed_data