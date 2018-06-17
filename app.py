from flask import Flask, session, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	return render_template('home.html')

app.secret_key = os.urandom(12)

@app.route('/logout')
def logout():
   session['logged_in'] = False
   return render_template("logout.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
