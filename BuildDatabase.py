import sqlite3 
import json

DBNAME = 'USAF.db'
Squad_JSON_Name = 'AF_squad_updated.json'
Base_JSON_Name = 'AF_base.json'
Aircraft_JSON_Name = 'AF_plane.json'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

statement = "DROP TABLE IF EXISTS 'Squad'"
cur.execute(statement)

statement = '''
        CREATE TABLE 'Squad'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'SquadName' TEXT NOT NULL,
        'CommandName' TEXT NOT NULL,
        'WingName' TEXT NOT NULL,
        'BaseName' TEXT NOT NULL,
        'AircraftName' TEXT NOT NULL,
        'BattleAircraftCode' TEXT NOT NULL
        )
    '''
cur.execute(statement)


statement = "DROP TABLE IF EXISTS 'Airbase'"
cur.execute(statement)

statement = '''
        CREATE TABLE 'Airbase'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'BaseName' TEXT NOT NULL,
        'Latitude' REAL,
        'Longitude' REAL
        )
    '''
cur.execute(statement)


statement = "DROP TABLE IF EXISTS 'Aircraft'"
cur.execute(statement)

statement = '''
        CREATE TABLE 'Aircraft'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'AircraftName' TEXT NOT NULL,
        'Role' TEXT NOT NULL,
        'Manufacturer' TEXT NOT NULL,
        'MaxSpeed' REAL,
        'CombatRadius' REAL
        )
    '''
cur.execute(statement)


###Read from JSON for Squad
with open(Squad_JSON_Name) as f:
    cache_contents = f.read()
    Squad_CD = json.loads(cache_contents)

for i in Squad_CD:
    row = [0,1,2,3,4,5]
    row[0] = i["squad_nm"]
    row[1] = i["command_nm"]
    row[2] = i["wing_nm"]
    row[3] = i["base_nm"]
    row[4] = i["aircraft_nm"]
    row[5] = i["BAid"]
    statement = '''INSERT INTO Squad VALUES (NULL, ?, ?, ?, ?, ?, ?)'''
    cur.execute(statement, row)


###Read from JSON for Airbase
with open(Base_JSON_Name) as f:
    cache_contents = f.read()
    Base_CD = json.loads(cache_contents)

for i in Base_CD:
    row = [0,1,2]
    row[0] = i["base_nm"]
    row[1] = i["lat"]
    row[2] = i["lon"]
    statement = '''INSERT INTO Airbase VALUES (NULL, ?, ?, ?)'''
    cur.execute(statement, row)


###Build a Database for Aircraft
Aircraft_Info_List = [["A10", "Ground-attack Aircraft", "FR", 833, 460],
                      ["F15", "Air Superiority Fighter", "McDonnell Douglas", 2665, 1967],
                      ["F16", "Multirole Fighter", "General Dynamics, Lockheed Martin", 2120, 550],
                      ["F22", "Stealth Air Superiority Fighter", "Lockheed Martin, Boeing", 2410, 852],
                      ["F35", "Stealth Multirole Fighter", "Lockheed Martin", 1930, 1407],
                      ["NA", "NA", "NA", 0, 0]]

for i in Aircraft_Info_List:
    statement = '''INSERT INTO Aircraft VALUES (NULL, ?, ?, ?, ?, ?)'''
    cur.execute(statement, i)





conn.commit()
conn.close()




