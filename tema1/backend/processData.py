import MySQLdb
import MySQLdb.cursors
import datetime

def saveDataToDB(data):
   
    firstName = data['firstName']
    lastName = data['secondName']
    email = data['email']
    cnp = data['cnp']
    birthdate = data['birthdate']
    camin = data['camin']
    room = data['room']
    floor = data['floor']
    pay = data['pay']
    total = data['total']

    try:
        db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'flory95', db = 'egov')
        cursor = db.cursor()
    except Exception as e:
        print(str(e))


    for p in pay:
        month = p['month']
        pay = p['sum']
        extra = p['extra']

        query = """INSERT INTO smartform (firstname, lastname, email, cnp, birthdate, camin, room, floor, paymonth, paysum, payextra, payment, paydate) VALUES ({0});"""
        values = [firstName, lastName, email, cnp, birthdate, camin, str(room), str(floor), month, str(pay), str(extra), str(pay + extra), str(datetime.datetime.now())]
        placeholders = ','.join(['%s'] * len(values))
        query = query.format(placeholders)

        try:
            cursor.execute(query, values)
            db.commit()
        except Exception as e:
            db.rollback()
            print(str(e))

    try:
        db.close();
    except Exception as e:
        print(str(e))

    return True
