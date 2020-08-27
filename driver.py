import sys
import argparse
from utils import blockPrint, enablePrint, get_auth_cred, get_all_tweets, serialize_tweets
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

parser.add_argument("--block_file",
                    default = None,
                    type = str,
                    required = True,
                    help = "block.js file from downloaded Twitter archive")

parser.add_argument("--user_name",
                    default = None,
                    type = str,
                    required = True,
                    help = "Twitter username associated with provided files")

args = parser.parse_args()

# Using Twitter API, fetch tweet threads
api = get_auth_cred()

# Pull tweet threads from archive
tweet_dict, mute_set, block_set = get_all_tweets(args.tweet_file, args.mute_file, args.block_file)
tweet_threads_from_archive = TweetThreadsFromArchive(api, tweet_dict, mute_set, block_set, args.user_name)
tweet_threads_archive = tweet_threads_from_archive.get_tweet_threads_list()

# Pull tweet threads from search results
search_query = "from:" + args.user_name
search_results = api.search(q = search_query, count = 100, tweet_mode = "extended")
tweet_threads_from_search = TweetThreadsFromSearch(api, search_results, args.user_name)
tweet_threads_search = tweet_threads_from_search.get_tweet_threads_list()

# Pull together and save in json format
all_tweet_threads = tweet_threads_archive + tweet_threads_search
serialize_tweets(all_tweet_threads)