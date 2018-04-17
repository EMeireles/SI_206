from requests_oauthlib import OAuth1Session
import secrets
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
CACHE_FNAME="Youtube_Cache.json"
db_name='YoutuberDB.db'
client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
resource_owner_key = secrets.TWITTER_ACCESS_TOKEN
resource_owner_secret = secrets.TWITTER_ACCESS_SECRET
YoutubeAPI=secrets.YOUTUBE_API_KEY
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
oauth = OAuth1Session(client_key,client_secret=client_secret, resource_owner_key=resource_owner_key,resource_owner_secret=resource_owner_secret)



try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def init_db(db_name):
    #code to create a new database goes here
    #handle exception if connection fails by printing the error
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)    

    cur=conn.cursor()
    statement = '''
    DROP TABLE IF EXISTS 'Youtubers';
    '''
    cur.execute(statement)
    conn.commit()

    cur=conn.cursor()
    statement = '''
    DROP TABLE IF EXISTS 'YoutubeStats';
    '''
    cur.execute(statement)
    conn.commit()

    cur=conn.cursor()
    statement = '''
    DROP TABLE IF EXISTS 'Tweets';
    '''
    cur.execute(statement)
    conn.commit()


    create_cur=conn.cursor()
    statement= '''
    CREATE TABLE "Youtubers"(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Youtuber' TEXT NOT NULL,
    'TotalGrade' TEXT NOT NULL,
    'SubscriberRank' INTEGER NOT NULL,
    'VideoViewRank' INTEGER NOT NULL,
    'SocialBladeRank' INTEGER NOT NULL,
    'ViewsLastThirty' INTEGER NOT NULL,
    'SubscribersLastThirty' INTEGER NOT NULL,
    'EstimatedYearEarn' REAL NOT NULL
    );
     '''
    create_cur.execute(statement)
    conn.commit()

    statement= '''
    CREATE TABLE "YoutubeStats"(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Uploads' INTEGER NOT NULL,
    'Subscribers' INTEGER NOT NULL,
    'VideoViews' INTEGER NOT NULL,
    'ChannelType' TEXT NOT NULL,
    'YoutuberId' INTEGER,
    FOREIGN KEY (YoutuberId) REFERENCES Youtubers(Id)
    );
     '''
    create_cur.execute(statement)
    conn.commit()

    statement= '''
    CREATE TABLE "Tweets"(
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Tweet' INTEGER,
    'SetniScore' INTEGER NOT NULL,
    'Reference' INTEGER NOT NULL,
    'YoutuberReferencedId' INTEGER NOT NULL,
    FOREIGN KEY (YoutuberReferencedId) REFERENCES Youtubers(Id)
    );
     '''
    create_cur.execute(statement)
    conn.commit()
    conn.close()


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def cache(baseurl, params='',auth=''):
    if params!='':
        unique_ident = params_unique_combination(baseurl,params)
    else:
        unique_ident=baseurl

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]

    else:
        # Make the request and cache the new data
        if params !='' and auth=='':
            resp = requests.get(baseurl, params)
            CACHE_DICTION[unique_ident] = json.loads(resp.text)
        elif params!='' and auth!='':
            resp = oauth.get(baseurl, params=params)
            CACHE_DICTION[unique_ident] = json.loads(resp.text)
        else:
            resp=requests.get(baseurl)
            CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def get_comments(query):
    base_Azure='https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/'+'sentiment'
    headers_Azure={
        'Ocp-Apim-Subscription-Key':secrets.MICRO_KEY,
        'Content-Type':'application/json',
        'Accept':'application/json'
    }
    base_url='https://www.googleapis.com/youtube/v3/search'
    params={'part':'snippet','q':query,'type':'video','key':YoutubeAPI,'maxResults':'25'}
    tube_data=cache(base_url,params)
    v_ids=[]
    for dic in tube_data['items']:
        v_ids.append(dic['id']['videoId'])

    base_comments='https://www.googleapis.com/youtube/v3/commentThreads'
    params_comments={'videoId':'Vgd9mAHjcuo','part':'snippet','key':YoutubeAPI,'maxResults':'100'}
    comment_data=cache(base_comments,params_comments)

    text_list=[]
    for dic in comment_data['items']:
        text_list.append(dic['snippet']['topLevelComment']['snippet']['textDisplay'])

    text_obj=[]

    for comment in text_list:
        documents= {'documents' : [ {'id': '1', 'language': 'en', 'text':comment}]}
        data_Azure=requests.post(base_Azure,headers=headers_Azure,json=documents)
        rating_data=json.loads(data_Azure.text)
        rating=rating_data['documents'][0]['score']
        text_obj.append((comment,rating))

    return text_obj


#scrapes Scoial Blade for all the data
def get_social(channel):
    baseurl='https://socialblade.com/youtube/search/{}'.format(channel)
    dig_url='https://socialblade.com'
    data=cache(baseurl)
    soup=BeautifulSoup(data,'html.parser')
    boxes=soup.find_all('div', style='width: 1200px; height: 88px; background: #fff; padding: 15px 30px; margin: 2px auto; border-bottom: 2px solid #e4e4e4;')
    link=list(boxes[0].find('h2').children)[0]['href']
    

    #Gets Sumamry Data of of Social Balde
    new_page=cache(dig_url+link)
    page_soup=BeautifulSoup(new_page,'html.parser')
    summary=page_soup.find('div',style='width: 1200px; height: 250px; padding: 30px;')
    top=page_soup.find('div',id='YouTubeUserTopInfoBlockTop')
    name=top.find('h1').text.strip()
    stats=top.find_all('span',style='font-weight: bold;')
    top_list=[item.text.strip() for item in stats]
    top_list.append(name)
    summary_list=[]
    for item in summary.find_all('p'):
        summary_list.append(item.text.strip())

    #Scrapes for the subscriber data and revenue data
    detailed_url=page_soup.find('div',id='YouTubeUserMenu')
    nav_list=detailed_url.find_all('a')
    detailed_soup=cache(dig_url+nav_list[2]['href'])
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
    detailed_soup=cache(dig_url+nav_list[1]['href'])
    future_soup=BeautifulSoup(detailed_soup,'html.parser')
    lv1_soup=future_soup.find('div',style='width: 900px; float: left;')
    lv2_soup=lv1_soup.find_all('div',class_='TableMonthlyStats')
    future_list=[]
    for item in lv2_soup:
        future_list.append(item.text.strip())
    return(summary_list,top_list,stat_list,future_list)

def get_tweets(search_term):
    protected_url ='https://api.twitter.com/1.1/search/tweets.json'
    params={'q':search_term,'count':5}
    data=cache(protected_url ,params=params,auth=oauth)
    text=[]
    for dic in data['statuses']:
        text.append(dic['text'])
    return (text,search_term)

    
    

def get_tweet_senti(tweets,socialblade_name):
    base_Azure='https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/'+'sentiment'
    headers_Azure={
        'Ocp-Apim-Subscription-Key':secrets.MICRO_KEY,
        'Content-Type':'application/json',
        'Accept':'application/json'
    }
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()


    common_tweets=["https","http","RT"]
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tweets_l=[]
    for tup in tweets:
        tweets.append(tup[0])


    filtered_tweets=[]
    for strng in tweets_l:
        word_tokens=word_tokenize(strng)
        if word_tokens[0] not in common_tweets:
            filtered_tweets.append(strng)

    tweet_object=[]
    for text in filtered_tweets:
        documents= {'documents' : [ {'id': '1', 'language': 'en', 'text':text}]}
        data_Azure=requests.post(base_Azure,headers=headers_Azure,json=documents)
        rating_data=json.loads(data_Azure.text)
        rating=rating_data['documents'][0]['score']
        tweet_object.append((text,rating))

    return (tweet_object,socialblade_name)

def pop_table(channels):
    conn = sqlite3.connect(db_name)
    cur=conn.cursor()
    social_list=[]
    for youtuber in channels:
        social_list.append(get_social(youtuber))

    for tup_set in social_list:
        insertion = (None,tup_set[1][-1],tup_set[0][0],tup_set[0][2][:-2],tup_set[0][4][:-2],tup_set[0][6][:-2],tup_set[0][8].split('\n')[0],tup_set[0][9].split('\n')[0],float(tup_set[0][12].split('-')[0][1:-2])*1000)
        statement = 'INSERT INTO "Youtubers" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()
        id_cur=conn.cursor()
        statement='''
        SELECT Id FROM Youtubers WHERE Youtubers.Youtuber= '''+"'{}'".format(tup_set[1][-1])
        id_cur.execute(statement)
        Y_id=id_cur.fetchone()[0]
        stats_insert=(None,tup_set[1][0],tup_set[1][1],tup_set[1][2],tup_set[1][4],Y_id)
        statement = 'INSERT INTO "YoutubeStats" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'
        stats_cur=conn.cursor()
        stats_cur.execute(statement,stats_insert)
        conn.commit()

    tweet_list=[]
    for youtuber in channels:
        tweet=get_tweets(youtuber)
    

    for obj in tweet_list:
        for tweets in obj[0]:
            statement='''
            SELECT Id FROM Youtubers WHERE Youtubers.Youtuber= '''+"'{}'".format(obj[1])
            id_cur.execute(statement)
            Y_id=id_cur.fetchone()[0]
            insertion=(None,tweets[0],tweets[1],obj[1],Y_id)
            statement = 'INSERT INTO "Tweets" '
            statement += 'VALUES (?, ?, ?, ?, ?)'
            conn.commit()

    conn.close()

def get_data(spec):
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()
    if spec=='subs':
        statement='''
        SELECT Y.Youtuber,YS.Subscribers FROM Youtubers AS Y JOIN YoutubeStats AS YS ON Y.Id=YS.YoutuberId
        '''
        cur.execute(statement)
        options=cur.fetchall()
        return options
    if spec=='views':
        statement=='''
        SELECT Y.Youtuber,YS.VideoViews FROM Youtubers AS Y JOIN YoutubeStats AS YS ON Y.Id=YS.YoutuberId
        '''
        cur.execute(statement)
        options=cur.fetchall()
        return options
    if spec=='ViewsLastThirty':
        statement='''
        SELECT Y.Youtuber,Y.ViewsLastThirty FROM Youtubers AS Y 
        '''
        cur.execute(statement)
        options=cur.fetchall()
        return options
    if spec=='SubsLastThirty':
        statement='''
        SELECT Y.Youtuber,Y.SubscribersLastThirty FROM Youtubers AS Y 
        '''
        cur.execute(statement)
        options=cur.fetchall()
        return options


yts=['nigahiga','Zerkaa','seananners']
init_db(db_name)
pop_table(yts)
