import secrets
import json
import tweepy
import sqlite3
import requests
from bs4 import BeautifulSoup
CACHE_FNAME="Youtube_Cache.json"
db_name='YoutubeTweets.db'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params=''):
    if params!='':
        unique_ident = params_unique_combination(baseurl,params)
    else:
        unique_ident=baseurl

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        if params !='':
            resp = requests.get(baseurl, params)
            CACHE_DICTION[unique_ident] = json.loads(resp.text)
        else:
            resp=requests.get(baseurl)
            CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



YoutubeAPI=secrets.YOUTUBE_API_KEY
#uses Youtube APIs to gather channel information 
def get_channel_info(query):
    base_url='https://www.googleapis.com/youtube/v3/search'
    params={'part':'snippet','q':query,'type':'channel','key':YoutubeAPI}
    tube_data=make_request_using_cache(base_url,params)
    return tube_data
#gets current subscriber count of channel
def get_current_subcribers(id_):
    base_url='https://www.googleapis.com/youtube/v3/channels'
    params={'id':id_,'part':'statistics','key':YoutubeAPI}
    tube_data=make_request_using_cache(base_url,params)
    return tube_data

#scrapes Scoial Blade for all the data
def get_social(channel):
    baseurl='https://socialblade.com/youtube/search/{}'.format(channel)
    dig_url='https://socialblade.com'
    data=make_request_using_cache(baseurl)
    soup=BeautifulSoup(data,'html.parser')
    boxes=soup.find_all('div', style='width: 1200px; height: 88px; background: #fff; padding: 15px 30px; margin: 2px auto; border-bottom: 2px solid #e4e4e4;')
    link=list(boxes[0].find('h2').children)[0]['href']
    #Gets Sumamry Data of of Social Balde
    new_page=make_request_using_cache(dig_url+link)
    page_soup=BeautifulSoup(new_page,'html.parser')
    summary=page_soup.find('div',style='width: 1200px; height: 250px; padding: 30px;')
    summary_list=[]
    for item in summary.find_all('p'):
        summary_list.append(item.text.strip())

    #Scrapes for the subscriber data and revenue data
    detailed_url=page_soup.find('div',id='YouTubeUserMenu')
    nav_list=detailed_url.find_all('a')
    detailed_soup=make_request_using_cache(dig_url+nav_list[2]['href'])
    sub_soup=BeautifulSoup(detailed_soup,'html.parser')
    sub_data=sub_soup.find_all('div',style='width: 860px; height: 32px; line-height: 32px; background: #f8f8f8;; padding: 0px 20px; color:#444; font-size: 9pt; border-bottom: 1px solid #eee;')
    stat_list=[]
    for item in sub_data:
        stat_list.append(item.text.strip())
    c_stat_list=[]
    for item in stat_list:
        clean=item.split('\n')
        data_tup=(clean[0],clean[2],clean[4],clean[5],clean[8],clean[9],clean[12])
        c_stat_list.append(data_tup)
    stat_list=c_stat_list
    
    #Scrapes for the projection data
    detailed_soup=make_request_using_cache(dig_url+nav_list[1]['href'])
    future_soup=BeautifulSoup(detailed_soup,'html.parser')
    lv1_soup=future_soup.find('div',style='width: 900px; float: left;')
    lv2_soup=lv1_soup.find_all('div',class_='TableMonthlyStats')
    future_list=[]
    for item in lv2_soup:
        future_list.append(item.text.strip())

    return(summary_list,stat_list,future_list)

def init_db(db_name):
    #code to create a new database goes here
    #handle exception if connection fails by printing the error
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)    

    statement = '''
    DROP TABLE IF EXISTS 'Tweets';
    '''
    cur=conn.cursor()
    cur.execute(statement)
    conn.commit()

    create_cur=conn.cursor()
    statement= '''
    CREATE TABLE "Tweets"(
    'TweetId' INTEGER PRIMARY KEY,
    'TweetText' TEXT NOT NULL,
    'RetweetCount' INTEGER NOT NULL,
    'UserId' TEXT NOT NULL,
    'ScreenName' TEXT NOT NULL,
    'Location' TEXT NOT NULL,
    'FollowerCount' INTEGER NOT NULL
    );
     '''
    create_cur.execute(statement)
    conn.commit()
    conn.close()

consumer_key=secrets.TWITTER_API_KEY
consumer_secret=secrets.TWITTER_API_SECRET
access_token=secrets.TWITTER_ACCESS_TOKEN
access_secret=secrets.TWITTER_ACCESS_SECRET
def get_tweets(search_term, num_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=search_term).items(num_tweets)]
    return searched_tweets


def insert_tweet_data(tweets):
    #add code to connect to database and get a Cursor
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()

    #Add code to insert each of these data of interest to the Tweets table
    for tweet in tweets:
        if tweet.user.location=="":
            empty="No Location"
        else:
            empty=tweet.user.location
        insertion = (tweet.id, tweet.text.encode('utf8'), tweet.retweet_count, tweet.user.id,tweet.user.screen_name,empty,tweet.user.followers_count)
        statement = 'INSERT INTO "Tweets" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    

    #Close database connection
    conn.commit()
    conn.close()
#gets tweets and gives sentiment analysis 
def get_tweet_senti():
    pass



tweets=get_tweets('Phillip Defranco',30)
init_db(db_name)
insert_tweet_data(tweets)
