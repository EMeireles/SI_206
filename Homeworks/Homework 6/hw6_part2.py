# 507/206 Homework 6 Part 2
import requests
from bs4 import BeautifulSoup
import sys


#### Part 2 ####
print('\n*********** PART 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Part 2 solution goes here

url=sys.argv[1]

html=requests.get(url).text
soup=BeautifulSoup(html,"html.parser")

most_read=soup.find("div",class_="panel-pane pane-mostread")

headlines=most_read.find_all("a")
headlines=list(headlines)

for item in headlines:
	x=item.contents[0]
	print(x)




