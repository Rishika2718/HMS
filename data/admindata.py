import sqlite3

# connect to the same database file
conn = sqlite3.connect('hospital_mgmt.db')

# create a cursor to fetch data
cur = conn.cursor()

# example: print all doctors
cur.execute("SELECT * FROM admin;")
admins = cur.fetchall()

print("=== Admin Table ===")
for admin in admins:
    print(admin)

# example: print all departments
cur.execute("SELECT * FROM Department;")
departments = cur.fetchall()

conn.close()
