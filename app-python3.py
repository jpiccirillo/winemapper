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
import time
import random

dbname = "winemapper"
user = "ec2_user" #"postgres"
password = "winemapper" #"postgres"
host = "winemapper.ctm2fbq02abz.us-east-2.rds.amazonaws.com" #"localhost"
port = "5432"
conn_string = "host={} port={} dbname={} user={} password={}".format(host, port, dbname, user, password)
# session['logged_in'] = False
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    if not session.get('logged_in'):
        print("not logged in")
        session['logged_in'] = False;

    return render_template('browse.html', loggedin = checkLogin())

app.secret_key = os.urandom(12)

def checkLogin():
    if not session.get('logged_in'):
        session['logged_in'] = False;
        return False;
    else:
        return session['logged_in']

@app.route('/api/checkLoginForClient', methods=['GET'])
def checkLoginForClient():
    if checkLogin()==False:
        return "false"
    else:
        return "true"

@app.route('/openProfile', methods=['GET'])
def openProfile():
    print(UID)
    #queries to get user info and their favorites
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        # Selects a user's favorite wines

        favorites = []
        sql = 'SELECT w."wineID", w."title", v."vName", wn."name", wn."country" FROM "Favorites" f JOIN "Wine" w ON f."wineID" = w."wineID" JOIN "Wineries" wn ON  wn."wineryID" = w."wineryID" JOIN "Variety" v ON v."varietyID" = w."varietyID" WHERE f."userID" = {}'.format(UID)
        cur.execute(sql)
        rows = cur.fetchall()
        favorites = [row for row in rows]

        count = 0
        sql = 'SELECT COUNT(f."wineID") FROM "Favorites" f WHERE f."userID" = {} GROUP BY f."userID"'.format(UID)
        cur.execute(sql)
        count = cur.fetchone()[0]

        varieties = []
        sql = "SELECT * FROM favoriteVariety({})".format(UID)
        cur.execute(sql)
        rows = cur.fetchall()
        varieties = [row for row in rows]

        wineries = []
        sql = "SELECT * FROM favoriteWinery({})".format(UID)
        cur.execute(sql)
        rows = cur.fetchall()
        wineries = [row for row in rows]

        userName = ''
        sql = 'SELECT u."name" FROM "User" u WHERE u."userID" = {}'.format(UID)
        cur.execute(sql)
        userName = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return render_template('user.html', uid = UID, count = count, userName = userName, favorites = favorites, varieties = varieties, wineries = wineries, loggedin = checkLogin())


@app.route('/api/getWines', methods=['GET'])
def wines():
    # checkLogin()
    wineryid = str(request.args.get('id'))
    print(wineryid)

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        # Selects all wines from a given winery
        sql = 'SELECT * FROM "Wine" w JOIN "Wineries" wn ON w."wineryID" = wn."wineryID" WHERE wn."wineryID" = {}'.format(wineryid)

        cur.execute(sql)
        rows = cur.fetchall()
        print("Number of rows: ", cur.rowcount)
        data = [row for row in rows]
        print(data)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()
        return json.dumps(data)


@app.route('/api/wineryDetail', methods=['GET'])
def wineryDetail():
    wineryid = str(request.args.get('id'))

    print(wineryid)
    return render_template("wineryDetail.html", wid = wineryid, winery = getBasicWineryData(wineryid), wines = winesAtWinery(wineryid), loggedin = checkLogin())


def winesAtWinery(wid):
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT w.*, v.*, a.*, p.* FROM "Wineries" wn JOIN "Wine" w ON w."wineryID" = wn."wineryID" JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE wn."wineryID" = {}'.format(wid)
        cur.execute(sql)
        rows = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return rows


def getBasicWineryData(wid):
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT wn.* FROM "Wineries" wn WHERE wn."wineryID" = {}'.format(wid)
        cur.execute(sql)
        winery = cur.fetchone()
        print(winery)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return winery


def getWineData(wid):
    # Returns all winedata for the given wine
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        sql = 'SELECT ' + 
        'w.wineID, w.title, w.price, p.name, p.wikilink,'+ 
        'a.name, a.wikilink, v.name, v.description, w.designation '+
        'FROM "Wine" w LEFT JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" LEFT JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE w."wineID" = {}'.format(wid)
        cur.execute(sql)
        data = cur.fetchone()
        print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return data


def getClimateData(wid):
    print(wid)
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        sql = 'SELECT * FROM (SELECT w.name, w."wineryID", s.* FROM "Station" s, "Wineries" w WHERE w."wineryID" = {} AND w."stationID" = s."STNnum") station INNER JOIN public."STNData" d ON station."STNnum" = d."USAF_ID"'.format(wid)

        cur.execute(sql)
        rows = cur.fetchall()
        data = list([list(row) for row in rows])
        # print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    # print(data)
    # ['x', 'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    totalData = [];
    totalTemps = [];
    totalTemps.append(['x', '2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', '2018-06-01', '2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01'])
    # x = numpy.array(data).T

    c = 1;
    normalized = [];
    print(data)
    for row in data:
        write = False;
        if row[8] == c%12:
            write=True;

        else:

            while (row[8] >= c%12):
                print(row[8], c%12, c)
                if (row[8]%12==c%12):
                    # time.sleep(.5)
                    write=True;
                    break;

                else:
                    print(row[8], c%12)
                    # time.sleep(.5)
                    newRow = row[:8]
                    newRow.append(c%12)
                    newRow.append("None")
                    newRow.append("None")
                    newRow.append("None")
                    normalized.append(newRow)
                    c+=1;
        if write:
                print(row[8], c%12)
                normalized.append(row)
                # time.sleep(.5)
                c+=1

    print(normalized)

    x = [list([row[i] for row in normalized]) for i in range(len(normalized[0]))]
    unique = sorted(set(x[7]))
    print(unique)
    for i in range(len(x)):

        if (i==2): #append USAF ID
            totalData.append([x[i][0]])

        elif (i==3): #append Station Name
            totalData[0].append(x[i][0].title())

        elif (i==9):
            temps = [x[i][j:j + 12] for j in range(0, len(x[i]), 12)]

            k = 0
            for year in unique:
                # if len(temps[k]) == 12:
                temps[k].insert(0, year)
                totalTemps.append(temps[k])
                k+=1;

    totalData.append(totalTemps)
    return json.dumps(totalData)


def getReveiwData(wid):
    # Returns all reviews for the given wine
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        sql = 'SELECT r."description", r."points", t."tasterID", t."name" FROM "Review" r LEFT JOIN "Taster" t ON r."tasterID" = t."tasterID" WHERE "wineID" = {} ORDER BY r."points" DESC'.format(wid)

        cur.execute(sql)
        rows = cur.fetchall()
        data = [row for row in rows]
        print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return data


@app.route('/api/wineDetail', methods=['GET'])
def wineDetail():
    print(session['logged_in'])
    wineID = str(request.args.get('id'))
    wineData = getWineData(wineID)
    reviewData = getReveiwData(wineID)
    return render_template("wineDetails.html", w = wineData, reviews = reviewData, loggedin = checkLogin())


@app.route('/api/getCliamteData', methods=['GET'])
def climateDataResults():

    wineryID = str(request.args.get('id'))
    print(wineryID)
    return getClimateData(wineryID)


@app.route('/api/tasterDetail', methods=['GET'])
def tasterDetail():
    tasterID = str(request.args.get('id'))
    tasterData = getTasterData(tasterID)
    reviewData = getTasterReviewData(tasterID)

    return render_template("tasterDetails.html", taster = tasterData, reviews = reviewData, loggedin = checkLogin())

def getTasterReviewData(tasterID):
    """
    Gets taster's review information from the server
    """
    reviewData = []
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT r."description", r."points", w."wineID", w."title", v."vName", wn."name", wn."country" FROM "Review" r JOIN "Taster" t ON r."tasterID" = t."tasterID" JOIN "Wine" w ON w."wineID" = r."wineID" LEFT JOIN "Wineries" wn ON w."wineryID" = wn."wineryID" LEFT JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE t."tasterID" = {} ORDER BY r."points" DESC LIMIT 100'.format(tasterID)
        cur.execute(sql)
        reviewData = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None: db.close()
    return reviewData

def getTasterData(tasterID):
    """
    Gets taster information from the DB
    """
    tasterData = []
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT t.*, COUNT(r."revID"), AVG(r."points") FROM "Taster" t JOIN "Review" r on t."tasterID" = r."tasterID" WHERE t."tasterID" = {} GROUP BY t."tasterID"'.format(tasterID)
        cur.execute(sql)
        tasterData = list(cur.fetchone())

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None: db.close()

    if tasterData[1]:
        tasterData[1] = tasterData[1].replace('@', '')

    return tasterData

@app.route('/api/search', methods=['GET'])
def search():
    title = request.args.get('title')
    variety = request.args.get('variety')
    designation = request.args.get('variety')
    maxprice = request.args.get('maxprice')
    area = request.args.get('area')
    winery = request.args.get('winery')
    keyword = request.args.get('keyword')

    title = NULL
    variety = NULL
    designation = NULL
    maxprice = NULL
    area = NULL
    keyword = NULL
    
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        data = [];
        # Returns a list of reviewers who have reviewed the winery the most as [tasterID, name, count]
        sql = 'SELECT * from public.findwines(%s, %s, %s, %s, %s, %s, %s, NULL, NULL)'
        insertValues = (title, variety, designation, maxprice, area, winery, keyword)
        print(sql)
        cur.execute(sql, insertValues)
        rows = cur.fetchall()
        data = [row for row in rows]
        print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return json.dumps(data)

@app.route('/api/reviewedWineryMost', methods=['GET'])
def reviewedWineryMost():
    wineryID = str(request.args.get('id'))
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        data = [];
        # Returns a list of reviewers who have reviewed the winery the most as [tasterID, name, count]
        sql = 'SELECT * FROM wineryReviewedMostBy({})'.format(wineryID)
        cur.execute(sql)
        rows = cur.fetchone()
        data = [row for row in rows]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return json.dumps(data)


@app.route('/api/getWineries', methods=['GET'])
def wineries():

    args = request.args
    keys = args.keys()
    values = args.values()

    for i in values: bounds = i.split(",")

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        # SELECT * FROM public."Winery" w
        # WHERE w.lat > 37.743571187449064 AND
        # w.lat < 38.542795073979015 AND
        # w.lon < -121.94686889648439 AND
        # w.lon > -122.66784667968751
        # LIMIT 10;

        sql = 'SELECT * FROM "Wineries" w WHERE w.lat > ' + bounds[0] + ' AND w."lat" < ' + bounds[1] + ' AND w."lon" < ' + bounds[3] + ' AND w."lon" > ' + bounds[2] + ' LIMIT 30'

        cur.execute(sql)
        rows = cur.fetchall()
        print("Number of rows: ", cur.rowcount)
        data = [row for row in rows]

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()
        return json.dumps(data)

@app.route('/login')
def loginpage():
    return render_template("login.html")

@app.route('/login_action', methods=['POST', 'GET'])
def login():
    global UID
    username = request.form['username']
    print(username)
    password = request.form['password']
    print(password)

    db = psycopg2.connect(conn_string)
    cur = db.cursor()

    query = 'SELECT * FROM "User" WHERE "uName"=\'' + username +'\''
    cur.execute(query)
    user = list(cur.fetchone())

    if password == user[2]:
        session['logged_in'] = True
        session['username'] = user[0]
        UID = user[0]
        return home()

    else:
        return loginpage()

@app.route('/addUser', methods = ['POST', 'GET'])
def new_user():
    # if not session.get('logged_in'):
    #     return render_template('login.html')

    return render_template('newUser.html')

@app.route('/addUserData', methods = ['POST', 'GET'])
def addUserData():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # if not session.get('is_power'):
    #     return render_template('home.html')
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        username = request.form['username']
        password = request.form['password']
        # email = request.form['email']
        address = request.form['inputAddress']
        firstname = request.form['firstname']

        print(username, password, address, firstname)
        getUserID = 'SELECT MAX("userID") FROM "User"'
        cur.execute(getUserID)
        max = cur.fetchone()
        uID = max[0]+1
        print(uID)

        sql = 'INSERT INTO "User" ("userID", "uName", "pWord", name, address) VALUES (%s,%s,%s,%s,%s)'
        insertValues = (uID, username, password, address, firstname)

        cur.execute(sql, insertValues)
        db.commit()
        msg = "You're in! Welcome to WineMapper :)"

    except Exception as e:
        con.rollback()
        msg = e

    finally:
        return render_template("result.html", msg = msg)
        db.close()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template("logout.html", loggedin = checkLogin())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

    # @app.route('/api/wineryWineInfo', methods=['GET'])
    # def wineryWineInfo():
    #     wineryid = str(request.args.get('id'))
    #     # print(wineryid)
    #
    #     try:
    #         db = psycopg2.connect(conn_string)
    #         # Returns all other info related to that winery surrounding its wines (Wine, Area, Variety info all joined to Winery)
    #         sql = 'SELECT w.*, v.*, a.* FROM "Wineries" wn JOIN "Wine" w ON w."wineryID" = wn."wineryID" JOIN "Area" a ON w."areaID" = a."areaID" JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE wn."wineryID" = {}'.format(wineryid)
    #         cur = db.cursor()
    #         cur.execute(sql)
    #         rows = cur.fetchall()
    #         data = [row for row in rows]
    #         print("Number of rows: ", cur.rowcount)
    #
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #
    #     finally:
    #         if db is not None: db.close()
    #
    #     return json.dumps(data)

    # @app.route('/api/wineReviews', methods=['GET'])
    # def wineReviews():
    #     wineID = str(request.args.get('id'))
    #
    #     try:
    #         db = psycopg2.connect(conn_string)
    #         cur = db.cursor()
    #
    #         # Returns all reviews for the given wine
    #         sql = 'SELECT r."description", r."points", t."tasterID", t."name" FROM "Review" r LEFT JOIN "Taster" t ON r."tasterID" = t."tasterID" WHERE "wineID" = {} ORDER BY r."points" DESC'.format(wineID)
    #
    #         cur.execute(sql)
    #         rows = cur.fetchall()
    #         data = [row for row in rows]
    #         print(data)
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #
    #     finally:
    #         if db is not None: db.close()
    #
    #     return json.dumps(data)
