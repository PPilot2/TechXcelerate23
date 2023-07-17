import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
	users = User.query.all()
	return render_template('index.html', users=users)

@app.route('/<int:user_id>/')
def user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user.html', user=user)

@app.route('/create/', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		# age = request.form['age']
		email = request.form['email']
		bio = request.form['bio']
		user = User(firstname=firstname, lastname=lastname, email=email, bio=bio)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template('create.html')

@app.route('/<int:user_id>/edit/', methods=('GET', 'POST'))
def edit(user_id):
	user = User.query.get_or_404(user_id)

	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		# age = request.form['age']
		email = request.form['email']
		bio = request.form['bio']

		user.firstname = firstname
		user.lastname = lastname
		# user.age = age
		user.email = email
		user.bio = bio

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template('edit.html', user=user)

@app.post('/<int:user_id>/delete/')
def delete(user_id):
	user = User.query.get_or_404(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('index'))

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100), nullable=False)
	lastname = db.Column(db.String(100), nullable=False)
	# age = db.Column(db.Integer)
	email = db.Column(db.String(80), unique=True, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	bio = db.Column(db.Text)
	city = db.Column(db.String(255), nullable=False)
	houseSize = db.Column(db.Integer(), nullable=False)
	electricityPerMonth = db.Column(db.Integer(), nullable=False)
	travelType = db.Column(db.Integer(), nullable=True)
	annMileage = db.Column(db.Integer(), nullable=True)
	MPGe = db.Column(db.Integer(), nullable=True)
	electricYN = db.Column(db.Integer(), nullable=False)
	yearlyHoursFlown = db.Column(db.Integer(), nullable=False)
	animalProductsEaten = db.Column(db.Integer(), nullable=False)
	majorityConsumedMeat = db.Column(db.String(255), nullable=True)
	clothesBoughtPerYear = db.Column(db.Integer(), nullable=False)
	wasteProduced = db.Column(db.Integer(), nullable=False)
	compostYN = db.Column(db.String(255), nullable=False)
	recycleYN = db.Column(db.String(255), nullable=False)

	def _repr_(self):
		return f"<User> {self.firstname}>"

if __name__ == '__main__':
	app.run()