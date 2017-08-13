from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Team(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable False)

	@property
	def serialize(self):
		return {
			'name' : self.name,
			'id' : self.id
		}

class Media(Base):
	__tablename__ = 'media'

	id = Column(Integer, primary_key = True)



class Tweets(Base):
	__tablename__ = 'tweets'

	id = Column(Integer, primary_key = True)