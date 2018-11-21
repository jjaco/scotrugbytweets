import os
import yaml
import csv
import tweepy
import pandas as pd

with open('./twitter_credentials.yaml', 'r') as f:
	creds = yaml.load(f)

auth = tweepy.OAuthHandler(creds['consumer']['key'], creds['consumer']['secret'])
auth.set_access_token(creds['access']['key'], creds['access']['secret'])

api = tweepy.API(auth, wait_on_rate_limit=True)

csv_file = open('tweets.csv', 'a')
csv_writer = csv.writer(csv_file)

api_query = tweepy.Cursor(api.search, q='#AsOne', lang='en', since='2018-11-01')

locations = (
	'Scotland', 'SCO', 'Glasgow', 'Edinburgh',
	'Aberdeen',	'Inverness', 'Dundee', 'Perth'
	'Stirling', 'Alba', 'United Kingdom', 'UK'
	)

tweets = []
for tweet in api_query.items():
	if any(location in tweet.user.location for location in locations):
		tweet_data = (tweet.created_at, tweet.text, tweet.user.location)
		tweets.append(tweet_data)

tweets_df = pd.DataFrame(tweets)
tweets_df.columns = ['datetime', 'tweet', 'location']

tweets_df.to_pickle("./tweets_df.pickle")