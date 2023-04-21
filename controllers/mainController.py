import mysql.connector
import json
from flask import jsonify, current_app, g

def getDB():
    if 'db' not in g:
        g.db=mysql.connector.connect( 
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c



def proccessData(type):
    db, g= getDB()
    # Crear un cursor para ejecutar las consultas
    mycursor = db.cursor()
    
    # Definir la consulta SQL
    if type== "historical":
        sql = "SELECT * FROM datos_historicos"
    else:
        sql = "SELECT * FROM datos_mensuales"
    mycursor.execute(sql)
    result= mycursor.fetchall()

    # Obtener los nombres de las columnas
    column_names = [desc[0] for desc in mycursor.description]

    # Crear una lista para almacenar los objetos JSON de cada fila de datos
    json_list = []

    # Leer el archivo JSON
    with open(f"./data/glosary_{type}.json", "r") as file:
        data = json.load(file)

    # Iterar sobre los resultados y agregar cada fila de datos a la lista
    for row in result:
        # Crear un diccionario para almacenar los datos de esta fila
        data_dict = {}
        # Iterar sobre las columnas y agregar los valores al diccionario
        for i, col_name in enumerate(column_names):
            data_dict[data[col_name]] = row[i]
        # Agregar el diccionario a la lista de objetos JSON
        json_list.append(data_dict)
    # Devolver la lista de objetos JSON en formato JSON
    return jsonify(json_list)


def loadDatabase():
    pass