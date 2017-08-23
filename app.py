from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_bootstrap import Bootstrap
from twitter import getMedia, getTweets, getTeam
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Base, Team, Media, Tweets

app = Flask(__name__)
Bootstrap(app)

engine = create_engine('sqlite:///nba_proj.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

global team

# add route where user types in search term and then will use that as a parameter for getTweets()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/search', methods = ['GET', 'POST'])
def search():

	if request.method == 'POST':
		# get team name
		name = request.form['team']

		# check if valid team
		global team
		team = getTeam(str(name))
		if team == None:
			return render_template('base.html', invalid=True)
		else:
			print('Team selected')
			print(team.screen_name)
			return redirect(url_for('home', name=team.screen_name))
	else:
		return render_template('base.html')

@app.route('/search/<string:name>', methods = ['GET', 'POST'])
def home(name):
	global team
	
	
	# add more tweets and db to media
	# pull the top of each 

	# getMedia(team)
	# getTweets(team)
	# if request.method == 'POST':

	media = session.query(Media).filter(Media.team_id == team.id).all()
	tweets = session.query(Tweets).filter(Tweets.team_id == team.id).all()

	# sort media by likes
	for i in range(len(media)):
		for j in range(i, len(media)):
			if(media[i].likes < media[j].likes):
				media[i], media[j] = media[j], media[i]

	topMedia = []
	for i in range(5):
		topMedia.append(media[i])

	# sort tweets by likes
	for i in range(len(tweets)):
		for j in range(i, len(tweets)):
			if(tweets[i].likes < tweets[j].likes):
				tweets[i], tweets[j] = tweets[j], tweets[i]
	topTweets = []
	for i in range(10):
		topTweets.append(tweets[i])

	# return jsonify(Tweets = [m.serialize for m in topTweets])

	return render_template('search.html', team=team)



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)