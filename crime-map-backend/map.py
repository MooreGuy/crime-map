from flask import Flask, session
from flask import render_template
from flask import request
from flask import send_file

import pprint

import json
from bson import json_util
import bson

import jwt
import time
import os

from mongodb import PoliceLogs, Alerts
from bson import objectid


from alert import Alert, WatchNotFoundException

app = Flask(__name__)

#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def main_page():
    if os.getenv("FLASK_ENV") == "development":
        frontend_root = "http://localhost:8080"
    else:
        frontend_root = "https://crime-map.sfo2.cdn.digitaloceanspaces.com"

    return render_template('index.html', frontend_root=frontend_root, environment=os.getenv("FLASK_ENV"))


@app.route('/entries')
def entries():
    days_string = request.args['days']
    try:
        days = int(days_string)
    except:
        return "Invalid days"

    cutoff = time.time() - (days * 86400)
    with PoliceLogs() as police_logs:
        logs = list(police_logs.find({'timestamp': {'$gt': cutoff}}))
        return json.dumps(logs, default=json_util.default)

@app.route('/dates_with_entries')
def dates_with_entries():
    dates_with_entries = dict()
    end_of_today = (time.time() - (time.time() % 86400)) + 86400
    previous_days = [end_of_today - (x * 86400) for x in range(1,8)]
    with PoliceLogs() as police_logs:
        for previous_day_end in previous_days:
            day_before_previous_day_end = previous_day_end - 86400
            entries = list(police_logs.find({
                'timestamp': {
                    '$gt': day_before_previous_day_end,
                    '$lt': previous_day_end,
                }
            }).sort({'timestamp': 1}))
            if len(entries) == 0:
                dates_with_entries[time.strftime("%d-%m", previous_day_end)] = entries


@app.route('/log')
def log():
    requestedDate = request.args['date']
    with PoliceLogs() as police_logs:
        logs = list(police_logs.find({'date': requestedDate}))
        return json.dumps(logs, default=json_util.default)

@app.route('/categories')
def categories():
    with PoliceLogs() as police_logs:
        logs = list(police_logs.distinct('type', {}))
        return json.dumps(logs, default=json_util.default)

@app.route('/search')
def search():
    title = request.args['title']
    with PoliceLogs() as police_logs:
        logs = list(police_logs.find({'type': title}))
        return json.dumps(logs, default=json_util.default)

@app.route('/services/jwt')
def sign_jwt():
    with open('./secrets/private-key', 'r') as private_key, open('./secrets/issuer-id') as issuer_id, open('./secrets/key-id') as key_id:
        key_id_val = key_id.read().strip()
        issuer_id_val = issuer_id.read().strip()
        private_key_val = private_key.read().strip()
        jwt_headers = {
            'alg': "ES256",
            'kid': key_id_val,
            'typ': "JWT"
        }

        claims = {
            'iss': issuer_id_val,
            'iat': time.time(),
            'exp': time.time() + 20 * 60,
        }

        return jwt.encode(claims, key=private_key_val, algorithm="ES256", headers=jwt_headers)

@app.route('/alert', methods=["POST"])
def create_alert():
    body = request.get_json()

    # TODO Create real session management
    #if not 'email' in session:
    #    return "Permission Denied", 403
    #email = session['email']
    email = "guy@g1y.io"
    body['email'] = email
    #user = User(email)

    inserted = None
    print(body)
    try:
        id = objectid.ObjectId(body['id'])
    except bson.errors.InvalidId:
        id = None

    id_filter= {'_id': id}
    with Alerts() as alerts:
        if id and alerts.find_one(id_filter):
            body['_id'] = id
            del body['id']
            update = { '$set': body }
            alerts.update_one(id_filter, update)
        else:
            inserted = alerts.insert_one(body)
            id = inserted.inserted_id

    alert_dict = Alert(id).__dict__

    return json.dumps(alert_dict)

@app.route('/alert/<id>', methods=["DELETE"])
def delete_alert(id):
    # TODO Check for correct ownership before removal
    with Alerts() as alerts:
        result = alerts.delete_one({'_id': objectid.ObjectId(id)})
        if result.deleted_count != 1:
            return json.dumps({"success": False}), 404

    return json.dumps({"success": True})

@app.route('/alerts')
def get_all_alerts():
    # TODO: Get actual email from session
    email = 'guy@g1y.io'
    return json.dumps(Alert.get_all(email))