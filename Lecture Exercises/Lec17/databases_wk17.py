import sqlite3

conn=sqlite3.connect('Northwind_small.sqlite')
cur=conn.cursor()
cur.execute('SELECT o.Id,o.ShippedDate,s.CompanyName, s.Phone FROM [Order] AS o JOIN Shipper AS s ON s.ID=o.shipVia')

cur2=conn.cursor()
cur2.execute('SELECT o.Id, o.Freight FROM [Order] AS o JOIN Shipper AS s ON s.Id = o.ShipVia WHERE s.CompanyName = "United Package" AND o.Freight > 100')

cur3=conn.cursor()
cur3.execute('SELECT c.CompanyName,o.ShipCountry FROM [Order] AS o JOIN Customer AS c ON c.Id=o.CustomerId WHERE o.ShippedDate> "2012-10"')

cur4=conn.cursor()
cur4.execute('SELECT e.FirstName,e.LastName,e.ReportsTo FROM Employee AS e WHERE e.ReportsTo="2"')



print("Problem 1 Lec Excercise")
print("-----------------------------------")
for item in cur:
	print(item[0],item[1],item[2],item[3],end='\n\n')

print("Problem 2 Lec Excercise")
print("-----------------------------------")
for item in cur2:
	print(item[0],item[1], end='\n\n')

print("Problem 3 Lec Excercise")
print("-----------------------------------")
for item in cur3:
	print(item[0],item[1], end='\n\n')

print("Problem 4 Lec Excercise")
print("-----------------------------------")
for item in cur4:
	print(item[0],item[1],item[2], end='\n\n')


