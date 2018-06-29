from flask import Flask, session, render_template, request
import os
import urllib3
import json
import datetime
import time
import pytz
import psycopg2
import re
import html.parser

dbname = "winemapper"
user = "ec2_user"
password = "winemapper"
host = "winemapper.ctm2fbq02abz.us-east-2.rds.amazonaws.com"
port = "5432"
conn_string = "host={} port={} dbname={} user={} password={}".format(host, port, dbname, user, password)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    session['logged_in'] = True
    data = refreshData()
    return render_template('browse.html', entries=json.dumps(data))

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

    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")

    db = psycopg2.connect(conn_string)
    cur = db.cursor()
    sql = "INSERT INTO public.\"ListOfNames\" (first_name, last_name, age) VALUES (%s,%s,%s)"
    insert_data = (firstname, lastname, 5)
    try:
        cur.execute(sql, insert_data)
        db.commit()

    except Exception as e:
        print(insert_data)
        print(e)

    return "success"

# @app.route('api/refresh'):
def refreshData():
    db = None
    data = []
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = "SELECT * FROM public.\"popularWineries\" ORDER BY \"wineryID\" ASC"
        cur.execute(sql)

        rows = cur.fetchall()
        print("The number of rows: ", cur.rowcount)
        for row in rows:
            data.append(row)
            print(row)
        print(data)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None:
            db.close()
        return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
