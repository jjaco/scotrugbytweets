from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Tweet(base):
	__tablename__ = 'tweets'

	id = Column(String, primary_key=True)
	timestamp = Column(Integer)
	tweet = Column(String)
	entities = Column(String)