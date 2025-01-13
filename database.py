from main import mysql
from flask import request, redirect, flash, url_for, render_template
import bcrypt

def readDiary(form):
    
    username = request.form['username']
    # password is encoded to bytes for hashing
    password = request.form['password'].encode("utf-8")
    email = request.form['email']
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
    
    
