from flask import Flask

# create Flask application
app = Flask(__name__)

#create secret key for flask & session
app.secret_key = 'philobeddoe'

#configure MYSQL server:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '323768CR10'
app.config['MYSQL_DB'] = 'diary'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'