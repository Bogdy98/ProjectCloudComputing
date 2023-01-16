import mysql.connector
from mysql.connector import connect, Error
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Application favourites'

@app.route('/favourites/create-table')
def createTable():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS favourites"
			create_table_query = "CREATE TABLE favourites (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), userId INT, songId INT, PRIMARY KEY (id), FOREIGN KEY(userId) REFERENCES users(id), FOREIGN KEY(songId) REFERENCES songs(id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table favourites created'
		
		except errors.ProgrammingError:
			pass

@app.route('/favourites/add/<userId>', methods=('GET', 'POST'))
def addFavourite(userId):
	if request.method == 'POST':
		#userName = request.form['userName']
		songName = request.form['songName']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			
			#select_query_1 = "SELECT id FROM users WHERE name = %s"
			#data_select_query_1 = [userName]
			#with connection.cursor() as cursor:
				#cursor.execute(select_query_1, data_select_query_1)
				#row_header=[x[0] for x in cursor.description]
				#result = cursor.fetchall()
				#users=[]
				#for row in result:
					#users.append(dict(zip(row_header, row)))
				#if not users:
					#return ("User with name %s not found!" %(userName))
				#userId = users[0].get('id')
				#connection.commit()
			
			select_query_1 = "SELECT name FROM users WHERE id = %s"
			data_select_query_1 = [userId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_1, data_select_query_1)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				users=[]
				for row in result:
					users.append(dict(zip(row_header, row)))
				if not users:
					return ("User with id %s not found!" %(userId))
				userName = users[0].get('name')
				connection.commit()
			
			
			select_query_2 = "SELECT id FROM songs WHERE name = %s"
			data_select_query_2 = [songName]
			with connection.cursor() as cursor:
				cursor.execute(select_query_2, data_select_query_2)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				songs=[]
				for row in result:
					songs.append(dict(zip(row_header, row)))
				if not songs:
					return ("Song with name %s not found!" %(songName))
				songId = songs[0].get('id')
				connection.commit()
			
			select_query_3 = "SELECT * FROM favourites WHERE userId = %s AND songId = %s"
			data_select_query_3 = [userId, songId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_3, data_select_query_3)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				favourites=[]
				for row in result:
					favourites.append(dict(zip(row_header, row)))
				if favourites:
					return ("Favourite with User Name %s and Song Name %s already exists!" %(userName, songName))
				connection.commit()
			
			insert_query = "INSERT INTO favourites (userId, songId) VALUES (%s, %s)"
			data_insert_query = [userId, songId]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_insert_query)
				connection.commit()
				#return redirect(url_for('getFavourites'))
				return redirect("http://localhost:8003/favourites/%s" %(userId))
	
	return render_template('addFavourite.html')
	
@app.route('/favourites/<userId>')
def getFavourites(userId):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = """SELECT f.id AS 'favourite.id', u.name AS 'user.name', s.name AS 'song.name'
		FROM favourites f
		JOIN users u ON f.userId = u.id AND u.id = %s
		JOIN songs s ON f.songId = s.id
		"""
		data_query = [userId]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			favourites=[]
			for row in result:
				favourites.append(dict(zip(row_header, row)))
			connection.commit()
			if not favourites:
					return "No favourites found!"
			return render_template('listFavourites.html', favourites=favourites)

@app.route('/favourites/delete/<id>')
def deleteFavourite(id):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM favourites WHERE id = %s"
		data_select_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			favourites=[]
			for row in result:
				favourites.append(dict(zip(row_header, row)))
			if not favourites:
				return ("Favourite with id %s not found!" %(id))
			connection.commit()
		
		delete_query = "DELETE FROM favourites WHERE id = %s;"
		data_delete_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(delete_query, data_delete_query)
			connection.commit()
			return redirect("http://localhost:8002/users")

class Favourite:
	def __init__(self, id, name, userId, songId):
		self.id = id
		self.name = name
		self.userId = userId
		self.songId = songId

	def getId(self):
		return self.id
	
	def getName(self):
		return self.name

	def getUserId(self):
		return self.userId
	
	def getSongId(self):
		return self.songId
	
	def setId(self, id):
		self.id = id
	
	def setName(self, name):
		self.name = name
	
	def setUserId(self, userId):
		self.userId = userId
	
	def setSongId(self, songId):
		self.songId = songId

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5003)
