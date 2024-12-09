import socket
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
import user_service
import threading


app = Flask(__name__)
CORS(app)

WS_URL = "ws://localhost:12345"
ws = None
server_host = 'localhost'
server_port = 12345
sock = None

selectedUserId = 0

@app.route('/api/message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    response_message = f"Received your message: {message}"
    return jsonify({"response": response_message})

@app.route('/api/get-all-user', methods=['GET'])
def getUsers():
    data =  user_service.getUsers()
    return jsonify({"response" : data})

def connect_to_server():
    global sock
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_host, server_port))
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 10 seconds...")
            time.sleep(30)

def start_connection_thread():
    global connection_thread
    connection_thread = threading.Thread(target=connect_to_server)
    connection_thread.start()


def startTestServer(userId, session):
    try:
        message = "UI:" + str(userId) + ":" + str(session)
        sock.send(message.encode())
        return jsonify(({"response": "Ok"})), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/gate-pass-data/<selectedUser>', methods=['GET'])
def getGatePassData(selectedUser):
    print("Path parametat: ", selectedUser)
    result = user_service.getGatePassData(selectedUser)
    return jsonify({"response" : result[0], "difference" : result[1]}), 200

@app.route('/api/start-test', methods=['POST'])
def startTest():
    data = request.json
    startTestServer(data.get('userId'), data.get('session'))
    return jsonify({"response": "Ok"}), 200

@app.route('/api/finish-test', methods=['POST'])
def enbdTest():
    data = request.json
    resultGate = user_service.endTest(data.get('userId'), data.get('session'))
    return jsonify({"response": resultGate[0], "difference": resultGate[1]}), 200


if __name__ == '__main__':
    start_connection_thread()
    #connect_to_server()  # Connect to the socket server
    app.run(debug=True)
