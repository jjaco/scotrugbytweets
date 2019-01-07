from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Tweet(base):
	__tablename__ = 'tweets'

	id = Column(String, primary_key=True)
	timestamp = Column(DateTime)
	tweet = Column(String)
	entities = Column(String)