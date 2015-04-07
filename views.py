# coding: utf-8
from runrun import *
from models import *
from forms import *
from functools import wraps

def require_login(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.account is None:
			return redirect(url_for('account_login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

@app.before_request
def before_request():
	g.is_active = is_active
	if session.has_key('u') and session.has_key('p'):
		a = Account.query.get(session['u'])
		if a and a.password == session['p']:
			g.account = a
		else:
			g.account = None
	else:
		g.account = None

@app.route('/login', methods=['GET', 'POST'])
def account_login():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		account = Account.findByEmail(login_form.email.data)
		if account == None:
			app.logger.warn('Wrong username')
			login_form.password.errors.append(gettext('Wrong! Try one more time.'))
		elif not account.checkPassword(login_form.password.data):
			app.logger.warn('Wrong password')
			login_form.password.errors.append(gettext('Wrong! Try one more time.'))
		else:
			# save id and shadow to session
			session['u'] = account.id
			session['p'] = account.password
			# insure that we do not redirect user outside.
			if login_form.next.data.startswith(request.host_url):
				return redirect(login_form.next.data)
			else:
				return redirect('/')
	else:
		if request.args.has_key('next'):
			login_form.next.data = request.args['next']
	return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/places/all')
def places_all():
	all_places = Place.query.all()
	return jsonify(success={ "places": [ place.toDict() for place in all_places ] })

@app.route('/places/form', methods=['GET', 'POST'])
@require_login
def places_form():
	if request.args.has_key('place_id'):
		place = Place.query.get_or_404(request.args['place_id'])
	else:
		place = Place()
	place_form = PlaceForm(obj=place)
	if place_form.validate_on_submit():
		place_form.populate_obj(place)
		db.session.add(place)
		db.session.commit()
		return jsonify(success={ "saved": True })
	else:
		if request.args.has_key('latitude') and not place_form.latitude.data:
			place_form.latitude.data = request.args['latitude']
		if request.args.has_key('longitude') and not place_form.longitude.data:
			place_form.longitude.data = request.args['longitude']
	return jsonify(success={ "saved": False, "form": render_template("place_form.html", form=place_form)})

@app.route('/places/delete', methods=['POST'])
@require_login
def places_delete():
	place = Place.query.get_or_404(request.args['place_id'])
	db.session.delete(place)
	db.session.commit()
	return jsonify(success={})

@app.route('/contact/form', methods=['GET', 'POST'])
def contact_form():
	contact_form = ContactForm()
	if contact_form.validate_on_submit():
		msg = Message("FFLC care service")
		msg.add_recipient(app.config['MAIL_ADMIN_EMAILS'])
		msg.body = render_template("mail/contact.txt", form=contact_form)
		mail.send(msg)
		return jsonify(success={ "saved": True })
	return jsonify(success={ "saved": False, "form": render_template("contact_form.html", form=contact_form)})
