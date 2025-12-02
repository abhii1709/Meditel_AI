import sqlite3

conn = sqlite3.connect("meditel.db")
cursor = conn.cursor()

print("\n--- DOCTORS ---")
for row in cursor.execute("SELECT * FROM doctors"):
    print(row)

print("\n--- PATIENTS ---")
for row in cursor.execute("SELECT * FROM patients"):
    print(row)

print("\n--- APPOINTMENTS ---")
for row in cursor.execute("SELECT * FROM appointments"):
    print(row)

conn.close()
