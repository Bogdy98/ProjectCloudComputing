import mysql.connector
from mysql.connector import connect, Error
import json
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Application likes_and_comments'

@app.route('/likes/create-table')
def createTableLikes():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS likes"
			create_table_query = "CREATE TABLE likes (id INT NOT NULL AUTO_INCREMENT, userId INT, songId INT, PRIMARY KEY (id), FOREIGN KEY(userId) REFERENCES users(id), FOREIGN KEY(songId) REFERENCES songs(id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table likes created'
		
		except errors.ProgrammingError:
			pass

@app.route('/comments/create-table')
def createTableComments():
	with connect(host='mysqldb', user='root', password='p@ssw0rd1', database="projectdb") as connection:
		try:
			drop_table_query = "DROP TABLE IF EXISTS comments"
			create_table_query = "CREATE TABLE comments (id INT NOT NULL AUTO_INCREMENT, comment VARCHAR(255), userId INT, songId INT, PRIMARY KEY (id), FOREIGN KEY(userId) REFERENCES users(id), FOREIGN KEY(songId) REFERENCES songs(id))"
			with connection.cursor() as cursor:
				cursor.execute(drop_table_query)
				cursor.execute(create_table_query)
				connection.commit()
				return 'Table comments created'
		
		except errors.ProgrammingError:
			pass

@app.route('/likes/add/<songId>', methods=('GET', 'POST'))
def addLike(songId):
	if request.method == 'POST':
		userName = request.form['userName']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			
			select_query_1 = "SELECT name FROM songs WHERE id = %s"
			data_select_query_1 = [songId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_1, data_select_query_1)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				songs=[]
				for row in result:
					songs.append(dict(zip(row_header, row)))
				if not songs:
					return ("Song with id %s not found!" %(songId))
				songName = songs[0].get('name')
				connection.commit()
			
			
			select_query_2 = "SELECT id FROM users WHERE name = %s"
			data_select_query_2 = [userName]
			with connection.cursor() as cursor:
				cursor.execute(select_query_2, data_select_query_2)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				users=[]
				for row in result:
					users.append(dict(zip(row_header, row)))
				if not users:
					return ("User with name %s not found!" %(userName))
				userId = users[0].get('id')
				connection.commit()
			
			select_query_3 = "SELECT * FROM likes WHERE userId = %s AND songId = %s"
			data_select_query_3 = [userId, songId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_3, data_select_query_3)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				likes=[]
				for row in result:
					likes.append(dict(zip(row_header, row)))
				if likes:
					return ("Like with User Name %s and Song Name %s already exists!" %(userName, songName))
				connection.commit()
			
			insert_query = "INSERT INTO likes (userId, songId) VALUES (%s, %s)"
			data_insert_query = [userId, songId]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_insert_query)
				connection.commit()
				return redirect("http://localhost:8004/likes/%s" %(songId))
	
	return render_template('addLike.html')

@app.route('/comments/add/<songId>', methods=('GET', 'POST'))
def addComment(songId):
	if request.method == 'POST':
		comment = request.form['comment']
		userName = request.form['userName']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			
			select_query_1 = "SELECT name FROM songs WHERE id = %s"
			data_select_query_1 = [songId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_1, data_select_query_1)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				songs=[]
				for row in result:
					songs.append(dict(zip(row_header, row)))
				if not songs:
					return ("Song with id %s not found!" %(songId))
				songName = songs[0].get('name')
				connection.commit()
			
			
			select_query_2 = "SELECT id FROM users WHERE name = %s"
			data_select_query_2 = [userName]
			with connection.cursor() as cursor:
				cursor.execute(select_query_2, data_select_query_2)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				users=[]
				for row in result:
					users.append(dict(zip(row_header, row)))
				if not users:
					return ("User with name %s not found!" %(userName))
				userId = users[0].get('id')
				connection.commit()
			
			insert_query = "INSERT INTO comments (comment, userId, songId) VALUES (%s, %s, %s)"
			data_insert_query = [comment, userId, songId]
			with connection.cursor() as cursor:
				cursor.execute(insert_query, data_insert_query)
				connection.commit()
				return redirect("http://localhost:8004/comments/%s" %(songId))
	
	return render_template('addComment.html')

@app.route('/likes/<songId>')
def getLikes(songId):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = """SELECT l.id AS 'like.id', u.name AS 'user.name', s.name AS 'song.name'
		FROM likes l
		JOIN users u ON l.userId = u.id
		JOIN songs s ON l.songId = s.id AND s.id = %s
		"""
		data_query = [songId]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			likes=[]
			for row in result:
				likes.append(dict(zip(row_header, row)))
			connection.commit()
			if not likes:
					return "No likes found!"
			return render_template('listLikes.html', likes=likes)

@app.route('/comments/<songId>')
def getComments(songId):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = """SELECT c.id AS 'comment.id', c.comment AS 'comment.comment', u.name AS 'user.name', s.name AS 'song.name'
		FROM comments c
		JOIN users u ON c.userId = u.id
		JOIN songs s ON c.songId = s.id AND s.id = %s
		"""
		data_query = [songId]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			comments=[]
			for row in result:
				comments.append(dict(zip(row_header, row)))
			connection.commit()
			if not comments:
					return "No comments found!"
			return render_template('listComments.html', comments=comments)

@app.route('/likes/delete/<id>')
def deleteLike(id):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM likes WHERE id = %s"
		data_select_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			likes=[]
			for row in result:
				likes.append(dict(zip(row_header, row)))
			if not likes:
				return ("Like with id %s not found!" %(id))
			connection.commit()
		
		delete_query = "DELETE FROM likes WHERE id = %s;"
		data_delete_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(delete_query, data_delete_query)
			connection.commit()
			return redirect("http://localhost:8001/songs")

@app.route('/comments/delete/<id>')
def deleteComment(id):
	with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
		select_query = "SELECT * FROM comments WHERE id = %s"
		data_select_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(select_query, data_select_query)
			row_header=[x[0] for x in cursor.description]
			result = cursor.fetchall()
			comments=[]
			for row in result:
				comments.append(dict(zip(row_header, row)))
			if not comments:
				return ("Comment with id %s not found!" %(id))
			connection.commit()
		
		delete_query = "DELETE FROM comments WHERE id = %s;"
		data_delete_query = [id]
		with connection.cursor() as cursor:
			cursor.execute(delete_query, data_delete_query)
			connection.commit()
			return redirect("http://localhost:8001/songs")

@app.route('/likes/deleteLikeBySongId/<songId>', methods=('GET', 'POST'))
def deleteLikeBySongId(songId):
	if request.method == 'POST':
		userName = request.form['userName']
		with connect(host='mysqldb', user='root',password='p@ssw0rd1' ,database='projectdb') as connection:
			select_query_1 = "SELECT name FROM songs WHERE id = %s"
			data_select_query_1 = [songId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_1, data_select_query_1)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				songs=[]
				for row in result:
					songs.append(dict(zip(row_header, row)))
				if not songs:
					return ("Song with id %s not found!" %(songId))
				songName = songs[0].get('name')
				connection.commit()
			
			select_query_2 = "SELECT id FROM users WHERE name = %s"
			data_select_query_2 = [userName]
			with connection.cursor() as cursor:
				cursor.execute(select_query_2, data_select_query_2)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				users=[]
				for row in result:
					users.append(dict(zip(row_header, row)))
				if not users:
					return ("User with name %s not found!" %(userName))
				userId = users[0].get('id')
				connection.commit()
			
			select_query_3 = "SELECT * FROM likes WHERE songId = %s AND userId = %s"
			data_select_query_3 = [songId, userId]
			with connection.cursor() as cursor:
				cursor.execute(select_query_3, data_select_query_3)
				row_header=[x[0] for x in cursor.description]
				result = cursor.fetchall()
				likes=[]
				for row in result:
					likes.append(dict(zip(row_header, row)))
				if not likes:
					return ("Like with Song Name %s and User Name %s not found!" %(songName, userName))
				connection.commit()
			
			delete_query = "DELETE FROM likes WHERE songId = %s AND userId = %s"
			data_delete_query = [songId, userId]
			with connection.cursor() as cursor:
				cursor.execute(delete_query, data_delete_query)
				connection.commit()
				return redirect("http://localhost:8001/songs")
	
	return render_template('deleteLike.html')

class Like:
	def __init__(self, id, userId, songId):
		self.id = id
		self.userId = userId
		self.songId = songId

	def getId(self):
		return self.id

	def getUserId(self):
		return self.userId
	
	def getSongId(self):
		return self.songId
	
	def setId(self, id):
		self.id = id
	
	def setUserId(self, userId):
		self.userId = userId
	
	def setSongId(self, songId):
		self.songId = songId

class Comment:
	def __init__(self, comment, id, userId, songId):
		self.id = id
		self.comment = comment
		self.userId = userId
		self.songId = songId

	def getId(self):
		return self.id
	
	def getComment(self):
		return self.comment

	def getUserId(self):
		return self.userId
	
	def getSongId(self):
		return self.songId
	
	def setId(self, id):
		self.id = id
	
	def setComment(self, comment):
		self.comment = comment
	
	def setUserId(self, userId):
		self.userId = userId
	
	def setSongId(self, songId):
		self.songId = songId

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5004)
