import secrets
import json
import requests

CACHE_FNAME="Youtube_Cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

#class YoutubeChannel(object):
#    """docstring for YoutubeChannel"""
#    def __init__(self, arg):
#        super(YoutubeChannel, self).__init__()
#        self.arg = arg
        


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



YoutubeAPI=secrets.YOUTUBE_API_KEY
#uses Youtube APIs to gather channel information 
def get_channel_info(query):
    base_url='https://www.googleapis.com/youtube/v3/search'
    params={'part':'snippet','q':query,'type':'channel','key':YoutubeAPI}
    tube_data=requests.get(base_url,params)
    data=json.loads(tube_data.text)
    return data
#gets current subscriber count of channel
def get_current_subcribers(id_):
    base_url='https://www.googleapis.com/youtube/v3/channels'
    params={'id':id_,'part':'statistics','key':YoutubeAPI}
    tube_data=requests.get(base_url,params)
    data=json.loads(tube_data.text)
    print(json.dumps(data,indent=2))

#scrapes Scoial Blade for subs gained over a period of time
def get_timed_subs(channel):
    baseurl='https://socialblade.com/youtube/search/{}'.format(channel)


#gets revenue over a period of time
def get_timed_rev():
    pass

#gets tweets and gives sentiment analysis 
def get_tweet_senti():
    pass

#gets tweets for youtuber mentioned
def get_tweets():
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
#get_channel_info('Philip Defranco')
get_current_subcribers('UClFSU9_bUb4Rc6OYfTt5SPw')