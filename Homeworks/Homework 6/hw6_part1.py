# 507/206 Homework 6 Part 1
import requests
from bs4 import BeautifulSoup
import sys

#### Part 1 ####
print('\n*********** PART 1 ***********')
print("Mark's page -- Alt tags\n")

### Your Part 1 solution goes here
url=sys.argv[1]

html=requests.get(url).text
soup=BeautifulSoup(html,"html.parser")
imgs=soup.find_all("img")

for i in imgs:
	try:
		print(i['alt'])
	except:
		print("No alt text associated with this image!")

