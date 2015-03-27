import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask.ext.mail import Mail
from momentjs import momentjs
from flask.ext.babel import Babel, lazy_gettext 
from flask.json import JSONEncoder



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('You need to be logged in to see this page')

oid = OpenID(app, os.path.join(basedir, 'tmp'))

mail = Mail(app)

app.jinja_env.globals['momentjs'] = momentjs
babel = Babel(app) 


class CustomJSONEncoder(JSONEncoder):
	""" This is a class adds support for lazy translation to Flasks JSON encoder. THis is necessary when flashing 
	translated texts."""
	def default(self, obj):
		from speaklater import is_lazy_string
		if is_lazy_string(obj):
			try:
				return unicode(obj)
			except NameError:
				return str(obj)
		return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

#automatic exception loggin hadler emails / major issue tracking
if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials = (MAIL_USERNAME, MAIL_PASSWORD)
	mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER, ADMINS,
                               'blog failure', credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

#set up minor error log
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/blog.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in  %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('718 Digital')



from app import views, models