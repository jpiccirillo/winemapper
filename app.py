from flask import Flask, session, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	session['logged_in'] = True
	return render_template('home.html')

app.secret_key = os.urandom(12)

@app.route('/logout')
def logout():
   session['logged_in'] = False
   return render_template("logout.html")

@app.route('/api/insert', methods=['POST', 'GET'])
def insertUser():
	if not session.get('logged_in'):
		return render_template('login.html')

	args = request.args
	keys = args.keys()
	values = args.values()
	print(values)




	
	return "success"
	# try:
	# 	with sql.connect("data/test.db") as con:
    #
	# 		# (Username,Password,Email,Address,City,State,Zip,FirstName,LastName)
	# 		curs = con.cursor()
	# 		con = sql.connect(db)
	# 		con.row_factory = sql.Row
	# 		username = session.get('username')
    #
    #
	# 		for i in range(0, len(values)):
	# 		    #Need to update Lat Lon in the database if address changes
	# 		    #In addition, seems like parts of address do not arrive in order they are sent? Address is sometimes last in for loop.  Put the different parts of the address in in boxes of array to keep them in order
    #
	# 		    query = "UPDATE User SET " + keys[i] + "=\'" + str(values[i]) + "\' WHERE Username = \'" + username + "\'"
	# 		    inserted = con.execute(query)
    #
	# 		if adrParts[0] is not None:
	# 		    query = "UPDATE User SET Lat=\'" + str(lat) + "\' WHERE Username = \'" + username + "\'"
	# 		    con.execute(query)
	# 		    query = "UPDATE User SET Lon=\'" + str(lon) + "\' WHERE Username = \'" + username + "\'"
	# 		    con.execute(query)
    #
	# 		con.commit()
	# 		return "success"
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
