import sqlite3 as sql


def reassign_territory(emp_first_name, emp_last_name, terr_desc):
        conn = sqlite3.connect('Northwind_small.sqlite')
        cur = conn.cursor()
        query = '''
            SELECT Id
            FROM Employee
            WHERE Employee.FirstName = ?
                AND Employee.LastName = ?
        '''
        params = (emp_first_name, emp_last_name)
        cur.execute(query,params)
        emp_id = cur.fetchone()[0]

        query = '''
            SELECT Id
            FROM Territory
            WHERE TerritoryDescription=?
        '''
        params = (terr_desc,)
        cur.execute(query,params)
        terr_id = cur.fetchone()[0]

        update = '''
            UPDATE EmployeeTerritory
            SET Id = ? || '/' || ?,
                EmployeeId = ?
            WHERE TerritoryId = ?
        '''
        params = (emp_id, terr_id, emp_id, terr_id)
        cur.execute(update, params)

        print(cur.rowcount, 'rows inserted')
        conn.commit()
        conn.close()