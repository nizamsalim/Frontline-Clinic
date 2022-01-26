import datetime
import mysql.connector as ms
import pywhatkit.whats as whatsapp

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
            db.execute(
                """
                    CREATE TABLE IF NOT EXISTS doctors(
                        doc_id INT(5) PRIMARY KEY AUTO_INCREMENT,
                        doctor_name VARCHAR(50),
                        dept VARCHAR(25),
                        salary INT(6),
                        experience INT(2)
                    )
                """
            )
            db.execute("ALTER TABLE doctors AUTO_INCREMENT=1000")
            return True
    except:
        return False


def getPatientName(patientId):
    db.execute(f'SELECT * from patients WHERE id={patientId}')
    data = db.fetchone()
    if data == None:
        return
    else:
        return data[1]


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
        f"SELECT app_id FROM appointments ORDER BY app_id desc LIMIT 1")
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


def getPastAppointments(p_id):
    db.execute(
        f"SELECT app_id, doctor_name, booking_date, appointment_date, status FROM appointments WHERE patient_id={p_id}")
    return db.fetchall()


def sendWhatsappConfirmation(name, docName, date, time, refId, p_id):
    db.execute(f"SELECT phone FROM patients WHERE id={p_id}")
    (phone,) = db.fetchone()
    phone = f"+91{phone}"
    message = f"Hello {name}\nYour appointment with {docName} at Frontline Clinic on {date} during {time} has been confirmed.\nPlease note appointment reference number {refId}.\nThank you. "
    whatsapp.sendwhatmsg_instantly(phone, message, tab_close=True)


def addDoctor(d_name, dept, sal, exp):
    db.execute(
        f"INSERT INTO doctors(doctor_name,dept,salary,experience) VALUES('{d_name}','{dept}',{sal},{exp})")
    conn.commit()
    db.execute("SELECT * FROM doctors ORDER BY doc_id desc LIMIT 1")
    return db.fetchone()


def getAllDoctors():
    db.execute("SELECT * FROM doctors")
    return db.fetchall()


def getDoctorsForDropDown():
    db.execute("SELECT doctor_name,dept FROM doctors")
    lst = []
    for doctor in db.fetchall():
        lst.append(f"{doctor[0]} ({doctor[1]}) ")
    return lst


def updateDoctor(d_id, name, dpt, sal, exp):
    db.execute(
        f"UPDATE doctors SET doctor_name='{name}',dept='{dpt}',salary={int(sal)},experience={int(exp)} WHERE doc_id={d_id}")
    conn.commit()


def deleteDoctor(d_id):
    db.execute(f"DELETE FROM doctors WHERE doc_id={d_id}")
    conn.commit()


def closeDatabase():
    db.close()
    conn.close()
