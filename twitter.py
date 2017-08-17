import tweepy
import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Base, Team, Media, Tweets

CONSUMER_KEY = 'iBaC5IkDaRNzFp7VU8ijeEDa6'
CONSUMER_SECRET = 'G8SkwtF63MxWLGQP4gmnRZTkAs7Xqi3B5w1p0PQS2jkZDZlUVG'
ACCESS_TOKEN = '387527916-FMWSYRpM6qurZuqdJXlAv5tClZRoAPx6YJ4iJ2S2'
ACCESS_TOKEN_SECRET = 'omu5WUCZT1jkyQaFOxaH7RjOQbSn9fbg9fwgWGImLZZAy'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

engine = create_engine('sqlite:///nba_proj.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


def getTweets(team):
	tweets = []
	for tweet in tweepy.Cursor(api.search, q=team.name, result_type='popular', count=1000).items(1000):
		tweets.append(tweet)
	print(len(tweets))
	for i in range(len(tweets)):
		for j in range(i, len(tweets)):
			if (tweets[i].favorite_count < tweets[j].favorite_count):
				tweets[i], tweets[j] = tweets[j], tweets[i]
	print(len(tweets))

	for tweet in tweets:
		if len(session.query(Tweets).filter(Tweets.tweet_id == tweet.id).all()) == 0:
			print('tweet not in DB')
			newTweet = Tweets(user = tweet.user.name, text = tweet.text)
			newTweet.tweet_id = tweet.id
			newTweet.likes = tweet.favorite_count
			newTweet.team_id = team.id
			session.add(newTweet)
			session.commit()
		else:
			print('tweet in db')

	return tweets 

def findTeam(text):
	users = api.search_users(q=text, per_page=1, page=1)
	official = users[0]
	for user in users:
		if str(user.verified) == 'True' and user.url:
			if official.followers_count < user.followers_count:
				official = user
	return official


def getMedia(user):
	media = []
	tweets = api.user_timeline(screen_name=str(user.screen_name), count=200, page=1)
	print(len(tweets))
	for tweet in tweets:
		if tweet.entities.get('media') and tweet.favorite_count > 0:
			url = tweet.entities.get('media')[0].get('media_url')
			sizes = tweet.entities.get('media')[0].get('sizes')
			pic = {
				'url' : url,
				'text' : tweet.text,
				'sizes' : sizes,
				'likes' : tweet.favorite_count,
				'id' : tweet.id
			}
			media.append(pic)

	# sort media by most likes
	for i in range(len(media)):
		for j in range(i, len(media)):
			if(media[i].get('likes') < media[j].get('likes')):
				media[i], media[j] = media[j], media[i]

	topMedia = []
	for x in range(5):
		topMedia.append(media[x])

	print(topMedia[0].get('sizes').get('medium').get('w'))
	for media in topMedia:
		newMedia = Media(image = media.get('url'), text = media.get('text'))
		newMedia.likes = media.get('likes')
		newMedia.tweet_id = media.get('id')
		newMedia.width = media.get('sizes').get('medium').get('w')
		newMedia.height = media.get('sizes').get('medium').get('h')
		newMedia.team_id = user.id
		session.add(newMedia)
	session.commit()


	return topMedia

def populateEast():
	east = []

	east.append(findTeam('celtics'))
	east.append(findTeam('toronto raptors'))
	east.append(findTeam('nyknicks'))
	east.append(findTeam('76ers'))
	east.append(findTeam('brooklyn nets'))
	east.append(findTeam('cavs'))
	east.append(findTeam('bucks'))
	east.append(findTeam('pacers'))
	east.append(findTeam('chicago bulls'))
	east.append(findTeam('detroit pistons'))
	east.append(findTeam('washington wizards'))
	east.append(findTeam('heat'))
	east.append(findTeam('charlotte hornets'))
	east.append(findTeam('orlando magic'))

	for team in east:
		newTeam = Team(name = team.name, image = team.profile_image_url, screen_name = team.screen_name)
		newTeam.user_id = team.id
		session.add(newTeam)
		session.commit()

def populateWest():
	west = []

	west.append(findTeam('spurs'))
	west.append(findTeam('clippers'))
	west.append(findTeam('jazz'))
	west.append(findTeam('thunder'))
	west.append(findTeam('trail blazers'))
	west.append(findTeam('denver nuggets'))
	west.append(findTeam('dallas mavericks'))
	west.append(findTeam('lakers'))
	west.append(findTeam('phoenix suns'))
	west.append(findTeam('sacramento kings'))

	for team in west:
		newTeam = Team(name = team.name, image = team.profile_image_url, screen_name = team.screen_name)
		newTeam.user_id = team.id
		session.add(newTeam)
		session.commit()

def populateOthers():
	teams = []
	teams.append(api.get_user('warriors'))
	teams.append(api.get_user('houstonrockets'))
	teams.append(api.get_user('memgrizz'))
	teams.append(api.get_user('pelicansnba'))
	teams.append(api.get_user('timberwolves'))
	teams.append(api.get_user('atlhawks'))
	for team in teams:
		newTeam = Team(name = team.name, image = team.profile_image_url, screen_name = team.screen_name)
		newTeam.user_id = team.id
		session.add(newTeam)
	session.commit()


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def getTeam(string):
	# parameter is the search query from beggining route
	# compare to all teams in DB and see which one has lowest edit distance
	teams = session.query(Team).all()
	distances = []
	for team in teams:
		temp = team.name.split()
		distances.append(levenshtein(string, temp[len(temp)-1]))

	minPos = 0
	for x in range(len(distances)):
		if distances[x] < distances[minPos]:
			minPos = x
	print(teams[minPos].name)
	return teams[minPos]

if __name__ == '__main__':

	# team = getTeam('clippers')
	# getTweets(team)
	# getMedia(team)

	
	


