# coding: utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
from flask.ext.migrate import Migrate
from flask.ext.babel import Babel, gettext
from flask import *
from urllib import urlencode
from groups import groups

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
babel = Babel(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	mail_handler = SMTPHandler('127.0.0.1', app.config['MAIL_DEFAULT_SENDER'], app.config['MAIL_ADMIN_EMAILS'], 'RunRun error')
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

app.jinja_env.globals['groups'] = groups

def google_maps_url():
	url = "https://maps.googleapis.com/maps/api/js?"
	url += urlencode({
		"signed_in": "true",
		"key": app.config['GOOGLE_MAPS_API_KEY']
	})
	return url

app.jinja_env.globals['google_maps_url'] = google_maps_url

def is_active(name):
	if request.endpoint and request.endpoint.startswith(name):
		return 'active'
	else:
		return ''

app.jinja_env.globals['is_active'] = is_active

@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(['en', 'ru'])
