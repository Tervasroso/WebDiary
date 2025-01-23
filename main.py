from flask import Flask, request, render_template, redirect, url_for, session, flash
import bcrypt
from flask_mysqldb import MySQL
from functions import *
from yleNews import getNews
from database import *
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
        registerUser(request.form)
        # redirects user to login page
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template("register.html", title='REGISTER')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # create user variable for user information from MySQL database
        user = logIn()
        password = request.form['password'].encode("utf-8")
        # create hash_pass variable witch stores password
        res = list(user.items())
        hash_pass = res[2][1].encode("utf-8")
        # if user exists and password is correct
        if user and bcrypt.checkpw(password, hash_pass):
            startSession(user)
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

@app.route("/diary", methods = ["GET"])
def diary():
    if request.method == "GET" and session['user_id']:
        id = session['user_id']
        data = readDiary(id)
        # if data is found
        if data:
            return render_template("diary.html", data = data, title='HOME')
        else:
            flash("No diary entries")
            return render_template("diary.html", title='HOME')

@app.route("/diary/create", methods=['GET','POST'])
def insert():
    if request.method == 'GET' and session['user_id']:
        return render_template("create.html", title="CREATE")
    elif request.method == 'POST':
        # we are inside user_id session
        user_id = session['user_id']
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
        flash("Entry created")
        # redirects user back to diary page
        return redirect(url_for('diary'))

@app.route("/diary/<id>", methods = ["GET"])
def show_entry(id):
    if request.method == 'GET' and session['user_id']:
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM entries WHERE id =%s"
        param = [id]
        cur.execute(sql, param)
        # open single specific entry
        entry = cur.fetchone()
        return render_template("partials/entry.html", entry = entry, title="ENTRY")

@app.route("/diary/update/<id>", methods=['GET','POST'])
def update(id):
    if request.method == 'GET' and session['user_id']:
        cur = mysql.connection.cursor()
        sql ="SELECT * FROM entries WHERE id =%s"
        param = [id]
        cur.execute(sql, param)
        # open single specific entry for update 
        data = cur.fetchone()
        return render_template("partials/update.html", data = data, title="UPDATE")
    elif request.method == 'POST' and session['user_id']:    
        # updated data 
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
            flash("Entry updated")
            return redirect(url_for('diary'))
        else:
            flash("permission denied")
            return redirect(url_for('diary'))

@app.route("/diary/delete/<id>", methods=['GET'])
def delete(id):
    if request.method == 'GET' and session['user_id']:
        cur = mysql.connection.cursor()
        sql ="SELECT * FROM entries WHERE id =%s"
        param = [id]
        cur.execute(sql, param)
        data = cur.fetchone()
        # delete specific entry according to entry id 
        if data['user_id'] == session['user_id']:
            sql2 = "DELETE FROM entries WHERE id = %s"
            param2 = [id]
            cur.execute(sql2, param2)
            mysql.connection.commit()
            flash("Entry deleted")
            return redirect(url_for('diary'))
        else:
            flash("permission denied")
            return redirect(url_for('diary'))

@app.route('/logout')
def logout():
    stopSession()
    return redirect(url_for('login'))

@app.route("/news")
def news():
    return render_template("news.html", data = getNews(), title="NEWS")
    

if __name__ == "__main__":
    app.run(debug=True)