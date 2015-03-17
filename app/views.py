from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm 
from .models import User 
from datetime import  datetime


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	posts = [
		{
			'author': {'username':'Joe'},
			'body': 'Beautiful day in the X'
		},
		{
			'author': {'username':'Chris'},
			'body': 'Beautiful day in the BK'
		},
		{
			'author': {'username':'James'},
			'body': 'Beautiful day in the QZ'
		},
		{
			'author': {'username':'Dwight'},
			'body': 'Beautiful day in the MH'
		},
		{
			'author': {'username':'Giligan'},
			'body': 'Beautiful day in the SI'
		}

	]
	return render_template('index.html', title='Home', user=user, posts=posts)





@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and  g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['email'])
	return render_template('login.html', title="Sign In", form=form, providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email =="":
		flash("Invalid Login, please try again..")
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		username = resp.email.split('@')[0]	
		username = User.make_unique_username(username)
		user = User(username=username, email=resp.email)
		db.session.add(user)
		db.session.commit()
		db.session.add(user.follow(user))
		db.session.commit() 
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user == None:
		flash('User %s not found.' % username)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.username)
	if form.validate_on_submit():
		g.user.username = form.username.data
		g.user.about_me = form.about_me.data 
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.username.data = g.user.username
		form.about_me.data =  g.user.about_me
	return render_template('edit.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %s is not found.' % username)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t follow yourself!')
		return redirect(url_for('user', username=username))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow ' + username + '.')
		return redirect(url_for('user', username=username))
	db.session.add(u)
	db.session.commit()
	flash('You are now following ' + username + '!')
	return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %s not found.' % username)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t unfollow yourself!')
		return redirect(url_for('user', username=username))
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow %s.' % username)
		return redirect(url_for('user', username=username))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following ' + username + '.')
	return redirect(url_for('user', username=username))

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500  




