import sqlite3

# connect to the same database file
conn = sqlite3.connect('hospital_mgmt.db')

# create a cursor to fetch data
cursor = conn.cursor()

# example: print all doctors
cursor.execute("SELECT * FROM Treatment;")
treatments = cursor.fetchall()

print("=== Treatments Table ===")
for tmt in treatments:
    print(tmt)
conn.close()
