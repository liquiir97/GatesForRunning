import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
import os

load_dotenv()

def connect_to_database():

    db_host = os.getenv("database_host")
    db_port = os.getenv("database_port")
    db_user = os.getenv("database_user")
    db_pass = os.getenv("database_pass")
    database = 'footballanalytics'
    try:
        databse_connection = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=database)

        if databse_connection.is_connected():
            print("Successfully connected to the database.")
            return databse_connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    return None

def close_database_connection(database_connection):
    if database_connection and database_connection.is_connected():
        database_connection.close()
        print("Connection closed.")
    else:
        print("No connection to close.")

def create_cursor(database_connection):
    if database_connection and database_connection.is_connected():
        try:
            cursor = database_connection.cursor()
            print("Cursor created.")
            return cursor
        except Error as e:
            print(f"Error creating cursor: {e}")
            return None
    else:
        print("Connection is not established. Cannot create cursor.")
        return None

def close_cursor(cursor):
    if cursor:
        cursor.close()
        print("Cursor closed.")
    else:
        print("No cursor to close.")
