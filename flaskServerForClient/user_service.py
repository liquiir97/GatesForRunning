from datetime import datetime, date
import database_connector

#TODO change to get this variable from .env
host = 'localhost'
user_db = 'tmp'
password = 'tmp'
database='tmp'

selectUserId = None
sessionTest = None

class Gate:
    def __init__(self, id, message, date_time_pass, user_id, testiranje_id, datum_testiranja, sesija):
        self.id = id
        self.message = message
        self.date_time_pass = date_time_pass
        self.user_id = user_id
        self.testiranje_id = testiranje_id
        self.datum_testiranja = datum_testiranja
        self.sesija = sesija

    def convert_to_dict(self):
        return \
            {
                "id" : self.id,
                "message" : self.message,
                "date_time_pass" : self.date_time_pass,
                "user_id" : self.user_id,
                "testiranje_id" : self.testiranje_id,
                "datum_testiranja" : self.datum_testiranja,
                "sesija" : self.sesija
            }

class User:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def convert_to_dict(self):
        return \
            {
                "id" : self.id,
                "name" : self.name,
            }

def getUsers():
    database_connection = database_connector.connecttion_to_database(host, user_db, password, database)
    cursor = database_connector.create_cursor(database_connection)

    query = "SELECT id, name FROM user"
    cursor.execute(query)
    user_result = cursor.fetchall()
    print(user_result)
    list_users = [User(row['id'], row['name']).convert_to_dict() for row in user_result]

    database_connector.close_cursor(cursor)
    database_connector.close_database_connection(database_connection)
    return  list_users

def selectedUserId(id):
    global selectUserId
    selectUserId = id
    return selectUserId
def getIdSelectedUser():
    return selectedUserId

def getGatePassData(selectedUser):
    database_connection = database_connector.connecttion_to_database(host, user_db, password, database)
    cursor = database_connector.create_cursor(database_connection)
    query = "SELECT gp.*, t.datum_testiranja, t.sesija FROM gate_pass gp LEFT JOIN testiranje t ON gp.testiranje_id = t.id WHERE user_id = %s ORDER BY gp.testiranje_id ASC"
    if selectedUser is not None:
        cursor.execute(query, (selectedUser,))
        gate_result = cursor.fetchall()
        list_gate_pass = [Gate(gate_pass['id'], gate_pass['message'], gate_pass['date_time_pass'], gate_pass['user_id'], gate_pass['testiranje_id'], gate_pass['datum_testiranja'], gate_pass['sesija']).convert_to_dict() for gate_pass in gate_result]
        differences_between_gate = list_gate_pass[1].get("date_time_pass") - list_gate_pass[0].get("date_time_pass")

        dictDiferences = []
        for i in range(len(list_gate_pass) -1, -1, -1):
            for j in range(i-1, -1,-1):
                if (list_gate_pass[i].get('testiranje_id')==list_gate_pass[j].get('testiranje_id')) and (list_gate_pass[i].get('sesija') == list_gate_pass[j].get('sesija')):
                    print("dodavanje")
                    dictDiferences.append(
                        {"gate": "Gate: " + list_gate_pass[i].get('message') + "-" + list_gate_pass[j].get('message'),
                         "difference": (list_gate_pass[i].get('date_time_pass') - list_gate_pass[j].get('date_time_pass')).total_seconds(), "dateTesting" : list_gate_pass[i].get('datum_testiranja'), 'session' : list_gate_pass[i].get('sesija'), 'gateForChart' :  '1' if int(list_gate_pass[i].get('message'))-int(list_gate_pass[j].get('message')) == 1 else '0'})
                    print(dictDiferences)
                else:
                    print("break")
                    break
        database_connector.close_cursor(cursor)
        database_connector.close_database_connection(database_connection)
        return (list_gate_pass, dictDiferences)

def startTest(userId, session):
    global selectUserId
    selectUserId = userId
    global sessionTest
    sessionTest = session

def endTest(userId, session):
    global selectUserId
    selectUserId = None
    global sessionTest
    sessionTest = None
    database_connection = database_connector.connecttion_to_database(host, user_db, password, database)
    cursor = database_connector.create_cursor(database_connection)

    query = "SELECT gp.*, t.datum_testiranja, t.sesija FROM gate_pass gp LEFT JOIN testiranje t ON gp.testiranje_id = t.id WHERE user_id = %s AND t.datum_testiranja = %s AND t.sesija = %s"
    dateNow = date.today()
    if userId is not None:

        cursor.execute(query, (userId,dateNow,session, ))
        databaseResult = cursor.fetchall()
        if len(databaseResult) > 0:
            list_gate_pass = [Gate(gate_pass['id'], gate_pass['message'], gate_pass['date_time_pass'], gate_pass['user_id'],
                               gate_pass['testiranje_id'], gate_pass['datum_testiranja'],
                               gate_pass['sesija']).convert_to_dict() for gate_pass in databaseResult]
            differences_between_gate = list_gate_pass[1].get("date_time_pass") - list_gate_pass[0].get("date_time_pass")

            dictDiferences = []
            for i in range(len(list_gate_pass) - 1, -1, -1):
                for j in range(i - 1, -1, -1):
                    if (list_gate_pass[i].get('testiranje_id') == list_gate_pass[j].get('testiranje_id')) and (
                        list_gate_pass[i].get('sesija') == list_gate_pass[j].get('sesija')):
                        print("dodavanje")
                        dictDiferences.append(
                            {"gate": "Gate: " + list_gate_pass[i].get('message') + "-" + list_gate_pass[j].get('message'),
                            "difference": (list_gate_pass[i].get('date_time_pass') - list_gate_pass[j].get(
                                'date_time_pass')).total_seconds(),
                            "dateTesting": list_gate_pass[i].get('datum_testiranja'),
                            'session': list_gate_pass[i].get('sesija'), "gateForChart" : '1' if int(list_gate_pass[i].get('message'))-int(list_gate_pass[j].get('message')) == 1 else '0'})

                    else:
                        break
        else:
            list_gate_pass = []
            dictDiferences = []
        database_connector.close_cursor(cursor)
        database_connector.close_database_connection(database_connection)
        return (list_gate_pass, dictDiferences)