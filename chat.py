import os
import json
from datetime import datetime
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash

from models import db, User, Chatroom, Message
app = Flask(__name__)

DEBUG = True
SECRET_KEY = 'super secure'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')

app.config.from_object(__name__)
app.config.from_envvar('CHAT_SETTINGS', silent=True)

db.init_app(app)

@app.cli.command('initdb')
def initdb():
	db.create_all()
	print('Initialized the database.')

def get_user_username(username):
	u = User.query.filter_by(username=username).first()
	return u.username if u else None

@app.before_request
def before_request():
	g.user = None
	g.room = None
	g.lastMessageId = None
	if 'lastMessageId' in session:
		g.lastMessageId = session['lastMessageId']
	if 'username' in session:
		g.user = User.query.filter_by(username=session['username']).first()
	if 'roomname' in session:
		g.room = Chatroom.query.filter_by(name=session['roomname']).first()

@app.route("/", methods=['GET', 'POST'])
def default():
	if not g.user:
		return render_template('login.html')
	else:
		return redirect(url_for('navigation'))

@app.route('/login', methods=['POST'])
def login():
	msg = None
	user = User.query.filter_by(username=request.form['username']).first()
	if user is None:
		return 'Invalid username'
	elif not check_password_hash(user.pw_hash, request.form['password']):
		return 'Invalid password'
	else:
		msg = 'You were logged in'
		session['username'] = user.username
		return "ok"

@app.route('/register')
def register():
	if g.user:
		return redirect(url_for("chatroom"))
	return render_template('register.html')

@app.route('/newaccount', methods=['GET', 'POST'])
def register_submit():
	if not request.form['username']:
		return "You have to enter a username"
	elif not request.form['password']:
		return "You have to enter a password"
	elif request.form['password'] != request.form['password2']:
		return 'The two passwords do not match'
	elif get_user_username(request.form['username']) is not None:
		return 'The username is already taken'
	else:
		db.session.add(User(request.form['username'], generate_password_hash(request.form['password'], method='pbkdf2')))
		db.session.commit()
		#flash('You successfully registered a new account with username: ' + request.form['username'])\
		return 'ok'

@app.route('/chatroom', methods=['GET', 'POST'])
def navigation():
	if not g.user:
		return redirect(url_for('default'))
	return render_template('nav.html', chatrooms=Chatroom.query.all(), currUser=g.user.username)

@app.route('/newroom', methods=['GET', 'POST'])
def new_chatroom():
	room = Chatroom.query.filter_by(name=request.form['roomname']).first()
	if room:
		return 'Chatroom already exists. Please use a different name.'
	elif not request.form['roomname']:
		return 'Roomname cannot be empty'
	elif ' ' in request.form['roomname']:
		return 'Can\'t have space in room name'
	else:
		db.session.add(Chatroom(request.form['roomname'], session['username']))
		db.session.commit()
		#flash('You successfully created a chatroom with name ' + request.form['roomname'])
		return "ok"

@app.route('/deleteroom', methods=['GET', 'POST'])
def delete_room():
	if g.user.username == Chatroom.query.filter_by(name=request.form['roomname']).first().creater:
		Chatroom.query.filter_by(name=request.form['roomname']).delete()
		Message.query.filter_by(chatroom=request.form['roomname']).delete()
		db.session.commit()
		#flash('You successfully deleted chatroom ' + roomname)
		return "Deleted chatroom"
	else:
		return "Something went wrong"

@app.route('/<roomname>', methods=['GET', 'POST'])
def joinroom(roomname):
	if not g.user:
		return redirect(url_for('default'))
	if not Chatroom.query.filter_by(name=roomname).first():
		return redirect(url_for('navigation'))

	session['roomname'] = roomname
	messages = Message.query.filter_by(chatroom=roomname).all()
	if messages:
		session['lastMessageId'] = messages[-1].id
	else:
		print("no messages")
		session['lastMessageId'] = -1
	print("last message id {}".format(g.lastMessageId))
	#messages = [{ 'author':'Andy', 'text':'ahh', 'pub_date':20191111},{ 'author':'Who', 'text':'this is awesome', 'pub_date':20191111}]
	return render_template('chatroom.html', roomname=roomname, messages=messages)

@app.route('/newmsg', methods=['GET', 'POST'])
def newMessage():
	if request.form['msg']:
		db.session.add(Message(g.user.username, session['roomname'], request.form['msg'], datetime.now().strftime("%m/%d/%Y, %H:%M:%S") ))
		db.session.commit()
		print (request.form['msg'])
		return "ok"
	else:
		return "message can't be empty"

@app.route('/updatemsg', methods=['GET', 'POST'])
def getMessage():
	msg = Message.query.filter_by(chatroom=session['roomname']).all()
	print("all messages: {}".format(msg))
	print(g.lastMessageId)
	newmsg = [m for m in msg if m.id > g.lastMessageId]
	print ("new messages: {}".format(newmsg))

	if not g.room:
		print("room has been deleted ")
		return json.dumps("roomdeleted")

	if newmsg:
		session['lastMessageId'] = newmsg[-1].id
	return json.dumps(stringify(newmsg))

def stringify(msg):
	list = []
	for m in msg:
		dict = {
			"id" : m.id,
			"author" : m.author,
			"chatroom" : m.chatroom,
			"text" : m.text,
			"pub_date" : m.pub_date
		}
		list.append(dict)
	print(list)
	return list

@app.route('/logout')
def logout():
	flash('You were logged out')
	session.pop('username', None)
	return redirect(url_for('default'))


if __name__ == "__main__":
	app.run()
