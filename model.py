from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = "User"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

	def __repr__(self):
		return self.username

class Chatroom(db.Model):
	__tablename__ = "Chatroom"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True, nullable=False)
	creater = db.Column(db.String(30), nullable=False)

	def __init__(self, name, creater):
		self.name = name
		self.creater = creater

	def __repr__(self):
		return 'Room name: {}, creater: {}'.format(self.name, self.creater)

class Message(db.Model):
	__tablename__ = "Message"
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(30), nullable=False)
	chatroom = db.Column(db.String(60), nullable=False)
	text = db.Column(db.Text, nullable=False)
	pub_date = db.Column(db.String(30), nullable=False)

	def __init__(self, author, chatroom, text, pub_date):
			self.author = author
			self.chatroom = chatroom
			self.text = text
			self.pub_date = pub_date

	def __repr__(self):
			return '"id":{}, "author":{},"chatroom":{}, "text":{}, "pub_date":{}'.format(self.id, self.author,self.chatroom, self.text, self.pub_date)
