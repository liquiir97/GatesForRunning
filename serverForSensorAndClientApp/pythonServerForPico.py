
from datetime import datetime
import database_connector
from database_connector import create_cursor, close_cursor, close_database_connection
import socket
import threading

#TODO get these variables from .env
host = 'localhost'
user = 'tmp'
password = 'tmp'
database='tmp'

selectedUserId = None

database_connection = database_connector.connecttion_to_database(host, user, password, database)
cursor = create_cursor(database_connection)

insert_query =  """INSERT INTO gate_pass (message, date_time_pass, user_id, testiranje_id) VALUES (%s, %s, %s, %s)"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Listen on all interfaces
server_socket.listen(1)

start_signal = None
firts_gate = None
testiranjeId = None

def assign_time(message) :
    if(message == "0"):
        global start_signal
        start_signal = datetime.now()
    elif (message == "1"):
        global  firts_gate
        firts_gate = datetime.now()


def calculate_time():
    if start_signal is not None and firts_gate is not None :
        duration = firts_gate - start_signal
        duration_in_seconds = duration.total_seconds()
    else:
        print("Some gates are not activated.")
print("Server is listening...")

def handle_client(conn, addr):
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            print("No data from", addr)
            break
        print(f"Received from {addr}: {data.decode('utf-8')}")

        data_decoded = data.decode()
        data_decoded_split = data_decoded.split(':')
        if (data_decoded_split[0] == 'Pico'):
            handle_data_from_pico(data_decoded_split[1])
        else:
            handle_data_from_ui(data_decoded_split[1],data_decoded_split[2])

def handle_data_from_pico(data_pico):
    if selectedUserId is not None:
        now = datetime.now()
        val = (data_pico, now, int(selectedUserId), int(testiranjeId))
        cursor.execute(insert_query, val)
        database_connection.commit()

def handle_data_from_ui(dataUiUserId, dataUiSesija):
    global selectedUserId
    selectedUserId = dataUiUserId
    global testiranjeId
    testiranjeId = addNewTestiranje(dataUiSesija)

def addNewTestiranje(sesija):
    insert_query_testiranje = """INSERT INTO testiranje (datum_testiranja, sesija) VALUES (%s, %s)"""
    now = datetime.now()
    val = (now, int(sesija))
    cursor.execute(insert_query_testiranje, val)
    database_connection.commit()
    return cursor.lastrowid

try:
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
except KeyboardInterrupt:
    print("Server interrupted.")

finally:
    conn.close()  # Ensure the connection is closed
    server_socket.close()  # Ensure the server socket is closed
    print("Server closed.")
    close_cursor(cursor)
    close_database_connection(database_connection)