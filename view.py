from flask import Flask, jsonify, request, session, render_template, redirect
import requests
import os
import time
from datetime import datetime
import calendar

app = Flask(__name__)

app.secret_key = "iot-test"

dbapi_host = "api" if (os.environ.get('DBAPI_ENDPOINT_URL') == None) else os.environ.get('DBAPI_ENDPOINT_URL')

def get_measurements_url(host, clientid, datetime_from_str, datetime_to_str):
    unix_datetime_from = -1
    unix_datetime_to = -1
    if datetime_from_str != "":
        datetime_from = datetime.strptime(datetime_from_str, "%Y-%m-%dT%H:%M")
        unix_datetime_from = calendar.timegm(datetime_from.timetuple())
    if datetime_to_str != "":
        datetime_to = datetime.strptime(datetime_to_str, "%Y-%m-%dT%H:%M")
        unix_datetime_to = calendar.timegm(datetime_to.timetuple())

    if datetime_from_str != "":
        if datetime_to_str != "":
            return "http://" + host + ":5000/measurements/" + clientid + "?from=" + str(unix_datetime_from) + "&to=" + str(unix_datetime_to)
        else:
            return "http://" + host + ":5000/measurements/" + clientid + "?from=" + str(unix_datetime_from)
    else:
        if datetime_to_str != "":
            return "http://" + host + ":5000/measurements/" + clientid + "?to=" + str(unix_datetime_to)
        else:
            return "http://" + host + ":5000/measurements/" + clientid


def get_db_values(host, clientid, datetime_from="", datetime_to=""):
    try:
        url = get_measurements_url(host, clientid, datetime_from, datetime_to)
        res = requests.get(url, timeout=60.0)
    except Exception, e:
        app.logger.error(e);
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, product details are currently unavailable for this book.'}

@app.route("/", methods=['GET', 'POST'])
def index():
    sts = None
    values = None
    datetime_from = ""
    datetime_to = ""
    if "user" in session:
        if "datetime_from" in request.form and "datetime_to" in request.form:
            datetime_from = request.form["datetime_from"]
            datetime_to = request.form["datetime_to"]
            sts, values = get_db_values(dbapi_host, "0", datetime_from, datetime_to)
        else:
            sts, values = get_db_values(dbapi_host, "0")
    return render_template('index.html', values=values, datetime_from=datetime_from, datetime_to=datetime_to)

@app.route("/login", methods=['POST'])
def login():
    session['user'] = request.values.get('username')
    return app.make_response(redirect(request.referrer))

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('user', None)
    return app.make_response(redirect(request.referrer))

@app.route("/health", methods=['GET'])
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
