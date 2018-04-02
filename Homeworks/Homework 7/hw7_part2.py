# 507/206 Homework 7 Part 2
import hw7_part1

count = 0
#### Your Part 2 solution goes here ####
student_list=hw7_part1.get_umsi_data()

for student in student_list:
	if student[1]=='PhD student':
		count+=1


#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
