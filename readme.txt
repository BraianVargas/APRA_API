Procedimiento para ejecución del sistema en localhost.

*Entorno Windows*
1. Ingresar por consola al directorio del proyecto y crear entorno virtual con "virtualenv .venv" siendo ".venv" el directorio del entorno virtual.
2. Escribir y ejecutar el comando "cd .venv/scripts". Una vez dentro del directorio ejecutar "activate"
3. Ejecutar "pip install -r requeriments.txt" 
4. Volver al directorio raiz del proyecto.
5. Ejecutar el comando "flask --debug run"
6. Asegurarse de tener una DDBB creada en local con el nombre "apra_etl" (respetar minusculas).
7. Ingresar a "localhost:5000/etl" este endpoint cargará los datos en la DDBB.
8. Ingresar a los distintos endpoint para lo que se requiera. "localhost:5000/monthly" para los datos mensuales y "localhost:5000/historical" para los datos historicos.