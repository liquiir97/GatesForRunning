from datetime import datetime

import mysql.connector
from mysql.connector import Error
from datetime import datetime


def connecttion_to_database(host, user, password, database):
    try:
        databse_connection = mysql.connector.connect(host=host, user=user, password = password, database=database)

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
            cursor = database_connection.cursor(dictionary=True)
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