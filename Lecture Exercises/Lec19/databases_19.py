import sqlite3 as sql


print("#Q1------------")
conn=sql.connect('Northwind_small.sqlite')
cur=conn.cursor()
statement='SELECT SupplierId,COUNT(ProductName) AS CountProduct FROM Product GROUP BY SupplierId  ORDER BY CountProduct ASC '
cur.execute(statement)

for tup in cur:
	if tup[1]>=5:
		print(str(tup[0]+tup[1]))

print("#Q2------------")
cur2=conn.cursor()
statement='SELECT Region,COUNT(CompanyName) AS RegionCount FROM Customer GROUP BY Region ORDER BY RegionCount DESC'
cur2.execute(statement)
for tup in cur2:
	print (tup[0]+" "+str(tup[1]))

import sqlite3 as sql


print("#Q3------------")
conn=sql.connect('Northwind_small.sqlite')
cur3=conn.cursor()
statement='''
SELECT e.FirstName,e.Title, COUNT([Order].EmployeeId),[Order].OrderDate
FROM [Order] 
JOIN Employee as e
ON e.Id=[Order].EmployeeId
WHERE [Order].OrderDate LIKE '2014-04-%%'
GROUP BY [Order].EmployeeId
'''
cur3.execute(statement)

for tup in cur3:
	print(tup[0],tup[1],tup[2],tup[3])


print("#Q4------------")
cur4=conn.cursor()
statement='''
SELECT p.ProductName, COUNT(od.ProductId) AS ProductCount FROM OrderDetail AS od 
JOIN Product AS p 
ON p.Id=od.ProductId
JOIN [Order] AS o
ON o.Id=od.OrderId
WHERE o.OrderDate LIKE '2013-%%-%%'
GROUP BY p.ProductName
ORDER BY ProductCount DESC 
'''
cur4.execute(statement)
for tup in cur4:
	print(tup[0],tup[1])




