from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User 

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
	user = {'username':'Joe'}
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
@oid.login_handler
def login():
	if g.user is not None and  g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['username', 'email'])
	return render_template('login.html', title="Sign In", form=form, providers=app.config[OPENID_PROVIDERS])


@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email =="":
		flash("Invalid Login, please trey again..")
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		username = resp.username
		if username = None or username=="":
			username = resp.email.split('@')[0]
		user = User(username=username, email=resp.email)
		db.session.add(user)
		db.session.commit()

	remember_me = False
	if 'remember_me' in session
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login.user = (user, remember = rememeber_me)
	return redirect(request.args.get('next') or url_for('index'))

	
	







