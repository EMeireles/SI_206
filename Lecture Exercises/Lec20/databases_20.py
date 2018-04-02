import sqlite3 as sql

print('#----Q1')
conn=sql.connect('Northwind_small.sqlite')
cur=conn.cursor()
statement='''
SELECT e.FirstName,c.ContactName,c.Phone 
FROM Employee as e
JOIN [Order] AS o
ON o.EmployeeId=e.Id
JOIN Customer AS c
ON o.CustomerId=c.ID
WHERE o.ShippedDate IS NULL
'''
cur.execute(statement)

for tup in cur:
	print(tup[0],tup[1],tup[2])

print('#----Q2')
cur2=conn.cursor()
statement='''
SELECT p.ProductName,COUNT(o.Id)AS OrderCount
FROM Product AS p
JOIN OrderDetail as od
ON od.ProductId=p.Id
JOIN [Order] as o
ON o.Id=od.OrderId
WHERE o.ShippedDate LIKE '2014-%%-%%'
GROUP BY o.Id
'''
cu2.execute(statement)

for item in cur2:
	print(item[0],item[1])

