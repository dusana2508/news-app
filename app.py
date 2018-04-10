from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

news = requests.get('http://api-news-me.ml/public/today-news').json()

config = news['clientConfiguration']
newsCategories = news['newsCategories']

@app.route('/')
def homepage():
  return render_template('index.html', config = config, categories = newsCategories)

@app.route('/<newsid>')
def getNewsById(newsid):
  for category in newsCategories: 
    for singleNews in category['news']:
      if newsid == singleNews['_id']:
        return render_template('index-news.html', news = singleNews)
  return 'ok'

@app.route ('/category/<categoryURL>')
def getOneCategoryNews(categoryURL):
  for category in newsCategories: 
    if category['categoryName'] == categoryURL:
      return render_template('category.html', allNews=category['news'])

  return 'ok'
@app.route ('/category')
def getOnlyCategories():
  return render_template('allcategories.html', categories = newsCategories)

@app.route ('/login', methods =['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  else : 
    response = requests.post ('http://api-news-me.ml/public/login', data = request.form).json()
    print (response)
    return 'ok'

app.run()
