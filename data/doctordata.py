import sqlite3

# connect to the same database file
conn = sqlite3.connect('hospital_mgmt.db')

# create a cursor to fetch data
cursor = conn.cursor()

# example: print all doctors
cursor.execute("SELECT * FROM Doctor;")
doctors = cursor.fetchall()

print("=== Doctors Table ===")
for doc in doctors:
    print(doc)

# example: print all departments
cursor.execute("SELECT * FROM Department;")
departments = cursor.fetchall()

print("\n=== Department Table ===")
for dept in departments:
    print(dept)
    
conn.close()

