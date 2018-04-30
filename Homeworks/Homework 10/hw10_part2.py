import sqlite3

DB_NAME = 'tweets.db'

try:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
except Error as e:
    print(e)

def get_most_retweeted_tweet():
	conn=sqlite3.connect(DB_NAME)
	cur=conn.cursor()
	statement="SELECT t.TweetText,t.RetweetCount FROM Tweets AS t ORDER BY t.RetweetCount DESC"
	cur.execute(statement)
	tweet_list=[(tup[0],tup[1])for tup in cur]
	print(str(tweet_list[0][0])+"Number of Retweets: "+str(tweet_list[0][1]))



def get_most_followed_user():
	conn=sqlite3.connect(DB_NAME)
	cur=conn.cursor()
	statement="SELECT t.ScreenName,t.FollowerCount FROM Tweets AS t ORDER BY t.FollowerCount DESC"
	cur.execute(statement)
	tweet_list=[(tup[0],tup[1])for tup in cur]
	print(str(tweet_list[0][0])+"Number of followers: "+str(tweet_list[0][1]))

def get_most_retweeted_user():
	conn=sqlite3.connect(DB_NAME)
	cur=conn.cursor()
	statement="SELECT t.ScreenName,t.RetweetCount FROM Tweets AS t ORDER BY t.RetweetCount DESC"
	cur.execute(statement)
	tweet_list=[(tup[0],tup[1])for tup in cur]
	print(str(tweet_list[0][0])+"Number of Retweets: "+str(tweet_list[0][1]))

def get_tweets_from_most_followed():
	conn=sqlite3.connect(DB_NAME)
	cur=conn.cursor()
	statement="SELECT t.TweetText,t.ScreenName,t.FollowerCount FROM Tweets AS t ORDER BY t.FollowerCount DESC"
	cur.execute(statement)
	follower_list=[(tup[0],tup[1],tup[2])for tup in cur]
	for item in follower_list[:5]:
		print(str(item[0])+" ScreenName: "+str(item[1])+" Follower Count: "+str(item[2]))
def get_trending_location():
	conn=sqlite3.connect(DB_NAME)
	cur=conn.cursor()
	statement="SELECT t.Location,COUNT(t.Location) FROM Tweets AS t GROUP BY t.Location ORDER BY COUNT(t.Location) DESC"
	cur.execute(statement)
	Location_list=[(tup[0],tup[1])for tup in cur]
	for item in Location_list[:5]:
		print(str(item[0])+"Count: "+str(item[1]))

print("Most retweeted Tweet")
get_most_retweeted_tweet()
print("----------------------")
print("Tweets from Most followed User")
get_tweets_from_most_followed()
print("----------------------")
print("Most Followed Users")
get_most_followed_user()
print("----------------------")
print("Most Retweeetd Users")
get_most_retweeted_user()
print("----------------------")
print("Trending Locations")
get_trending_location()
