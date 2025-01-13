from flask_mysqldb import MySQL
from flask import request, redirect, flash, url_for
import bcrypt

def readDiary():

    username = request.form['username']
    # password is encoded to bytes for hashing
    password = request.form['password'].encode("utf-8")
    email = request.form['email']
    # create hashed (encrypted) password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    # create cursor for SQL query
    cur = MySQL.connection.cursor()
    sql = 'INSERT INTO user VALUES (%s, %s, %s, %s)'
    params = ('', username, hashed, email)
    cur.execute(sql, params)
    MySQL.connection.commit()
    # creates message to HTML page
    flash("Successful registration")
    # redirects user to login page
    return redirect(url_for('login'))


