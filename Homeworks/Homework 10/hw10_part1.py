import tweepy
import json
import sys
import sqlite3
from secrets import *

DB_NAME = 'tweets.db'

def get_tweets(search_term, num_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=search_term).items(num_tweets)]
    return searched_tweets

def check_table_exists(db,table):
    conn=sqlite3.connect(db)
    cur = conn.cursor()
    statement='SELECT name FROM sqlite_master WHERE type="table" AND name="Tweets"'
    cur.execute(statement)
    tables=[]
    for tbl in cur:
        tables.append(tbl[0])

    if len(tables)!=0:
        return True
    else:
        return False


def init_db(db_name):
    #code to create a new database goes here
    #handle exception if connection fails by printing the error
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)    
    
    #code to test whether table already exists goes here
    table_bool=check_table_exists(db_name,'Tweets')
    #if exists, prompt to user: "Table exists. Delete?yes/no"

    if table_bool==True:
        del_bool=input("Table exists. Delete? yes/no: ")
        
    #if user input is yes, drop table. Else, use move on and use existing table
        if del_bool=='yes':
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
            
        else:
            conn.close()

    #code to create table(if not exists) goes here
    else:
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

    #close database connection
    conn.close()

    #this function is not expected to return anything, you can modify this if you want

def insert_tweet_data(tweets):
    #add code to connect to database and get a Cursor
    conn=sqlite3.connect(DB_NAME)
    cur=conn.cursor()

    #Add code to insert each of these data of interest to the Tweets table
    for tweet in tweets:
        if tweet.user.location=="":
            empty="No Location"
        else:
            empty=tweet.user.location
        insertion = (tweet.id, tweet.text, tweet.retweet_count, tweet.user.id,tweet.user.screen_name,empty,tweet.user.followers_count)
        statement = 'INSERT INTO "Tweets" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    

    #Close database connection
    conn.commit()
    conn.close()

    #Not expecting return, you can modify if you wish

if __name__ == "__main__":
    search_term = input("Enter search term: ")
    num_tweets = int(input("Enter number of tweets to retrieve: "))
    #fetch tweets
    tweets =get_tweets(search_term, num_tweets)
    print("Fetched",len(tweets),"tweets")
    #create database and table
    init_db(DB_NAME)
    #insert data into table
    insert_tweet_data(tweets)
