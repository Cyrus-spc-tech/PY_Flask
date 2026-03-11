from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Tanishh#123'
app.config['MYSQL_DATABASE_DB'] = 'g1b2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
   