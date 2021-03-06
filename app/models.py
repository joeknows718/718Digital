from app import db
from hashlib import md5
from app import app 
import re 

import sys

if sys.version_info >= (3, 0):
	enable_search = False
else:
 enable_search = True
 import flask.ext.whooshalchemy as whooshalchemy 


followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User',
								secondary=followers,
								primaryjoin=(followers.c.follower_id == id),
								secondaryjoin=(followers.c.followed_id == id),
								backref=db.backref('followers', lazy='dynamic'),
								lazy='dynamic')


	@staticmethod
	def make_valid_username(username):
		return re.sub('[^a-zA-Z0-9_\.]', '', username)

	@staticmethod
	def make_unique_username(username):
		if User.query.filter_by(username=username).first() is None:
			return username
		version = 2
		while True:
			new_username = username + str(version)
			if User.query.filter_by(username=new_username).first() is None:
				break  
			version += 1 
		return new_username


	def is_authenticated(self):
		return True

	def is_active(self):
		return True 

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self


	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		return Post.query.join(followers, 
			(followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc()
			)




	def __repr__(self):
		return '<User %r>' % (self.username)



class Post(db.Model):
	
	__searchable__ = ['body']

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	language = db.Column(db.String(5))

	def __repr__(self):
		return '<Post %r>' % (self.body)

if enable_search:
	whooshalchemy.whoosh_index(app, Post)




