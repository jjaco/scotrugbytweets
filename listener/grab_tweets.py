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

from nlp import extract_entities 

with open('./credentials.yaml', 'r') as f:
	creds = yaml.load(f)

auth = OAuthHandler(creds['consumer']['key'], creds['consumer']['secret'])
auth.set_access_token(creds['access']['key'], creds['access']['secret'])

engine_str = 'postgresql://{0}:{1}@db:5432/scotrugbytweet'.format(creds['postgres']['user'], creds['postgres']['pass'])

engine = create_engine(engine_str)
base = declarative_base()

Session = sessionmaker(engine)
session = Session()

base.metadata.create_all(engine)

class Listener(StreamListener):

    def on_data(self, data):
        tweet_data = json.loads(data)
        print(tweet_data['text'])
        
        tweet = Tweet(
            id=uuid.uuid4(), 
            timestamp=pd.to_datetime(int(tweet_data['timestamp_ms']), unit='ms'), 
            tweet=tweet_data['text'],
            entities=extract_entities(tweet_data['text'])
            )
        
        session.add(tweet)
        session.commit()
        return(True)

    def on_error(self, status):
        print(status)


scottish_rugby_terms = [
	"@Scotlandteam",
	"@GlasgowWarriors",
	"@EdinburghRugby"
]

stream = Stream(auth, Listener())
stream.filter(track=scottish_rugby_terms, stall_warnings=True)
