# coding: utf-8
from os import path

SECRET_KEY				= ''
SQLALCHEMY_DATABASE_URI	= 'postgres://localhost/runrun'
GOOGLE_MAPS_API_KEY		= ''
MAIL_DEFAULT_SENDER		= 'runrun@localhost'

if path.isfile('config_local.py'):
	execfile('config_local.py')
