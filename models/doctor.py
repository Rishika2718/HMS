import sqlite3
import json
def doclogin(mobile, email):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur=conn.cursor()
    cur.execute("SELECT doc_id, DName FROM Doctor WHERE Email = ? AND DMobileNumber = ?", (email, mobile))
    user = cur.fetchone()
    conn.close()
    return user

def s_doc(kword):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()
    cur.execute("""
        SELECT doc_id, DName, Email, Timings, DeptName 
        FROM Doctor 
        JOIN Department ON Doctor.Dept_id = Department.Dept_id
        WHERE DName LIKE ? OR DeptName LIKE ? OR Dept_id LIKE ?
    """, (f"%{kword}%", f"%{kword}%",  f"%{kword}%"))
    result = cur.fetchall()
    conn.close()
    return result

# Update doctor's availability
def update_doc(current_user_id,doc_id, new_dname=None, new_mno=None, new_email=None, new_timings=None, new_did=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()

    if current_user_id != doc_id:
        return "Access Denied! Doctors cannot update other doctors' information."
    updates = []
    params = []
    if new_dname:
        updates.append("DName = ?")
        params.append(new_dname)
    if new_mno:
        updates.append("DMobileNumber = ?")
        params.append(new_mno)
    if new_email:
        updates.append("Email = ?")
        params.append(new_email)
    if new_timings:
        updates.append("Timings = ?")
        params.append(new_timings)
    if new_did:
        updates.append("Dept_id = ?")
        params.append(new_did)
    params.append(doc_id)

    sql = f"UPDATE Doctor SET {', '.join(updates)} WHERE doc_id = ?"

    try:
        cur.execute(sql, tuple(params))
        conn.commit()
        result = "Doctor updated successfully!"
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return result

def view_doc():
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()

    cur.execute("""
        SELECT Doctor.doc_id,Doctor.DName,Doctor.DMobileNumber,Doctor.Email,Department.Dept_id
        FROM Doctor
        JOIN Department ON Doctor.Dept_id = Department.Dept_id
    """)

    data = cur.fetchall()
    conn.close()
    return data

def docappt(doc_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()

    cur.execute("""
        SELECT Appointment.App_id, Patient.PName, Appointment.Date, Appointment.Time, Appointment.status
        FROM Appointment
        JOIN Patient ON Appointment.patient_id = Patient.patient_id
        WHERE Appointment.doc_id = ?
        ORDER BY Appointment.Date
    """, (doc_id,))

    result = cur.fetchall()
    conn.close()
    return result

def statusupdate(App_id, status,diagnosis=None, prescription=None, followup=None, notes=None, cost=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()

    if status not in ['Completed', 'Cancelled']:
        return "Invalid status"

    cur.execute("SELECT * FROM Appointment WHERE App_id = ?", (App_id,))
    v = cur.fetchone()
    if not v:
        conn.close()
        return "Appointment not found"

    cur.execute("UPDATE Appointment SET status = ? WHERE App_id = ?", (status, App_id))
    if status == 'Completed':
        cur.execute("SELECT * FROM Treatment WHERE App_id = ?", (App_id,))
        tmt = cur.fetchone()
        if tmt:
            # Update existing treatment
            cur.execute("""
                UPDATE Treatment
                SET Diagnosis = ?, prescription = ?, FollowUp = ?, Notes = ?, Cost = ?
                WHERE App_id = ?
            """, (diagnosis, prescription, followup, notes, cost, App_id))
        else:
            # Insert new treatment
            cur.execute("""
                INSERT INTO Treatment (App_id, Diagnosis, prescription, FollowUp, Notes, Cost)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (App_id, diagnosis, prescription, followup, notes, cost))

    conn.commit()
    conn.close()
    return f"Appointment {App_id} marked as {status} with treatment info"

def patdet(patient_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur=conn.cursor()

    cur.execute("""
        SELECT a.App_id, a.doc_id, a.Date, a.Time, a.status,
               t.Diagnosis, t.prescription, t.FollowUp, t.Notes, t.Cost
        FROM Appointment a
        LEFT JOIN Treatment t ON a.App_id = t.App_id
        WHERE a.patient_id = ?
        ORDER BY a.Date DESC
    """, (patient_id,))
    
    data = cur.fetchall()
    conn.close()
    return data

def todayappt(doc_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT App_id, patient_id, Date, Time, status
        FROM Appointment
        WHERE doc_id = ?
        AND Date = DATE('now')
        ORDER BY Time
    """, (doc_id,))

    d = cur.fetchall()
    conn.close()
    return d

def weekappt(doc_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT App_id, patient_id, Date, Time, status
        FROM Appointment
        WHERE doc_id = ?
        AND Date BETWEEN DATE('now') AND DATE('now', '+7 days')
        ORDER BY Date, Time
    """, (doc_id,))

    result = cur.fetchall()
    conn.close()
    return result

def viewpat(doc_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT p.patient_id, p.PName, p.Email, p.Mobile
        FROM Appointment a
        JOIN Patient p ON a.patient_id = p.patient_id
        WHERE a.doc_id = ?
    """, (doc_id,))

    d = cur.fetchall()
    conn.close()
    return d

def addpattmt(App_id, diagnosis, prescription, followup, notes, cost):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()

    # Check if appointment exists
    cur.execute("SELECT * FROM Appointment WHERE App_id = ?", (App_id,))
    appt = cur.fetchone()

    if not appt:
        conn.close()
        return "Appointment not found!"

    # Insert a NEW treatment entry (do NOT update old ones)
    try:
        cur.execute("""
            INSERT INTO Treatment (App_id, Diagnosis, prescription, FollowUp, Notes, Cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (App_id, diagnosis, prescription, followup, notes, cost))

        conn.commit()
        conn.close()
        return "Treatment added successfully!"
    
    except Exception as e:
        conn.close()
        return f"Error adding treatment: {e}"
    
def addavail(doc_id, avail):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    jd = json.dumps(avail)
    try:
        cur.execute(
            "UPDATE Doctor SET Timings = ? WHERE doc_id = ?",
            (jd, doc_id)
        )
        conn.commit()
        result = "Availability updated successfully"
    except Exception as e:
        result = f"Error: {e}"

    conn.close()
    return result

def getavail(doc_id):
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()

    cur.execute("SELECT Timings FROM Doctor WHERE doc_id = ?", (doc_id,))
    r = cur.fetchone()
    conn.close()
    if r is None or r[0] is None:
        return None
    try:
        return json.loads(r[0])
    except:
        return {"error": "Invalid JSON stored in database"}
