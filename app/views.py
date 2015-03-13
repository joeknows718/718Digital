from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

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


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s'%
			(form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html', title="Sign In", form=form, providers = app.config['OPENID_PROVIDERS'])