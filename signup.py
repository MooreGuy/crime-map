from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

from celery import Celery

from pymongo import MongoClient

from flask_mail import Mail
from flask_mail import Message

import json
from bson import json_util
from bson.binary import Binary

import os

import time

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


celery = make_celery(app)

@celery.task()
def send_confirmation_email(email):
    token = create_confirmation_token(email)
    mail = Mail()
    mail.init_app(app)
    link = 'mooreguy.com/confirm?email=' + email + '&token=' + token
    anchor = '<a href="' + link + '">Confirm here!</a>'
    msg = Message(anchor, sender="noreply@mooreguy.com", recipients=email)
    mail.send(msg)
    return

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    street = request.form['street']

    signup_entry = {'email': email, 'street': street, 'confirmed': False}
    signup_db = get_db()
    if not signup_db.find_one(signup_entry):
        signup_db.insert_one(signup_entry)

    #send_confirmation_email(email)

    #return render_template('confirmation.html', email=email)
	return "feature coming soon"

@app.route('/confirm', methods=['GET'])
def confirm():
    email = request.get('email')
    token = request.get('token')

    signup_db = get_db()
    if signup_db.find_one({'email': email, 'token': token}):
        signup_db.update({'email': email}, {'$set': {'confirmed': True}})
        return "You're confirmed!"
    else:
        return "Invalid confirmation link"

@app.route('/')
def main_page():
    return render_template('map.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/entries')
def entries():
	cutoff = time.time() - (4 * 86400)
	db = get_logs_db()
	logs = list(db.find({'timestamp': {'$gt': cutoff}}))
	return json.dumps(logs, default=json_util.default)

@app.route('/js/bundle.js')
def send_js():
	return send_file('dist/bundle.js')

def get_db():
		client = MongoClient('localhost', 27017)
		db = client.snoopy
		logs = db.signups
		return logs

def get_logs_db():
		client = MongoClient('localhost', 27017)
		db = client.snoopy
		logs = db.police_logs
		return logs

def create_confirmation_token(email):
    token = os.urandom(20)
    client = MongoClient('localhost', 27017)
    signups = get_db()
    signups.update({'email': email}, {'$set': {'confirmation_token': Binary(token)}}, upsert=False)
    return token

