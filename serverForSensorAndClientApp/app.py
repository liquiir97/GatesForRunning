import atexit
import os
from sys import prefix

from dotenv import load_dotenv

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from database.database_connection import connect_to_database, close_database_connection, create_cursor
from routes.api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix="/api")

@app.before_request
def before_request():
    g.db_connection = connect_to_database()
@app.teardown_appcontext
def teardown_appcontext(exception=None):
    # Close the database connection after the request ends
    if hasattr(g, 'db_connection'):
        close_database_connection(g.db_connection)
#cursor = create_cursor(db_connection)


# def shutdown():
#     if hasattr(g, "db_connection"):
#         close_database_connection(g.db_connection)

#atexit.register(shutdown)

if __name__ == '__main__':
    app.run(debug=True, port=5001)