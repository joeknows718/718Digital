from flask import render_template 
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname':'Joe'}
	posts = [
		{
			'author': {'nickname':'Joe'},
			'body': 'Beautiful day in the X'
		},
		{
			'author': {'nickname':'Chris'},
			'body': 'Beautiful day in the BK'
		},
		{
			'author': {'nickname':'James'},
			'body': 'Beautiful day in the QZ'
		},
		{
			'author': {'nickname':'Dwight'},
			'body': 'Beautiful day in the MH'
		},
		{
			'author': {'nickname':'Giligan'},
			'body': 'Beautiful day in the SI'
		}

	]
	return render_template('index.html', title='Home', user=user, posts=posts)


