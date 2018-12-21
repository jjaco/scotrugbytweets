from sqlalchemy import Column, Integer, String

from db.base import Base

class Tweet(Base):
	__tablename__ = 'tweets'

	id = Column(String, primary_key=True)
	timestamp = Column(Integer)
	tweet = Column(String)