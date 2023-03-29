import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/datos_historicos')
def obtener_datos_historicos():
    # Establecer la conexión con la base de datos
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="apra_etl"
    )

    # Crear un cursor para ejecutar las consultas
    mycursor = mydb.cursor()

    # Definir el número de registros por página
    page_size = 500

    # Definir la consulta SQL
    sql = "SELECT * FROM datos_historicos"

    # Obtener el número total de registros
    mycursor.execute("SELECT COUNT(*) FROM datos_historicos")
    result = mycursor.fetchone()
    total_records = result[0]

    # Calcular el número total de páginas
    total_pages = (total_records // page_size) + 1

    # Recuperar los registros de cada página
    datos_historicos = []
    for page in range(total_pages):
        offset = page * page_size
        query = f"{sql} LIMIT {page_size} OFFSET {offset}"
        mycursor.execute(query)
        results = mycursor.fetchall()
        if page == 0:  # Incluye los nombres de las columnas en la primera página
            column_names = [i[0] for i in mycursor.description]
        for row in results:
            datos_historicos.append(dict(zip(column_names, row)))


    # Cerrar la conexión con la base de datos
    mydb.close()

    # Devolver los resultados como una respuesta JSON
    return jsonify(datos_historicos)









if __name__ == '__main__':
    app.run()
