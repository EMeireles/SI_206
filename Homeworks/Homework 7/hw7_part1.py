# 507/206 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

def get_data_using_cache(baseurl):
	unique_ident=baseurl
	if  baseurl in CACHE_DICT:
		return CACHE_DICT[baseurl]
	else:
		header={'User-Agent':'SI_CLASS'}
		resp=requests.get(baseurl, headers=header)
		CACHE_DICT[unique_ident]=resp.text
		fref=open('cache_data.json','w')
		dumped_data=json.dumps(CACHE_DICT,indent=4)
		fref.write(dumped_data)
		fref.close()
		return CACHE_DICT[unique_ident]




#### Your Part 1 solution goes here ####
def get_umsi_data():
	list_of_names_and_titles=[]
	for x in range(13):
		baseurl='https://www.si.umich.edu/directory/person/joyojeet-pal?field_person_firstname_value=&field_person_lastname_value=&rid=All&page='+str(x)
		email_url='https://www.si.umich.edu'
		header = {'User-Agent': 'SI_CLASS'}
		resp=get_data_using_cache(baseurl)
		page_html=resp
		page_soup= BeautifulSoup(page_html,"html.parser")
		faculty=page_soup.find_all('div',class_='ds-1col node node-person node-teaser view-mode-teaser clearfix')

		for teacher in faculty:
			des=teacher.find_all('div',class_='field-item even')
			try:
				title=des[3].contents[0]
			except:
				title='N/A'

			
			if title=='':
				title='N/A'

			list_of_names_and_titles.append((des[1].contents[0].contents[0],title))
	return list_of_names_and_titles
	

#### Execute funciton, get_umsi_data, here ####

try:
	fref=open('cache_data.json','r')
	data=fref.read()

	CACHE_DICT = json.loads(data)
	fref.close()

except:
	CACHE_DICT={}



#### Write out file here #####
l=get_umsi_data()
dict_file=open('directory_dict.json','w')
directory={}

for infor in l:
	directory[infor[0]]=infor[1]

dumped_directory=json.dumps(directory,indent=4)

dict_file.write(dumped_directory)
