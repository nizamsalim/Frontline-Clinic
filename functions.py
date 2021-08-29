def getPatientName(db,patientId):
    db.execute(f'SELECT * from patients WHERE id={patientId}')
    data = db.fetchall()
    if len(data) == 0:
        return
    else:
        return data[0][1]
    
def createNewUser(db,conn,name,age,phone,place,visits=0):
    db.execute(f"INSERT INTO patients(name,age,phone,place,visits) VALUES('{name}',{age},'{phone}','{place}',{visits})")
    conn.commit()


