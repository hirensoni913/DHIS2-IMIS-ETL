import json
import os
from dotenv import load_dotenv
import pyodbc


load_dotenv()

connection_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={};DATABASE={};UID={};PWD={}'.format(
    os.getenv("SERVER"),
    os.getenv("DATABASE"),
    os.getenv("DBUSERNAME"),
    os.getenv("DBPASSWORD"))

connection = pyodbc.connect(connection_string)

cursor = connection.cursor()


def execute_query(query):
    cursor.execute(query)
    data = [{c[0]: v for (c, v) in zip(row.cursor_description, row)}
            for row in cursor.fetchall()]

    return data
