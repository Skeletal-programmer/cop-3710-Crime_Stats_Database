'''
If you are running this code first time, and you don't have oracledb installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install oracledb
'''

import oracledb

# --- CONFIGURATION ---
# Path to your extracted Instant Client (Required for FreeSQL/Cloud or older oracle DB versions)
LIB_DIR = r"C:\oracle\instantclient_11_2"


# Your Oracle Credentials
DB_USER = "cop3710" # or your FreeSQL username
DB_PASS = "sp2026" # your password for the dbms user
DB_DSN  = "127.0.0.1:1521/XE" # or your FreeSQL DSN
#jdbc:oracle:thin:@127.0.0.1:1521:XE
# 1. Initialize Thick Mode (Required for encrypted Cloud/FreeSQL connections)
if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=db.freesql.com)
else: oracledb.enable_thin_mode()

# 2. Establish Connection
conn = oracledb.connect(user=GCOFFEY0744_SCHEMA_CC17P, password=LG!TAVU11CFLEFBBQ0P75Ap13S6JAL, dsn=23ai_34ui2)
cursor = conn.cursor()
print("Connected to Oracle Database")

# 3. Insert data
def create_record(name, email):

    sql = "INSERT INTO students (name, email) VALUES (:1, :2)"

    cursor.execute(sql, [name, email])
    conn.commit()
    print(f"Created record for {name}")

create_record("Florida Poly Student", "student@floridapoly.edu")

# 4. Fetch data
def read_records():
    print("\n--- Student Directory ---")
    cursor.execute("SELECT name, email FROM students")
    for row in cursor:
        print(f"Name: {row[0]} | Email: {row[1]}")

read_records()

# 5. Modify data
def update_email(student_id, new_email):
    sql = "UPDATE students SET email = :1 WHERE id = :2"
    cursor.execute(sql, [new_email, student_id])
    conn.commit()
    print(f"Updated Student {student_id} successfully.")

# 6. Delete data
def delete_record(student_email):
    sql = "DELETE FROM students WHERE email = :1"
    cursor.execute(sql, [student_email])
    conn.commit()
    print(f"Deleted Student {student_email} successfully.")

# 7. Closing connection
cursor.close()
conn.close()
print("Oracle connection closed.")
