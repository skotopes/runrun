# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, BooleanField, HiddenField, SelectField, FloatField, TextAreaField
from wtforms.validators import InputRequired, Email
from groups import groups

class LoginForm(Form):
	email		= TextField('Email', validators=[ InputRequired(), Email() ])
	password	= TextField('Password', validators=[ InputRequired() ])
	next		= HiddenField('Next Page', validators=[])

class PlaceForm(Form):
	latitude	= FloatField("Latitude", validators=[ InputRequired() ])
	longitude	= FloatField("Longitude", validators=[ InputRequired() ])
	group		= SelectField("Group", choices=[ (k,v['name']) for k,v in groups.items()], validators=[ InputRequired() ])
	title		= TextField("Title", validators=[ InputRequired() ])
	description	= TextAreaField("Description (supports markdown)", validators=[ InputRequired() ])

class ContactForm(Form):
	email		= TextField('Email', validators=[ Email() ])
	text		= TextAreaField("How can we help you?", validators=[ InputRequired() ])