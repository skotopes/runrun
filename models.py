# coding: utf-8
from runrun import db
from datetime import datetime

from os import urandom
from hashlib import sha256
from binascii import b2a_hex
from markdown import markdown

class Account(db.Model):
	id				= db.Column(db.Integer, primary_key=True)
	email			= db.Column(db.String(320), nullable=False, unique=True)
	salt			= db.Column(db.String(6), nullable=False)
	salted			= db.Column(db.String(64), nullable=False)

	def __init__(self, email, password):
		self.email = email
		self.password = password

	@property
	def password(self):
		return self.salted

	@password.setter
	def password(self, value):
		self.salt = b2a_hex(urandom(3))
		self.salted = sha256(value + self.salt).hexdigest()

	def checkPassword(self, password):
		return self.salted == sha256(password + self.salt).hexdigest()

	def toDict(self):
		return {
			"id": self.id,
			"email": self.email
		}

	@staticmethod
	def findByEmail(email):
		return Account.query.filter(Account.email == email).first()

class Place(db.Model):
	id				= db.Column(db.Integer, primary_key=True)
	latitude		= db.Column(db.Float(Precision=64), nullable=False, index=True)
	longitude		= db.Column(db.Float(Precision=64), nullable=False, index=True)
	created_at		= db.Column(db.DateTime(), nullable=False, default=datetime.now)
	group			= db.Column(db.String(64), nullable=False, index=True)
	title			= db.Column(db.Text(), nullable=False)
	description		= db.Column(db.Text(), nullable=False)

	def toDict(self):
		return {
			"id": self.id,
			"latitude": self.latitude,
			"longitude": self.longitude,
			"created_at": self.created_at,
			"group": self.group,
			"title": self.title,
			"description": markdown(
				self.description,
				output_format="html5",
				extensions=[
					'markdown.extensions.tables',
					'markdown.extensions.nl2br'
				]
			)
		}
	