from flask import Flask, jsonify, request, session, render_template, redirect
import requests
import os

app = Flask(__name__)

app.secret_key = "iot-test"

dbapi_host = "api" if (os.environ.get('DBAPI_ENDPOINT_URL') == None) else os.environ.get('DBAPI_ENDPOINT_URL')

def get_db_values(host, clientid):
    try:
        url = "http://" + host + ":5000/measurements/" + clientid
        res = requests.get(url, timeout=3.0)
    except Exception, e:
        print e;
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, product details are currently unavailable for this book.'}

@app.route("/")
def index():
    sts, values = get_db_values(dbapi_host, "0")
    return render_template('index.html', values=values)

@app.route("/login", methods=['POST'])
def login():
    session['user'] = request.values.get('username')
    return app.make_response(redirect(request.referrer))

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('user', None)
    return app.make_response(redirect(request.referrer))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
