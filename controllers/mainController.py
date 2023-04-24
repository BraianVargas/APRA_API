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



def proccessData(type):
    db, g= getDB()

    mycursor = db.cursor()
    
    sql = f"SELECT * FROM datos_{str(type)}"

    mycursor.execute(sql)
    result= mycursor.fetchall()

    column_names = [desc[0] for desc in mycursor.description]

    json_list = []

    with open(f"./data/glosario_{type}.json", "r") as file:
        data = json.load(file)

    for row in result:
        data_dict = {}
        for i, col_name in enumerate(column_names):
            data_dict[data[col_name]] = row[i]
        json_list.append(data_dict)
    return jsonify(json_list)
