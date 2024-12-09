import machine
import time
import network
import socket
from machine import Pin


ssid = 'WIFI Name'
password = 'WIFI PASS'

server_ip = ''
server_port = 12345
pir_sensor = Pin(20, Pin.IN)
previous_state = pir_sensor.value()

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def socket_connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print("Pico connected to socket server")
        return client_socket
    except Exception as e:
        print("Connection failed:", e)
        return None
    

try:
    ip = connect()
    client_socket = socket_connection()
    gate_access = 0
    #handle when socket is not connected or wifi
    if client_socket:
        print("Starting PIR sensor check...")
        print(previous_state)
        while True:
            current_state = pir_sensor.value()
            print(previous_state)
            print(current_state)
            # Check for state change
            if current_state != previous_state:
                if current_state:
                    print("Motion detected!")
                    message = "Pico:" + str(gate_access)
                    client_socket.send(message.encode())
                    time.sleep(0.5)
                    gate_access = gate_access + 1
                else:
                    print("No motion.")
        
            # Update previous state
            previous_state = current_state
        
            time.sleep(0.2)  # Short delay to reduce flooding
except KeyboardInterrupt:
    client_socket.close()
    print("Program stopped.")
    
