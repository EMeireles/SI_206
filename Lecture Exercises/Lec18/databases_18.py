import sqlite3
import sys
import csv
data_list=[]

with open('Airport_data.csv', 'r') as f:
    reader = csv.reader(f)
    for item in reader:
        tup=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
        data_list.append(tup)

def init_db():
    conn = sqlite3.connect('airport.db')
    cur = conn.cursor()

    statement='''

    DROP TABLE IF EXISTS 'Airports';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Airports' (
            'Iata' TEXT PRIMARY KEY,
            'Airport' TEXT NOT NULL,
            'City' TEXT NOT NULL,
            'State' TEXT NOT NULL,
            'Country' TEXT NOT NULL,
            'latitude' INTEGER NOT NULL,
            'longitude' INTEGER NOT NULL,
            'TrafficCount' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()


def insert_data(data):
    conn=sqlite3.connect('airport.db')
    cur=conn.cursor()
    

    for tup in data:
        insertion= (tup[0],tup[1],tup[2],tup[3],tup[4],tup[5],tup[6],tup[7])
        statement="INSERT INTO 'Airports'"
        statement += 'VALUES (?,?,?,?,?,?,?,?)'
        cur.execute(statement,insertion)
    conn.commit()
    conn.close()

#insert_data(data_list[1:])

conn=sqlite3.connect('airport.db')
cur=conn.cursor()
statement='UPDATE Airports SET "TrafficCount"=8500 WHERE "Iata"="DTW" '
cur.execute(statement)

statement='SELECT Iata,City,TrafficCount FROM Airports WHERE "State"="MI"'
cur.execute(statement)

for x in cur:
    print(x[0],x[1],x[2])





