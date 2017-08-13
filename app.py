from flask import Flask, render_template, url_for, redirect, request
from twitter import findTeam, getMedia

app = Flask(__name__)

# add route where user types in search term and then will use that as a parameter for getTweets()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/search', methods = ['GET', 'POST'])
def search():
	if request.method == 'POST':
		query = request.form['query']
		return redirect(url_for('tweets', query = query))
	else:
		return render_template('search.html')

@app.route('/search/<string:query>')
def tweets(query):
	user = findTeam(query)
	media = getMedia(user)
	return render_template('tweets.html', user=user, media=media)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)