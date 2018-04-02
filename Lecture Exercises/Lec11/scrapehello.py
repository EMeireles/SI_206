from bs4 import BeautifulSoup


#scrapehello.py

from bs4 import BeautifulSoup

f = open("hello.html")
html = f.read()
soup = BeautifulSoup(html, 'html.parser')


# searching by tag
all_list_items = soup.find_all('li')
all_divs = soup.find_all('div')

# searching by class
all_goodbye_elements = soup.find_all(class_='goodbye')

# searching by tag AND class
all_french_list_items = soup.find_all('li', class_='french')

# searching by id
all_hello_elements = soup.find_all(id='hello-list')


print('list items:', all_list_items)
print('------')
print('divs:', all_divs)
print('------')
print('goodbye elements:', all_goodbye_elements)
print('------')
print('french stuff:', all_french_list_items)
print('------')
print('hello id elements:', all_hello_elements)
print('------')

print(type(all_list_items[0]))
print('-------------')


for li in all_list_items:
  print(li.string)
print('------')


for child in all_hello_elements[0].children:
  print(child.string)
print('------')
