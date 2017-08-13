import tweepy
import urllib2

CONSUMER_KEY = 'iBaC5IkDaRNzFp7VU8ijeEDa6'
CONSUMER_SECRET = 'G8SkwtF63MxWLGQP4gmnRZTkAs7Xqi3B5w1p0PQS2jkZDZlUVG'
ACCESS_TOKEN = '387527916-FMWSYRpM6qurZuqdJXlAv5tClZRoAPx6YJ4iJ2S2'
ACCESS_TOKEN_SECRET = 'omu5WUCZT1jkyQaFOxaH7RjOQbSn9fbg9fwgWGImLZZAy'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def getTweets(text):
	tweets = []
	for tweet in tweepy.Cursor(api.search, q=text, result_type='popular').items(1000):
		tweets.append(tweet)
	print(len(tweets))
	for i in range(len(tweets)):
		for j in range(i, len(tweets)):
			if (tweets[i].favorite_count < tweets[j].favorite_count):
				tweets[i], tweets[j] = tweets[j], tweets[i]
	for tweet in tweets:
		print(tweet.user.name)
		print(tweet.text)
		print(tweet.favorite_count)
		print '\n'
	return tweets 

def findTeam(text):
	users = api.search_users(q=text, per_page=1, page=1)
	official = users[0]
	for user in users:
		if str(user.verified) == 'True':
			if official.followers_count < user.followers_count:
				official = user
	print(official.screen_name)
	print(official.followers_count)
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
				'likes' : tweet.favorite_count
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


	return topMedia


if __name__ == '__main__':

	getTweets('lakers')

	# searched_tweets = api.search(q='lakers', count = 50, result_type='popular')
	# print(searched_tweets)
	# print(len(searched_tweets))
	# print(searched_tweets[0].entities)

	# timeline = api.user_timeline(screen_name='lakers', count=50)
