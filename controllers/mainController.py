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

    abn_req = f"SELECT DISTINCT ABN FROM datos_{str(his_mont)} LIMIT 150"
    sql_col_names = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'datos_{his_mont}'"

    cursor.execute(abn_req)
    abn_res = cursor.fetchall()

    abn_list = list(set([x[0] for x in abn_res])) # Remove duplicates from ABN list

    placeholders = ', '.join(['%s'] * len(abn_list))
    sql = f"SELECT * FROM datos_{str(his_mont)} WHERE ABN IN ({placeholders})"
    
    cursor.execute(sql, abn_list)
    data = cursor.fetchall()

    cursor.execute(sql_col_names)
    req_col_names = [col[0] for col in cursor.fetchall()]

    def get_column_names():
        path = f"./data/glosario_{his_mont}.json"

        with open(path) as json_file:
            file_data_json = json.load(json_file)

        column_names = [file_data_json.get(col, col).lower() for col in req_col_names]
        return column_names

    col_names = get_column_names()  # Get column names outside the loop

    # Convert data to a dictionary for faster lookup
    data_dict = {}
    for element in data:
        abn = element[2]
        if abn not in data_dict:
            data_dict[abn] = []
        data_dict[abn].append({col_names[i]: element[i] for i in range(len(element))})

    processed_data = {
        "__values__": [
            {"ABN": abn, "__data__": data_dict[abn]} for abn in abn_list
        ]
    }

    return processed_data

