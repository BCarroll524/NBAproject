from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Team(Base):
	__tablename__ = 'team'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	image = Column(String(1000), nullable = False)

	@property
	def serialize(self):
		return {
			'name' : self.name,
			'image' : self.image,
			'id' : self.id
		}

class Media(Base):
	__tablename__ = 'media'

	id = Column(Integer, primary_key = True)
	image = Column(String(1000), nullable = False)
	text = Column(String(300), nullable = False)
	likes = Column(Integer)
	tweet_id = Column(In)
	team_id = Column(Integer, ForeignKey('team.id'))
	team = relationship(Team)

	@property
	def serialize(self):
		return {
			'text' : self.text,
			'image' : self.image,
			'likes' : self.likes,
			'id' : self.id
		}



class Tweets(Base):
	__tablename__ = 'tweets'

	id = Column(Integer, primary_key = True)
	user = Column(String(200), nullable = False)
	text = Column(String(300), nullable = False)
	likes = Column(Integer)
	team_id = Column(Integer, ForeignKey('team.id'))
	team = relationship(Team)

	@property
	def serialize(self):
		return {
			'user' : self.user,
			'text' : self.text,
			'likes' : self.likes,
			'id' : self.id
		}

engine = create_engine('sqlite:///nba_proj.db')
Base.metadata.create_all(engine)
