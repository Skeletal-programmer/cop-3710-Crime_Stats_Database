import cx_Oracle
conn = cx_Oracle.connect('username/password@localhost/XEPDB1')
cur = conn.cursor()

# Insert dats for Agency
agencies = [
    (1, 'Rocky', 'Forensic'),
    (2, 'Granite', 'Investigative'),
    (3, 'Catchem', 'State'),
    (4, 'Summit', 'Private'),
    (5, 'Sentinel', 'Federal'),
    # ... add remaining agencies
]
cur.executemany("INSERT INTO Agency (Agency_ID, Agency_Name, Agency_Type) VALUES (:1, :2, :3)", agencies)

# Insert data for Geograpic
geographics = [
    ('01', 'Tampa', 'FL', 1),
    ('02', 'Orlando', 'CAL', 2),
    ('03', 'Lakeland', 'NY', 3),
    # ... add remaining geographic data
]
cur.executemany("INSERT INTO Geographic (GEO_ID, City, State, Agency_ID) VALUES (:1, :2, :3, :4)", geographics)

# Insert data for Demographic
demographics = [
    ('V1', 19, 'M', 'White', 1, 'AA', 1),
    ('V2', 62, 'F', 'Albino', 2, 'B&E', 2),
    ('V3', 29, 'M', 'Dangerously pale', 3, 'TE', 3),
    # ... add remaining demographic data
]
cur.executemany("""INSERT INTO Demographic (Victim_ID, Age, Gender, Ethnicity, Offender_ID, Crim_Rec, Agency_ID)
                   VALUES (:1, :2, :3, :4, :5, :6, :7)""", demographics)

# Insert data for Victimology
victimology = [
    ('V1', 1, 'AA'),
    ('V2', 2, 'B&E'),
    ('V3', 3, 'TE'),
    # ... add remaining victimology data
]
cur.executemany("INSERT INTO Victimology (Victim_ID, Offender_ID, Crim_Rec) VALUES (:1, :2, :3)", victimology)

# Insert data for Modus_Operandi
modus_operandi = [
    ('R1', 'AA', 'Gun', 'N/A', 'Pyramid Scheme', '01', 'V1', 1),
    ('R2', 'B&E', 'Tactical Shovel', 'Classified', 'Ponsey Scheme', '02', 'V2', 2),
    ('R3', 'TE', 'Pokeball', 'Redacted', 'Drug Mules', '03', 'V3', 3),
    # ... add remaining modus_operandi data
]

cur.executemany("""INSERT INTO Modus_Operandi 
                   (Crim_Rec_ID, Crim_Rec, Weapon, Connections, Tactics, GEO_ID, Victim_ID, Offender_ID)
                   VALUES (:1, :2, :3, :4, :5, :6, :7, :8)""", modus_operandi)

conn.commit()
cur.close()
conn.close()
print("Database populated successfully!")
