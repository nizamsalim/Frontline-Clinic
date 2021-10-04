import datetime


def getPatientName(db, patientId):
    db.execute(f'SELECT * from patients WHERE id={patientId}')
    data = db.fetchall()
    if len(data) == 0:
        return
    else:
        return data[0][1]


def createNewUser(db, conn, name, age, phone, place, visits=0):
    db.execute(
        f"INSERT INTO patients(name,age,phone,place,visits) VALUES('{name}',{age},'{phone}','{place}',{visits})")
    conn.commit()


def createNewAppointment(db, conn, d_name, p_id, time, date, status='pending'):
    bookingDate = datetime.datetime.now().strftime('%d/%m/%y')
    db.execute(
        f"INSERT INTO appointments(patient_id,doctor_name,booking_date,appointment_date,time,status) VALUES({p_id},'{d_name}','{bookingDate}','{date}','{time}','{status}')")
    conn.commit()
