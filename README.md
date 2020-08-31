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
In this repository, we have included core code components used to fetch tweet threads potentially containing hate speech from Twitter archive data. The primary heuristics currently used to fetch this data are:
- Get threads containing blocked and muted users from the target's Twitter archive
- Get threads containing subtweets (mention of real name, but not of username) from the Twitter Search API

## Structure
`driver.py`: Main driver script for scraping data from Twitter archive and Twitter Search API

`utils.py`: Helper Tweet retrieval functions used in `driver.py` and `ways_to_fetch_tweet_threads.py`

`ways_to_fetch_tweet_threads.py`: Classes for fetching tweet threads (from Archive, Search, ...)

## Requirements
- tweepy = 3.9.0
  - See `requirements.txt` for dependencies.

## How to run code with Twitter archive data

First, modify the function `get_auth_cred()` in `utils.py` with your appropriate Twitter Developer API keys. If you don't already have these, or are unfamiliar with the Twitter API, please see the below links.
- [Twitter Developer API application](https://developer.twitter.com/en/apply-for-access) 
- [Tweepy documentation](http://docs.tweepy.org/en/v3.5.0/auth_tutorial.html)

Next, learn how to download your Twitter Archive [here](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive).

After everything is set up and ready to go, you can run `driver.py` using Twitter archive files (tweet, mute, block) in the following manner:

```
python driver.py --tweet_file=<tweet file path> --mute_file=<mute file path> --block_file=<block file path> --real_name=<real name> --user_name=<twitter username>
```

You can also provide optional arguments that specify the number of tweets to fetch using each method (muted, blocked, non-muted/non-blocked, subtweets). The default values are 100, 100, 200, 100, respectively:
```
python driver.py ...... --mute_tweets_ct=10 --block_tweets_ct=10 --other_tweets_ct=20 --subtweet_tweets_ct=10
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