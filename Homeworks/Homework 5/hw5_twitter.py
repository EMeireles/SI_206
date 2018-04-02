from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize

## SI 206 - HW
##Emil Meriles
##SEC 005

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
data=requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching

CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweet
def get_tweets(username,num_tweets):
	base_url="https://api.twitter.com/1.1/statuses/user_timeline.json"
	prep_URL="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count={}".format(username,num_tweets)
	if prep_URL in CACHE_DICTION:
		print("Pulling Cached Data!")
		return CACHE_DICTION[prep_URL]
	else:
		print("Fetching new information...")
		r= requests.get(base_url,params={"screen_name":username,"count":num_tweets},auth=auth)
		CACHE_DICTION[prep_URL]=json.loads(r.text)
		dumped_tweets=json.dumps(CACHE_DICTION,indent=4)
		fw=open(CACHE_FNAME,"w")
		fw.write(dumped_tweets)
		fw.close()
		return CACHE_DICTION[prep_URL]

#Code for Part 2:Analyze Tweets

def analyze_tweets(dic):
	common_tweets=["https","http","RT"]
	letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	tweets=[]
	for dictionary in dic:
		tweets.append(dictionary['text'])
	word_dic={}
	for strng in tweets:
		word_tokens=word_tokenize(strng)
		filtered=[word for word in word_tokens if not word in stop_words]
		for word in filtered:
			if word[0] in letters and word not in common_tweets:
				if word not in word_dic:
					word_dic[word]=1
				word_dic[word]+=1
				
	tup=[(key,word_dic[key]) for key in word_dic]

	sor_tup=sorted(tup,key=lambda x: x[1],reverse=True)

	return (sor_tup[:5],len(dic))

		

d=get_tweets(username,num_tweets)
freq_words=analyze_tweets(d)

print("Tweets Analyzed:{}".format(freq_words[1]))
print("Most Used words:")
for word in freq_words[0]:
	print("{} ({})".format(word[0],word[1]))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
