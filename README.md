# A Novel Methodology for Developing Automatic Harassment Classifiers for Twitter
Research conducted by Columbia University Speech Lab

Part of the [Fourth Workshop on Online Abuse and Harms](https://www.aclweb.org/anthology/volumes/2020.alw-1/) (co-hosted with EMNLP)

Development done by:
- Ishaan Arora (MS '20, Columbia CS)
- Julia Guo (BA '22, Columbia CS)

Advised by:
- Sarah Ita Levitan (Professor, Hunter College; Previous postdoctorate, Columbia CS)
- Susan E. McGregor (Professor, Columbia Journalism & CS)
- Julia Hirschberg (Professor, Columbia CS)

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

## Setting up environment
```
conda create -n <env_name>
conda activate <env_name>
pip install -r requirements.txt
```

## How to run code with Twitter archive data

First, modify the function `get_auth_cred()` in `utils.py` with your appropriate Twitter Developer API keys. If you don't already have these, or are unfamiliar with the Twitter API, please see the below links.
- [Twitter Developer API application](https://developer.twitter.com/en/apply-for-access)
- [Tweepy documentation](http://docs.tweepy.org/en/v3.5.0/auth_tutorial.html)

Next, learn how to download your Twitter Archive [here](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive).

After everything is set up and ready to go, you can run `driver.py` using Twitter archive files (tweet, mute, block) in the following manner:

```
python driver.py --tweet_file=<tweet file path> --mute_file=<mute file path> --block_file=<block file path> --real_name=<real name> --user_name=<twitter username>
```

You can also provide optional arguments that specify the number of tweets to fetch using each method (muted, blocked, non-muted/non-blocked, subtweets). The default values are 100, 100, 200, 100, respectively.

Here is an example command to run:
```
python driver.py \
  --tweet_file="jd_tweet.js" \
  --mute_file="jd_mute.js" \
  --block_file="jd_block.js" \
  --real_name="Jane Doe" \
  --user_name="JaneDoe" \
  --mute_tweets_ct=10 \
  --block_tweets_ct=20 \
  --other_tweets_ct=30 \
  --subtweet_tweets_ct=40
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
