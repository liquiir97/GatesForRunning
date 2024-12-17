from datetime import datetime

from database.database_connection import create_cursor, close_cursor
from flask import g

selected_user_id = None
first_gate = None
testiranje_id = None

def handle_data_from_pico(gate: str):
    print("handling data from pico")
    connection = g.get("db_connection")
    print("USER ID: " + str(selected_user_id))
    if connection and selected_user_id is not None:
        cursor = create_cursor(connection)
        insert_query = """INSERT INTO gate_pass (message, date_time_pass, user_id, testiranje_id) VALUES (%s, %s, %s, %s)"""
        now = datetime.now()
        value = (gate, now, int(selected_user_id), int(testiranje_id))
        cursor.execute(insert_query, value)
        connection.commit()
        print("value is inserted")
        close_cursor(cursor)
        return "OK"
    print("Problem with connection or user id")
    return "NOK"

def handle_data_from_ui(user_id, session):
    print("handling data from ui")
    global selected_user_id
    selected_user_id = user_id
    global testiranje_id
    testiranje_id = add_new_testing(session)

    if testiranje_id is None:
        return "NOK"
    return "OK"

def add_new_testing(session):
    connection = g.get("db_connection")
    if connection:
        cursor = create_cursor(connection)
        insert_query_testing = """INSERT INTO testiranje (datum_testiranja, sesija) VALUES (%s, %s)"""
        now = datetime.now()
        value = (now, int(session))
        cursor.execute(insert_query_testing, value)
        connection.commit()
        id_of_testing = cursor.lastrowid
        close_cursor(cursor)
        return id_of_testing
    return None


