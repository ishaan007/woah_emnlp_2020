# Automatic Identification of Online Harassment of Women Journalists
Research conducted by Columbia University Speech Lab

Application development done by:
- Ishaan Arora (MS '20, Columbia CS)
- Julia Guo (BA '22, Columbia CS)

Advised by:
- Julia Hirschberg (Professor, Columbia CS)
- Susan E. McGregor (Professor, Columbia Journalism & CS)
- Sarah Ita Levitan (Postdoctorate, Columbia CS)

## Overview
In this repository, we have included core code components used to fetch tweet threads potentially containing hate speech from Twitter archive data.

## Structure
`driver.py`: Main driver script for scraping data from Twitter archive and Twitter Search API

`utils_v2.py`: Helper Tweet retrieval functions used in `driver.py` and `ways_to_fetch_tweet_threads.py`

`ways_to_fetch_tweet_threads.py`: Classes for fetching tweet threads (from Archive, Search, ...)

## Requirements
- tweepy = 3.9.0
  - See `requirements.txt` for dependencies.

## How to run code with Twitter archive data

First, modify the function `get_auth_cred()` in `utils_v2.py` with your appropriate Twitter Developer API keys.

You can run `driver.py` using Twitter archive files in the following manner:

***Note: need to specify user API key***
***Provide some documentation on how to get API key***

```
python driver.py --tweet_file=<tweet file path> --mute_file=<mute file path> --block_file=<block file path> --real_name=<real name> --user_name=<twitter username>
```

You can also provide optional arguments that specify the number of tweets to fetch using each method ([muted, blocked, non-muted/non-blocked, subtweets]; default [100, 100, 200, 100]) from the archive:
```
python driver.py ... --mute_tweets_ct=10 --block_tweets_ct=10 --other_tweets_ct=20 --subtweet_tweets_ct=10
```

After the script finishes running, it will create a new data file, `dump/filtered.json`, containing tweet threads pulled from both the provided Twitter archive files, and the Search API.

## To add a new tweet filtering heuristic:
Define a new subclass of TweetThreadsFromSource in `ways_to_fetch_tweet_threads.py`

Example:
```
class TweetThreadsFromSearch(TweetThreadsFromSource):
```

Override the method `get_tweet_threads_list` in this newly defined class.

## Contact information:
```
Ishaan Arora: ia2419@columbia.edu
Julia Guo: jzg2110@columbia.edu
```