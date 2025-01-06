from flask import Flask, request, render_template, redirect, url_for, session, flash
import bcrypt
from flask_mysqldb import MySQL
from functions import *

# create Flask application
app = Flask(__name__)

# create secret key for flask & session
app.secret_key = 'philobeddoe'

# configure MySQL server:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '323768CR10'
app.config['MYSQL_DB'] = 'diary'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# create MySQL instance
mysql = MySQL(app)

@app.route('/register', methods =['GET', 'POST'])   # mapping the URLs to a specific function "register" that will handle the logic for that URL
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
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
        # redirects user to login page
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template("register.html", title='REGISTER')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password'].encode("utf-8")
        cur = mysql.connection.cursor()
        sql = 'SELECT * FROM user WHERE username = %s'
        param = [username]
        cur.execute(sql, param)
        # create user variable for user information from MySQL database
        user = cur.fetchone()
        # create res variable and transform user (dictionary) to iterable sequence of key-value pairs 
        res = list(user.items())
        # create hash_pass variable witch stores password 
        hash_pass = res[2][1].encode("utf-8")
        # if user exists and password is correct
        if user and bcrypt.checkpw(password, hash_pass):
            # session is started with listed below parameters:
            session['loggedin'] = True
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            flash("You are logged in")
            return render_template('index.html')
        else:
            flash("Check you credentials")
            return redirect("/login")
    elif request.method == 'GET':
        return render_template('login.html', title='LOGIN')

@app.route("/", methods = ["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html", title='HOME')
    

if __name__ == "__main__":
    app.run(debug=True)