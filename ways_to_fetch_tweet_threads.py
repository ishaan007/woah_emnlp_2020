from abc import ABCMeta, abstractmethod
import tweepy,json
import random
from utils import process_status

class TweetThreadsFromSource(object):
    __metaclass__ = ABCMeta
    def __init__(self, tweet_dict):
        """
        tweet_dict: list of source tweets
            Can be isolated tweets from archive or tweets
            fetched from search/stream api
        """
        self.tweet_dict = tweet_dict

    @abstractmethod
    def get_tweet_threads_list(self):
      """ To override
      Parameters
      ----------
      None
      Return
      ----------
      tweet_threads : list
          Every element of tweet_threads should be another list of
          entire tweet thread conversation

      """
      pass

class TweetThreadsFromArchive(TweetThreadsFromSource):
    def __init__(self, api, tweet_dict, mute_set, user_name):
      self.api = api
      self.tweet_dict = tweet_dict
      self.mute_set = mute_set
      self.user_name = user_name
    def get_tweet_threads_list(self):
        tweet_list = []
        used = {}
        try:
            for index in range(len(self.tweet_dict)):
                dic = self.tweet_dict[index]["tweet"]
                currentid = dic["id_str"]
                stack = []
                # print("len of tweet list is", len(tweet_list))
                if index % 100 == 0:
                    print(index,"tweets visited")
                    print(len(tweet_list), "actual dump size")
                is_muted=False # TODO: Unused variable
                is_used=False
                if "in_reply_to_user_id" in dic and dic["in_reply_to_user_id"] in self.mute_set:
                    is_muted=True
                if dic["id"] in self.mute_set:
                    is_muted=True
                unique_conversation_peeps = set()

                while currentid != None:
                    if currentid in used:
                        is_used = True
                        break
                    used[currentid] = 1
                    # print(currentid)

                    tweet = None
                    try:
                        tweet = self.api.get_status(currentid, tweet_mode="extended")
                    except Exception as e:
                        print(e)
                        break
                    unique_conversation_peeps.add(tweet.user.screen_name)
                    dic = dict(tweet._json)
                    keys_list = list(dict(tweet._json).keys()) # TODO: Unused variable
                    # print("keys list", keys_list)
                    currentid = dic["in_reply_to_status_id_str"]
                    # print("tweet text is", tweet.text)
                    # print("dictionary looks like", dic)
                    ttext = None
                    try:
                        # print("tweet full text is", tweet.retweeted_status.full_text)
                        ttext = tweet.retweeted_status.full_text
                    except Exception as e:
                        #print("tweet full text is", tweet.full_text)
                        ttext = tweet.full_text
                    display_y = tweet.user.screen_name != self.user_name

                    # TODO: This is super unwieldy, can you rewrite by setting fields 1 by 1
                    stack.append({"tweet":ttext,"retweet_count":dic["retweet_count"],"favorite_count":dic["favorite_count"],
                    "user_name":tweet.user.screen_name,"timestamp":str(tweet.created_at),"id":str(tweet.id),"display_tags":display_y})
                    is_muted = False
                if not is_used and len(stack) > 2:
                    if len(unique_conversation_peeps) >= 2:
                        stack.reverse()
                        tweet_list.append(stack)
        except Exception as e:
            print(e)
            pass
        finally:
            return tweet_list
            #serialize_tweets(tweet_list)
        return tweet_list

class TweetThreadsFromSearch(TweetThreadsFromSource):
    def __init__(self, api, search_results, user_name):
      self.api = api
      self.search_results = search_results
      self.user_name = user_name

    def get_tweet_threads_list(self):
        count = 0
        # TODO: Can you add some comments? Or make more descriptive var names?
        ac_ct = 0
        tweet_list = []
        for tweet in self.search_results:
            dic = json.loads(json.dumps(tweet._json))
            # print(count)
            count = count + 1
            # print(dic["full_text"])
            # print("*******************************************")
            current_id = dic["id_str"]
            # if count == 11:
            stack = process_status(current_id, self.user_name, self.api)
            if stack != None:
                ac_ct = ac_ct + 1
                stack.reverse()
                print("************************************ ", ac_ct)
                tweet_list.append(stack)
        return tweet_list
