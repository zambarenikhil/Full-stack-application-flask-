from app import app
from flask import render_template, request, redirect, url_for, jsonify
import os
import json
from pymongo import MongoClient
from bson import json_util
#headers included for newspaper library
import newspaper
from newspaper import Article
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

#connection to our Database MongoDB hosted on mLab

# *** Here you can use your own uri, by vreating account on mlab, or you can also setup
#	  mongodb on your local system/server and pass the uri for the instance here

uri = 'mongodb://saadahmed20940:syed2saad@ds241968.mlab.com:41968/fullstack?retryWrites=false'
client = MongoClient(uri,connectTimeoutMS=30000,socketTimeoutMS=None)
db = client.get_default_database()


# Route for home page / Main landing Page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


#Route for displaying all the data in DB to a HTML page, interface to DB.
@app.route('/display', methods=['GET'])
def get_all_data():
	try:
		all_data  = list(db.test.find())
		return json.dumps(all_data, default=json_util.default, sort_keys=True, indent=4)
	except Exception as e:
		return json.dumps({'error' : str(e)})


#Route for submitting the fields to DB
@app.route('/submit', methods=['GET', 'POST'])
def hello():
	#got the data from HTML web form
	data = request.get_json()
	#submitting all the params to DB
	if request.method == 'POST':
		data_insertion = [{
			"beleivabilityindex":data['_beleivabilityindex'],
			"priorknowledge":data['_priorknowledge'],
			"headline":data['_headline'],
			"body":data['_body'],
			"newsurl":data['_newsurl'],
			"newslabel":data['_newslabel'],
			"newsdate":data['_newsdate']
		}]
		db.test.insert_many(data_insertion)
		return json.dumps(True)
	else:
		return render_template('index.html')


#Route for rendering the data from JSON file for display
@app.route('/render')
def render():
    filename = os.path.join(app.static_folder, 'sample.json')
    with open(filename) as blog_file:
        return json.dumps(json.loads(blog_file.read()))


#Route for processing the URLs from JSON file
@app.route('/processing', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		data = request.get_json();
		#usage of newspaper3k here to extract information from the URLs
		toi_article = Article(data['_newsurl'], language="en")
		toi_article.download()
		toi_article.parse()
		toi_article.nlp() 
		processed_bits = {
		'news_title': toi_article.title,
		'news_summary': toi_article.summary,
		'news_keywords': toi_article.keywords,
		'news_top_image': toi_article.top_image,
		'news_movies': toi_article.movies
		}
		return jsonify(processed_bits)
	else:
		return render_template('index.html')
