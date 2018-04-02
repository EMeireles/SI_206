
from bs4 import BeautifulSoup
import requests
import json


def get_unique_key(url):
  return url  

def make_request_using_cache(url):
    global header
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

class CourseListing:
    def __init__(self, course_num, course_name):
        self.num = course_num
        self.name = course_name

    def init_from_details_url(self, details_url):
        global header
        page_text = make_request_using_cache(details_url)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        self.description = page_soup.find(class_='course2desc').text

    def __str__(self):
        str_ = self.num + ' ' + self.name + '\n\t' + self.description
        return str_

baseurl = 'https://www.si.umich.edu'
catalogurl = baseurl + '/programs/courses/catalog'
header = {'User-Agent': 'SI_CLASS'}
page_text = make_request_using_cache(catalogurl)
page_soup = BeautifulSoup(page_text, 'html.parser')
view_content_section = page_soup.find(class_='view-content')
table_rows = view_content_section.find_all('tr')

course_listings = []
# changing the loop for debugging -- test on a subset before doing all of them
#for row in table_rows:
for i in range(4):
    row = table_rows[i]
    cells = row.find_all('td')
    if len(cells) == 2:
        course_num = cells[0].text.strip()
        course_name = cells[1].text.strip()
        # this gets rid of extra lines--only the first line of
        # multi-line names is kept
        course_name = course_name.split('\n')[0].strip()
        # this gets rid of a trailing colon if it exists
        if course_name[-1] == ':':
            course_name = course_name[:-1]

        course_listing = CourseListing(course_num, course_name)
        details_url = baseurl + cells[0].find('a')['href']
        course_listing.init_from_details_url(details_url)
        course_listings.append(course_listing)

for cl in course_listings:
    print(cl)
    print('_'*40)