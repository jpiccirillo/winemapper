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
lastFaveCount = ''
lastID = ''
lastAvgReview = ''
mapBounds = ''
UID = 0

# session['logged_in'] = False
app = Flask(__name__)

def checkMapBounds():
    global mapBounds
    if mapBounds == '':
        return [[37.74031329210266, -122.84912109375001], [38.53957267203907, -121.50329589843751]] #bay area
    return mapBounds

@app.route('/', methods=['GET'])
def home():
    global UID
    global mapBounds
    # if not session.get('logged_in'):
    #     print("not logged in")
    #     session['logged_in'] = 0;

    mapBounds = checkMapBounds();
    # mapparams = [mapcenter, marker array (if present), zoom level] basically how to kick off the map.
    # this flask function is the "homepage view", while the search flask function will use different parameters

    return render_template('browse.html', uid = UID, mapparams = [mapBounds, "", 10], searchparams = [])

app.secret_key = os.urandom(12)

# def checkLogin():
    # if not session.get('logged_in'):
    #     session['logged_in'] = 0;
    #     return 0;
    # else:
    #     return session['logged_in']

# @app.route('/api/checkLoginForClient', methods=['GET'])
# def checkLoginForClient():
#     global UID
#     return json.dumps(UID)

@app.route('/api/addFavorite', methods=['GET'])
def addFavorite():
    global UID
    print("UID: " + str(UID))
    wineID = request.args.get('wid')
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'INSERT INTO "Favorites" VALUES({}, {})'.format(UID, wineID)
        cur.execute(sql)
        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed'

    finally:
        if db is not None: db.close()

    return 'added' + wineID

@app.route('/api/removeFavorite', methods=['GET'])
def removeFavorite():
    global UID
    print("UID: " + str(UID))
    wineID = request.args.get('wid')

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'DELETE FROM "Favorites" WHERE "userID" = {} AND "wineID" = {}'.format(UID, wineID)
        cur.execute(sql)
        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed'

    finally:
        if db is not None: db.close()

    return 'removed ' + wineID

@app.route('/openProfile', methods=['GET'])
def openProfile():
    global UID

    print("UID: " + str(UID))
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
        print("favorites: " + str(favorites))

        print(UID)
        sql = 'SELECT COUNT(f."wineID") FROM "Favorites" f WHERE f."userID" = {} GROUP BY f."userID"'.format(UID)
        cur.execute(sql)
        count = cur.fetchone()
        print(count)
        if count is not None:
            count = list(count)[0]
            print("non-none count", count)
        else: count = 0

        print("count: " + str(count))

        varieties = []
        sql = "SELECT * FROM favoriteVariety({})".format(UID)
        cur.execute(sql)
        rows = cur.fetchall()
        varieties = [row for row in rows]
        print("varieties: " + str(varieties))

        wineries = []
        sql = "SELECT * FROM favoriteWinery({})".format(UID)
        cur.execute(sql)
        rows = cur.fetchall()
        wineries = [row for row in rows]
        print("wineries: " + str(wineries))

        sql = 'SELECT u."name" FROM "User" u WHERE u."userID" = {}'.format(UID)
        cur.execute(sql)
        userName = list(cur.fetchone())[0]
        print(userName)
        cur.close()
        print("userName: " + str(userName))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return render_template('user.html', uid = UID, count = count, userName = userName, favorites = favorites, varieties = varieties, wineries = wineries)


@app.route('/api/getWines', methods=['GET'])
def wines():
    global UID
    wineryid = str(request.args.get('id'))
    print("WineryID: " + str(wineryid))
    print("UserID: " + str(UID))

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        # Selects all wines from a given winery
        sql = 'SELECT * FROM "Wine" w JOIN "Wineries" wn ON w."wineryID" = wn."wineryID"JOIN "Variety" v ON w."varietyID" = v."varietyID" LEFT JOIN ( SELECT "wineID", count(*) c FROM "Favorites" WHERE "userID" = {} GROUP BY "wineID") f ON w."wineID" = f."wineID" WHERE wn."wineryID" = {}'.format(UID, wineryid)

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
    return render_template("wineryDetail.html",  uid = UID, wid = wineryid, winery = getBasicWineryData(wineryid), wineInfo = json.dumps(winesAtWinery(wineryid)), wines = winesAtWinery(wineryid), soil = getSoil(wineryid))

def getSoil(wid):
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT * FROM public."SoilData" sd join public."Soil" s on sd.soilID = s."soilID" join public."Wineries" w on (w."soilID" = sd.soilID and w."wineryID" = {}) join "SoilType" st on st."SU_SYMBOL" = s."SU_SYMBOL"'.format(wid)
        cur.execute(sql)
        rows = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return json.dumps(rows)

def winesAtWinery(wid):
    global UID

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT w.*, v.*, a.*, p.* FROM "Wineries" wn  JOIN "Wine" w ON w."wineryID" = wn."wineryID" JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" JOIN "Variety" v ON w."varietyID" = v."varietyID" LEFT JOIN (SELECT "wineID", count(*) c FROM "Favorites" WHERE "userID" = {} GROUP BY "wineID") f ON w."wineID" = f."wineID" WHERE wn."wineryID" = {}'.format(UID, wid)

        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)

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
    global UID
    # Returns all winedata for the given wine
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        sql = 'SELECT w."wineID", w.title, w.price, p.name, p."wikiLink", a.name, a."wikiLink", v."vName", v.description, w.designation, f.c FROM "Wine" w LEFT JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" LEFT JOIN "Variety" v ON w."varietyID" = v."varietyID" LEFT JOIN (SELECT "wineID", count(*) c FROM "Favorites" WHERE "userID" = {} GROUP BY "wineID") f ON w."wineID" = f."wineID" WHERE w."wineID" = {}'.format(UID, wid)
        cur.execute(sql)
        data = cur.fetchone()
        print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return data


def writeRow(month, oldContents):
    newRow = oldContents;
    newRow.append(month)
    newRow.append("None")
    newRow.append("None")
    newRow.append("None")
    return newRow;

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

    c = 1;
    normalized = [];
    for index, row in enumerate(data):
        write = False;
        if row[8] == c%12:
            write=True;
        else:
            while (row[8] < c%12):
                normalized.append(writeRow(c%12, data[index-1][:8]))
                c+=1;

                if c%12==0 and data[index+1][8] !=1:
                    normalized.append(writeRow(12, data[index-1][:8]))
                    c+=1;

            while (row[8] >= c%12):
                if (row[8]%12==c%12):
                    write=True;
                    break;

                else:
                    normalized.append(writeRow(c%12, row[:8]))
                    c+=1;
        if write:
                normalized.append(row)
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
            print(temps)
            k = 0
            for year in unique:
                print(year)
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
        # print(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return data


@app.route('/api/wineDetail', methods=['GET'])
def wineDetail():
    global UID
    # print("Loggedin: " + str(session['logged_in']))
    wineID = str(request.args.get('id'))
    wineData = getWineData(wineID)
    reviewData = getReveiwData(wineID)
    return render_template("wineDetails.html", uid = UID, favorited = json.dumps(list(wineData)[-1]), wineid = wineID, w = wineData, reviews = reviewData)


@app.route('/api/getCliamteData', methods=['GET'])
def climateDataResults():

    wineryID = str(request.args.get('id'))
    print(wineryID)
    return getClimateData(wineryID)


@app.route('/api/tasterDetail', methods=['GET'])
def tasterDetail():
    global UID
    tasterID = str(request.args.get('id'))
    tasterData = getTasterData(tasterID)
    reviewData = getTasterReviewData(tasterID)

    return render_template("tasterDetails.html", uid = UID, taster = tasterData, reviews = reviewData)

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

@app.route('/api/searchInitial', methods=['GET'])
def search():
    global UID
    global lastID
    global lastFaveCount
    global lastAvgReview
    global mapbounds

    mapBounds = checkMapBounds();
    # global count
    # count += 1

    # if count==1:
    #     lastID = None
    #     lastFaveCount = None

    form = ['title', 'variety', 'designation', 'maxprice', 'area', 'winery', 'keyword']
    insertValues = [None if request.args[entry]=='' else request.args[entry] for entry in form]
    print(insertValues)

    # twoargs = [lastID, lastFaveCount]
    # for arg in twoargs:
    #     if arg != None: arg = int(arg)
    #     insertValues.append(arg)

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        data = [];
        # Returns a list of reviewers who have reviewed the winery the most as [tasterID, name, count]
        sql = 'SELECT * from public.findwines(%s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL)'
        cur.execute(sql, insertValues)
        rows = cur.fetchall()
        data = [row for row in rows]
        print("Last Row: " + str(data[-1]))

        lastID = data[-1][0]
        lastFaveCount = 0 if not data[-1][-2] else data[-1][-2]
        lastAvgReview = 0 if not data[-1][4] else data[-1][4]

        print("lastID: " + str(lastID))
        print("lastfavCount: " + str(lastFaveCount))
        print("lastAvgReview: " + str(lastAvgReview))
        # print("count: " + str(count))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None: db.close()

    return render_template("browse.html", uid = UID, mapparams = [mapBounds, json.dumps(data), 10], searchparams = json.dumps(insertValues))

@app.route('/api/searchLater', methods=['GET'])
def searchLater():
    global lastID
    global lastFaveCount
    global lastAvgReview

    form = ['title', 'variety', 'designation', 'maxprice', 'area', 'winery', 'keyword']
    insertValues = [None if request.args[entry]=='null' else request.args[entry] for entry in form]

    returnargs = [lastFaveCount, lastID, lastAvgReview]
    for arg in returnargs:
    #     if arg != None: arg = int(arg)
        insertValues.append(arg)

    print(insertValues)
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        data = [];
        # Returns a list of reviewers who have reviewed the winery the most as [tasterID, name, count]
        sql = 'SELECT * from public.findwines(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql, insertValues)
        rows = cur.fetchall()
        data = [row for row in rows]
        print("Last Row: " + str(data[-1]))

        lastID = data[-1][0]
        lastFaveCount = 0 if not data[-1][-2] else data[-1][-2]
        lastAvgReview = 0 if not data[-1][4] else data[-1][4]

        print("lastID: " + str(lastID))
        print("lastFaveCount: " + str(lastFaveCount))
        print("lastAvgReview: " + str(lastAvgReview))
        # print("count: " + str(count))

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
    global mapBounds

    args = request.args
    keys = args.keys()
    values = args.values()

    for i in values: bounds = i.split(",")
    mapBounds = [[bounds[0], bounds[2]], [bounds[1],bounds[3]]]
    print(mapBounds)
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
        session['logged_in'] = 1
        session['username'] = user[0]
        UID = user[0]
        print("Logged In as: " + str(UID))
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
        UID = max[0]+1
        print(UID)

        sql = 'INSERT INTO "User" ("userID", "uName", "pWord", name, address) VALUES (%s,%s,%s,%s,%s)'
        insertValues = (UID, username, password, address, firstname)

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
    global UID
    UID = 0
    return render_template("logout.html")

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
