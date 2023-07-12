import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import mysql.connector
from sqlalchemy import create_engine



def abrev(text):
    words = text.split()
    abbreviation = '_'.join(words).lower().replace(':', '').replace('-', '_')
    truncated_abbreviation = abbreviation[:64]
    return truncated_abbreviation


def separate(text):
    words = text.split()
    print(words)
    if '-' in words[:-1]:
        print(True)
        i = words.index('-')
        splited = words[i].split('-')
        words = words[:i] + splited + words[i+1:]
    abbreviation = '_'.join(words).upper()

    input()
    
    return abbreviation

def fromURLtoDB():
    url = "https://www.apra.gov.au/monthly-authorised-deposit-taking-institution-statistics"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    excel_links = []

    for link in soup.find_all("a"):
        href = link.get("href")

        if href and href.endswith(".xlsx"):
            excel_links.append(href)
        else:
            pass

    # Creamos las carpetas si no existen
    if not os.path.exists("./data/historical"):
        os.makedirs("./data/historical")
    if not os.path.exists("./data/monthly"):
        os.makedirs("./data/monthly")

    # Descargamos los archivos y los guardamos en las carpetas correspondientes

    for i, link in enumerate(excel_links):
        response = requests.get(link)
        filename = link.split("/")[-1].replace("%20","_")
        print(filename)
        if i == 1:
            path = os.path.join("./data/monthly", filename)
        elif i == 2:
            path = os.path.join("./data/historical", filename)
        else:
            continue
        with open(path, "wb") as f:
            f.write(response.content)

def getDB():
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "apra_etl",
            connect_timeout = 60
        )
        c = db.cursor(dictionary=True)
        return db, c

def loadHistorical(engine):
    folder = "./data/historical/"
    files = os.listdir(folder)
    files = [f for f in files]

    filename = files[0]
    historical_df = pd.read_excel(os.path.join(folder,filename), sheet_name='Table 1')

    columns = historical_df.columns

    i = 0
    for col in columns:
        if len(col.split()) > 1:
            # Generate an abbreviation for the column name
            abbr = abrev(col)
            if abbr in historical_df.columns:
                i += 1
                abbr += f"_{i}"
            else:
                # Update the DataFrame with the abbreviated column name
                historical_df.rename(columns={col: abbr}, inplace=True)

    db, c = getDB()


    try:
        historical_df.to_sql('datos_historicos', con=engine, if_exists='replace', chunksize=1000)
    except Exception as e:
        print(e)


def loadMonthly(engine):
    folder = "./data/monthly/"
    files = os.listdir(folder)
    files = [f for f in files]

    filename = files[0]
    df = pd.read_excel(os.path.join(folder,filename), sheet_name='Table 1', skiprows=1)
    columns = df.columns


    i = 0
    for col in columns:
        if len(col.split()) > 1:
            # Generate an abbreviation for the column name
            abbr = abrev(col)
            if abbr in df.columns:
                i += 1
                abbr += f"_{i}"
                df.rename(columns={col: abbr}, inplace=True)
            else:
                # Update the DataFrame with the abbreviated column name
                df.rename(columns={col: abbr}, inplace=True)
    try:
        df.to_sql('datos_mensuales', con=engine, if_exists='replace', chunksize=1000)
    except Exception as e:
        print(e)

def loadDatabase(engine):
    # fromURLtoDB()
    loadHistorical(engine)
    loadMonthly(engine)
    return "SUCCESS"
