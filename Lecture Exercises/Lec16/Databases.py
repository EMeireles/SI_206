import sqlite3

conn=sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()
cur.execute('SELECT CompanyName FROM Customer WHERE Region="Western Europe"')

cur2=conn.cursor()
cur2.execute('SELECT ProductName FROM Product WHERE Discontinued=1')

cur3=conn.cursor()
cur3.execute('SELECT FirstName, LastName FROM Employee WHERE ReportsTo=2')

cur4=conn.cursor()
cur4.execute('SELECT OrderDate, ShippedDate FROM [Order] WHERE ShipCountry="USA"')


print("Western Europe Custormers:")
print("------------------------------")
for row in cur:
  print(row[0])

print('\n\n\n')
print("Discontinued Products")
print("--------------------------")

for row in cur2:
	print(row[0])

print(end='\n\n\n')
print("Andrew's Employees")
print("--------------------------")

for row in cur3:
	print(row[0],row[1])

print('\n\n\n\n')
print("USA Products")
print("--------------------------")

for row in cur4:
	print(row[0],row[1])

conn.close()