from flask import Flask, session, render_template, request
import os, urllib2, json
# import datetime
# import time
# import pytz
# import psycopg2
# import re
# import HTMLParser

dbname = "winemapper"
user = "postgres"
password = "JFPicc`"
conn_string = "dbname=%s user=%s password=%s" % (dbname, user, password)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	session['logged_in'] = True
	# data = refreshData()
	return render_template('home.html')

app.secret_key = os.urandom(12)

@app.route('/logout')
def logout():
   session['logged_in'] = False
   return render_template("logout.html")


@app.route('/api/insert', methods=['POST', 'GET'])
def insertUser():
	print("Logged In: ", session.get('logged_in'))
	if not session.get('logged_in'):
		return render_template('login.html')

	args = request.args
	keys = args.keys()
	values = args.values()
	firstname = values[0]
	lastname = values[1]
	print(values)

	db = psycopg2.connect(conn_string)
	cur = db.cursor()
	SQL = "INSERT INTO ListOfNames (first_name, last_name, age) VALUES (%s,%s,%s)"
	insert_data = (values, "", 5)
	try:
	    cur.execute(SQL, insert_data)
	    db.commit()

	except Exception, e:
		print insert_data
		print e

	return "success"

def refreshData():
	try:
		db = psycopg2.connect(conn_string)
		cur = db.cursor()
		SQL = "SELECT * FROM ListOfNames"
		cur.execute(SQL)
		rows = cur.fetchall()
		print("The number of rows: ", cur.rowcount)
		for row in rows:
			print(row)
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if db is not None:
			db.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
