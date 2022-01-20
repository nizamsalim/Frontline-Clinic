import datetime
import mysql.connector as ms

conn, db = None, None


def initDatabase():
    try:
        global conn, db
        conn = ms.connect(
            host="localhost",
            user='root',
            passwd='nizam123',
        )
        if conn.is_connected():
            db = conn.cursor()
            db.execute("CREATE DATABASE IF NOT EXISTS frontline")
            db.execute("USE frontline")
            db.execute(
                """
                    CREATE TABLE IF NOT EXISTS patients(
                        id INT(5) PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50),
                        age VARCHAR(3),
                        phone VARCHAR(10),
                        place VARCHAR(50),
                        visits INT(3)
                    )
                """
            )
            db.execute("ALTER TABLE patients AUTO_INCREMENT=100")
            db.execute(
                """
                    CREATE TABLE IF NOT EXISTS appointments(
                        app_id INT(5) PRIMARY KEY AUTO_INCREMENT,
                        patient_id INT(5),
                        doctor_name VARCHAR(70),
                        booking_date VARCHAR(10),
                        appointment_date VARCHAR(10),
                        time VARCHAR(20),
                        status VARCHAR(10)
                    )
                """
            )
            db.execute("ALTER TABLE appointments AUTO_INCREMENT=10000")
            db.execute(
                """
                    CREATE TABLE IF NOT EXISTS tokens(
                        date VARCHAR(25),
                        token VARCHAR(10)
                    )
                """
            )
            return True
    except:
        return False


def getPatientName(patientId):
    db.execute(f'SELECT * from patients WHERE id={patientId}')
    data = db.fetchall()
    if len(data) == 0:
        return
    else:
        return data[0][1]


def createNewUser(name, age, phone, place, visits=0):
    db.execute(
        f"INSERT INTO patients(name,age,phone,place,visits) VALUES('{name}',{age},'{phone}','{place}',{visits})")
    conn.commit()
    db.execute("SELECT id FROM patients ORDER BY id desc LIMIT 1")
    id = db.fetchone()
    return id[0]


def createNewAppointment(d_name, p_id, time, date, status='pending'):
    bookingDate = datetime.datetime.now().strftime('%d/%m/%y')
    db.execute(
        f"INSERT INTO appointments(patient_id,doctor_name,booking_date,appointment_date,time,status) VALUES({p_id},'{d_name}','{bookingDate}','{date}','{time}','{status}')")
    conn.commit()
    db.execute(
        f"SELECT app_id FROM appointments WHERE patient_id={p_id} ORDER BY app_id desc LIMIT 1")
    id = db.fetchone()
    return id[0]


def updateNumberOfVisits(p_id):
    db.execute(f'UPDATE patients SET visits=visits+1 WHERE id={p_id}')
    conn.commit()


def updateAppointmentStatus(p_id, status):
    db.execute(
        f'UPDATE appointments SET status="{status}" WHERE patient_id={p_id}')
    conn.commit()


def saveToken(tkn):
    db.execute('SELECT * FROM tokens')
    date = datetime.datetime.now().strftime('%d-%m-%y')
    # 15-12-18
    data = db.fetchall()
    if len(data) == 0:
        db.execute(f'INSERT INTO tokens(date,token) VALUES("{date}","{tkn}")')
        conn.commit()
    else:
        # data.reverse()
        # ('15-12-18','1512-1')
        lastRow = data[0]
        if lastRow[0] == date:
            db.execute(f'UPDATE tokens SET token="{tkn}" WHERE date="{date}"')
            conn.commit()
        else:
            db.execute(f"DELETE FROM tokens")
            db.execute(f'INSERT INTO tokens VALUES("{date}","{tkn}")')
            conn.commit()


def getInitialTokenNumber():
    date = datetime.datetime.now().strftime('%d-%m-%y')
    db.execute('SELECT * FROM tokens')
    data = db.fetchall()
    if len(data) == 0:
        return 1
    else:
        data.reverse()
        lastRow = data[0]
        # ('15-12-18','1512-1')
        if lastRow[0] == date:
            initToken = int(lastRow[1].split('-')[1])+1
        else:
            initToken = 1
        return initToken


def getPatientIdByAppId(appId):
    db.execute(f'SELECT patient_id FROM appointments WHERE app_id={appId}')
    data = db.fetchone()
    if data == None:
        return
    return data[0]

def isAppointmentPending(appId):
    db.execute(f"SELECT status from appointments WHERE app_id={appId}")
    data = db.fetchone()
    return True if data[0] == 'pending' else False

