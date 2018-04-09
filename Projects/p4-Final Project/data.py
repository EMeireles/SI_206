import tweepy
import json
import dstk
import requests

#uses Youtube APIs to gather channel information 
def get_channel_info():
    base_url='https://www.googleapis.com/youtube/v3/search'
    data=requests.get(base_url,params)
    
    

#gets current subscriber count of channel
def get_current_subcribers():
    pass

#scrapes Scoial Blade for subs gained over a period of time
def get_timed_subs():
    pass

#gets revenue over a period of time
def get_timed_rev():
    pass

#gets tweets and gives sentiment analysis 
def get_tweet_senti():
    pass

#gets tweets for youtuber mentioned
def get_tweets():
    pass


