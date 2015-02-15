#!/usr/bin/env python
# coding: utf-8
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand
from views import app

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def addAccount():
	"""Add admin user"""
	from models import db, Account
	email = raw_input("Email: ")
	password = raw_input("Password: ")
	a = Account(email, password)
	db.session.add(a)
	db.session.commit()

if __name__ == "__main__":
	manager.run()
