import tweepy, json
import random
import os
import sys

# Disable console logging
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore console logging
def enablePrint():
    sys.stdout = sys.__stdout__

# Authorize Twitter API access
def get_auth_cred():
    """
    Returns API object to make twitter search calls
    Return
    ----------
     api: twitter data structure
     use api object to make search/stream/status calls
    """
    auth = tweepy.OAuthHandler("consumer token", "consumer secret")
    auth.set_access_token("key", "secret")
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api

def return_dict(json_file):
    """
    De-serializes json file to a json object 
    Parameters
    ----------
    json_file: string
    json file name

    Return
    ----------
    json_obj
    json object for the json file
    """
    json_obj = None
    with open(json_file, encoding="utf8") as data_file:
        data = data_file.read()
        obj = '''[''' + data[data.find('{') : data.rfind('}') + 1] + ''']'''
        json_obj = json.loads(obj)
    data_file.close()
    return json_obj

def get_muted_ids(muted_file):
    """
    Reads the muted file and returns muted user ids as a set
    Parameters
    ----------
    muted_file: string
    full path to muted.js file uploaded by the user
    Return
    ----------
     mute_set: set
        set of muted user ids
    """
    mute_set = set()
    muted_dict = return_dict(muted_file)
    for index in range(len(muted_dict)):
        mute_set.add(muted_dict[index]["muting"]["accountId"])
    return mute_set

def get_blocked_ids(blocked_file):
    """
    Reads the blocked file and returns blocked user ids as a set
    Parameters
    ----------
    blocked_file: string
    full path to blocked.js file uploaded by the user
    Return
    ----------
     block_set: set
        set of blocked user ids
    """
    block_set = set()
    blocked_dict = return_dict(blocked_file)
    for index in range(len(blocked_dict)):
        block_set.add(blocked_dict[index]["blocking"]["accountId"])
    return block_set

def get_tweets_from_muted(mute_set, tweet_dict, limit):
    """
    Reads the muted set and archive tweets and returns tweets from muted users
    Parameters
    ----------
    mute_set: set
    set of muted ids

    tweet_dict: dictionary
    dictionary of all tweets from archive

    limit: int
    number of tweets to be considered, muted tweets max out after a point

    Return
    ----------
    new_tweet_list: list
    list of tweets from muted users
    """
    new_tweet_list = []
    counter = 0
    for index in range(len(tweet_dict)):
        if counter >= limit:
            return new_tweet_list
        if "in_reply_to_user_id" in tweet_dict[index]["tweet"] and tweet_dict[index]["tweet"]["in_reply_to_user_id"] in mute_set:
            print("Muted user found", tweet_dict[index]["tweet"]["in_reply_to_user_id"])
            new_tweet_list.append(tweet_dict[index])
            counter += 1
    return new_tweet_list

def get_tweets_from_blocked(block_set, tweet_dict, limit):
    """
    Reads the blocked set and archive tweets and returns tweets from blocked users
    Parameters
    ----------
    block_set: set
    set of blocked ids

    tweet_dict: dictionary
    dictionary of all tweets from archive

    limit: int
    number of tweets to be considered, blocked tweets max out after a point

    Return
    ----------
    new_tweet_list: list
    list of tweets from blocked users
    """
    new_tweet_list = []
    counter = 0
    for index in range(len(tweet_dict)):
        if counter >= limit:
            return new_tweet_list
        if "in_reply_to_user_id" in tweet_dict[index]["tweet"] and tweet_dict[index]["tweet"]["in_reply_to_user_id"] in block_set:
            print("Blocked user found", tweet_dict[index]["tweet"]["in_reply_to_user_id"])
            new_tweet_list.append(tweet_dict[index])
            counter += 1
    return new_tweet_list

def get_tweets_from_unmuted_unblocked(mute_set, block_set, tweet_dict, limit):
    """
    Reads the muted and blocked sets and archive tweets and returns tweets from non-muted, non-blocked users
    Parameters
    ----------
    mute_set: set
    set of muted ids

    block_set: set
    set of muted ids

    tweet_dict: dictionary
    dictionary of all tweets from archive

    limit: int
    number of tweets to be considered, muted tweets max out after a point

    Return
    ----------
    new_tweet_list: list
    list of tweets from NON muted users
    """
    new_tweet_list = []
    counter = 0
    for index in range(len(tweet_dict)):
        if counter >= limit:
            return new_tweet_list
        if "in_reply_to_user_id" in tweet_dict[index]["tweet"] and tweet_dict[index]["tweet"]["in_reply_to_user_id"] not in (mute_set or block_set):
            new_tweet_list.append(tweet_dict[index])
            counter += 1
    return new_tweet_list

def get_all_tweets(tweet_file_name, muted_file_name, blocked_file_name, mute_len, block_len, other_len):
    """
    Reads the muted file, blocked file, and archive tweets file and returns final list of tweets 
    whose threads need to be fetched
    Parameters
    ----------
    tweet_file_name: string
    name of tweet archive file

    muted_file_name: string
    name of muted file

    blocked_file_name: string
    name of blocked file

    mute_len: int
    number of muted tweets to fetch

    block_len: int
    number of blocked tweets to fetch

    other_len: int
    number of non-muted, non-blocked tweets to fetch

    Return
    ----------
    tweet_dict: list
    list of tweets whose threads need to be fetched

    mute_set: set
    set of ids from muted users

    block_set: set
    set of ids from blocked users
    """

    # Read tweet, block, mute.js files
    tweet_dict = return_dict(tweet_file_name)    
    mute_set = get_muted_ids(muted_file_name)
    block_set = get_blocked_ids(blocked_file_name)
    print("Set of muted users is:", mute_set)
    print("Set of blocked users is:", block_set)
    
    # Get tweets from muted   
    limit = mute_len
    t1 = get_tweets_from_muted(mute_set, tweet_dict, limit)
    print("Finished retrieving tweets with muted users")
    print("Muted length is:", len(t1))

    # Get tweets from blocked
    limit = block_len
    t2 = get_tweets_from_blocked(block_set, tweet_dict, limit)
    print("Finished retrieving tweets with blocked users")
    print("Blocked length is:", len(t2))
    
    # Get tweets from non-muted, non-blocked
    limit = other_len
    t3 = get_tweets_from_unmuted_unblocked(mute_set, block_set, tweet_dict, limit)
    print("Finished retrieving tweets with non-muted, non-blocked users")
    print("Non-muted, non-blocked length is:", len(t3))
    
    # Combine and return
    tweet_dict = t1 + t2 + t3
    print("Final tweet dict length:", len(tweet_dict))
    
    return tweet_dict, mute_set, block_set

def serialize_tweets(tweet_list):
    """
    Writes list of tweet threads as a json file
    Parameters
    ----------
    tweet_list: list
    list of tweet threads

    Return
    ----------
    None
    writes json folder
    """
    random.seed(123)
    # Shuffle tweets
    random.shuffle(tweet_list)
    s = json.dumps(tweet_list)
    if not os.path.exists('dump'):
        os.makedirs('dump')
    filtered_file_name = os.path.join('dump', 'filtered.json')
    open(filtered_file_name, 'w+').write(s)
    print('Final number of threads written:', len(tweet_list))

# Function to get thread from tweet
def process_status(currentid, user_name, api):
    unique_conversation_peeps = set()
    stack = []
    used = set()
    is_used = False
    while currentid != None:
        if currentid in used:
            is_used = True
            break
        used.add(currentid)
        tweet = None
        try:
            tweet = api.get_status(currentid, tweet_mode="extended")
        except Exception as e:
            print(e)
            break
        unique_conversation_peeps.add(tweet.user.screen_name)
        dic = dict(tweet._json)
        currentid = dic["in_reply_to_status_id_str"]
        ttext = None
        try:
            ttext = tweet.retweeted_status.full_text
        except Exception as e:
            ttext = tweet.full_text
        display_y = tweet.user.screen_name != user_name
        stack.insert(0, {"tweet":ttext,"retweet_count":dic["retweet_count"],"favorite_count":dic["favorite_count"],
                    "user_name":tweet.user.screen_name,"timestamp":str(tweet.created_at),"id":str(tweet.id),"display_tags":display_y})
    if not is_used and len(stack) >= 2:
        if len(unique_conversation_peeps) >= 2:
            stack.reverse()
            return stack
    return None
