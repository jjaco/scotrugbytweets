import os
import yaml

import csv
import json
import sqlite3
import pandas as pd

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import uuid
from db.models import Tweet

with open('./twitter_credentials.yaml', 'r') as f:
	creds = yaml.load(f)

auth = OAuthHandler(creds['consumer']['key'], creds['consumer']['secret'])
auth.set_access_token(creds['access']['key'], creds['access']['secret'])

engine = create_engine('postgresql://postgres:postgres@localhost:5432/scotrugbytweet')
base = declarative_base()

Session = sessionmaker(engine)
session = Session()

base.metadata.create_all(engine)

class Listener(StreamListener):

    def on_data(self, data):
        tweet_data = json.loads(data)
        print(tweet_data['text'])
        
        tweet = Tweet(id=uuid.uuid4(), timestamp=int(tweet_data['timestamp_ms']), tweet=tweet_data['text'])        
        session.add(tweet)
        session.commit()
        return(True)

    def on_error(self, status):
        print(status)


scottish_rugby_terms = [
	"#AsOne",
	"WarriorNation",
	"#AlwaysEdinburgh"
	"@scotlandteam",
	"@GlasgowWarriors",
	"@EdinburghRugby"
]

stream = Stream(auth, Listener())
stream.filter(track=scottish_rugby_terms)
