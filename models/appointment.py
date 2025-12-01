import sqlite3

def slotbook(doc_id, date, time):
    """Check if slot is already booked"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM Appointment 
        WHERE doc_id = ? AND Date = ? AND Time = ? AND status = 'Booked'
    """, (doc_id, date, time))
    
    result = cur.fetchone()
    conn.close()
    
    return result is not None  # Returns True if slot is booked

def bookappt(patient_id, doc_id, date, time):
    """Book a new appointment"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO Appointment(patient_id, doc_id, Date, Time, status)
            VALUES (?, ?, ?, ?, 'Booked')
        """, (patient_id, doc_id, date, time))
        conn.commit()
        result = "Appointment booked successfully!"
    except Exception as e:
        result = f"Error: {e}"
    
    conn.close()
    return result

def getappt(app_id):
    """Get appointment details"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM Appointment WHERE App_id = ?
    """, (app_id,))
    
    result = cur.fetchone()
    conn.close()
    return result

def updateappt(app_id, new_status=None, new_date=None, new_time=None):
    """Update appointment details"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    
    updates = []
    params = []
    
    if new_status:
        updates.append("status = ?")
        params.append(new_status)
    
    if new_date:
        updates.append("Date = ?")
        params.append(new_date)
    
    if new_time:
        updates.append("Time = ?")
        params.append(new_time)
    
    if not updates:
        conn.close()
        return "No fields to update."
    
    params.append(app_id)
    sql = f"UPDATE Appointment SET {', '.join(updates)} WHERE App_id = ?"
    
    try:
        cur.execute(sql, tuple(params))
        conn.commit()
        result = "Appointment updated successfully!"
    except Exception as e:
        result = f"Error: {e}"
    
    conn.close()
    return result

def cancelappt(app_id):
    """Cancel an appointment"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE Appointment SET status = 'Cancelled' WHERE App_id = ?
        """, (app_id,))
        conn.commit()
        result = "Appointment cancelled successfully!"
    except Exception as e:
        result = f"Error: {e}"
    
    conn.close()
    return result

def changestatus():
    import sqlite3
    from datetime import datetime
    conn = sqlite3.connect("hms.db")
    cur = conn.cursor()
    now = datetime.now()
    cur.execute("""
        SELECT appointment_id, date, time 
        FROM appointments 
        WHERE status = 'Booked'
    """)
    rows = cur.fetchall()
    for appt_id, date_str, time_str in rows:
        appt_datetime = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")

        if appt_datetime < now:
            cur.execute("""
                UPDATE appointments
                SET status = 'Completed'
                WHERE appointment_id = ?
            """, (appt_id,))
    
    conn.commit()
    conn.close()
