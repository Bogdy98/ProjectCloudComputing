import mysql.connector
from mysql.connector import connect, Error
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Application users'

@app.route('/users/create-table')
def createTable():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS users"
			create_table_query = "CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), PRIMARY KEY (id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table users created'
				
		except errors.ProgrammingError:
			pass

@app.route('/users/add', methods=('GET', 'POST'))
def addUser():
	if request.method == 'POST':
		name = request.form['name']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			insert_query = "INSERT INTO users (name) VALUES (%s)"
			data_query = [name]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_query)
				connection.commit()
				return redirect(url_for('getUsers'))
				
	return render_template('addUser.html')
	
@app.route('/users')
def getUsers():
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM users"
		with connection.cursor() as cursor:
			cursor.execute(select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			users=[]
			for row in result:
				users.append(dict(zip(row_header, row)))
			connection.commit()
			if not users:
					return "No users found!"
			return render_template('listUsers.html', users=users)

class User:
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def getId(self):
		return self.id
	
	def getName(self):
		return self.name
	
	def setId(self, id):
		self.id = id
	
	def setName(self, name):
		self.name = name

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5002)
