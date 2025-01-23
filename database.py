from main import mysql
from flask import request, redirect, flash, url_for, render_template, session
import bcrypt

def startSession(user):

    # Session is started with the parameters listed below
    session['loggedin'] = True
    session['user_id'] = user['user_id']
    session['username'] = user['username']
    session['email'] = user['email']

def stopSession():

    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)

def registerUser(form): # This function registers user to database
    
    username = form['username']
    # password is encoded to bytes for hashing
    password = form['password'].encode("utf-8")
    email = form['email']
    # create hashed (encrypted) password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    # create cursor for SQL query
    cur = mysql.connection.cursor()
    sql = 'INSERT INTO user VALUES (%s, %s, %s, %s)'
    params = ('', username, hashed, email)
    cur.execute(sql, params)
    mysql.connection.commit()
    # creates message to HTML page
    flash("Successful registration")

def logIn():
    
    username = request.form['username']
    password = request.form['password'].encode("utf-8")
    cur = mysql.connection.cursor()
    sql = 'SELECT * FROM user WHERE username = %s'
    param = [username]
    cur.execute(sql, param)
    user = cur.fetchone()
    return user

def writeEntry(user_id):

    # input of date + heading + content
    date = request.form['date']
    heading = request.form['heading']
    content = request.form['content']
    # makes cursor & query
    cur = mysql.connection.cursor()
    sql = "INSERT INTO entries (user_id, date, heading, content) VALUES (%s, %s, %s, %s)"
    params = (user_id, date, heading, content)
    cur.execute(sql, params)
    # commit changes to MySQL
    mysql.connection.commit()

def readDiary(id):

    cur = mysql.connection.cursor()
    sql = "SELECT * FROM entries WHERE user_id =%s"
    param = [id]
    cur.execute(sql, param)
    # create data variable for database entries
    data = cur.fetchall()
    # deactivate cursor 
    cur.close()
    return data

def showEntry(id):

    cur = mysql.connection.cursor()
    sql = "SELECT * FROM entries WHERE id =%s"
    param = [id]
    cur.execute(sql, param)
    # open single specific entry
    entry = cur.fetchone()
    return entry

def readOne(id):

    cur = mysql.connection.cursor()
    sql ="SELECT * FROM entries WHERE id =%s"
    param = [id]
    cur.execute(sql, param)
    # open single specific entry for update 
    data = cur.fetchone()
    return data

def updateOne(id):

    cur = mysql.connection.cursor()
    sql ="SELECT * FROM entries WHERE id =%s"
    param = [id]
    cur.execute(sql, param)
    data = cur.fetchone()
    date = request.form['date']
    heading = request.form['heading']
    content = request.form['content']
    cur = mysql.connection.cursor()
    sql = "UPDATE entries SET date = %s, heading= %s, content= %s WHERE id= %s"
    params = (date, heading, content, id)
    if data['user_id'] == session['user_id']:
            cur.execute(sql, params)
            mysql.connection.commit()
