import sys
import argparse
from utils import blockPrint, enablePrint, get_auth_cred, get_tweets_from_muted_and_unmuted, serialize_tweets
from ways_to_fetch_tweet_threads import TweetThreadsFromArchive, TweetThreadsFromSearch

# Toggle console logging on/off <> True/False
ENABLE_PRINT_LOGS = True

if not ENABLE_PRINT_LOGS:
    blockPrint()
else:
    enablePrint()

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("--tweet_file",
                    default = None,
                    type = str,
                    required = True,
                    help = "tweet.js file from downloaded Twitter archive")

parser.add_argument("--mute_file",
                    default = None,
                    type = str,
                    required = True,
                    help = "mute.js file from downloaded Twitter archive")

parser.add_argument("--username",
                    default = None,
                    type = str,
                    required = True,
                    help = "Twitter username associated with provided files")

args = parser.parse_args()

# Using Twitter API, fetch tweet threads
api = get_auth_cred()

# Pull tweet threads from archive
tweet_dic, mute_set = get_tweets_from_muted_and_unmuted(args.tweet_file, args.mute_file)
tweet_threads_from_archive = TweetThreadsFromArchive(api, tweet_dic, mute_set, args.username)
tweet_threads_archive = tweet_threads_from_archive.get_tweet_threads_list()

# Pull tweet threads from search results
search_query = "from:" + args.username
search_results = api.search(q = search_query, count = 100, tweet_mode = "extended")
tweet_threads_from_search = TweetThreadsFromSearch(api, search_results, args.username)
tweet_threads_search = tweet_threads_from_search.get_tweet_threads_list()

# Pull together and save in json format
all_tweet_threads = tweet_threads_archive + tweet_threads_search
serialize_tweets(all_tweet_threads)