# Automatic Identification of Online Harassment of Women Journalists
Research conducted by Columbia Speech Lab
- Ishaan Arora (Columbia MS CS '20)
- Julia Guo (Columbia BA CS '22)

## Overview
In this repository, we have included core code components used to fetch tweet threads potentially containing hate speech from Twitter archive data.

## Structure
`driver.py`: Main driver script for scraping data

`utils.py`: Helper functions used in driver.py

`retrieve_tweet_text.py`: ?

`ways_to_fetch_tweet_threads.py`: Classes for fetching tweet threads

todo @Julia + @Ishaan: explain this better

## How to run code with sample data
We have provided some sample data for fetching tweet threads.

You can run `driver.py` using this sample data (or any files you would like) in the following manner:

```
python driver.py <tweet file path> <mute file path> <twitter username>
```

For example:

```
python driver.py sample_tweet.js sample_mute.js JohnDoe12345
```

todo @Julia + @Ishaan: generate some sample data? maybe?

## To add a new tweet filtering heuristic:
Define a new subclass of TweetThreadsFromSource in ways_to_fetch_tweet_threads.py

Example:
```
class TweetThreadsFromSearch(TweetThreadsFromSource):
```

Override the method `get_tweet_threads_list` in this newly defined class.

todo: explain this better

## Contact information:
Ishaan: ia2419@columbia.edu
Julia: jzg2110@columbia.edu 
