# 507/206 Homework 11 Part 1
import csv
import sqlite3 as sqlite

#### Part 1 ####
print('\n*********** PART 1 ***********')

# Creates a database called big10.sqlite and drops Teams, Games, &
# Rounds tables if they exist
def create_tournament_db():

    conn = sqlite.connect('big10.sqlite')
    cur = conn.cursor()

    # Code below provided for your convenience to clear out the big10 database
    # This is simply to assist in testing your code.  Feel free to comment it
    # out if you would prefer
    statement = '''
        DROP TABLE IF EXISTS 'Teams';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Rounds';
    '''
    cur.execute(statement)
    conn.commit()

    # Your code to create the tables in the dB goes here

    statement = '''
        CREATE TABLE 'Teams' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Seed' INTEGER,
            'Name' TEXT NOT NULL,
            'ConfRecord' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Games' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Winner' INTEGER NOT NULL,
            'Loser' INTEGER NOT NULL,
            'WinnerScore' INTEGER NOT NULL,
            'LoserScore' INTEGER NOT NULL,
            'Round' INTEGER NOT NULL,
            'Time' TEXT
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Rounds' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'Date' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


def populate_tournament_db():
    conn = sqlite.connect('big10.sqlite')
    cur = conn.cursor()

    # Column order in teams.csv file: Seed,Name,ConfRecord
    with open('teams.csv') as teamsCsvFile:
        teamsData = csv.reader(teamsCsvFile)
        row_num = 0
        for row in teamsData:
            if row_num == 0:
                row_num += 1
            else:
                insertion = (None, row[0], row[1], row[2])
                statement = 'INSERT INTO "Teams" '
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, insertion)

    # Dictionary mapping team names to ids
    teams_dict = {}

    # Get team names and id's
    statement = '''SELECT id, name FROM Teams'''
    cur.execute(statement)
    for team_info in cur:
        teams_dict[team_info[1]] = team_info[0]

    # Column order in games.csv file: Winner,Loser,WinnerScore,LoserScore,Round,Time
    with open('games.csv') as gamesCsvFile:
        gamesData = csv.reader(gamesCsvFile)
        row_num = 0
        for row in gamesData:
            if row_num == 0:
                row_num += 1
            else:
                insertion = (None, teams_dict[row[0]], teams_dict[row[1]],
                row[2], row[3], row[4], row[5])
                statement = 'INSERT INTO "Games" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)

    # Column order in rounds.csv file: Name,Date
    with open('rounds.csv') as roundsCsvFile:
        roundsData = csv.reader(roundsCsvFile)
        row_num = 0
        for row in roundsData:
            if row_num == 0:
                row_num += 1
            else:
                insertion = (None, row[0], row[1])
                statement = 'INSERT INTO "Rounds" '
                statement += 'VALUES (?, ?, ?)'
                cur.execute(statement, insertion)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tournament_db()
    print("Created big10 Database")
    populate_tournament_db()
    print("Populated big10 Database")