# # import sqlite3

# # def dashboard():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur = conn.cursor()

# #     cur.execute("SELECT COUNT(*) FROM Doctor")
# #     dc = cur.fetchone()[0]

# #     cur.execute("SELECT COUNT(*) FROM Patient")
# #     pc = cur.fetchone()[0]

# #     cur.execute("SELECT COUNT(*) FROM Appointment")
# #     ac = cur.fetchone()[0]
# #     conn.close()
# #     return dc,pc,ac


# # # ADMIN LOGIN
# # def admin_login(username, password, check_pwd):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()

# #     cur.execute("SELECT id, username, password, name FROM admin WHERE username = ?", (username,))
# #     admin = cur.fetchone()
# #     conn.close()
# #     if admin and check_pwd(admin[2], password):
# #         return True, admin[3]  # (success, admin_name)
# #     return False, None

# # # DOCTOR MANAGEMENT
# # def add_doc(doc_id, dname, mno, email, timings, did):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         cur.execute("""
# #             INSERT INTO Doctor (doc_id, DName, DMobileNumber, Email, Timings, Dept_id)
# #             VALUES (?, ?, ?, ?, ?, ?)
# #         """, (doc_id, dname, mno, email, timings, did))
# #         conn.commit()
# #         result = "Doctor added successfully!"
# #     except Exception as e:
# #         result = f"Error: {e}"
# #     conn.close()
# #     return result


# # def update_doc(doc_id, new_dname=None, new_mno=None, new_email=None, new_timings=None, new_did=None):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     updates = []
# #     params = []
# #     if new_dname:
# #         updates.append("DName = ?")
# #         params.append(new_dname)
# #     if new_mno:
# #         updates.append("DMobileNumber = ?")
# #         params.append(new_mno)
# #     if new_email:
# #         updates.append("Email = ?")
# #         params.append(new_email)
# #     if new_timings:
# #         updates.append("Timings = ?")
# #         params.append(new_timings)
# #     if new_did:
# #         updates.append("Dept_id = ?")
# #         params.append(new_did)
# #     params.append(doc_id)

# #     sql = f"UPDATE Doctor SET {', '.join(updates)} WHERE doc_id = ?"

# #     try:
# #         cur.execute(sql, tuple(params))
# #         conn.commit()
# #         result = "Doctor updated successfully!"
# #     except Exception as e:
# #         result = f"Error: {e}"
# #     conn.close()
# #     return result


# # def delete_doc(doc_id):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         cur.execute("DELETE FROM Doctor WHERE doc_id = ?", (doc_id,))
# #         conn.commit()
# #         result = "Doctor deleted successfully!"
# #     except Exception as e:
# #         result = f"Error: {e}"
# #     conn.close()
# #     return result

# # def search_doc(kword):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT doc_id, DName, Email, Timings, DeptName 
# #         FROM Doctor 
# #         JOIN Department ON Doctor.Dept_id = Department.Dept_id
# #         WHERE DName LIKE ? OR DeptName LIKE ? OR Dept_id LIKE ?
# #     """, (f"%{kword}%", f"%{kword}%",  f"%{kword}%"))

# #     result = cur.fetchall()
# #     conn.close()
# #     return result

# # def view_doc():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT Doctor.doc_id,Doctor.DName,Doctor.DMobileNumber,Doctor.Email,Department.Dept_id
# #         FROM Doctor
# #         JOIN Department ON Doctor.Dept_id = Department.Dept_id
# #     """)

# #     data = cur.fetchall()
# #     conn.close()
# #     return data


# # # PATIENT MANAGEMENT

# # def addpat(pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         cur.execute("""
# #             INSERT INTO Patient 
# #             (patient_id, PName, PMobileNumber, Email, Gender, DOB, Address, Optional_Contact, Blood_group)
# #             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
# #         """, (pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp))

# #         conn.commit()
# #         result = "Patient added successfully!"
# #     except Exception as e:
# #         result = f"Error: {e}"

# #     conn.close()
# #     return result

# # def update_pat(pid, new_pname=None,new_mno=None,new_email=None,new_gen=None,new_dob=None,new_address=None,new_optionalmno=None,new_bgrp=None):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     updates = []
# #     params = []
# #     if new_pname:
# #         updates.append("PName = ?")
# #         params.append(new_pname)
# #     if new_mno:
# #         updates.append("PMobileNumber = ?")
# #         params.append(new_mno)
# #     if new_email:
# #         updates.append("Email = ?")
# #         params.append(new_email)
# #     if new_gen:
# #         updates.append("Gender = ?")
# #         params.append(new_gen)
# #     if new_dob:
# #         updates.append("DOB = ?")
# #         params.append(new_dob)
# #     if new_address:
# #         updates.append("Address = ?")
# #         params.append(new_address)
# #     if new_optionalmno:
# #         updates.append("Optional_Contact= ?")
# #         params.append(new_optionalmno)
# #     if new_bgrp:
# #         updates.append("Blood_group= ?")
# #         params.append(new_bgrp)
# #     params.append(pid)

# #     sql = f"UPDATE Patient SET {', '.join(updates)} WHERE patient_id = ?"

# #     try:
# #         cur.execute(sql, tuple(params))
# #         conn.commit()
# #         result = "Patient updated successfully!"
# #     except Exception as e:
# #         result = f"Error: {e}"
# #     conn.close()
# #     return result


# # def searchpat(key):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT * FROM Patient 
# #         WHERE PName LIKE ? OR PMobileNumber LIKE ? OR patient_id LIKE ?
# #     """, (f"%{key}%", f"%{key}%", f"%{key}%"))

# #     result = cur.fetchall()
# #     conn.close()
# #     return result

# # def view_pat():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT Patient.patient_id,Patient.Pname,Patient.PMobileNumber,Patient.Email,Patient.Gender,Patient.DOB,Patient.Address,Patient.Optional_Contact,Patient.Blood_group
# #         FROM Patient
# #     """)

# #     data = cur.fetchall()
# #     conn.close()
# #     return data


# # # APPOINTMENT MANAGEMENT

# # def view_appt():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT Appointment.App_id, Patient.PName, Doctor.DName, Appointment.Date, Appointment.Time, Appointment.status
# #         FROM Appointment
# #         JOIN Patient ON Appointment.patient_id = Patient.patient_id
# #         JOIN Doctor ON Appointment.doc_id = Doctor.doc_id
# #         ORDER BY Date
# #     """)
# #     data = cur.fetchall()
# #     conn.close()
# #     return data

# # def updateappt(app_id, new_status=None, new_date=None, new_time=None):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         updates = []
# #         params = []

# #         if new_status:
# #             updates.append("status = ?")
# #             params.append(new_status)

# #         if new_date:
# #             updates.append("Date = ?")
# #             params.append(new_date)

# #         if new_time:
# #             updates.append("Time = ?")
# #             params.append(new_time)

# #         if not updates:
# #             return "No fields to update."

# #         params.append(app_id)

# #         sql = f"UPDATE Appointment SET {', '.join(updates)} WHERE App_id = ?"
# #         cur.execute(sql, tuple(params))

# #         conn.commit()
# #         conn.close()
# #         return "Appointment updated!"

# #     except Exception as e:
# #         return f"Error: {e}"

# # def delete_appt(app_id):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         cur.execute("DELETE FROM Appointment WHERE app_id = ?", (app_id,))
# #         conn.commit()
# #         return "Appointment deleted successfully!"
# #     except Exception as e:
# #         return f"Error: {e}"
# #     finally:
# #         conn.close()

# # def searchappt(key):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT * FROM Appointment 
# #         WHERE App_id LIKE ? OR patient_id LIKE ? OR doc_id LIKE ? OR Date LIKE ? OR Time LIKE ? OR status LIKE ?
# #     """, (f"%{key}%", f"%{key}%", f"%{key}%",f"%{key}%", f"%{key}%", f"%{key}%"))

# #     result = cur.fetchall()
# #     conn.close()
# #     return result

# # # TreaTMENT MANAGEMENT
# # def view_tmt():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT Treatment.App_id,Treatment.Tmt_id,Treatment.Diagnosis,Treatment.prescription,Treatment.FollowUp,Treatment.Notes,Treatment.Cost
# #         FROM Treatment
# #         JOIN  Appointment ON Treatment.App_id = Appointment.App_id
# #         ORDER BY Date
# #     """)
# #     data = cur.fetchall()
# #     conn.close()
# #     return data

# # def searchtmt(key):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT * FROM Treatment 
# #         WHERE Tmt_id LIKE ? OR App_id LIKE ? OR FollowUp LIKE ? 
# #     """, (f"%{key}%", f"%{key}%", f"%{key}%"))

# #     result = cur.fetchall()
# #     conn.close()
# #     return result

# # # Department MANAGEMENT
# # def adddept(dept_id, name, description):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     try:
# #         cur.execute("""
# #             INSERT INTO Department(Dept_id, DeptName, Description)
# #             VALUES (?, ?, ?)
# #         """, (dept_id, name, description))
# #         conn.commit()
# #         conn.close()
# #         return "Department added successfully!"

# #     except Exception as e:
# #         return f"Error: {e}"
    
# # def viewdept():
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("SELECT * FROM Department")
# #     result = cur.fetchall()

# #     conn.close()
# #     return result

# # def searchdept(key):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     cur.execute("""
# #         SELECT * FROM Department 
# #         WHERE Dept_id LIKE ? OR DeptName LIKE ?
# #     """, (f"%{key}%", f"%{key}%"))
# #     result = cur.fetchall()
# #     conn.close()
# #     return result

# # def update_department(dept_id, new_name=None, new_description=None):
# #     conn = sqlite3.connect('hospital_mgmt.db')
# #     cur=conn.cursor()
# #     updates = []
# #     params = []

# #     if new_name:
# #         updates.append("DeptName = ?")
# #         params.append(new_name)

# #     if new_description:
# #         updates.append("Description = ?")
# #         params.append(new_description)

# #     if not updates:
# #         return "No fields to update."

# #     params.append(dept_id)

# #     sql = f"UPDATE Department SET {', '.join(updates)} WHERE Dept_id = ?"

# #     try:
# #         cur.execute(sql, tuple(params))
# #         conn.commit()
# #         conn.close()
# #         return "Department updated successfully!"
# #     except Exception as e:
# #         conn.close()
# #         return f"Error: {e}"




# import sqlite3
# from werkzeug.security import check_password_hash

# def dashboard():
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()

#     cur.execute("SELECT COUNT(*) FROM Doctor")
#     dc = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM Patient")
#     pc = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM Appointment")
#     ac = cur.fetchone()[0]
#     conn.close()
#     return dc,pc,ac


# # ADMIN LOGIN - Fixed function name
# def adminlog(username, password):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()

#     cur.execute("SELECT id, username, password, name FROM admin WHERE username = ?", (username,))
#     admin = cur.fetchone()
#     conn.close()
    
#     if admin and check_password_hash(admin[2], password):
#         return True, admin[3]  # (success, admin_name)
#     return False, None

# # DOCTOR MANAGEMENT
# def add_doc(doc_id, dname, mno, email, timings, did):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO Doctor (doc_id, DName, DMobileNumber, Email, Timings, Dept_id)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (doc_id, dname, mno, email, timings, did))
#         conn.commit()
#         result = "Doctor added successfully!"
#     except Exception as e:
#         result = f"Error: {e}"
#     conn.close()
#     return result


# def update_doc(doc_id, new_dname=None, new_mno=None, new_email=None, new_timings=None, new_did=None):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     updates = []
#     params = []
#     if new_dname:
#         updates.append("DName = ?")
#         params.append(new_dname)
#     if new_mno:
#         updates.append("DMobileNumber = ?")
#         params.append(new_mno)
#     if new_email:
#         updates.append("Email = ?")
#         params.append(new_email)
#     if new_timings:
#         updates.append("Timings = ?")
#         params.append(new_timings)
#     if new_did:
#         updates.append("Dept_id = ?")
#         params.append(new_did)
#     params.append(doc_id)

#     sql = f"UPDATE Doctor SET {', '.join(updates)} WHERE doc_id = ?"

#     try:
#         cur.execute(sql, tuple(params))
#         conn.commit()
#         result = "Doctor updated successfully!"
#     except Exception as e:
#         result = f"Error: {e}"
#     conn.close()
#     return result


# def delete_doc(doc_id):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("DELETE FROM Doctor WHERE doc_id = ?", (doc_id,))
#         conn.commit()
#         result = "Doctor deleted successfully!"
#     except Exception as e:
#         result = f"Error: {e}"
#     conn.close()
#     return result

# def search_doc(kword):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT doc_id, DName, Email, Timings, DeptName 
#         FROM Doctor 
#         JOIN Department ON Doctor.Dept_id = Department.Dept_id
#         WHERE DName LIKE ? OR DeptName LIKE ? OR doc_id LIKE ?
#     """, (f"%{kword}%", f"%{kword}%",  f"%{kword}%"))

#     result = cur.fetchall()
#     conn.close()
#     return result

# def viewdoc(doc_id):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT Doctor.doc_id, Doctor.DName, Doctor.Email, Doctor.DMobileNumber, Department.Dept_id
#         FROM Doctor
#         JOIN Department ON Doctor.Dept_id = Department.Dept_id
#         WHERE Doctor.doc_id = ?
#     """, (doc_id,))

#     data = cur.fetchone()
#     conn.close()
#     return data


# # PATIENT MANAGEMENT

# def addpat(pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO Patient 
#             (patient_id, PName, PMobileNumber, Email, Gender, DOB, Address, Optional_Contact, Blood_group)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp))

#         conn.commit()
#         result = "Patient added successfully!"
#     except Exception as e:
#         result = f"Error: {e}"

#     conn.close()
#     return result

# def update_pat(pid, new_pname=None, new_mno=None, new_email=None, new_address=None):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     updates = []
#     params = []
    
#     if new_pname:
#         updates.append("PName = ?")
#         params.append(new_pname)
#     if new_mno:
#         updates.append("PMobileNumber = ?")
#         params.append(new_mno)
#     if new_email:
#         updates.append("Email = ?")
#         params.append(new_email)
#     if new_address:
#         updates.append("Address = ?")
#         params.append(new_address)
    
#     if not updates:
#         conn.close()
#         return "No fields to update."
    
#     params.append(pid)
#     sql = f"UPDATE Patient SET {', '.join(updates)} WHERE patient_id = ?"

#     try:
#         cur.execute(sql, tuple(params))
#         conn.commit()
#         result = "Patient updated successfully!"
#     except Exception as e:
#         result = f"Error: {e}"
#     conn.close()
#     return result


# def searchpat(key):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT * FROM Patient 
#         WHERE PName LIKE ? OR PMobileNumber LIKE ? OR patient_id LIKE ?
#     """, (f"%{key}%", f"%{key}%", f"%{key}%"))

#     result = cur.fetchall()
#     conn.close()
#     return result

# def view_pat(patient_id):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT patient_id, PName, Email, PMobileNumber, Address, Gender, DOB, Blood_group
#         FROM Patient
#         WHERE patient_id = ?
#     """, (patient_id,))

#     data = cur.fetchone()
#     conn.close()
#     return data

# def getpatient(patient_id):
#     """Get patient details for editing"""
#     return view_pat(patient_id)

# def blacklistpatient(patient_id):
#     """Delete/blacklist a patient"""
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("DELETE FROM Patient WHERE patient_id = ?", (patient_id,))
#         conn.commit()
#         result = "Patient removed successfully!"
#     except Exception as e:
#         result = f"Error: {e}"
#     conn.close()
#     return result


# # APPOINTMENT MANAGEMENT

# def view_appt():
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT Appointment.App_id, Patient.PName, Doctor.DName, Appointment.Date, Appointment.Time, Appointment.status
#         FROM Appointment
#         JOIN Patient ON Appointment.patient_id = Patient.patient_id
#         JOIN Doctor ON Appointment.doc_id = Doctor.doc_id
#         ORDER BY Date DESC
#     """)
#     data = cur.fetchall()
#     conn.close()
#     return data

# def updateappt(app_id, new_status=None, new_date=None, new_time=None):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         updates = []
#         params = []

#         if new_status:
#             updates.append("status = ?")
#             params.append(new_status)

#         if new_date:
#             updates.append("Date = ?")
#             params.append(new_date)

#         if new_time:
#             updates.append("Time = ?")
#             params.append(new_time)

#         if not updates:
#             return "No fields to update."

#         params.append(app_id)

#         sql = f"UPDATE Appointment SET {', '.join(updates)} WHERE App_id = ?"
#         cur.execute(sql, tuple(params))

#         conn.commit()
#         conn.close()
#         return "Appointment updated!"

#     except Exception as e:
#         return f"Error: {e}"

# def delete_appt(app_id):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("DELETE FROM Appointment WHERE App_id = ?", (app_id,))
#         conn.commit()
#         return "Appointment deleted successfully!"
#     except Exception as e:
#         return f"Error: {e}"
#     finally:
#         conn.close()

# def searchappt(key):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT * FROM Appointment 
#         WHERE App_id LIKE ? OR patient_id LIKE ? OR doc_id LIKE ? OR Date LIKE ? OR Time LIKE ? OR status LIKE ?
#     """, (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"))

#     result = cur.fetchall()
#     conn.close()
#     return result

# # TREATMENT MANAGEMENT
# def view_tmt():
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT Treatment.App_id, Treatment.Tmt_id, Treatment.Diagnosis, Treatment.prescription, Treatment.FollowUp, Treatment.Notes, Treatment.Cost
#         FROM Treatment
#         JOIN Appointment ON Treatment.App_id = Appointment.App_id
#         ORDER BY Appointment.Date
#     """)
#     data = cur.fetchall()
#     conn.close()
#     return data

# def searchtmt(key):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT * FROM Treatment 
#         WHERE Tmt_id LIKE ? OR App_id LIKE ? OR FollowUp LIKE ? 
#     """, (f"%{key}%", f"%{key}%", f"%{key}%"))

#     result = cur.fetchall()
#     conn.close()
#     return result

# # DEPARTMENT MANAGEMENT
# def adddept(dept_id, name, description):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO Department(Dept_id, DeptName, Description)
#             VALUES (?, ?, ?)
#         """, (dept_id, name, description))
#         conn.commit()
#         conn.close()
#         return "Department added successfully!"

#     except Exception as e:
#         return f"Error: {e}"
    
# def viewdept():
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Department")
#     result = cur.fetchall()

#     conn.close()
#     return result

# def searchdept(key):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT * FROM Department 
#         WHERE Dept_id LIKE ? OR DeptName LIKE ?
#     """, (f"%{key}%", f"%{key}%"))
#     result = cur.fetchall()
#     conn.close()
#     return result

# def update_department(dept_id, new_name=None, new_description=None):
#     conn = sqlite3.connect('hospital_mgmt.db')
#     cur = conn.cursor()
#     updates = []
#     params = []

#     if new_name:
#         updates.append("DeptName = ?")
#         params.append(new_name)

#     if new_description:
#         updates.append("Description = ?")
#         params.append(new_description)

#     if not updates:
#         return "No fields to update."

#     params.append(dept_id)

#     sql = f"UPDATE Department SET {', '.join(updates)} WHERE Dept_id = ?"

#     try:
#         cur.execute(sql, tuple(params))
#         conn.commit()
#         conn.close()
#         return "Department updated successfully!"
#     except Exception as e:
#         conn.close()
#         return f"Error: {e}"





import sqlite3
from werkzeug.security import check_password_hash

def dashboard():
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Doctor")
    dc = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Patient")
    pc = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Appointment")
    ac = cur.fetchone()[0]
    conn.close()
    return dc, pc, ac


# ADMIN LOGIN - Fixed function name to adminlog
def adminlog(username, password):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()

    cur.execute("SELECT id, username, password, name FROM admin WHERE username = ?", (username,))
    admin = cur.fetchone()
    conn.close()
    
    if admin and check_password_hash(admin[2], password):
        return True, admin[3]  # (success, admin_name)
    return False, None

# DOCTOR MANAGEMENT
def add_doc(doc_id, dname, mno, email, timings, did):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Doctor (doc_id, DName, DMobileNumber, Email, Timings, Dept_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (doc_id, dname, mno, email, timings, did))
        conn.commit()
        result = "Doctor added successfully!"
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return result

def listdocs():
    conn = sqlite3.connect("hospital_mgmt.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Doctor")
    d = cur.fetchall()
    conn.close()
    return d

def update_doc(doc_id, new_dname=None, new_mno=None, new_email=None, new_timings=None, new_did=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
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


def delete_doc(doc_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Doctor WHERE doc_id = ?", (doc_id,))
        conn.commit()
        result = "Doctor deleted successfully!"
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return result

def search_doc(kwd):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT Doctor.doc_id, Doctor.DName, Doctor.Email, Doctor.DMobileNumber, Doctor.Timings, Department.DeptName
        FROM Doctor
        JOIN Department ON Doctor.Dept_id = Department.Dept_id
        WHERE Department.Dept_id=? OR DeptName=?""",(kwd,kwd))
    r = cur.fetchall()
    conn.close()
    return r


def view_doc(doc_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT Doctor.doc_id, Doctor.DName, Doctor.Email, Doctor.DMobileNumber, Doctor.Timings,Department.Dept_id
        FROM Doctor
        JOIN Department ON Doctor.Dept_id = Department.Dept_id
        WHERE Doctor.doc_id = ?
    """, (doc_id,))

    data = cur.fetchone()
    conn.close()
    return data


# PATIENT MANAGEMENT

def addpat(pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Patient 
            (patient_id, PName, PMobileNumber, Email, Gender, DOB, Address, Optional_Contact, Blood_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pid, pname, mno, email, gen, dob, address, optionalmno, blood_grp))

        conn.commit()
        result = "Patient added successfully!"
    except Exception as e:
        result = f"Error: {e}"

    conn.close()
    return result

def update_pat(pid, new_pname=None, new_mno=None, new_email=None, new_address=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    updates = []
    params = []
    
    if new_pname:
        updates.append("PName = ?")
        params.append(new_pname)
    if new_mno:
        updates.append("PMobileNumber = ?")
        params.append(new_mno)
    if new_email:
        updates.append("Email = ?")
        params.append(new_email)
    if new_address:
        updates.append("Address = ?")
        params.append(new_address)
    
    if not updates:
        conn.close()
        return "No fields to update."
    
    params.append(pid)
    sql = f"UPDATE Patient SET {', '.join(updates)} WHERE patient_id = ?"

    try:
        cur.execute(sql, tuple(params))
        conn.commit()
        result = "Patient updated successfully!"
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return result


def searchpat(key):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Patient 
        WHERE PName LIKE ? OR PMobileNumber LIKE ? OR patient_id LIKE ?
    """, (f"%{key}%", f"%{key}%", f"%{key}%"))

    result = cur.fetchall()
    conn.close()
    return result

def view_pat(patient_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT patient_id, PName, Email, PMobileNumber, Address, Gender, DOB, Blood_group
        FROM Patient
        WHERE patient_id = ?
    """, (patient_id,))

    data = cur.fetchone()
    conn.close()
    return data

def getpatient(patient_id):
    """Get patient details for editing"""
    return view_pat(patient_id)

def blacklistpatient(patient_id):
    """Delete/blacklist a patient"""
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Patient WHERE patient_id = ?", (patient_id,))
        conn.commit()
        result = "Patient removed successfully!"
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return result


# APPOINTMENT MANAGEMENT

def view_appt():
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT Appointment.App_id, Patient.PName, Doctor.DName, Appointment.Date, Appointment.Time, Appointment.status
        FROM Appointment
        JOIN Patient ON Appointment.patient_id = Patient.patient_id
        JOIN Doctor ON Appointment.doc_id = Doctor.doc_id
        ORDER BY Date DESC
    """)
    data = cur.fetchall()
    conn.close()
    return data

def updateappt(app_id, new_status=None, new_date=None, new_time=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
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
            return "No fields to update."

        params.append(app_id)

        sql = f"UPDATE Appointment SET {', '.join(updates)} WHERE App_id = ?"
        cur.execute(sql, tuple(params))

        conn.commit()
        conn.close()
        return "Appointment updated!"

    except Exception as e:
        return f"Error: {e}"

def delete_appt(app_id):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Appointment WHERE App_id = ?", (app_id,))
        conn.commit()
        return "Appointment deleted successfully!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def searchappt(key):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Appointment 
        WHERE App_id LIKE ? OR patient_id LIKE ? OR doc_id LIKE ? OR Date LIKE ? OR Time LIKE ? OR status LIKE ?
    """, (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"))

    result = cur.fetchall()
    conn.close()
    return result

# TREATMENT MANAGEMENT
def view_tmt():
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT Treatment.App_id, Treatment.Tmt_id, Treatment.Diagnosis, Treatment.prescription, Treatment.FollowUp, Treatment.Notes, Treatment.Cost
        FROM Treatment
        JOIN Appointment ON Treatment.App_id = Appointment.App_id
        ORDER BY Appointment.Date
    """)
    data = cur.fetchall()
    conn.close()
    return data

def searchtmt(key):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Treatment 
        WHERE Tmt_id LIKE ? OR App_id LIKE ? OR FollowUp LIKE ? 
    """, (f"%{key}%", f"%{key}%", f"%{key}%"))

    result = cur.fetchall()
    conn.close()
    return result

# DEPARTMENT MANAGEMENT
def adddept(dept_id, name, description):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Department(Dept_id, DeptName, Description)
            VALUES (?, ?, ?)
        """, (dept_id, name, description))
        conn.commit()
        conn.close()
        return "Department added successfully!"

    except Exception as e:
        return f"Error: {e}"
    
def viewdept():
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Department")
    result = cur.fetchall()

    conn.close()
    return result

def searchdept(key):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Department 
        WHERE Dept_id LIKE ? OR DeptName LIKE ?
    """, (f"%{key}%", f"%{key}%"))
    result = cur.fetchall()
    conn.close()
    return result

def update_department(dept_id, new_name=None, new_description=None):
    conn = sqlite3.connect('hospital_mgmt.db')
    cur = conn.cursor()
    updates = []
    params = []

    if new_name:
        updates.append("DeptName = ?")
        params.append(new_name)

    if new_description:
        updates.append("Description = ?")
        params.append(new_description)

    if not updates:
        return "No fields to update."

    params.append(dept_id)

    sql = f"UPDATE Department SET {', '.join(updates)} WHERE Dept_id = ?"

    try:
        cur.execute(sql, tuple(params))
        conn.commit()
        conn.close()
        return "Department updated successfully!"
    except Exception as e:
        conn.close()
        return f"Error: {e}"