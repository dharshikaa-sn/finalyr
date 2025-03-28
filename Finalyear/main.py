from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()


def database_connection():
    connection = mysql.connector.connect(
        host=os.getenv('mysql_host'),
        port=os.getenv('mysql_port'),
        user=os.getenv('mysql_user'),
        password=os.getenv('mysql_password'),
        database=os.getenv('mysql_database')

    )
    return connection