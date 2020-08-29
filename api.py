import flask
from flask import request
from flask import jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True
con = sqlite3.connect('database.db', check_same_thread=False)

#API to  view tickets of a particular time
@app.route('/api/showtickets', methods=['GET'])
def show_rows():
	query_parameters = request.args
	timing = query_parameters.get("timing")
	if timing :
		time = timing
		cursorObj = con.cursor()
		cursorObj.execute("SELECT * from tickets where timings=?",[time])
		rows = cursorObj.fetchall()
		results = []
		for row in rows:
			#print(,' ','username',row[1],' ','phonenumber',row[2],' ','timing',row[3])
			dic = {}
			dic["ticketid"] = row[0]
			dic["User's name"] = row[1]
			dic["Phone Number"] = row[2]
			dic["Timing"] = row[3]
			results.append(dic)
		return jsonify(results)
	else:
		return "<h1>Error!!</h1><p>Time parameter is not provided.</p>"

# API to book a ticket using a user’s name, phone number, and timings.
@app.route('/api/bookticket', methods=['GET'])
def insert_row():
	query_parameters = request.args
	username = query_parameters.get("username")
	phonenumber = query_parameters.get("phonenumber")
	timing = query_parameters.get("timing")

	if not (username or phonenumber or timing):
		return "<h1>Error!!</h1><p>Some parameter's missing. Please pass the username, phonenumber and timing.</p>"

	l = []
	l.append(username)
	l.append(phonenumber)
	l.append(timing)
	
	cursorObj = con.cursor()
	query = "INSERT INTO tickets VALUES(null,?,?,?);".format(username,phonenumber,timing)
	try:
		cursorObj.execute(query,l)
		con.commit()
		print("Inserted!")
		rowid = cursorObj.lastrowid
		print("Last row id:",rowid)
		return "<h1>Your ticket id is {}</h1><p>Thank you for the booking.</p>".format(rowid)
	except:
		print("Insert fail.")

if __name__ == '__main__':
	app.run()