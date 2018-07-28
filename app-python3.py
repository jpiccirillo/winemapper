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

dbname = "winemapper"
user = "ec2_user"
password = "winemapper"
host = "winemapper.ctm2fbq02abz.us-east-2.rds.amazonaws.com"
port = "5432"
conn_string = "host={} port={} dbname={} user={} password={}".format(host, port, dbname, user, password)

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     if session.get('is_power'):
#         return render_template('powerHome.html')
#     else:
#         return render_template('home.html')
#        #if session.get('is_regular'):
#         #   return render_template('home.html')
#        #if session.get('is_power'):
#         #   return render_template('powerHome.html')

@app.route('/', methods=['GET'])
def home():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    #
    # else:
    session['logged_in'] = True
    data = [1, 2, 3]
    return render_template('browse.html', entries=data)

app.secret_key = os.urandom(12)

@app.route('/api/getWines', methods=['GET'])
def wines():
    wineryid = str(request.args.get('id'))
    print(wineryid)

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        # Selects all wines from a given winery
        sql = 'SELECT * FROM "Wine" w JOIN "Wineries" wn ON w."wineryID" = wn."wineryID" WHERE wn."wineryID" = ' + wineryid;

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
    return render_template("wineryDetail.html", wid = wineryid, winery = getBasicWineryData(wineryid), wines = winesAtWinery(wineryid))

def winesAtWinery(wid):
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT w.*, v.*, a.*, p.* FROM "Wineries" wn JOIN "Wine" w ON w."wineryID" = wn."wineryID" JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE wn."wineryID" = {}'.format(wid)
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
    # Returns all winedata for the given wine
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()

        sql = 'SELECT w.*, v.*, a.*, p.* FROM "Wine" w LEFT JOIN "Area" a ON w."areaID" = a."areaID" LEFT JOIN "Area" p ON a."provinceID" = p."areaID" LEFT JOIN "Variety" v ON w."varietyID" = v."varietyID" WHERE w."wineID" = {}'.format(wid)
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
        # for month in range(1, 13):
        # print("newrecord")
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
                #
                # elif (row[8]%12==c%12):
                #     time.sleep(.5)
                #     write=True;
                #     break;

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
    wineID = str(request.args.get('id'))
    wineData = getWineData(wineID)
    reviewData = getReveiwData(wineID)
    return render_template("wineDetails.html", w = wineData, reviews = reviewData)

@app.route('/api/getCliamteData', methods=['GET'])
def climateDataResults():

    wineryID = str(request.args.get('id'))
    print(wineryID)
    return getClimateData(wineryID)

@app.route('/api/tasterDetail', methods=['GET'])
def tasterDetail():
    tasterID = str(request.args.get('id'))
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        sql = 'SELECT * FROM "Taster" t WHERE t."tasterID" = {}'.format(tasterID)
        cur.execute(sql)
        data = list(cur.fetchone())

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None: db.close()

    data[1] = data[1].replace('@', '')

    return render_template("tasterDetails.html", taster = data)

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


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")
#    global UID
#    username = request.form['username']
#    print(username)
#    password = request.form['password']
#    print(password)
#    con = sql.connect(db)
#    con.row_factory = sql.Row
#    cur = con.cursor()
#
#    query = "SELECT * FROM User WHERE Username=\'" + username + "\'"
#    cur.execute(query)
#    rows = cur.fetchall()
#
#    if len(rows) == 0:
#       return home()
#
#    elif helper_function.checkPassword(password.encode(), rows[0]['Password'].encode()):
#        if rows[0]['UserLevel'] == 'power':
#           session['is_power'] = True
#        elif rows[0]['UserLevel'] == '':
#           session['is_regular'] = True
#        session['logged_in'] = True
#        session['username'] = username
#        UID = rows[0]['UID']
#       #print("UID: ", UID)
#
#        return home()
#
#    else:
#       return home()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template("logout.html")

@app.route('/climate')
def showPlot():
    return render_template("climate.html")

@app.route('/api/insert', methods=['POST'])
def insertUser():
    print("Logged In: ", session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')

    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")

    db = psycopg2.connect(conn_string)
    cur = db.cursor()
    sql = 'INSERT INTO public."User" VALUES (%s,%s,%s)'
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
    args = request.args
    keys = args.keys()
    values = args.values()

    for i in range(0, len(values)):
        print(keys[i] + values[i])

    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
#         SELECT * FROM public."Winery" w
# WHERE w.lat > 37.743571187449064 AND
# w.lat < 38.542795073979015 AND
# w.lon < -121.94686889648439 AND
# w.lon > -122.66784667968751
# LIMIT 10;
        sql = 'SELECT * FROM public."Winery" w WHERE w."lat" > ORDER BY s"wineryID" ASC'
        cur.execute(sql)

        rows = cur.fetchall()
        print("The number of rows: ", cur.rowcount)
        for row in rows:
            data.append(row)
            print(row)
        # print(data)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if db is not None:
            db.close()
        return data


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
