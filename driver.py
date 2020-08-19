import sys
from utils import blockPrint,enablePrint,get_auth_cred,get_tweets_from_muted_and_unmuted,serialize_tweets
from ways_to_fetch_tweet_threads import TweetThreadsFromArchive,TweetThreadsFromSearch

#make it false to avoid seeing console logs
ENABLE_PRINT_LOGS=True

if(not ENABLE_PRINT_LOGS):
    blockPrint()
else:
    enablePrint()

tweet_file_name=str(sys.argv[1])
muted_file_name=str(sys.argv[2])
user_nm=str(sys.argv[3])
print(tweet_file_name," ",muted_file_name," ",user_nm)

api=get_auth_cred()
#tweet threads from archive
tweet_dic,mute_set=get_tweets_from_muted_and_unmuted(tweet_file_name,muted_file_name)
tweet_threads_from_archive=TweetThreadsFromArchive(api,tweet_dic,mute_set,user_nm)
tweet_threads_archive=tweet_threads_from_archive.get_tweet_threads_list()
#tweet_threads_archive=[]


#tweet threds from search results
search_query="from:"+user_nm
search_results = api.search(q=search_query, count=100,tweet_mode="extended")
tweet_threads_from_search=TweetThreadsFromSearch(api,search_results,user_nm)
tweet_threads_search=tweet_threads_from_search.get_tweet_threads_list()

all_tweet_threads=tweet_threads_archive+tweet_threads_search

serialize_tweets(all_tweet_threads)
