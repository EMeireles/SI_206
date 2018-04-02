#Emil Meireles
#emimeirl
#Project 2- National Park Service Scraping
import requests
import json
from bs4 import BeautifulSoup
import secrets
from requests_oauthlib import OAuth1

#Importing Secrets form Secrets.py
API_KEY=secrets.twitter_api_key
API_SECRET=secrets.twitter_api_secret
ACCESS_TOKEN=secrets.twitter_access_token
ACCESS_SECRET=secrets.twitter_access_token_secret

#Class to parse the data from the NPS website. This class primarliy uses the last parameter to take in "soup" and parse it
class NationalSite:
    def __init__(self, type_='', name='', desc='', address_street='',address_city='',address_state='',address_zip='', soup=None):
        if soup!=None:
            try:
                self.type=soup[0][0].contents[0]
            except:
                self.type='Unclassified'
            self.name = soup[1][0].contents[0].contents[0]
            self.description = soup[2][0].contents[0]
            

            #Code block for parsing the address information 
            self.address_street = soup[3].strip()
            self.address_city = soup[4].strip()
            self.address_state = soup[5].strip()
            self.address_zip = soup[6].strip()

        else:
            self.type=type_
            self.name=name
            self.desc=desc
            self.address_street=address_street
            self.address_city=address_city
            self.address_state=address_state
            self.address_zip=address_zip
    def __str__(self):
        return "{} ({}): {}, {}, {} {}".format(self.name,self.type, self.address_street,self.address_city,self.address_state, self.address_zip)

#Class to parse the data from the Google API. This class primarliy uses the last parameter to take in a dictionary and parse it.
class NearbyPlace():
    def __init__(self, name='',cat='',json=None):
        if json!=None:
            self.name = json[0]
            self.cat=json[1][0]
        else:
            self.name=name
            self.cat=cat

    def __str__(self):
        return "{} [closest description:{} ]".format(self.name,self.cat)

#Class to parse the data from the Twitter API. This class primarily uses the last parameter to take in a dictionary and parse it.
class Tweet:
    def __init__(self,text='',username='',creation_date='',num_retweets='',num_favorites='',popularity_score=0,id_='',is_retweet=False,json=None):
        if json!=None:
            self.text=json['text']
            self.username=json['user']['screen_name']
            self.creation_date=json['created_at']
            self.num_retweets=json['retweet_count']
            self.num_favorites=json['favorite_count']
            if self.text[:2]=='RT':
                self.is_retweet=True
            else:
                self.is_retweet=False
            self.popularity_score=(self.num_retweets*2)+(self.num_favorites*3)
            self.id_=json['id']
        else:
            self.text=text
            self.username=username
            self.creation_date=creation_date
            self.num_retweets=num_retweets
            self.num_favorites=num_favorites
            self.popularity_score=popularity_score
            self.id=id_
            self.is_retweet=is_retweet


    def __str__(self):
        return """
        @{}: {}
        [retweeted {} times]
        [favorited {} times]
        [popularity {}]
        [tweeted on {} | id:{}]
        """.format(self.username,self.text,self.num_retweets,self.num_favorites,self.popularity_score,self.creation_date,self.id_)

#Code block to set up file for Caching
try:
    fref=open('NPS_CACHE.json','r')
    data=fref.read()

    CACHE_DICT = json.loads(data)
    fref.close()

except:
    CACHE_DICT={}

#Dictionary of state Abreviatoins for use in main()
state_abbr_dict = {
        'ak': 'Alaska',
        'al': 'Alabama',
        'ar': 'Arkansas',
        'as': 'American Samoa',
        'az': 'Arizona',
        'ca': 'California',
        'co': 'Colorado',
        'ct': 'Connecticut',
        'dc': 'District of Columbia',
        'de': 'Delaware',
        'fl': 'Florida',
        'ga': 'Georgia',
        'gu': 'Guam',
        'hi': 'Hawaii',
        'ia': 'Iowa',
        'id': 'Idaho',
        'il': 'Illinois',
        'in': 'Indiana',
        'ks': 'Kansas',
        'ky': 'Kentucky',
        'la': 'Louisiana',
        'ma': 'Massachusetts',
        'md': 'Maryland',
        'me': 'Maine',
        'mi': 'Michigan',
        'mn': 'Minnesota',
        'mo': 'Missouri',
        'mp': 'Northern Mariana Islands',
        'ms': 'Mississippi',
        'mt': 'Montana',
        'na': 'National',
        'nc': 'North Carolina',
        'nd': 'North Dakota',
        'ne': 'Nebraska',
        'nh': 'New Hampshire',
        'nj': 'New Jersey',
        'nm': 'New Mexico',
        'nv': 'Nevada',
        'ny': 'New York',
        'oh': 'Ohio',
        'ok': 'Oklahoma',
        'or': 'Oregon',
        'pa': 'Pennsylvania',
        'pr': 'Puerto Rico',
        'ri': 'Rhode Island',
        'sc': 'South Carolina',
        'sd': 'South Dakota',
        'tn': 'Tennessee',
        'tx': 'Texas',
        'ut': 'Utah',
        'va': 'Virginia',
        'vi': 'Virgin Islands',
        'vt': 'Vermont',
        'wa': 'Washington',
        'wi': 'Wisconsin',
            'wv': 'West Virginia',
            'wy': 'Wyoming'
    }

#Function from class to make a unique indentifier in the case of parameters. For use in Chaching Function.
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

#Caching function. Gets and retrives data. 
def get_data_using_cache(baseurl,params='',auth=''):
    #If there are paramters, use the params_unique_combination() function, else use baseurl as the unique_ident
    if params!='':
        unique_ident=params_unique_combination(baseurl,params)
    else:
        unique_ident=baseurl

    #Traditional Caching code
    if  unique_ident in CACHE_DICT:
        return CACHE_DICT[unique_ident]

    else:
        '''
        Considering this program has multiple types of requests, 
        this logic block picks the right type of request to use
        '''
        if params!='' and auth!='':
            resp=requests.get(baseurl,params,auth=auth)
        elif params!='' and auth=='':
            resp=requests.get(baseurl,params)
        else:
            resp=requests.get(baseurl)

        CACHE_DICT[unique_ident]=resp.text
        dumped_data=json.dumps(CACHE_DICT,indent=4)
        fref=open('NPS_CACHE.json','w')
        fref.write(dumped_data)
        fref.close()
        return CACHE_DICT[unique_ident]

'''
This function get the national sites for each state based off the state abreviation given. 
It returns a list of sites for the state in the form of instances
'''
def get_sites_for_state(state_abbr):
    #Using state_abbr, get the html of that state's national parks
    base_url='https://www.nps.gov/state/'+ state_abbr + '/index.htm'
    resp=get_data_using_cache(base_url)
    resp_html=resp
    soup=BeautifulSoup(resp_html,'html.parser')

    #Get the blocks of information for the sites.
    park_list=soup.find_all('div',class_='col-md-9 col-sm-9 col-xs-12 table-cell list_left')

    park_soup=[]

    sites=[]

    for park in park_list:
        #Starts parsing the block for the link to go to that park's specific page
        spec=park.find_all('h3')[0].contents[0]['href']
        spec_resp='https://www.nps.gov'
        site_details=spec_resp+spec
        resp=get_data_using_cache(site_details)
        resp_html=resp

        #Parses the page to grab Basic info Link
        soup=BeautifulSoup(resp_html,'html.parser')
        nav_bar_list=soup.find_all('div',id='UtilityNav')
        a_soup=nav_bar_list[0].find_all('a')
        address_link=a_soup[0]['href']

        #Parses the Basic Info page for the Adress information 
        physical_address=spec_resp+address_link
        resp=get_data_using_cache(physical_address)
        resp_html=resp
        soup=BeautifulSoup(resp_html,'html.parser')
        actual_Address=soup.find_all('div', class_='physical-address-container')

        #If there's an adress, get the address, else, Write "No Information to the address"
        if len(actual_Address)>0:
            for a in actual_Address:
                s=a.find_all('span', itemprop='streetAddress')
                city=a.find_all('span', itemprop='addressLocality')
                st=a.find_all('span', itemprop='addressRegion')
                zi=a.find_all('span', itemprop='postalCode')
                #Try/Except Block to catch PO Boxes
                try:
                    s_a=s[0].contents[1].contents[0]
                except:
                    p_box=a.find_all('span',itemprop='postOfficeBoxNumber')
                    s_a=p_box[0].contents[0]
                c_a=city[0].contents[0]
                st_a=st[0].contents[0]
                zi_a=zi[0].contents[0]
                park_soup.append((park.find_all('h2'),park.find_all('h3'),park.find_all('p'),s_a,c_a,st_a,zi_a))
        else:
            s_a="No Information Currently"
            c_a="No Information Currently"
            st_a="No Information Currently"
            zi_a="No Information Currently"
            park_soup.append((park.find_all('h2'),park.find_all('h3'),park.find_all('p'),s_a,c_a,st_a,zi_a))

    #Parse the "soup" and append the instance to the sites list
    for item in park_soup:
       ins=NationalSite(soup=item)
       sites.append(ins)

    return sites

#Returns a list of instances of nearby places using the Google API
def get_nearby_places_for_site(site_object):
    #We must first Geocode the site
    geo_url='https://maps.googleapis.com/maps/api/geocode/json?'

    #The following Try/Except block checks for an actual address using the add_bool
    add_bool=True
    try:
        int(site_object.address_street[0])
    except:
        add_bool=False

    '''
    If we have an actual adress (and not a genral area) use the address for better lat and long, 
    else use the site's name for a more genreal lat and long
    '''
    if add_bool==False:
        params={'address':site_object.name+site_object.type, 'key':secrets.google_geocode_key}
    else:
        params={'address':site_object.address_street+', '+site_object.address_city+', '+site_object.address_state+', '+site_object.address_zip, 'key':secrets.google_geocode_key}


    geo_info=get_data_using_cache(requests.get(geo_url,params).url)
    info=json.loads(geo_info)

    #Gets lat and long
    lat=info['results'][0]['geometry']['location']['lat']
    lng=info['results'][0]['geometry']['location']['lng']

    #Using lat an long, get the nearby places
    near_url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params={'location':str(str(lat)+','+str(lng)), 'radius':str(10000),'key':secrets.google_places_key}
    naer_info=get_data_using_cache(near_url,params)
    n_info=json.loads(naer_info)

    class_List=[]

    for dic in n_info['results']:
        class_List.append((dic['name'],dic['types']))
    
    near_ins_list=[]

    #USe the NearbyPlace class to parse the data and create instances, append the instances to the near_ins_list    
    for n in class_List:
        ins=NearbyPlace(json=n)
        near_ins_list.append(ins)

    return near_ins_list

#Returns a list of instances of Tweets related to the site_object given using the Twitter API
def get_tweets_for_site(site_object):
    #OAtuh block 
    auth = OAuth1(API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_SECRET)
    tweet_url='https://api.twitter.com/1.1/search/tweets.json?'
    params={'q':site_object.name+" "+site_object.type}
    data=get_data_using_cache(tweet_url,params=params,auth=auth)
  

    #Using the Tweet class, create instances and parse the data
    for dic in tweet_resp['statuses']:
        ins=Tweet(json=dic)
        tweet_ins.append(ins)

    #Sort tweet_ins by the popularity score
    sorted_ins=sorted(tweet_ins,reverse=True,key= lambda x: x.popularity_score)

    #If the list is bigger than 11, find the difference from 10 and return a list of 10 tweets, taking off the difference
    if len(sorted_ins)>11:
        lst_len=len(sorted_ins)-10
        return short_tweet_list[0:-lst_len+1]
    #If the list is 11, take off the first tweet and return only 10 tweets
    elif len(sorted_ins)==11:
        return sorted_ins[1:]
    else:
        return sorted_ins

#Prints the help information
def help():
    print("""
          list <stateabbr>
           available anytime
           lists all National Sites in a state
           valid inputs: a two-letter state abbreviation

       nearby <result_number>
           available only if there is an active result set
           lists all Places nearby a given result
           valid inputs: an integer 1-len(result_set_size)

       tweets <result_number>
            available only if there is an active results set
            lists up to 10 most "popular" tweets that mention the selected Site
  
        exit
           exits the program
    
         help
           lists available commands (these instructions)



        """)

#main function
def main():
    #Bool for checking if there is a current data set present
    list_bool=False
    #Primer for commands
    commands=['abc']

    while(commands[0]!='exit'):
        #Takes in input
        c_input=input("Please enter a command or 'help' if you would like a list of available commands: ")
        #Turns input into a list for easy use in the coming logic block
        commands=c_input.split()

        #Print out list of sites for state
        if commands[0]=='list' and commands[1] in state_abbr_dict:
            list_bool=True
            print('Listing sites in '+ state_abbr_dict[commands[1]],end='\n\n')

            site_objs=get_sites_for_state(commands[1])
            num=1
            for sts in site_objs:
                print(str(num)+'. '+sts.__str__())
                num+=1

        #Print the help text
        elif commands[0]=='help' and len(commands)==1:
            help()

        #Print out the nearby places
        elif commands[0]=='nearby' and list_bool==True:
            print('Listing places nearby '+ site_objs[int(commands[1])-1].name)
            near_list=get_nearby_places_for_site(site_objs[int(commands[1])-1])

            if len(near_list)<1:
                print("Sorry, no nearby sites!")
            else:    
                num=1
                for place in near_list:
                    print(str(num)+'. '+place.__str__())
                    num+=1

        #Print out related Tweets
        elif commands[0]=='tweets' and list_bool==True:
            print('Listing tweets related to '+ site_objs[int(commands[1])-1].name)
            tweet_list=get_tweets_for_site(site_objs[int(commands[1])-1])

            if len(tweet_list)<1:
                print("Sorry! No tweets found!")

            else:
                for tweet in tweet_list:
                    if tweet.is_retweet==False:
                        print(tweet.__str__())
                        print("---------------------")

        else:
            print("Sorry! That's not an option!")


if __name__ == '__main__':
    main()
    print('Bye!')