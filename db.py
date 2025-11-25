import sqlite3
from werkzeug.security import generate_password_hash
# Connect to (or create) the database
conn = sqlite3.connect('hospital_mgmt.db')
cur=conn.cursor()
conn.execute("DROP TABLE Department")
conn.execute("DROP TRIGGER IF EXISTS increment_doctor_count;")
conn.execute("DROP TRIGGER IF EXISTS decrement_doctor_count;")
conn.commit()
conn.execute('''
CREATE TABLE IF NOT EXISTS Department(
     Dept_id TEXT PRIMARY KEY,
     DeptName TEXT,
     Description TEXT,
     Doctors_Registered INTEGER DEFAULT 0
);
''')
conn.execute('''
CREATE TABLE IF NOT EXISTS Doctor(
     doc_id TEXT PRIMARY KEY,
     DName TEXT,
     DMobileNumber INTEGER UNIQUE,
     Email TEXT UNIQUE,
     Timings TEXT,
     Dept_id TEXT,
     FOREIGN KEY(Dept_id) REFERENCES Department(Dept_id)
);
''')
conn.execute('''
CREATE TRIGGER IF NOT EXISTS increment_doctor_count
AFTER INSERT ON Doctor
FOR EACH ROW
BEGIN
     UPDATE Department
     SET Doctors_Registered = Doctors_Registered + 1
     WHERE Dept_id = NEW.Dept_id;
END;
''')
conn.execute('''
CREATE TRIGGER IF NOT EXISTS decrement_doctor_count
AFTER DELETE ON Doctor
FOR EACH ROW
BEGIN
     UPDATE Department
     SET Doctors_Registered = Doctors_Registered - 1
     WHERE Dept_id = OLD.Dept_id;
END;
''')
conn.execute("""
INSERT INTO Department(Dept_id, DeptName, Description)
VALUES ('GEN01','GENERAL','General Physician')
""")
conn.commit()
conn.execute("""
INSERT INTO Doctor (doc_id, DName, DMobileNumber, Email, Timings, Dept_id)
VALUES ('D011','Dr.Sulabh Bansal','9362170250','dr.sulab@gmail.com','10 am to 12pm and 2pm to 4pm','GEN01')
""")
conn.commit()
conn.execute('''
CREATE TABLE IF NOT EXISTS Patient(
     patient_id TEXT PRIMARY KEY,
     PName TEXT,
     PMobileNumber INTEGER UNIQUE,
     Email TEXT UNIQUE,
     Gender TEXT CHECK(Gender IN ('Male', 'Female','Other','Prefer not to say')),
     DOB DATE NOT NULL,
     Address TEXT,
     Optional_Contact INTEGER,
     Blood_group TEXT
);
''')
conn.execute("""
INSERT INTO Patient(patient_id,PName,PMobileNumber,Email,Gender,DOB,Address,Blood_group)
VALUES ('P001','Ashika Agrawal','9245678110','ashika@gmail.com','Female','2004-10-09','Old Palasia','A+')
""")
conn.commit()
conn.execute('''
CREATE TABLE IF NOT EXISTS Appointment(
     App_id INTEGER PRIMARY KEY,
     patient_id TEXT,
     doc_id TEXT,
     Date DATE,
     Time TEXT,
     status TEXT CHECK(status IN('Booked','Completed','Cancelled')),
     FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
     FOREIGN KEY(doc_id) REFERENCES Doctor(doc_id)
);
''')
conn.execute("""
INSERT INTO Appointment(App_id,patient_id,doc_id,Date,Time,status)
VALUES (1,'P001','D011','2025-11-10','2 pm','Booked')
""")
conn.commit()
conn.execute('''
CREATE TABLE IF NOT EXISTS Treatment(
     Tmt_id TEXT PRIMARY KEY,
     App_id INTEGER,
     Diagnosis TEXT,
     prescription TEXT,
     FollowUp DATE,
     Notes TEXT,
     Cost INTEGER DEFAULT 0,
     FOREIGN KEY (App_id) REFERENCES Appointment(App_id)
);
''')
conn.execute("""
INSERT INTO Treatment(Tmt_id,App_id,Diagnosis,prescription,FollowUp,Cost)
VALUES('T001','1','Viral','Azithromycin','2025-11-15','250')
""")
conn.commit()
conn.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT
      )
''')
conn.execute("SELECT * FROM admin WHERE username = ?", ("admin@hms.com",))
admin = cur.fetchone()

if not admin:
    hashed_pw = generate_password_hash("admin123")
    conn.execute(
        "INSERT INTO admin (username, password, name) VALUES (?, ?, ?)",
        ("admin@hms.com", hashed_pw, "Super Admin")
    )
print("Admin created → user: admin@hms.com pass: admin123")

conn.commit()
conn.close()



 

