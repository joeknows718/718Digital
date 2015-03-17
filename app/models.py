from app import db
from hashlib import md5

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(255))
	last_seen = db.Column(db.DateTime)

	@staticmethod
	def make_unique_username(username):
		if User.query.filter_by(username=username).first() is None:
			return unsername
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




	def __repr__(self):
		return '<User %r>' % (self.username)



class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(255))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)