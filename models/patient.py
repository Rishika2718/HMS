import sqlite3

import json

def regpat(patient_id, name, mobile, email, gender, dob, address, blood_group, optional_contact=None):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur=conn.cursor()
    cur.execute("""
        INSERT INTO Patient(patient_id, PName, PMobileNumber, Email, Gender, DOB, Address, Blood_group, Optional_Contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, name, mobile, email, gender, dob, address, blood_group, optional_contact))
    conn.commit()
    conn.close()
    return "Patient registered successfully!"

def patlogin(email, mobile):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur=conn.cursor()
    cur.execute("SELECT patient_id, PName FROM Patient WHERE Email = ? AND PMobileNumber = ?", (email, mobile))
    user = cur.fetchone()
    conn.close()
    return user  

def updpat(current_id, patient_id, name=None, mobile=None, email=None, address=None, blood_group=None, optional_contact=None):
    if current_id != patient_id:
        return "Access Denied! You can only update your own profile."

    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    updates = []
    params = []

    if name:
        updates.append("PName = ?")
        params.append(name)
    if mobile:
        updates.append("PMobileNumber = ?")
        params.append(mobile)
    if email:
        updates.append("Email = ?")
        params.append(email)
    if address:
        updates.append("Address = ?")
        params.append(address)
    if optional_contact:
        updates.append("Optional_Contact = ?")
        params.append(optional_contact)
    if not updates:
        conn.close()
        return "No changes provided."
    params.append(patient_id)
    sql = f"UPDATE Patient SET {', '.join(updates)} WHERE patient_id = ?"
    cur.execute(sql, tuple(params))
    conn.commit()
    conn.close()
    return "Patient profile updated successfully!"

def searchdoc(dept=None, timing=None):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    q = """
        SELECT Doctor.doc_id, DName, DMobileNumber,Email, Timings, DeptName 
        FROM Doctor
        JOIN Department ON Doctor.Dept_id = Department.Dept_id
        WHERE 1=1
    """
    params = []
    if dept:
        q += " AND DeptName LIKE ?"
        params.append(f"%{dept}%")
    if timing:
        q += " AND Timings LIKE ?"
        params.append(f"%{timing}%")
    cur.execute(q, tuple(params))
    result = cur.fetchall()
    conn.close()
    return result

def newappt(patient_id, doc_id, date, time):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Appointment(patient_id, doc_id, Date, Time, status)
        VALUES (?, ?, ?, ?, 'Booked')
    """, (patient_id, doc_id, date, time))
    conn.commit()
    conn.close()
    return "Appointment booked successfully!"

def appt_change(App_id, new_date, new_time):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE Appointment SET Date = ?, Time = ? WHERE App_id = ?
    """, (new_date, new_time, App_id))
    conn.commit()
    conn.close()
    return "Appointment rescheduled successfully!"

def canappt(App_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("UPDATE Appointment SET status = 'Cancelled' WHERE App_id = ?", (App_id,))
    conn.commit()
    conn.close()
    return "Appointment cancelled successfully!"

#views all appt pat and coming
def viewpat(patient_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT a.App_id, d.DName, a.Date, a.Time, a.status,
               t.Diagnosis, t.prescription, t.FollowUp, t.Notes, t.Cost
        FROM Appointment a
        JOIN Doctor d ON a.doc_id = d.doc_id
        LEFT JOIN Treatment t ON a.App_id = t.App_id
        WHERE a.patient_id = ?
        ORDER BY a.Date DESC
    """, (patient_id,))
    data = cur.fetchall()
    conn.close()
    return data

def listdept():
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Department")
    data = cur.fetchall()
    conn.close()
    return data

def listpats():
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Patient")
    data = cur.fetchall()
    conn.close()
    return data

def docavail(doc_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("SELECT DName, Timings FROM Doctor WHERE doc_id = ?", (doc_id,))
    data = cur.fetchone()
    conn.close()
    if not data:
        return None
    name, jd = data
    timings = json.loads(jd)
    return {"dname": name, "avail": timings}
import datetime

def weekavail(timings):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    today_idx = datetime.datetime.now().weekday()   # 0 = Monday
    result = []
    for i in range(7):
        day_idx = (today_idx + i) % 7
        day_name = days[day_idx]
        slot = timings.get(day_name, "Not Available")
        date = (datetime.date.today() + datetime.timedelta(days=i)).strftime("%d-%m-%Y")
        result.append({
            "day": day_name,
            "date": date,
            "slot": slot
        })
    return result


def searchpat(q):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Patient
        WHERE PName LIKE ? OR patient_id LIKE ? OR PMobileNumber LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))
    d = cur.fetchall()
    conn.close()
    return d
from datetime import datetime

def getpat(patient_id):
    d = viewpat(patient_id)  
    past = []
    today = datetime.today().date()

    for row in d:
        app_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        status = row[4]
        if status in ("Completed", "Cancelled") or app_date < today:
            past.append(row)

    return past
