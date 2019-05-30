from flask import Flask, jsonify, request, session, render_template, redirect

app = Flask(__name__)

app.secret_key = "iot-test"

@app.route("/")
def index():
    return render_template('index.html')

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
