# -*- coding: utf-8 -*-

from key import key as key, email_pw as password 
import os

basedir = os.path.abspath(os.path.dirname(__file__))


WTF_CSRF_ENABLED = True 
SECRET_KEY = key

OPENID_PROVIDERS = [
	{'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TSL = False 
MAIL_USE_SSL = True 
MAIL_USERNAME = 'joeknows718@gmail.com'
MAIL_PASSWORD = password

#admin list
ADMINS = ['joeknows718@gmail.com']

#pagination  
POSTS_PER_PAGE = 5

#Search db

WHOOSH_BASE = os.path.join(basedir, 'search.db')

MAX_SEARCH_RESULTS = 50

LANGUAGES = {
	'en' : 'English',
	'es' : 'Espanol'
}

