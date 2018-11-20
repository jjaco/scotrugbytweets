import os
import yaml
import csv
import tweepy

with open('./twitter_credentials.yaml', 'r') as f:
	creds = yaml.load(f)

auth = tweepy.OAuthHandler(creds['consumer']['key'], creds['consumer']['secret'])
auth.set_access_token(creds['access']['key'], creds['access']['secret'])

api = tweepy.API(auth, wait_on_rate_limit=True)

csv_file = open('tweets.csv', 'a')
csv_writer = csv.writer(csv_file)

api_query = tweepy.Cursor(api.search, q='#AsOne', lang='en', since='2018-11-16')

for tweet in api_query.items():
	csv_writer.writerow([tweet.created_at, tweet.text.encode('utf-8')])