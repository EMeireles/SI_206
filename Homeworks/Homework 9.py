'''
HW09: Basic SQL statements
'''

import sqlite3 as sqlite
conn=sqlite.connect('Northwind_small.sqlite')

#----- Q1. Show all rows from the Region table
print("#----Q1")
print('Id','|','RegionDescription')
cur=conn.cursor()
statement='SELECT Id,RegionDescription FROM "Region"'
cur.execute(statement)

for row in cur:
	print(row[0],row[1])

#----- Q2. How many customers are there? 
print("#----Q2")
cur2=conn.cursor()
statement='SELECT Id FROM "Customer"'
cur2.execute(statement)

num=0
for item in cur2:
	num+=1
print(num)

#----- Q3. How many orders have been made? 
print("#----Q3")
cur3=conn.cursor()
statement='SELECT Id FROM "Order"'
cur3.execute(statement)
num=0
for item in cur3:
	num+=1
print(num)
#----- Q4. Show the first five rows from the Product table 
print("#----Q4")
cur4=conn.cursor()
statement="SELECT * FROM 'Product' LIMIT 5"
cur4.execute(statement)


for row in cur4:
	print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])

#----- Q5. Show all available categories
print("#----Q5")
cur5=conn.cursor()
statement="SELECT Id,CategoryName FROM 'Category'"
cur5.execute(statement)

for item in cur5:
	print(str(item[1])+' --> Id: '+ str(item[0]))

#----- Q6. Show the five cheapest products 
print("#----Q6")
cur6=conn.cursor()
statement="SELECT ProductName,UnitPrice  FROM 'Product'"
cur6.execute(statement)

cheap_list=[]
for item in cur6:
	cheap_list.append(item)
cheap_list_2=sorted(cheap_list,key= lambda x:x[1])

for cheap in cheap_list_2[:5]:
	print(cheap[0]+ " Price: "+ str(cheap[1]))

#----- Q7. Show all products that have more than 100 units in stock
print("#----Q7")
cur7=conn.cursor()
statement="SELECT ProductName FROM 'Product' WHERE 'UnitsInStock'>100"
cur7.execute(statement)

for item in cur7:
	print(item[0])


#----- Q8. Show all columns in the Order table
print("#----Q8")
cur8=conn.cursor()
statement="PRAGMA table_info('Order')"
cur8.execute(statement)

for item in cur8:
	print(item[1])


#----- Q9. Identify each employee's first name and the number of order each employee has made. Sort them by the total number of orders in decreasing order
print("#----Q9")
cur9=conn.cursor()
statement="SELECT e.FirstName,o.EmployeeID,count(*) FROM [Order] as o JOIN 'Employee' as e WHERE e.Id=o.EmployeeId GROUP BY o.EmployeeId"
cur9.execute(statement)

for item in cur9:
	print("{} | Id:{} | Count:{}".format(item[0],item[1],item[2]))


#----- Q10. Identify the products and the corresponding supply companies in Ann Arbor 
print("#----Q10")
cur10=conn.cursor()
statement="SELECT s.CompanyName,ProductName FROM Product JOIN 'Supplier' as s ON Product.SupplierId=3 WHERE Product.SupplierId=s.Id"
cur10.execute(statement)

for item in cur10:
	print(item[0]+"|"+item[1])



