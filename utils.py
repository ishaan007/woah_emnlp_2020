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
# TODO: This should not be public information as it's my private access token...
# We should ask for these as arguments from the user.
def get_auth_cred():
    """
    Returns api object to make twitter search calls
    Return
    ----------
     api: twitter data structure
     use api object to make search/stream/status calls
    """
    auth = tweepy.OAuthHandler("j76KWhiYl1e3My0f0V1M336r1", "KLaTTVh8ErzWQ1R90RKVsWhKBfCc2z54zDdJEG47CNXJ85iqIN")
    auth.set_access_token("494384833-RftxP0lJJjJe3Q5fIu4OuiJEZUS9HPs7Zx0lV8Ga", "muClGZZgljeg1BPaCSbtJrm8uYKyuQ5EMqTmIrH4iBLel")
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api

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
    mute_set = {}
    muted_dict = return_dict(muted_file)
    for index in range(len(muted_dict)):
        id = muted_dict[index]["muting"]["accountId"]
        mute_set[id] = 1
    return mute_set

def get_tweets_from_muted(mute_set, tweet_dict, limit):
    """
    Reads the muted set and archive tweets and returns tweets from muted users
    Parameters
    ----------
    muted_set: set
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

def get_tweets_from_unmuted(mute_set, tweet_dict, limit):
    """
    Reads the muted set and archive tweets and returns tweets from non-muted users
    Parameters
    ----------
    muted_set: set
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
        if "in_reply_to_user_id" in tweet_dict[index]["tweet"] and tweet_dict[index]["tweet"]["in_reply_to_user_id"] not in mute_set:
            new_tweet_list.append(tweet_dict[index])
            counter += 1
    return new_tweet_list

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
    prev_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    # TODO: This doesn't actually work if the file does not already exist
    # Have to create file
    fitered_file_name = os.path.join(prev_path, "dump", "filtered.json")
    open(fitered_file_name, "w").write(s)

def return_dict(json_file):
    """
    De-serializes json file to a json object
    Parameters
    ----------
    json file: string
    json file name

    Return
    ----------
    jsonObj
    json object for the json file
    """
    jsonObj = None
    with open(json_file) as dataFile:
        data = dataFile.read()
        obj = '''[''' + data[data.find('{') : data.rfind('}') + 1] + ''']''' # TODO: What is this doing? Can you leave a comment
        jsonObj = json.loads(obj)
    dataFile.close()
    return jsonObj

def get_tweets_from_muted_and_unmuted(tweet_file_name, muted_file_name):
    """
    Reads the muted file and archive tweets file and returns final list of tweets 
    whose threads need to be fetched
    Parameters
    ----------
    tweet_file_name: string
    name of tweet archive file

    muted_file_name: string
    name of muted file

    Return
    ----------
    tweet_dict: list
    list of tweets whose threads need to be fetched

    muted_set: set
    set of ids from muted users
    """
    # TODO: Why do we need the below block of code?
    muted_dict = []
    muted = {}
    
    try:
        muted_dict = return_dict(muted_file_name)
    except Exception as e:
        print(e)
        pass
    
    for i in range(len(muted_dict)):
        muted[muted_dict[i]["muting"]["accountId"]] = 1 # TODO: Why do we set account ID to 1?
    # TODO: Since we never use muted_dict and muted again afterwards??

    tweet_dict = return_dict(tweet_file_name)    
    mute_set = get_muted_ids(muted_file_name)
    print("Set of muted users is:", mute_set)
    
    # Get tweets from muted
    # TODO: User should be able to set the limit using provided args, this should not be hardcoded?    
    limit = 4000
    t1 = get_tweets_from_muted(mute_set, tweet_dict, limit)
    print("Finished retrieving tweets with muted users")
    print("Muted length is:", len(t1))
    
    # Get tweets from non-muted
    limit = 400
    t2 = get_tweets_from_unmuted(mute_set, tweet_dict, limit)
    print("Finished retrieving tweets with non-muted users")
    print("Non-muted length is:", len(t2))
    
    # Combine and return
    tweet_dict = t1 + t2
    print("Final tweet dict length:", len(tweet_dict))
    
    return tweet_dict, mute_set

# TODO: Ishaan, can you document the purpose of this function
def process_status(currentid, user_name, api):
    # user_name="JessicaHuseman"
    unique_conversation_peeps = set()
    stack = []
    last_dic = None # TODO: unused variable? why?
    used = {}
    is_used = False
    while currentid != None:
        if currentid in used:
            is_used = True
            break
        used[currentid] = 1
        tweet = None
        try:
            tweet = api.get_status(currentid, tweet_mode="extended")
        except Exception as e:
            print(e)
            break
        unique_conversation_peeps.add(tweet.user.screen_name)
        dic = dict(tweet._json)
        keys_list = list(dict(tweet._json).keys()) # TODO: unused variable?
        currentid = dic["in_reply_to_status_id_str"]
        ttext = None
        try:
            ttext = tweet.retweeted_status.full_text
        except Exception as e:
            ttext = tweet.full_text
        # print(ttext)
        # print(dic)
        last_dic = dic
        display_y = tweet.user.screen_name != user_name
        # TODO: This is kind of unwieldy... should create dict object, set attributes, and then insert that
        stack.insert(0, {"tweet":ttext,"retweet_count":dic["retweet_count"],"favorite_count":dic["favorite_count"],
                    "user_name":tweet.user.screen_name,"timestamp":str(tweet.created_at),"id":str(tweet.id),"display_tags":display_y})
        # stack.insert(0, ttext)
    if not is_used and len(stack) >= 2:
        if len(unique_conversation_peeps) >= 2:
            stack.reverse()
            return stack
    return None
